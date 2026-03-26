import re
import math
from fractions import Fraction
from .parser import parse_natural_language
from .fractions import parse_fractions
from .variables import variables

def calc(expr: str):
    expr = parse_natural_language(expr)
    expr = parse_fractions(expr)
    expr = re.sub(r'(\d+(?:\.\d+)?|\w+)\^(\d+(?:\.\d+)?|\w+)', r'\1**\2', expr)

    safe_dict = {
        '__builtins__': {},
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'pi': math.pi,
        'e': math.e,
        'Fraction': Fraction,
    }

    for name, value in variables.items():
        expr = expr.replace(name, str(value))

    try:
        result = eval(expr, safe_dict)

        if str(result) == 'inf':
            return "Invalid - Division by zero"
        if str(result) == 'nan':
            return "Invalid - Not a number"

        if isinstance(result, Fraction):
            if result.denominator == 1:
                return result.numerator
            if abs(result.numerator) > result.denominator:
                whole = result.numerator // result.denominator
                remainder = abs(result.numerator) % result.denominator
                if remainder == 0:
                    return whole
                return f"{whole} {remainder}/{result.denominator}"
            return f"{result.numerator}/{result.denominator}"

        return result

    except ZeroDivisionError:
        return "Invalid - Division by zero"
    except NameError as e:
        return f"Invalid - Unknown variable: {str(e).split(chr(39))[1]}"
    except SyntaxError:
        return "Invalid - Syntax error"
    except ValueError as e:
        return f"Invalid - Value error: {str(e)}"
    except:
        return "Invalid - Math error"
