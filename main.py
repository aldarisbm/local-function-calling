import logging
import os

from dotenv import load_dotenv

from helpers import get_load_params, get_inference_params
from run import run

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

inference_params = get_inference_params()
load_params = get_load_params()
iterations = 1
run()
