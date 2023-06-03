# TO AID WITH REPRODUCIBILITY...
# ENVIRONMENT ============================= #
# Python                             3.11.3 #
#                                           #
# LIBRARIES ------------------------------- #
# sleepyask                           7.1.0 #
# pandas                              2.0.1 #
# ========================================= #

import os
from dotenv import load_dotenv

import pandas
from sleepyask.chat import Sleepyask

from prompts import BASIC_PROMPT

load_dotenv()  # take environment variables from .env.

TIMEOUT = 10000
RETRY_TIME = 5
RATE_LIMIT = 150
API_KEY = os.getenv('OPENAI_API_KEY')

# Generate prompts.
def gsm8k_prompt(row):
    text = BASIC_PROMPT.replace('{question}', row['question'])
    index = row['iIndex']
    return {"text": text, "id": index}

gsm8k = pandas.read_json('data/input/gsm8k.jsonl', lines=True)
gsm8k = gsm8k.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()

CONFIGS = { "model": "gpt-3.5-turbo", "n": 20, "temperature": 0.7}
sleepyask = Sleepyask(configs=CONFIGS, 
                      rate_limit=RATE_LIMIT,
                      api_key=API_KEY, 
                      timeout=TIMEOUT, 
                      verbose=True,
                      retry_time=RETRY_TIME)

sleepyask.start(question_list=gsm8k, out_path='data/output/response/sample_0.jsonl')