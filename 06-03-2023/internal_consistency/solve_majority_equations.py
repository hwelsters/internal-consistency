import os
import pandas as pd

from sympy_solver import SympySolver

def flag(solved):
    if str(solved).count('FAILED') > 0: return 'SUS'
    if str(solved).count('FREE VARIABLE') > 0: return 'FREE'
    if len(solved) == 0: return 'SUS'
    return 'OK'

# Load response data
sample_response = pd.read_json('../data/output/response/sample_0.jsonl', lines=True)

# Function to get all the assistant's responses
def get_responses(question_id):
    response_row = sample_response[sample_response['question_id'] == question_id]
    if response_row.empty:
        return []
    else:
        return [choice['message']['content'] for choice in response_row.iloc[0]['choices']]

for filename in os.listdir('../data/output/majority'):
    print(filename)
    sample = pd.read_json(f'../data/output/majority/{filename}', lines=True)

    for i in range(10):  # limit to first 10 responses
        samplex = sample.copy()
        samplex['solved'] = sample.apply(lambda row : SympySolver.solve_equations(row['majority_equation'].split('\n')), axis=1)
        samplex['flag'] = samplex['solved'].apply(lambda row : flag(row))
        samplex['solved'] = samplex['solved'].apply(lambda row : str(row))
        
        samplex['response'] = samplex['question_id'].apply(lambda row : get_responses(row)[i] if len(get_responses(row)) > i else None)
        samplex.to_json(f'../data/output/solve_majority_test/sample_{i}.jsonl', lines=True, orient='records')
