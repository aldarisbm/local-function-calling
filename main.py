import json
import logging
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

user_home_path = Path.home()
model_name = f'{user_home_path}/Development/llama.cpp/models/7B/mistral-7b-openorca.Q8_0.gguf'
grammar_file = "./grammars/json.gbnf"

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

logging.debug(f'Loaded model: {model_name}')

environment: Environment = Environment(loader=FileSystemLoader("prompts/"))
ptpl: Template = environment.get_template("functions.ptpl")
query: str = ptpl.render(query="What is the unicode point of the letter H")

json_result: str = llm(prompt=query)
print(json_result)
res = json_result.strip()
res = json.loads(res)
print(res)
