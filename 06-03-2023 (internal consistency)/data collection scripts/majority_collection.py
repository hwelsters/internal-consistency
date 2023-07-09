import os
import pandas as pd
import json
import random
from collections import defaultdict

# Directories of chatgpt answers and equations
dir_answers = '../data/output/chatgpt_answers/'
dir_equations = '../data/output/equations/'
dir_solved = '../data/output/solved/'

majority_ans_10_cnt = 0
majority_solve_10_cnt = 0

output_dir = '../data/output/majority_set/'
output_file = os.path.join(output_dir, 'sample_0.jsonl')

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# This dict will store question_id as key and a dict of answer: frequency as value
answers_dict = defaultdict(lambda: defaultdict(int))

# This dict will store question_id as key and a dict of equation: frequency as value
equations_dict = defaultdict(lambda: defaultdict(int))

solved_dict = defaultdict(lambda: defaultdict(int))

for i in range(10):  
    answers = pd.read_json(f'{dir_answers}sample_{i}.jsonl', lines=True)
    equations = pd.read_json(f'{dir_equations}sample_{i}.jsonl', lines=True)
    solved = pd.read_json(f'{dir_solved}sample_{i}.jsonl', lines=True)

    for _, row in answers.iterrows():
        if row['chatgpt_answer'] is not None:  
            question_id = row['question_id']
            content = tuple(row['chatgpt_answer'])
            answers_dict[question_id][content] += 1

    for _, row in equations.iterrows():
        if row['choices'][0]['message']['content'] is not None: 
            question_id = row['question_id']
            content = row['choices'][0]['message']['content']
            equations_dict[question_id][content] += 1

    for _, row in solved.iterrows():
        if row['solved'] is not None:
            question_id = row['question_id']
            content = str(row['solved'])  
            solved_dict[question_id][content] += 1

# Now, for each question_id, we'll select the answer and equation that appear most frequently
with open(output_file, 'w') as outfile:
    for question_id, answers in answers_dict.items():
        majority_answer = max(answers, key=answers.get)
        majority_answer_freq = answers[majority_answer]
        if majority_answer_freq == 10:
            majority_ans_10_cnt += 1
        if majority_answer_freq == 1:  # If there's no majority answer
            majority_answer = random.choice(list(answers.keys()))  # pick a random one
            majority_answer_freq = answers[majority_answer]

        
        equations = equations_dict[question_id]
        majority_equation = max(equations, key=equations.get)
        majority_equation_freq = equations[majority_equation]
        if majority_equation_freq == 1:  # If there's no majority equation
            majority_equation = random.choice(list(equations.keys()))  # pick a random one
            majority_equation_freq = equations[majority_equation]

        solved = solved_dict[question_id]
        majority_solved = max(solved, key=solved.get)
        majority_solved_freq = solved[majority_solved]
        if majority_solved_freq == 10:
            majority_solve_10_cnt += 1
        if majority_solved_freq == 1:
            majority_solved = random.choice(list(solved.keys()))  # pick a random one
            majority_solved_freq = solved[majority_solved]

        output_line = {'question_id': question_id, 'majority_answer': list(majority_answer), 'majority_answer_freq': majority_answer_freq, 'majority_equation': majority_equation, 'majority_equation_freq': majority_equation_freq, 'majority_solved': majority_solved,
            'majority_solved_freq': majority_solved_freq}
        outfile.write(json.dumps(output_line) + '\n')

print(majority_solve_10_cnt)
