import re

from sympy import parse_expr, Rel, solve
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations
from sympy.parsing.sympy_parser import T

from typing import List

class Standardize:
    def remove_leading_digits   (text : str) -> str: return re.sub(r"^\d+.?\d*", "", text)
    def remove_dollar_sign      (text : str) -> str: return text.replace('$', '')
    def replace_percentage      (text : str) -> str: return text.replace('%', '*0.01')
    def remove_excess_space     (text : str) -> str: return re.sub(r' +', ' ', text)

    def extract_variable_names  (equations : List[str]) -> List[str]:
        variable_names = []
        for equation in equations:
            # Step 1: Split it using math symbols
            math_symbol_tokens = re.split(r'[\+\-\/\*]', equation)

            # Step 2: Remove surrounding whitespace from tokens
            math_symbol_tokens = list(map(lambda equation : equation.strip(), math_symbol_tokens))

            # Step 3: Remove leading digits from tokens
            math_symbol_tokens = list(map(lambda equation : Standardize.remove_leading_digits(equation), math_symbol_tokens))

            # Step 4: Remove all tokens of length 0
            math_symbol_tokens = list(filter(lambda equation : len(equation) > 0, math_symbol_tokens))

            variable_names += math_symbol_tokens
        variable_names = list(set(variable_names))
        variable_names.sort(key=len, reverse=True)
        return variable_names

    def replace_variables_with_standard_form(equation : str, variable_names : List[str]) -> str:
        for index, variable_name in enumerate(variable_names): equation = equation.replace(variable_name, chr(index + 97))
        return equation

    def standardize_equations  (equations : List[str]) -> List[str]:   
        equations = list(map(lambda equation : Standardize.remove_dollar_sign(text=equation), equations))
        equations = list(map(lambda equation : Standardize.replace_percentage(text=equation), equations))
        equations = list(map(lambda equation : Standardize.remove_excess_space(text=equation), equations))
        variable_names = Standardize.extract_variable_names(equations=equations)
        equations = list(map(lambda equation : Standardize.replace_variables_with_standard_form(equation=equation, variable_names=variable_names), equations))
        return equations

class SympySolver:
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
        # Step 1: Remove all lines that do not contain an equal symbol
        equations = filter(lambda equation : equation.count('=') > 0, equations)
        equations = Standardize.standardize_equations(equations)

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

