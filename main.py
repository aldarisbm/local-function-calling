import json
import logging
import os

from dotenv import load_dotenv

from evals import regular
from helpers import get_available_functions
from runner import FunctionCaller

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

wandb_project = os.getenv('WANDB_PROJECT', 'local_function')
available_functions = get_available_functions()

with open('data/few_shots.json') as f:
    few_shots = json.load(f)

caller = FunctionCaller(wandb_project, available_functions)
caller.call(regular.tests, few_shots)
