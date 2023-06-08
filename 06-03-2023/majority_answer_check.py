import pandas as pd
import numpy as np
import json
import re
import os
from collections import defaultdict

dir_path = 'data/output/split_response/'
output_dir = 'data/output/chatgpt_answers/'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

questions_dict = defaultdict(lambda: defaultdict(int))
majority_count_frequencies = defaultdict(int)

# Loop through all the jsonl files
for i in range(10):
    with open(f'{dir_path}sample_{i}.jsonl', 'r') as file:
        for line in file:
            data = json.loads(line)
            question_id = data['question_id']
            response = data['response']

            # Regular expression to find the numbers after 'the answer is'
            match = re.search(r'the answer is(.*?)\.($|\n)', response, re.IGNORECASE)

            if match:
                answer_text = match.group(1)
                answer_numbers = re.findall(r'\b\d+\b', answer_text)
                answer_set = {int(number) for number in answer_numbers}
                
                key = str(answer_set)  # Use the set of answer numbers as the key
                questions_dict[question_id][key] += 1

    # For each file, store the majority counts and answers for each question into a new jsonl file
    with open(f'{output_dir}sample_{i}.jsonl', 'w') as outfile:
        for question_id, ans_dict in questions_dict.items():
            max_count = max(ans_dict.values())
            majority_answers_for_question = [answer for answer, count in ans_dict.items() if count == max_count]
            
            # Write the question id and majority answer as a json object to the new file
            json.dump({
                'question_id': question_id, 
                'chatgpt_answer': majority_answers_for_question[0]
            }, outfile)
            outfile.write('\n')

    # Reset the questions_dict for the next file
    questions_dict = defaultdict(lambda: defaultdict(int))
