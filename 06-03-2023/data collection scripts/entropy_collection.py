import os
import pandas as pd
import json
import math
from collections import defaultdict

# Directory of chatgpt answers
dir_answers = '../data/output/chatgpt_answers/'

# Output file directory
output_dir = '../data/output/entropy'
output_file = os.path.join(output_dir, 'sample0.jsonl')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# This dict will store question_id as key and a list of chatgpt_answer as value
answers_dict = defaultdict(list)

# Function to calculate the entropy
def entropy(prob_dist):
    return abs(sum([p * math.log2(p) for p in prob_dist.values()]))

# Reading files and populating answers_dict
for i in range(10):
    answers = pd.read_json(f'{dir_answers}/sample_{i}.jsonl', lines=True)
    for _, row in answers.iterrows():
        if row['chatgpt_answer'] is not None:
            question_id = row['question_id']
            # Treat the whole list of answers as a single answer
            answers_dict[question_id].append(tuple(row['chatgpt_answer']))

# Now, for each question_id, we'll calculate the entropy of answers
entropy_zero_counter = 0
with open(output_file, 'w') as outfile:
    for question_id, answers in answers_dict.items():
        prob_dist = {}
        total_answers = len(answers)
        for answer in answers:
            if answer in prob_dist:
                prob_dist[answer] += 1
            else:
                prob_dist[answer] = 1
        # Converting counts into probabilities
        prob_dist = {k: v/total_answers for k, v in prob_dist.items()}
        # Calculating entropy
        entropy_answer = entropy(prob_dist)
        if entropy_answer == 0:
            entropy_zero_counter += 1
        output_line = {'question_id': question_id, 'entropy_solution': entropy_answer}
        outfile.write(json.dumps(output_line) + '\n')

print(f"Entropy is zero for {entropy_zero_counter} questions.")
