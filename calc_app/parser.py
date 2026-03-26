import re

def parse_natural_language(expr: str) -> str:
    expr = expr.lower()
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*squared', r'(\1)**2', expr)
    expr = re.sub(r'(\d+(?:\.\d+)?)\s*cubed', r'(\1)**3', expr)
    expr = re.sub(r'sqrt\s*of\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    expr = re.sub(r'square\s*root\s*of\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    expr = re.sub(r'sqrt\s*(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    return expr
