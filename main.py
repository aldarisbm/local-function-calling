import json
import logging
import os

from dotenv import load_dotenv

from evals import regular
from function_caller import FunctionCaller
from helpers import get_available_functions

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Debug mode enabled')
else:
    logging.basicConfig(level=logging.INFO)
    logging.debug('Info mode enabled')

wandb_project = os.getenv('WANDB_PROJECT', 'local_function')
available_functions = get_available_functions()

with open('data/few_shots.json') as f:
    few_shots = json.load(f)

caller = FunctionCaller(wandb_project, available_functions)
caller.call(regular.tests, few_shots)
