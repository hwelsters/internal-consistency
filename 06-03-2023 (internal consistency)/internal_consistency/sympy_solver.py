import re

from sympy import parse_expr, Rel, solve
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations
from sympy.parsing.sympy_parser import T

import threading
from time import sleep
import sys

try:
    import thread
except ImportError:
    import _thread as thread

from typing import List

class Standardize:
    def remove_leading_digits   (text : str) -> str: return re.sub(r"^\d+\.?\d*", "", text)
    def remove_dollar_sign      (text : str) -> str: return text.replace('$', '')
    def replace_percentage      (text : str) -> str: return text.replace('%', '*0.01')
    def remove_excess_space     (text : str) -> str: return re.sub(r' +', ' ', text)
    def replace_special_symbols (text : str) -> str:
        text = text.replace('½', '1/2')
        text = text.replace('¼', '1/4')
        text = text.replace('\'', '')
        text = text.replace(',', '')
        return text

    def extract_variable_names  (equations : List[str]) -> List[str]:
        variable_names = []
        for equation in equations:
            # Step 1: Split it using math symbols
            math_symbol_tokens = re.split(r'[\+\-\/\*\=\(\)]', equation)

            # Step 2: Remove surrounding whitespace from tokens
            math_symbol_tokens = list(map(lambda equation : equation.strip(), math_symbol_tokens))

            # Step 3: Remove leading digits from tokens
            math_symbol_tokens = list(map(lambda equation : Standardize.remove_leading_digits(equation), math_symbol_tokens))

            # Step 4: Remove all tokens of length 0
            math_symbol_tokens = list(filter(lambda equation : len(equation) > 0, math_symbol_tokens))

            variable_names += math_symbol_tokens
        
        # Ensure that all variable names are unique
        variable_names = list(set(variable_names))

        # Sort it in descending order based on variable name length
        variable_names.sort(reverse=True)
        variable_names.sort(key=len, reverse=True)
        return variable_names

    def replace_variables_with_standard_form(equation : str, variable_names : List[str]) -> str:
        for index, variable_name in enumerate(variable_names): equation = equation.replace(variable_name, chr(index + 97))
        return equation

    def standardize_equations  (equations : List[str]) -> List[str]:
        equations = list(map(lambda equation : equation.lower(), equations))
        equations = list(map(lambda equation : Standardize.remove_dollar_sign(text=equation), equations))
        equations = list(map(lambda equation : Standardize.replace_percentage(text=equation), equations))
        equations = list(map(lambda equation : Standardize.remove_excess_space(text=equation), equations))
        equations = list(map(lambda equation : Standardize.replace_special_symbols(text=equation), equations))
        variable_names = Standardize.extract_variable_names(equations=equations)
        equations = list(map(lambda equation : Standardize.replace_variables_with_standard_form(equation=equation, variable_names=variable_names), equations))
        return variable_names, equations

class SympySolver:
    def quit_function(fn_name):
        # print to stderr, unbuffered in Python 2.
        sys.stderr.flush() # Python 3 stderr is likely buffered.
        thread.interrupt_main() # raises KeyboardInterrupt
    # ------------------------------------------- #
    #   A function that times out functions 
    #   after a certain period of time
    # ------------------------------------------- #
    def exit_after(s):
        '''
        use as decorator to exit process if 
        function takes longer than s seconds
        '''
        def outer(fn):
            def inner(*args, **kwargs):
                timer = threading.Timer(s, SympySolver.quit_function, args=[fn.__name__])
                timer.start()
                try:
                    result = fn(*args, **kwargs)
                finally:
                    timer.cancel()
                return result
            return inner
        return outer
    
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
    
    @exit_after(3)
    def capped_solve(equations):
        # Step 1: Remove all lines that do not contain an equal symbol
        equations = list(filter(lambda equation : equation.count('=') > 0, equations))

        # Step 2: Standardize the equations
        variable_names, equations = Standardize.standardize_equations(equations)
        equations = SympySolver.generate_system_of_equations(equations)
        try: 
            solved = solve(equations)
            if len(solved) != len(variable_names): return 'FREE VARIABLE' + str(solved)
            return solved
        except: return "FAILED"
    
    def solve_equations(equations):
        try: return SympySolver.capped_solve(equations)
        except: return "TIMEOUT"
