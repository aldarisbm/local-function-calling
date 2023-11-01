import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

load_dotenv()

logging.basicConfig(level=logging.DEBUG) if os.getenv('DEBUG', 'false').lower() == 'true' else None

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

home_path = Path.home()
model_folder = os.getenv('MODEL_FOLDER', 'Development/llama.cpp/models')
model_param_ct = os.getenv('MODEL_PARAM_CT', '7B')
model_name = os.getenv('MODEL_NAME', 'mistral-7b-openorca.Q8_0.gguf')
grammar_file = os.getenv('GRAMMAR_PATH', './grammars/json.gbnf')

model_name = f'{home_path}/{model_folder}/{model_param_ct}/{model_name}'

llm: LlamaCpp = LlamaCpp(
    model_path=model_name,
    temperature=0,
    use_mlock=True,
    grammar_path=grammar_file,
    max_tokens=-1,
    seed=42,
    n_batch=512,
    n_threads=4,
    n_ctx=10240,
    n_gpu_layers=30,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

logging.debug(f'loaded model: {model_name}')

environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
ptpl: Template = environment.get_template("functions.ptpl")
query: str = ptpl.render(query="What is the unicode point of the letter H")

json_result: str = llm(prompt=query)
print(json_result)
res = json_result.strip()
res = json.loads(res)
print(res)
