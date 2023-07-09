import os
import pandas as pd
import json
import math
import re
from collections import defaultdict

dir_answers = '../data/output/chatgpt_answers/'
dir_equations = '../data/output/equations/'
dir_solved = '../data/output/solved/'

# Output file directory
output_dir = '../data/output/entropy'
output_file = os.path.join(output_dir, 'sample_0.jsonl')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

answers_dict = defaultdict(list)
equations_dict = defaultdict(list)
solved_dict = defaultdict(list)

# Function to calculate the entropy
def entropy(prob_dist):
    return abs(sum([p * math.log2(p) for p in prob_dist.values()]))

def calculate_entropy(data):
    prob_dist = {}
    total_data = len(data)
    for item in data:
        if item in prob_dist:
            prob_dist[item] += 1
        else:
            prob_dist[item] = 1
    # Converting counts into probabilities
    prob_dist = {k: v/total_data for k, v in prob_dist.items()}
    # Calculating entropy
    return entropy(prob_dist)

# Function to parse the solved string
def parse_solved_string(solved_str):
    num_list = re.findall(r"[-+]?\d*\.\d+|\d+", solved_str)
    num_list = [int(float(num)) if float(num).is_integer() else float(num) for num in num_list]
    return tuple(sorted(num_list))


for i in range(10):
    answers = pd.read_json(f'{dir_answers}/sample_{i}.jsonl', lines=True)
    equations = pd.read_json(f'{dir_equations}/sample_{i}.jsonl', lines=True)
    solved = pd.read_json(f'{dir_solved}/sample_{i}.jsonl', lines=True)

    for _, row in answers.iterrows():
        question_id = row['question_id']
        answer = row['chatgpt_answer'] if row['chatgpt_answer'] is not None else [-1]
        answers_dict[question_id].append(tuple(answer))

    for _, row in equations.iterrows():
        question_id = row['question_id']
        equation = row['choices'][0]['message']['content'] if row['choices'][0]['message']['content'] is not None else 'null'
        equations_dict[question_id].append(equation)

    for _, row in solved.iterrows():
        question_id = row['question_id']
        solved_str = row['solved'] if row['solved'] is not None else ''
        solved_tuple = parse_solved_string(solved_str)
        solved_dict[question_id].append(solved_tuple)


entropy_zero_counter = 0
with open(output_file, 'w') as outfile:
    for question_id, answers in answers_dict.items():
        # Calculating entropy for answers
        entropy_answer = calculate_entropy(answers)

        # Calculating entropy for equations
        equations = equations_dict[question_id]
        entropy_equation = calculate_entropy(equations)

        # Calculating entropy for solved
        solved = solved_dict[question_id]
        entropy_solved = calculate_entropy(solved)

        output_line = {'question_id': question_id, 'entropy_solution': entropy_answer, 'entropy_equation_strict': entropy_equation, 'entropy_equation_loose': entropy_solved}
        outfile.write(json.dumps(output_line) + '\n')

print(f"Entropy is zero for {entropy_zero_counter} questions.")
