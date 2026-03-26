# aurora_calc/core.py

import re
import math
from fractions import Fraction

variables = {}
meme_mode = False

def parse_natural_language(expr):
    expr = expr.lower()
    expr = re.sub(r'(\d+(?:\.\d+)?)\s+squared', r'(\1)**2', expr)
    expr = re.sub(r'(\d+(?:\.\d+)?)\s+cubed', r'(\1)**3', expr)
    expr = re.sub(r'sqrt\s+of\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    expr = re.sub(r'square\s+root\s+of\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    expr = re.sub(r'sqrt\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    return expr

def parse_fractions(expr):
    def mixed_fraction_replacer(match):
        whole, num, den = match.groups()
        improper_num = int(whole) * int(den) + int(num)
        return f'Fraction({improper_num}, {den})'

    expr = re.sub(r'(\d+)\s+(\d+)/(\d+)', mixed_fraction_replacer, expr)

    def fraction_replacer(match):
        num, den = match.groups()
        return f'Fraction({num}, {den})'

    expr = re.sub(r'(\d+)/(\d+)', fraction_replacer, expr)
    return expr

def solve_equation(equation):
    if '=' not in equation:
        return None

    left, right = equation.split('=', 1)
    left, right = left.strip(), right.strip()

    var_match = re.search(r'[a-zA-Z]', left)
    if not var_match:
        return None

    var = var_match.group()

    left = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', left)
    left = re.sub(r'([a-zA-Z])\^(\d+)', r'\1**\2', left)

    try:
        if '**2' not in left and '*' in left:
            try:
                const_expr = left.replace(var, '0')
                b = eval(const_expr)

                coeff_expr = left.replace(var, '1')
                a_plus_b = eval(coeff_expr)
                a = a_plus_b - b

                c = eval(right)

                if a != 0:
                    solution = (c - b) / a
                    if abs(solution - round(solution)) < 0.0001:
                        return f"{var} = {int(round(solution))}"
                    else:
                        frac = Fraction(solution).limit_denominator(10000)
                        if frac.denominator == 1:
                            return f"{var} = {frac.numerator}"
                        return f"{var} = {frac.numerator}/{frac.denominator}"
            except:
                pass

        for test_val in range(-100000, 100001):
            try:
                test_expr = left.replace(var, str(test_val))
                if abs(eval(test_expr) - eval(right)) < 0.0001:
                    return f"{var} = {test_val}"
            except:
                continue

    except:
        pass

    return "Could not solve equation"

def calc(expr):
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
        'Fraction': Fraction
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

def main():
    global meme_mode

    print("Simple Calculator - Type math expressions or 'quit'")
    print("Type 'meme' to toggle meme mode!")

    while True:
        try:
            line = input("\n> ").strip()

            if line == 'quit':
                break

            if line == 'meme':
                meme_mode = not meme_mode
                print("Meme mode:", "ON" if meme_mode else "OFF")
                continue

            if '=' in line and re.search(r'[a-zA-Z]', line):
                print(solve_equation(line))
                continue

            if meme_mode and line == '9+10':
                print("= 21 😂")
                continue

            print("= " + str(calc(line)))

        except KeyboardInterrupt:
            break
        except:
            print("Error - try again")
