import pandas as pd
import re
from collections import defaultdict
from internal_consistency.sympy_solver import Standardize

dir_path = 'data/output/equations/'

questions_dict = defaultdict(lambda: defaultdict(int))
majority_count_frequencies = defaultdict(int)

# def canonicalize_equation(equation):
#     split_by_operator = re.split(r'(\s*[+\-*/=]\s*)', equation)
    
#     variable_mapping = {}
#     next_char = 97  

#     for i, term in enumerate(split_by_operator):
#         if not re.match(r'\s*[+\-*/=]\s*', term) and not re.fullmatch(r'\d+', term.strip()):
#             non_numeric_parts = re.findall(r'\D+', term.strip())
#             number_parts = re.findall(r'\d+', term.strip())
            
#             canonicalized_parts = []
#             for j, non_numeric_part in enumerate(non_numeric_parts):
#                 if non_numeric_part not in variable_mapping:
#                     variable_mapping[non_numeric_part] = chr(next_char)
#                     next_char += 1
#                 if j < len(number_parts):
#                     canonicalized_parts.append(number_parts[j] + ' * ' + variable_mapping[non_numeric_part])
#                 else:
#                     canonicalized_parts.append(variable_mapping[non_numeric_part])
#             split_by_operator[i] = ' + '.join(canonicalized_parts)
#         else:
#             if term not in variable_mapping:
#                 variable_mapping[term] = chr(next_char)
#                 next_char += 1
#             split_by_operator[i] = variable_mapping[term]

#     return ''.join(split_by_operator)


for i in range(10):  
    equations = pd.read_json(f'{dir_path}sample_{i}.jsonl', lines=True)
    
    for _, row in equations.iterrows():
        content = row['choices'][0]['message']['content']
        variable_names, standardized_content = Standardize.standardize_equations(content.split('/n'))
        
        variable_names_key = str(tuple(variable_names))
        standardized_content_key = str(tuple(standardized_content))
        key = standardized_content_key
        
        questions_dict[row['question_id']][key] += 1

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

    majority_count_frequencies[max_count] += 1
    
    print(f'question_id: {question_id}, majority_count = {max_count}, majority_equation = {majority_systems[question_id]}, random = {is_random}')

print(f'NUMBER OF NON-MAJORITIES: {random_count}')

for count in sorted(majority_count_frequencies):
    print(f'Majority count of {count} shows up {majority_count_frequencies[count]} times.')
