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

from prompts import EXTRACT_EQUATIONS

load_dotenv()  # take environment variables from .env.

TIMEOUT = 10000
RETRY_TIME = 5
RATE_LIMIT = 300
API_KEY = os.getenv('OPENAI_API_KEY')

# Generate prompts.
def gsm8k_prompt(row):
    text = EXTRACT_EQUATIONS.replace('{response}', row['response'])
    index = row['question_id']
    return {"text": text, "id": index}

sample_0 = pandas.read_json('data/output/response/sample_0.jsonl', lines=True)
sample_1 = pandas.read_json('data/output/response/sample_1.jsonl', lines=True)
sample_2 = pandas.read_json('data/output/response/sample_2.jsonl', lines=True)
sample_3 = pandas.read_json('data/output/response/sample_3.jsonl', lines=True)
sample_4 = pandas.read_json('data/output/response/sample_4.jsonl', lines=True)
sample_5 = pandas.read_json('data/output/response/sample_5.jsonl', lines=True)
sample_6 = pandas.read_json('data/output/response/sample_6.jsonl', lines=True)
sample_7 = pandas.read_json('data/output/response/sample_7.jsonl', lines=True)
sample_8 = pandas.read_json('data/output/response/sample_8.jsonl', lines=True)
sample_9 = pandas.read_json('data/output/response/sample_9.jsonl', lines=True)

sample_0 = sample_0.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_1 = sample_1.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_2 = sample_2.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_3 = sample_3.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_4 = sample_4.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_5 = sample_5.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_6 = sample_6.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_7 = sample_7.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_8 = sample_8.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()
sample_9 = sample_9.apply(lambda row : gsm8k_prompt(row), axis=1).to_list()

CONFIGS = { "model": "gpt-3.5-turbo", "n": 1, "temperature": 0.7}
sleepyask = Sleepyask(configs=CONFIGS, 
                      rate_limit=RATE_LIMIT,
                      api_key=API_KEY, 
                      timeout=TIMEOUT, 
                      verbose=True,
                      retry_time=RETRY_TIME)

sleepyask.start(question_list=sample_0, out_path='data/output/equations/sample_0.jsonl')
sleepyask.start(question_list=sample_1, out_path='data/output/equations/sample_1.jsonl')
sleepyask.start(question_list=sample_2, out_path='data/output/equations/sample_2.jsonl')
sleepyask.start(question_list=sample_3, out_path='data/output/equations/sample_3.jsonl')
sleepyask.start(question_list=sample_4, out_path='data/output/equations/sample_4.jsonl')
sleepyask.start(question_list=sample_5, out_path='data/output/equations/sample_5.jsonl')
sleepyask.start(question_list=sample_6, out_path='data/output/equations/sample_6.jsonl')
sleepyask.start(question_list=sample_7, out_path='data/output/equations/sample_7.jsonl')
sleepyask.start(question_list=sample_8, out_path='data/output/equations/sample_8.jsonl')
sleepyask.start(question_list=sample_9, out_path='data/output/equations/sample_9.jsonl')