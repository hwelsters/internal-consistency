import os
import pandas as pd
import json
import math
import re
from typing import List
from collections import Counter
from scipy.stats import entropy
from collections import defaultdict

dir_answers = '../data/output/chatgpt_answers/'
dir_equations = '../data/output/equations/'
dir_solved = '../data/output/solved/'
dir_check = '../data/output/split_sympy=ans/'

# Output file directory
output_dir_true = '../data/output/entropy_sympy=ans/'
output_dir_false = '../data/output/entropy_sympy!=ans/'

if not os.path.exists(output_dir_true):
    os.makedirs(output_dir_true)

if not os.path.exists(output_dir_false):
    os.makedirs(output_dir_false)

answers_dict = defaultdict(list)
equations_dict = defaultdict(list)
solved_dict = defaultdict(list)

# Function to calculate the entropy
def entropy(prob_dist):
    return abs(sum([p * math.log2(p) for p in prob_dist.values()]))

def probability_distribution(values : List[any]):
    counter = Counter(values)

    for key in counter.keys():
        counter[key] = counter[key] / len(values)
    
    return counter

def base(values : List[any], **kwargs) -> float:
    values = [str(value) for value in values]
    prob = probability_distribution(values).values()
    return entropy(pk=list(prob), **kwargs)

# Function to parse the solved string
def parse_solved_string(solved_str):
    num_list = re.findall(r"[-+]?\d*\.\d+|\d+", solved_str)
    num_list = [int(float(num)) if float(num).is_integer() else float(num) for num in num_list]
    return tuple(sorted(num_list))

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

check = pd.read_json(f'{dir_check}/sample_0.jsonl', lines=True)
check_dict = check.set_index('question_id')['sympy_equals_final_answer'].to_dict()
print(check_dict[question_id])

    
output_file_true = os.path.join(output_dir_true, f'sample_0.jsonl')
output_file_false = os.path.join(output_dir_false, f'sample_0.jsonl')

with open(output_file_true, 'w') as outfile_true, open(output_file_false, 'w') as outfile_false:
    for question_id, answers in answers_dict.items():
        # Calculating entropy for answers
        entropy_answer = calculate_entropy(answers)

        # Calculating entropy for equations
        equations = equations_dict[question_id]
        entropy_equation = calculate_entropy(equations)

        # Calculating entropy for solved
        solved = solved_dict[question_id]
        entropy_solved = calculate_entropy(solved)

        output_line = {'question_id': question_id, 'entropy_answer': entropy_answer, 'entropy_equation': entropy_equation, 'entropy_solved': entropy_solved}
        # print("Question ID: ", question_id, " is ", check_dict[question_id])
        # Write to the appropriate file
        if check_dict[question_id]:
            outfile_true.write(json.dumps(output_line) + '\n')
        else:
            outfile_false.write(json.dumps(output_line) + '\n')
