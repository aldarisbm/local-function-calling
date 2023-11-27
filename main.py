import logging
import os

from dotenv import load_dotenv

from evals import regular
from helpers import get_load_params, get_inference_params, get_available_functions
from runner import Runner

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

r = Runner(project, model_name, inference_params, load_params)
r.run(regular.tests, available_functions, 1)
