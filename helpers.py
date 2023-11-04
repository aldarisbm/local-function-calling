import logging
import os
from pathlib import Path

from jinja2 import Environment, Template, FileSystemLoader
from llama_cpp import Llama


def get_model_path() -> str:
    home_path = Path.home()
    model_folder = os.getenv('MODEL_FOLDER', 'Development/llama.cpp/models')
    model_param_ct = os.getenv('MODEL_PARAM_CT', '7B')
    model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q8_0.gguf')
    model_path = f'{home_path}/{model_folder}/{model_param_ct}/{model_name}'
    logging.info(f'loading model: {model_name}...')
    return model_path


def load_llm() -> Llama:
    model_path = get_model_path()
    grammar_file = os.getenv('GRAMMAR_FILE', './grammars/json.gbnf')
    llm: Llama = Llama(
        model_path=model_path,
        temperature=0,
        use_mlock=True,
        grammar=grammar_file,
        max_tokens=-1,
        n_batch=512,
        n_threads=4,
        n_ctx=4096,
        n_gpu_layers=30
    )
    return llm


def load_template(template: str) -> Template:
    environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
    ptpl: Template = environment.get_template(f"{template}.ptpl")
    return ptpl
