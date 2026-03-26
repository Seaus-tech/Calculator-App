import re
from fractions import Fraction

def solve_equation(equation: str) -> str | None:
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
