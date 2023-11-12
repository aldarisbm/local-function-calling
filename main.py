import logging
import os

from dotenv import load_dotenv

from evals import fail
from helpers import get_load_params, get_inference_params, get_available_functions
from run import run

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

inference_params = get_inference_params()
load_params = get_load_params()
iterations = 1
project = os.getenv('PROJECT', 'local_function')
model_name = os.getenv('MODEL_NAME', 'airoboros-m-7b-3.1.2.Q6_K.gguf')
available_functions = get_available_functions()

run(project, model_name, inference_params, load_params, iterations, fail.tests, available_functions)
