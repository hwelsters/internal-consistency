import os
import pandas

from sympy_solver import SympySolver

def flag(solved):
    if str(solved).count('FAILED') > 0: return 'SUS'
    if str(solved).count('FREE VARIABLE') > 0: return 'FREE'
    if len(solved) == 0: return 'SUS'
    return 'OK'

for filename in os.listdir('data/output/equations'):
    print('helo')
    sample = pandas.read_json(f'data/output/equations/{filename}', lines=True)
    sample['solved'] = sample.apply(lambda row : SympySolver.solve_equations(row['choices'][0]['message']['content'].split('\n')), axis=1)
    sample['flag'] = sample['solved'].apply(lambda row : flag(row))
    sample['solved'] = sample['solved'].apply(lambda row : str(row))
    sample.to_json(f'data/output/solved/{filename}', lines=True, orient='records')