import logging
import os
from inspect import signature

from jinja2 import Environment, Template, FileSystemLoader
from llama_cpp import Llama, LlamaGrammar

from function_map import fns_map


def load_llm(params: dict) -> Llama:
    llm: Llama = Llama(**params)
    return llm


def load_template(template: str) -> Template:
    environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
    ptpl: Template = environment.get_template(f"{template}.ptpl")
    return ptpl


def get_load_params() -> dict:
    model_name = os.getenv('MODEL', None)
    models_path = os.getenv('MODELS_PATH', None)
    model_path = f"{models_path}/{model_name}"
    logging.info(f'loading {model_path}...')

    load_params = dict(
        n_gpu_layers=-1,
        seed=0,
        use_mlock=True,
        n_ctx=4096,
        n_batch=512,
        verbose=True,
        model_path=model_path,
    )
    return load_params


def get_inference_params() -> dict:
    grammar_file = os.getenv('GRAMMAR_FILE', './grammars/json.gbnf')
    grammar = LlamaGrammar.from_file(grammar_file)

    inference_params = dict(
        temperature=0,
        grammar=grammar,
        max_tokens=-1,
        top_k=40,
    )
    return inference_params


def get_available_functions() -> list[dict]:
    return [dict(fn_name=k, fn=v, signature=f"{k}{signature(v)}", docstring=v.__doc__) for k, v in fns_map.items()]
