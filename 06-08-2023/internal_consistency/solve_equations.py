import os
import pandas

from sympy_solver import SympySolver

for filename in os.listdir('data/output/equations'):
    sample = pandas.read_json(f'data/output/equations/{filename}', lines=True)
