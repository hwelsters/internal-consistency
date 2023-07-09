import os
import pandas

for filename in os.listdir('data/output/solved'):
    sample = pandas.read_json(f'data/output/solved/{filename}')
    sample['response_correct'] = 
    sample['equations_correct'] 