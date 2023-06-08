import pandas as pd
import json
import os
from collections import defaultdict

dir_path = 'data/output/chatgpt_answers/'

questions_dict = defaultdict(lambda: defaultdict(int))
majority_count_frequencies = defaultdict(int)

for i in range(10):  
    answers = pd.read_json(f'{dir_path}sample_{i}.jsonl', lines=True)
    
    for _, row in answers.iterrows():
        answer = row['chatgpt_answer']
        
        if answer is not None:
            answer_key = str(answer)
            questions_dict[row['question_id']][answer_key] += 1

majority_sizes = {}
majority_answers = {}
random_count = 0

# For each question, store the majority counts in a list
all_majority_counts = []

for question_id, ans_dict in questions_dict.items():
    max_count = max(ans_dict.values())
    all_majority_counts.append(max_count)
    
    majority_answers_for_question = [answer for answer, count in ans_dict.items() if count == max_count]
    
    majority_sizes[question_id] = max_count
    majority_answers[question_id] = majority_answers_for_question[0]  

    is_random = 'no' if max_count > 1 else 'yes'

    if is_random == 'yes':
        random_count += 1

    majority_count_frequencies[max_count] += 1
    
    print(f'question_id: {question_id}, majority_count = {max_count}, majority_answer = {majority_answers[question_id]}, random = {is_random}')

print(f'NUMBER OF NON-MAJORITIES: {random_count}')

for count in sorted(majority_count_frequencies):
    print(f'Majority count of {count} shows up {majority_count_frequencies[count]} times.')
