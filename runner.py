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
from status import Status as st


class Runner:
    def __init__(self, wandb_project: str, model_name: str, inference_params: dict, load_params: dict):
        self.wandb_project = wandb_project
        self.model_name = model_name
        self.inference_params = inference_params
        self.load_params = load_params
        self.llm = self.__load_llm()

    def __load_llm(self) -> Llama:
        llm: Llama = Llama(**self.load_params)
        return llm

    def __inference(self, inference_params: dict, q: str) -> (str, any, float):
        t0 = time.perf_counter()
        raw_output = self.llm(q, **inference_params)
        answer = raw_output["choices"][0]["text"]
        return answer, raw_output, time.perf_counter() - t0

    @staticmethod
    def __load_template(template: str) -> Template:
        environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
        ptpl: Template = environment.get_template(f"{template}.ptpl")
        return ptpl

    @staticmethod
    def __get_pkgs_versions() -> dict:
        # we are adding most important packages here, they all get saved to wandb anyway.
        llama_cpp_version = metadata.version('llama-cpp-python')

        return dict(
            llama_cpp=llama_cpp_version
        )

    def run(self, evals: list[str], available_functions: list[dict], iterations: int):
        generations: list[dict] = []
        logging.debug(f'inference params: {self.inference_params}')
        # we are putting this outside of the loop to not re-initialize this every time.
        for i in range(iterations):
            for q in evals:
                with open('./data/set.json') as f:
                    few_shots = json.load(f)
                ptpl: Template = self.__load_template('functions')
                query: str = ptpl.render(query=q, few_shots=few_shots, functions=available_functions)
                res, raw_output, t = self.__inference(self.inference_params, query)
                tok_s = raw_output["usage"]["completion_tokens"] / t
                generation_tracker = {
                    "status": st.FAILURE.name,
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
                    fn = json.loads(stripped_res)
                except JSONDecodeError as e:
                    generation_tracker.update({
                        "error": f"decoding json: {e}",
                    })
                    generations.append(generation_tracker)
                    logging.error(f"for query: {q}")
                    logging.error(f"while decoding json: {e}")
                    logging.error(f"got response: {res}")
                    continue

                if 'error' in fn:
                    logging.info(f"could not pick a function for: {q}, got error: {fn}")
                    generation_tracker.update({
                        "error": fn['error']
                    })
                    generations.append(generation_tracker)
                    continue
                logging.info(f'got output: {fn}')
                fn_name = fn['function_name'] if 'function_name' in fn else None

                if not fn_name:
                    generation_tracker.update({
                        "error": f'could not generate for: "{q}", empty output'
                    })
                    generations.append(generation_tracker)
                    logging.error(f'generation not found for: "{q}"')
                    continue

                try:
                    func = next(f['fn'] for f in available_functions if f["fn_name"] == fn_name)
                    resp = func(**fn['parameters'] if 'parameters' in fn else {})
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
                        "invoked_fn_output": str(resp),  # we should always string this bc it gets saved to wandb
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
