import logging
import os
from importlib import metadata
from inspect import signature
from pathlib import Path

from jinja2 import Environment, Template, FileSystemLoader
from llama_cpp import Llama, LlamaGrammar

from function_map import fns_map


def get_model_path() -> str:
    home_path = Path.home()
    model_folder = os.getenv('MODEL_FOLDER', 'Development/llama.cpp/models')
    model_param_ct = os.getenv('MODEL_PARAM_CT', '7B')
    model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q8_0.gguf')
    model_path = f'{home_path}/{model_folder}/{model_param_ct}/{model_name}'
    logging.info(f'loading model: {model_name}...')
    return model_path


def load_llm(params: dict) -> Llama:
    llm: Llama = Llama(**params)
    return llm


def load_template(template: str) -> Template:
    environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
    ptpl: Template = environment.get_template(f"{template}.ptpl")
    return ptpl


def get_load_params() -> dict:
    model_path = get_model_path()
    load_params = dict(
        model_path=model_path,
        n_gpu_layers=-1,
        seed=0,
        use_mlock=True,
        n_ctx=4096,
        n_batch=512,
        verbose=False,
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


def get_pkgs_versions() -> dict:
    # we are adding most important packages here, they all get saved to wandb anyway.
    llama_cpp_version = metadata.version('llama-cpp-python')

    return dict(
        llama_cpp=llama_cpp_version
    )


def get_available_functions() -> list[dict]:
    return [dict(signature=f"{k}{signature(v)}", docstring=v.__doc__) for k, v, in fns_map.items()]
