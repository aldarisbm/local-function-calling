import json
import logging
import os
import sys
import time
from importlib import metadata
from json import JSONDecodeError

import pandas as pd
from jinja2 import Template, Environment, FileSystemLoader
from llama_cpp import Llama

import wandb
from helpers import get_inference_params, get_load_params
from status import Status as st


class FunctionCaller:
    wandb_project: str
    inference_params: dict
    load_params: dict
    model_name: str
    llm: Llama
    available_functions: list[dict]

    def __init__(self, wandb_project: str, available_functions: list[dict]):
        self.wandb_project = wandb_project
        self.inference_params = get_inference_params()
        self.load_params = get_load_params()
        self.model_name = os.path.basename(self.load_params['model_path'])
        self.available_functions = available_functions
        self.llm = self._get_llama()

    def _get_llama(self):
        logging.debug(f"Using load params: {self.load_params}")
        return Llama(**self.load_params)

    def __inference(self, inference_params: dict, q: str) -> (str, any, float):
        logging.debug(f"Starting inference...")
        t0 = time.perf_counter()
        logging.debug(f"inference params: {inference_params}")
        raw_output = self.llm(q, **inference_params)
        logging.debug(f"done with inference..")
        answer = raw_output["choices"][0]["text"]
        return answer, raw_output, time.perf_counter() - t0

    @staticmethod
    def __load_template(template: str) -> Template:
        environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
        ptpl: Template = environment.get_template(f"{template}.j2")
        return ptpl

    @staticmethod
    def __get_pkgs_versions() -> dict:
        # we are adding most important packages here, they all get saved to wandb anyway.
        llama_cpp_version = metadata.version('llama-cpp-python')

        return dict(
            llama_cpp=llama_cpp_version
        )

    def call(self, evals: list[str], few_shots: list[dict]):
        logging.debug(f'Running: {self.model_name}')
        generations: list[dict] = []
        logging.debug(f'inference params: {self.inference_params}')
        ptpl: Template = self.__load_template('functions')
        for q in evals:
            query: str = ptpl.render(query=q, few_shots=few_shots, functions=self.available_functions)
            logging.debug(f"Starting inference.\nQuery: {q}")
            res, raw_output, t = self.__inference(self.inference_params, query)
            tok_s = raw_output["usage"]["completion_tokens"] / t
            logging.debug(f"Tokens per second: {tok_s}")

            generation_tracker = {
                "status": st.FAILURE.name,  # defaulting to error, might want to change this
                "query": q,
                "invoked_fn_output": None,
                "generation": res if res != q else None,
                "full_prompt": query,
                "error": None,
                "model_name": self.model_name,
                "tokens_sec": tok_s,
                "inference_time": t,
                "lp": self.load_params,
                "ip": self.inference_params,
                "pkg_v": self.__get_pkgs_versions()
            }
            try:
                stripped_res = res.strip()
                res = json.loads(stripped_res)
            except JSONDecodeError as e:
                generation_tracker.update({
                    "error": f"decoding json: {e}",
                })
                generations.append(generation_tracker)
                logging.error(f"for query: {q}")
                logging.error(f"while decoding json: {e}")
                logging.error(f"got response: {res}")
                continue

            if 'error' in res:
                generation_tracker.update({
                    "error": res['error']
                })

                logging.info(f"could not pick a function for: {q}, got error: {res}")
                if res['error'] == "noop":
                    generation_tracker.update({
                        "status": st.SUCCESS.name
                    })

                generations.append(generation_tracker)
                continue
            logging.info(f'got output: {res}')

            # extracting function and arguments
            fn_name = res['function_name'] if 'function_name' in res else None
            fn_args = res['arguments'] if 'arguments' in res else {}

            if not fn_name:
                generation_tracker.update({
                    "error": f'could not generate for: "{q}", empty output'
                })
                generations.append(generation_tracker)
                logging.error(f'generation not found for: "{q}"')
                continue

            try:
                func = next(f['fn'] for f in self.available_functions if f["fn_name"] == fn_name)
                func_res = func(**fn_args)
            except Exception as e:
                generation_tracker.update({
                    "error": f'calling function: {e}',
                })
                generations.append(generation_tracker)
                logging.error(f"for query: {q}")
                logging.error(f"while calling the function with the generated parameters: {e}")
                continue
            # if we made it here we assume we succeeded.
            generation_tracker.update(
                {
                    "status": st.SUCCESS.name,
                    "invoked_fn_output": str(func_res),  # we should always string this bc it gets saved to wandb
                })
            generations.append(generation_tracker)

        pred_table = wandb.Table(dataframe=pd.DataFrame(generations))

        # create a config to save with the project run
        del self.inference_params['grammar']  # this is a LlamaGrammar object.
        self.inference_params['grammar'] = os.getenv('GRAMMAR_FILE', './grammars/json.gbnf')
        config = dict(model_name=self.model_name, load_params=self.load_params, inference_params=self.inference_params)

        # create a wandb run
        with wandb.init(project=self.wandb_project, job_type="inference", config=config):
            wandb.log({"preds_table": pred_table})
        sys.exit(0)
