import pandas

def split_into_columns(row):
    choices = row['choices']
    for index,choice in enumerate(choices):
        message = choice['message']['content']
        row[f'sample_{index}'] = message
    return row 

data = pandas.read_json('../data/output/response/sample_0.jsonl', lines=True)
data = data.apply(lambda row : split_into_columns(row), axis=1)
for SAMPLE_NO in range(20):
    to_save = data.copy()
    to_save = to_save[['question_id', 'id', 'object', 'created', 'model', 'question', f'sample_{SAMPLE_NO}', 'n', 'temperature']]
    to_save = to_save.rename(columns={f'sample_{SAMPLE_NO}': 'response'})
    to_save.to_json(f'sample_{SAMPLE_NO}.jsonl', lines=True, orient='records')