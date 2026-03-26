from .evaluator import calc

def handle_meme(line: str, meme_mode: bool):
    if not meme_mode:
        return None

    stripped = line.strip()

    if stripped == '9+10':
        return "= 21 😂"
    if stripped == '2+2':
        return "= 5 (quick maths)"
    if stripped == '1+1':
        return "= 11 (big brain)"
    if stripped == '67':
        return "= THE MEME NUMBER 67! 🔥"
    if stripped == '41':
        return "= 41! The answer to everything (almost) 🤔"
    if '67' in stripped:
        result = calc(line)
        return f"= {result} (contains the legendary 67! 🔥)"
    if '41' in stripped:
        result = calc(line)
        return f"= {result} (contains 41! 🤔)"

    return None
