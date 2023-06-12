import pandas as pd
import json
import re
import os
import numpy as np
from scipy.optimize import linear_sum_assignment

dir_path = 'data/output/split_response/'
output_dir = 'data/output/chatgpt_answers_2/'

# Load draw.json dataset and prepare a dictionary for solution values
with open('data/input/draw.json') as f:
    dataset = json.load(f)

solutions = {item['iIndex']: item['lSolutions'] for item in dataset}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def clean_up_answer(actual_answer, chatgpt_answer):
    cost_matrix = np.abs(np.subtract.outer(actual_answer, chatgpt_answer))
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    cleaned_answer = [chatgpt_answer[index] for index in col_ind]
    return cleaned_answer

def extract_numbers(text):
    """Extract numbers from given text."""
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers  # Return a list

count = 0;
total = 0;

for i in range(10):  
    responses = pd.read_json(f'{dir_path}sample_{i}.jsonl', lines=True)

    extracted_responses = []

    for _, row in responses.iterrows():
        total += 1
        question_id = row['question_id']
        response_text = row['response'].replace('\n', ' ')
        match = re.search(r"(?i)the answer is", response_text)
        if match:
            answer_text = response_text[match.end():]
            answer = extract_numbers(answer_text)
            original_answer = answer.copy()  # Store original answer
            if solutions.get(question_id) and answer: # make sure both lists are not empty
                cleaned_answer = clean_up_answer(solutions[question_id], answer)
                if cleaned_answer:  # If cleaned answer is not empty, update the answer
                    answer = cleaned_answer
                else:  # If cleaned answer is empty, retain the original answer
                    answer = original_answer
        else:
            answer = None

        # Prepare flag
        flag = "NORMAL" if len(solutions.get(question_id, [])) >= (len(answer) if answer is not None else 0) else "WEIRD"

        if flag == 'WEIRD':
            count += 1

        extracted_responses.append({
            'question_id': question_id,
            'chatgpt_answer': answer,
            'num_solutions': len(answer) if answer is not None else None,
            'flag': flag
        })

    # Write to jsonl file
    with open(f'{output_dir}sample_{i}.jsonl', 'w') as outfile:
        for resp in extracted_responses:
            json.dump(resp, outfile)
            outfile.write('\n')

print(count)
print(total)
