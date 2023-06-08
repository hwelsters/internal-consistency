import os
import pandas as pd
import json
import random
from collections import defaultdict
from internal_consistency.sympy_solver import Standardize

# Directories of chatgpt answers and equations
dir_answers = 'data/output/chatgpt_answers/'
dir_equations = 'data/output/equations/'

output_dir = 'data/output/majority/'
output_file = os.path.join(output_dir, 'majority_answers_equations.jsonl')

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# This dict will store question_id as key and a dict of answer: frequency as value
answers_dict = defaultdict(lambda: defaultdict(int))

# This dict will store question_id as key and a dict of equation: frequency as value
equations_dict = defaultdict(lambda: defaultdict(int))

for i in range(10):  
    answers = pd.read_json(f'{dir_answers}sample_{i}.jsonl', lines=True)
    equations = pd.read_json(f'{dir_equations}sample_{i}.jsonl', lines=True)

    # Create a dictionary with question_id as key and answers frequencies as value
    for _, row in answers.iterrows():
        if row['chatgpt_answer'] is not None:  # Add this line
            question_id = row['question_id']
            answer = tuple(row['chatgpt_answer'])
            answers_dict[question_id][answer] += 1

    # Create a dictionary with question_id as key and equations frequencies as value
    for _, row in equations.iterrows():
        question_id = row['question_id']
        content = row['choices'][0]['message']['content']
        _, standardized_content = Standardize.standardize_equations(content.split('/n'))
        standardized_content_key = str(tuple(standardized_content))
        equations_dict[question_id][standardized_content_key] += 1

# Now, for each question_id, we'll select the answer and equation that appear most frequently
with open(output_file, 'w') as outfile:
    for question_id, answers in answers_dict.items():
        majority_answer = max(answers, key=answers.get)
        if answers[majority_answer] == 1:  # If there's no majority answer
            majority_answer = random.choice(list(answers.keys()))  # pick a random one
        
        equations = equations_dict[question_id]
        majority_equation = max(equations, key=equations.get)
        if equations[majority_equation] == 1:  # If there's no majority equation
            majority_equation = random.choice(list(equations.keys()))  # pick a random one

        output_line = {'question_id': question_id, 'majority_answer': list(majority_answer), 'majority_equation': majority_equation}
        outfile.write(json.dumps(output_line) + '\n')
