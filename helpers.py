import logging
import os
from importlib import metadata
from pathlib import Path

from jinja2 import Environment, Template, FileSystemLoader
from llama_cpp import Llama, LlamaGrammar


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
        n_gpu_layers=30,
        use_mlock=True,
        n_ctx=4096,
        n_batch=512,
        n_threads=4,
    )
    return load_params


def get_inference_params() -> dict:
    grammar_file = os.getenv('GRAMMAR_FILE', './grammars/json.gbnf')
    grammar = LlamaGrammar.from_file(grammar_file)

    inference_params = dict(
        temperature=0,
        grammar=grammar,
        max_tokens=-1,
    )
    return inference_params


def get_pkgs_versions() -> dict:
    # we should keep track of important packages here, we do that in the project toml, but we won't be pushing that to
    # wandb every run.
    llama_cpp_version = metadata.version('llama-cpp-python')

    return dict(
        llama_cpp=llama_cpp_version
    )
