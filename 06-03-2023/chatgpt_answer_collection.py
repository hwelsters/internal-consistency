import pandas as pd
import json
import re
import os

dir_path = 'data/output/split_response/'
output_dir = 'data/output/chatgpt_answers/'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def extract_numbers(text):
    """Extract numbers from given text."""
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    numbers = [float(num) if '.' in num else int(num) for num in numbers]
    return numbers  # Return a list

for i in range(10):  
    responses = pd.read_json(f'{dir_path}sample_{i}.jsonl', lines=True)

    extracted_responses = []

    for _, row in responses.iterrows():
        # Look for the answer after "The answer is" ignoring case and line breaks
        response_text = row['response'].replace('\n', ' ')
        match = re.search(r"(?i)the answer is", response_text)
        if match:
            answer_text = response_text[match.end():]
            answer = extract_numbers(answer_text)
        else:
            answer = None

        extracted_responses.append({
            'question_id': row['question_id'],
            'chatgpt_answer': answer
        })

    # Write to jsonl file
    with open(f'{output_dir}sample_{i}.jsonl', 'w') as outfile:
        for resp in extracted_responses:
            json.dump(resp, outfile)
            outfile.write('\n')
