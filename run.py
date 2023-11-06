import json
import logging
import os
from json import JSONDecodeError

import pandas as pd
from jinja2 import Template
from llama_cpp import Llama

import wandb
from function_map import fns_map
from helpers import load_template, load_llm, get_inference_params, get_pkgs_versions
from inference import inference


def run():
    project = os.getenv('PROJECT', 'local-fn-calling')
    model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q8_0.gguf')

    tests: list[str] = [
        'what is the date today?',
        'What is the unicode point of the letter R?',
        'What is the zipcode of Saint Louis, MO?',
        'this should fail bc nothing',
        'can you check google for today\'s top news?'
    ]

    generations: list[dict] = []
    inference_params: dict = get_inference_params()
    logging.debug(f'inference params: {inference_params}')
    # we are putting this outside of the loop to not re-initialize this 3 times.
    llm: Llama = load_llm(inference_params)
    for test_query in tests:
        ptpl: Template = load_template('functions')
        query: str = ptpl.render(query=test_query)
        res, raw_output, t = inference(llm, query)
        tok_s = raw_output["usage"]["completion_tokens"] / t
        generation_tracker = {
            "is_valid": False,
            "query": test_query,
            "invoked_fn_output": None,
            "generation": res if res != test_query else None,
            "full_prompt": query,
            "error": None,
            "model_name": model_name,
            "tokens_sec": tok_s,
            "in_params": inference_params,
            "pkg_v": get_pkgs_versions()
        }
        try:
            fn = json.loads(res)
        except JSONDecodeError as e:
            generation_tracker.update({
                "error": f"decoding json: {e}",
            })
            generations.append(generation_tracker)
            logging.error(f"while decoding json: {e}")
            continue

        logging.info(f'Got output: {fn}')
        fn_name = fn['function_name'] if 'function_name' in fn else None

        if not fn_name:
            generation_tracker.update({
                "error": f'could not generate for: "{test_query}", empty output'
            })
            generations.append(generation_tracker)
            logging.error(f'generation not found for: "{test_query}"')
            continue

        try:
            resp = fns_map[fn_name](**fn['parameters'])
        except Exception as e:
            generation_tracker.update({
                "error": f'calling function: {e}',
            })
            generations.append(generation_tracker)
            logging.error(f"while calling the function with the generated parameters: {e}")
            continue
        # if we made it here we assume we succeeded.
        logging.info(f'Response: {resp}')
        generation_tracker.update(
            {
                "is_valid": True,
                "invoked_fn_output": str(resp),  # we should always string this bc it gets saved to wandb
            })
        generations.append(generation_tracker)

    pred_table = wandb.Table(dataframe=pd.DataFrame(generations))

    # create a config to save with the project run
    config = dict(model_name=model_name, params=inference_params)

    # create a wandb run
    with wandb.init(project=project, job_type="inference", config=config):
        wandb.log({"preds_table": pred_table})
