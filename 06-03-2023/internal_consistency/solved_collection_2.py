import pandas as pd
import os
import re
import ast
import json
import numpy as np
from sympy_solver import SympySolver
from scipy.optimize import linear_sum_assignment

output_dir = '../data/output/solved_2/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


# Load solutions
with open('../data/input/draw.json') as f:
    dataset = json.load(f)
solutions = {item['iIndex']: item['lSolutions'] for item in dataset}

def flag(solved):
    if str(solved).count('FAILED') > 0: return 'SUS'
    if str(solved).count('FREE VARIABLE') > 0: return 'FREE'
    if len(solved) == 0: return 'SUS'
    return 'OK'

def clean_up_answer(actual_answer, chatgpt_answer):
    # Bypass the cleanup function if chatgpt_answer is not existent, is "FREE VARIABLE[]", or is a list.
    if not chatgpt_answer or str(chatgpt_answer).startswith("FREE") or isinstance(chatgpt_answer, list):
        return chatgpt_answer
    
    # print('here??')
    actual_answer_list = list(actual_answer)
    # print("actual answer: " + str(actual_answer_list))
    chatgpt_answer_keys = list(chatgpt_answer.keys())
    # print("chatgpt_answer keys: " + str(chatgpt_answer_keys))
    chatgpt_answer_list = list(chatgpt_answer.values())
    # print("chatgpt_answers: "+ str(chatgpt_answer_list))
    
    # Apply the cleanup logic
    cost_matrix = np.abs(np.subtract.outer(actual_answer_list, chatgpt_answer_list))
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    cleaned_answer_values = [chatgpt_answer_list[index] for index in col_ind]
    
    # Construct cleaned answer as a dictionary
    cleaned_answer = {chatgpt_answer_keys[i]: cleaned_answer_values[i] for i in range(len(cleaned_answer_values))}

    return cleaned_answer

for filename in os.listdir('../data/output/solved'):
    sample = pd.read_json(f'../data/output/solved/{filename}', lines=True)

    # Clean-up logic
    for index, row in sample.iterrows():

        check = False

        test = ""
        solved_str = row['solved'].replace("'", '"')
        solved_str = re.sub(r'(\b[a-zA-Z_][a-zA-Z0-9_]*\b)', r'"\1"', solved_str)

        if "FREE" in solved_str or "[]" in solved_str or "FAILED" in solved_str:
            # test = "failed"
            continue

        try:
            solved_dict = json.loads(solved_str)
        except json.decoder.JSONDecodeError:
            # print(f"Failed to parse JSON for string: {solved_str}, {row['question_id']}, {test}")
            continue  

        question_id = row['question_id']
        original_solved_dict = solved_dict.copy()

        if solutions.get(question_id) and isinstance(solved_dict, dict):
            # Skip cleanup if number of answers is less than actual solution
            if len(solved_dict) <= len(solutions[question_id]):
                continue
            try:
                if 144 in solved_dict.values() and 72 in solved_dict.values():
                    print('144 and 72 found in solved_dict.')
                    print('solved_dict:', solved_dict)
                    print("Problematic question: ", question_id)
                    check = True
            except AttributeError:
                continue
            cleaned_answer = clean_up_answer(solutions[question_id], solved_dict)

            if (check):
                print('cleaned answer: ', cleaned_answer)

            if cleaned_answer:
                solved_dict = cleaned_answer
            else:
                solved_dict = original_solved_dict

            if (check):
                print('final cleaned answer: ', solved_dict)
        row['solved'] = str(solved_dict)
        sample.at[index, 'solved'] = str(solved_dict)

    sample.to_json(os.path.join(output_dir, filename), lines=True, orient='records')


    # sample['solved'] = sample['solved'].apply(lambda row: str(row))
    # sample.to_json(os.path.join(output_dir, filename), lines=True, orient='records')
