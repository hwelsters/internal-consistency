BASIC_PROMPT = '''Solve the math question below:
Solve by breaking the problem into steps. 
First, produce the algebraic system of equations needed to solve it. 
Second, output the final answer; format it like this: 'The answer is <put your answer here>'.

Question: {question}
'''.strip() + '\n\n\n'

EXTRACT_EQUATIONS = '''
Extract the equations from this response.
You should give me the minimal system of equations needed to solve the question.
You should not describe your steps, or explain or label your response.
You should separate each equation with a new line.
You should remove all units from your response.

Response: {response}
'''.strip() + '\n\n\n'

SOLVE_SYSTEM = '''
Solve the following system of equations:
First, solve the equations step-by-step
Second, output the final answer; format it like this: 'The answer is <put your answer here>'.

Equations:
{equations}
'''.strip() + '\n\n\n'