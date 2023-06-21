import os
import pandas as pd
import json

# Directories of majority answers and entropy
dir_majority = '../data/output/majority_set/'
dir_entropy = '../data/output/entropy/'

# Loading majority data
majority_file = os.path.join(dir_majority, 'sample_0.jsonl')
majority_data = pd.read_json(majority_file, lines=True)

# Loading entropy data
entropy_file = os.path.join(dir_entropy, 'sample_0.jsonl')
entropy_data = pd.read_json(entropy_file, lines=True)

# Merging two dataframes on question_id
merged_data = pd.merge(majority_data, entropy_data, on='question_id')

anomaly_count = 0

# Filtering data where entropy_solution is 0 and majority_answer_freq is not 10
filtered_data = merged_data[(merged_data['entropy_solved'] == 0) & (merged_data['majority_solved_freq'] != 10)]

# Printing question_ids
for _, row in filtered_data.iterrows():
    print(row['question_id'])
    anomaly_count += 1

print("Anomalies:" , anomaly_count)
