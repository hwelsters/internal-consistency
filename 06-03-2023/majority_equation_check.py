import pandas as pd
from collections import defaultdict

dir_path = 'data/output/equations/'

questions_dict = defaultdict(lambda: defaultdict(int))

for i in range(10):  
    equations = pd.read_json(f'{dir_path}sample_{i}.jsonl', lines=True)
    
    for _, row in equations.iterrows():
        content = row['choices'][0]['message']['content']  
        questions_dict[row['question_id']][content] += 1

majority_sizes = {}
majority_systems = {}
random_count = 0

for question_id, eq_dict in questions_dict.items():
    max_count = max(eq_dict.values())
    
    majority_systems_for_question = [system for system, count in eq_dict.items() if count == max_count]
    
    majority_sizes[question_id] = max_count
    majority_systems[question_id] = majority_systems_for_question[0]  

   
    is_random = 'no' if max_count > 1 else 'yes'

    if is_random == 'yes':
        random_count += 1
    
    print(f'question_id: {question_id}, majority_count = {max_count}, majority_equation = {majority_systems[question_id]}, random = {is_random}')

print(f'NUMBER OF NON-MAJORITIES: {random_count}')