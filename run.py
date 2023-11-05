import json
import logging
import os
from json import JSONDecodeError

import pandas as pd
from jinja2 import Template
from llama_cpp import Llama

import wandb
from function_map import fns_map
from helpers import load_template, load_llm, get_inference_params
from inference import inference


def run():
    project = os.getenv('PROJECT', 'local-function-calling')
    examples: list[str] = ['What is the unicode point of the letter R']
    model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q8_0.gguf')

    generations: list[dict] = []
    inference_params: dict = get_inference_params()
    logging.debug(f'inference params: {inference_params}')
    for example_query in examples:
        ptpl: Template = load_template('functions')
        query: str = ptpl.render(query=example_query)
        llm: Llama = load_llm(inference_params)
        res, raw_output, t = inference(llm, query)
        tok_s = raw_output["usage"]["completion_tokens"] / t
        generation_tracker = {
            "question": example_query,
            "full_prompt": query,
            "answer": res,
            "model_name": model_name,
            "tokens_sec": tok_s,
            "model_file": raw_output["model"],
            "inference_params": inference_params
        }
        try:
            fn = json.loads(res)
        except JSONDecodeError as e:
            generation_tracker.update({"is_valid": False})
            generations.append(generation_tracker)
            logging.error(e)
            continue

        fn_name = fn['function_name']
        try:
            resp = fns_map[fn_name](**fn['parameters'])
        except Exception as e:
            generation_tracker.update({"is_valid": False})
            generations.append(generation_tracker)
            logging.error(e)
            continue
        logging.info(f'Response: {resp}')
        generation_tracker.update({"is_valid": True})
        generations.append(generation_tracker)

    pred_table = wandb.Table(dataframe=pd.DataFrame(generations))

    # create a config to save with the project run
    config = dict(model_name=model_name, params=inference_params)

    # create a wandb run
    with wandb.init(project=project, job_type="inference", config=config):
        wandb.log({"preds_table": pred_table})
        wandb.finish(quiet=True)
