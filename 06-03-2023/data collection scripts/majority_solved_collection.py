import os
import pandas as pd
import json
from collections import defaultdict
import ast

# Set the directories
dir_solved = 'data/output/solved/'
output_dir = 'data/output/majority_solved/'

# If the output directory does not exist, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize the dictionary that will store the counts for each question_id
counts = defaultdict(lambda: defaultdict(int))

# Loop over all the files in the directory
for filename in os.listdir(dir_solved):
    if filename.endswith(".jsonl"):
        # Load the data from the current file
        solved_df = pd.read_json(os.path.join(dir_solved, filename), lines=True)

        # Loop over all the rows in the dataframe
        for _, row in solved_df.iterrows():
            if row['solved'] is not None:
                # Count the occurrence of the "solved" value for each question_id
                solved = str(row['solved'])  # Convert the "solved" value to string
                question_id = row['question_id']
                counts[question_id][solved] += 1

# Prepare to write the output to a file
output_file = os.path.join(output_dir, 'majority_solved.jsonl')

with open(output_file, 'w') as f:
    # Loop over all question_ids and their counts
    for question_id, solved_counts in counts.items():
        # Find the "solved" value that occurred most often
        majority_solved = max(solved_counts, key=solved_counts.get)
        majority_solved_freq = solved_counts[majority_solved]

        # Write the question_id, majority_solved, and majority_solved_freq to the output file
        output_line = {
            'question_id': question_id,
            'majority_solved': majority_solved,
            'majority_solved_freq': majority_solved_freq,
        }
        f.write(json.dumps(output_line) + '\n')

