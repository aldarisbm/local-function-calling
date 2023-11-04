import logging
import os

from dotenv import load_dotenv

from run import run

load_dotenv()
if os.getenv('DEBUG', 'false').lower() == 'true':
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
run()
