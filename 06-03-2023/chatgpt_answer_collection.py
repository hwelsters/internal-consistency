import pandas as pd
import os
import re
import ast
import json
import numpy as np
from sympy_solver import SympySolver
from scipy.optimize import linear_sum_assignment

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
    # Apply the cleanup logic
    cost_matrix = np.abs(np.subtract.outer(actual_answer, chatgpt_answer))
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    cleaned_answer_values = [chatgpt_answer[index] for index in col_ind]
    return cleaned_answer_values

def extract_numbers(text):
    """Extract numbers from given text."""
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers

for filename in os.listdir('../data/output/solved'):
    sample = pd.read_json(f'../data/output/solved/{filename}', lines=True)

    # Clean-up logic
    for index, row in sample.iterrows():
        solved_str = row['solved']
        solved_values = extract_numbers(solved_str)
        question_id = row['question_id']

        original_solved_values = solved_values.copy()
        if solutions.get(question_id) and solved_values:
            # Skip cleanup if number of answers is less than actual solution
            if len(solved_values) < len(solutions[question_id]):
                continue
            try:
                cleaned_answer = clean_up_answer(solutions[question_id], solved_values)
                if cleaned_answer:  
                    solved_values = cleaned_answer
                else: 
                    solved_values = original_solved_values
            except AttributeError:
                print(f"Question ID: {question_id}")
                print(f"Actual answer list: {solutions[question_id]}")
                print(f"Solved values: {solved_values}")
                raise
        row['solved'] = str(solved_values)


    sample['flag'] = sample['solved'].apply(lambda row : flag(row))
    sample.to_json(f'../data/output/solved_2/{filename}', lines=True, orient='records')
