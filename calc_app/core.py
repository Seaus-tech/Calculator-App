import re
from .solver import solve_equation
from .evaluator import calc
from .meme import handle_meme
from .variables import variables

meme_mode = False

def main():
    global meme_mode

    print("Simple Calculator - Type math expressions or 'quit'")
    print("Set variables: x=5")
    print("Use in math: x+3, 2*x, etc.")
    print("Solve equations: 6+x=7, 2*x-3=5")
    print("Functions: sqrt(16), 9**2, sin(pi/2)")
    print("Natural language: '9 squared', 'sqrt of 16', '5 cubed'")
    print("Fractions: 1/2 + 1/3, 2 1/2 + 3/4")
    print("Type 'meme' to toggle meme mode!")

    while True:
        try:
            line = input("\n> ").strip()

            if line == 'quit':
                break

            if line == 'meme':
                meme_mode = not meme_mode
                status = "ON 😂" if meme_mode else "OFF"
                print(f"Meme mode: {status}")
                continue

            if '=' in line and re.search(r'[a-zA-Z]', line):
                result = solve_equation(line)
                print(result)
                continue

            if '=' in line and not any(op in line.split('=')[0] for op in ['+', '-', '*', '/']):
                name, value = line.split('=', 1)
                variables[name.strip()] = float(value.strip())
                print(f"Set {name.strip()} = {value.strip()}")
                continue

            meme_output = handle_meme(line, meme_mode)
            if meme_output:
                print(meme_output)
                continue

            result = calc(line)
            print(f"= {result}")

        except KeyboardInterrupt:
            break
        except Exception:
            print("Error - try again")
