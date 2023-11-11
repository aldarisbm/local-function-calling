import json
import logging
import os
import sys
from json import JSONDecodeError

import pandas as pd
from jinja2 import Template
from llama_cpp import Llama

import wandb
from function_map import fns_map
from helpers import load_template, load_llm, get_inference_params, get_pkgs_versions, get_load_params
from inference import inference
from status import Status as St


def run():
    project = os.getenv('PROJECT', 'local_function')
    model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q6_K.gguf')

    fail_tests: list[str] = [
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
    ]
    reg_test: list[str] = [
        'what is the date today?',
        'what is the unicode point of the letter R?',
        'what is the zipcode of Saint Louis, MO?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?',
    ]

    generations: list[dict] = []
    inference_params: dict = get_inference_params()
    load_params: dict = get_load_params()
    logging.debug(f'inference params: {inference_params}')
    # we are putting this outside of the loop to not re-initialize this 3 times.
    llm: Llama = load_llm(load_params)
    for i in range(1):
        for test_query in reg_test:
            ptpl: Template = load_template('functions')
            query: str = ptpl.render(query=test_query)
            res, raw_output, t = inference(llm, inference_params, query)
            tok_s = raw_output["usage"]["completion_tokens"] / t
            generation_tracker = {
                "status": St.FAILURE.name,
                "query": test_query,
                "invoked_fn_output": None,
                "generation": res if res != test_query else None,
                "full_prompt": query,
                "error": None,
                "model_name": model_name,
                "tokens_sec": tok_s,
                "inference_time": t,
                "lp": load_params,
                "ip": inference_params,
                "pkg_v": get_pkgs_versions()
            }
            try:
                stripped_res = res.strip()
                fn = json.loads(stripped_res)
            except JSONDecodeError as e:
                generation_tracker.update({
                    "error": f"decoding json: {e}",
                })
                generations.append(generation_tracker)
                logging.error(f"for query: {test_query}")
                logging.error(f"while decoding json: {e}")
                logging.error(f"got response: {res}")
                continue

            if 'error' in fn:
                logging.info(f"could not pick a function for: {test_query}, got error: {fn}")
                generation_tracker.update({
                    "error": fn['error']
                })
                generations.append(generation_tracker)
                continue
            logging.info(f'got output: {fn}')
            fn_name = fn['function_name'] if 'function_name' in fn else None

            if not fn_name:
                generation_tracker.update({
                    "error": f'could not generate for: "{test_query}", empty output'
                })
                generations.append(generation_tracker)
                logging.error(f'generation not found for: "{test_query}"')
                continue

            try:
                resp = fns_map[fn_name](**fn['parameters'] if 'parameters' in fn else {})
            except Exception as e:
                generation_tracker.update({
                    "error": f'calling function: {e}',
                })
                generations.append(generation_tracker)
                logging.error(f"for query: {test_query}")
                logging.error(f"while calling the function with the generated parameters: {e}")
                continue
            # if we made it here we assume we succeeded.
            generation_tracker.update(
                {
                    "status": St.SUCCESS.name,
                    "invoked_fn_output": str(resp),  # we should always string this bc it gets saved to wandb
                })
            generations.append(generation_tracker)

    pred_table = wandb.Table(dataframe=pd.DataFrame(generations))

    # create a config to save with the project run
    del inference_params['grammar']  # this is a LlamaGrammar object.
    inference_params['grammar'] = os.getenv('GRAMMAR_FILE', './grammars/json.gbnf')
    config = dict(model_name=model_name, load_params=load_params, inference_params=inference_params)

    # create a wandb run
    with wandb.init(project=project, job_type="inference", config=config):
        wandb.log({"preds_table": pred_table})
    sys.exit(0)
