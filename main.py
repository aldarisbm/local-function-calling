import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from evals import regular
from helpers import get_load_params, get_inference_params, get_available_functions
from runner import Runner

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

project = os.getenv('PROJECT', 'local_function')

inference_params = get_inference_params()
load_params = get_load_params()
iterations = 1
available_functions = get_available_functions()

model_path = os.getenv(
    'MODEL_PATH',
    f'{Path.home()}/Development/llama.cpp/models/7B/dolphin-2.5-mixtral-8x7b.Q5_K_M.gguf'
)

load_params.update({
    "model_path": model_path
})

with open('data/few_shots.json') as f:
    few_shots = json.load(f)

r = Runner(project, inference_params, load_params)
r.run(regular.tests, available_functions, few_shots, 1)
