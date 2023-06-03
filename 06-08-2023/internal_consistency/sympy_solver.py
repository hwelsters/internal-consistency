import re

from sympy import parse_expr, Rel, solve
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations
from sympy.parsing.sympy_parser import T

from typing import List

class Canonicalize:
    def remove_leading_digits   (text : str) -> str: return re.sub(r"^\d+.?\d*", "", text)
    def remove_dollar_sign      (text : str) -> str: return text.replace('$', '')
    def replace_percentage      (text : str) -> str: return text.replace('%', '*0.01')
    def remove_excess_space     (text : str) -> str: return re.sub(r' +', ' ', text)

    def extract_variable_names  (equations : List[str]) -> List[str]:
        for equation in equations:
            math_symbol_tokens = re.split(r'[\+\-\/\*]', equation)
            

    def canonicalize_equations  (equations : List[str]) -> List[str]:   
        equations = list(map(lambda equation : Canonicalize.remove_dollar_sign(equation), equations))
        equations = list(map(lambda equation : Canonicalize.replace_percentage(equation), equations))
        equations = list(map(lambda equation : Canonicalize.remove_excess_space(equation), equations))
        return equations

class SympySolver:
    def __init__(self) -> None:
        pass

    # TODO: AAAAAAAAAAAAAAAAAAAAAHH
    # SO UGLY AND MESSY, REFACTOR THIS MESS!
    # Split the steps up into functions
    @staticmethod
    def canonicalize_equations(equations):
        # Step 1: Find all unique variables
        tokens = []
        for equation in equations:
            cleaned_equations = re.sub(r'[^\s\_a-zA-Z]', '[bingbonkdonkconk]', equation)   
            cleaned_equations = re.sub(r'\s+', ' ', cleaned_equations)   
            split_equations = cleaned_equations.split('[bingbonkdonkconk]')
            split_equations = [equation.strip() for equation in split_equations]
            split_equations = list(filter(lambda text : len(text) > 0, split_equations))
            tokens += split_equations
        tokens = list(set(tokens))
        tokens = list(sorted(tokens, key=len))
        tokens = list(reversed(tokens))

        # Step 2: Replace all the variables with a unique 
        # single-letter representation
        print('\n\n\n\n\n')
        new_equations = []
        for equation in equations:
            print("CANNOOON", equation)
            print("Tokens", tokens)
            for index, token in enumerate(tokens):
                print(index, token)
                var_char = chr(index + 97)
                equation = equation.replace(token, var_char)
                print(equation)
            new_equations.append(equation)
        
        print("BONKUS", new_equations)
        return new_equations


    def create_expression(equation : str):
        split_equations = equation.split('=')
        return Rel(
            parse_expr(split_equations[0], transformations=T[:6]),
            parse_expr(split_equations[1], transformations=T[:6]),
            'eq'
        )

    @staticmethod
    def generate_system_of_equations(equations):
        to_return = []

        for equation in equations:
            try: to_return.append(SympySolver.create_expression(equation))
            except: pass

        return to_return
    
    @staticmethod
    def solve_equations(equations):
        equations = filter(lambda equation : equation.count('=') > 0, equations)
        equations = list(equations)

        solved_base = set()
        solved_canonicalized = set()

        try:
            base_system = SympySolver.generate_system_of_equations(equations=equations)
            solved_base = set(utils.extract_numbers(str(solve(base_system))))
        except: pass

        try:
            canonicalize_equations = SympySolver.canonicalize_equations(equations=equations)
            canonicalized_system = SympySolver.generate_system_of_equations(equations=canonicalize_equations)
            solved_canonicalized = set(utils.extract_numbers(str(solve(canonicalized_system))))
        except: pass
        
        # TODO: hahahahahahahaha... NO. Split this into its own function
        return solved_base.union(solved_canonicalized)

