import re

def parse_fractions(expr: str) -> str:
    from fractions import Fraction  # local import for string generation

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
