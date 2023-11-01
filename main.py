import json
from pathlib import Path

from dotenv import load_dotenv
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp

load_dotenv()

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

user_home_path = Path.home()
model_name = f'{user_home_path}/Development/llama.cpp/models/7B/mistral-7b-openorca.Q8_0.gguf'
grammar_file = "./grammars/json.gbnf"

llm = LlamaCpp(
    model_path=model_name,
    temperature=0,
    use_mlock=True,
    grammar_path=grammar_file,
    max_tokens=-1,
    seed=42,
    n_batch=512,
    n_threads=4,
    n_gqa=8,
    n_ctx=10240,
    n_gpu_layers=30,
    callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

print(f'Loaded model: {model_name}')

with open("prompts/functions.ptpl") as prompt:
    pr = prompt.read()
    print(pr)
    json_result = llm(prompt=pr)
    print(json_result)
    res = json_result.strip()
    res = json.loads(res)
    print(res)
