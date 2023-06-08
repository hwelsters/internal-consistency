import os
import pandas

from sympy_solver import SympySolver

def flag(solved):
    if str(solved).count('FAILED') > 0: return 'SUS'
    if str(solved).count('FREE VARIABLE') > 0: return 'FREE'
    if len(solved) == 0: return 'SUS'
    return 'OK'

for filename in os.listdir('../data/output/majority'):
    print(filename)
    sample = pandas.read_json(f'../data/output/majority/{filename}', lines=True)
    samplex = pandas.DataFrame()
    samplex['solved'] = sample.apply(lambda row : SympySolver.solve_equations(row['majority_equation'].split('\n')), axis=1)
    samplex['flag'] = samplex['solved'].apply(lambda row : flag(row))
    samplex['solved'] = samplex['solved'].apply(lambda row : str(row))
    samplex.to_json(f'../data/output/solve_majority/{filename}', lines=True, orient='records')