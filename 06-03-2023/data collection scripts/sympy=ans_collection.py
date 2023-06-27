import os
import pandas as pd
import json
import math
import re
from collections import defaultdict

# Output file directory
output_dir = '../data/output/split_sympy=ans'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class NumberExtraction:

    @staticmethod
    def extract_decimals_from_text(text : str):
        # ======================================
        # 
        # Decimal extraction steps:
        # Step 0: Remove all commas between numbers
        #
        # ======================================
        
        extracted_decimals = re.findall(r'-?\d+\.?\d*', text)
        return extracted_decimals  

def is_sympy_equal_final_answer(row):
    solved = row['majority_solved']
    solved = NumberExtraction.extract_decimals_from_text(solved)
    solved = [float(s) for s in solved]
    solved = [round(s, 2) for s in solved]
    solved = set(solved)

    majority_answer = row['majority_answer']
    majority_answer = [round(s, 2) for s in majority_answer]
    majority_answer = set(majority_answer)

    return majority_answer.issubset(solved) and len(majority_answer) > 0

majority = pd.read_json('../data/output/majority_set/sample_0.jsonl', lines=True)
majority['sympy_equals_final_answer'] = majority.apply(lambda row : is_sympy_equal_final_answer(row), axis=1)

final_df = majority[['question_id', 'sympy_equals_final_answer']]

output_file = os.path.join(output_dir, f'sample_0.jsonl')
final_df.to_json(output_file, orient='records', lines=True)
