import urllib.request
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"

PROMPT = """You are a math solver. Given a word problem, respond with ONLY the final numeric answer. No explanation, no units, just the number.

Problem: {problem}
Answer:"""

def solve_word_problem(text: str):
    payload = json.dumps({
        "model": MODEL,
        "prompt": PROMPT.format(problem=text),
        "stream": False
    }).encode()

    try:
        req = urllib.request.Request(OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result.get("response", "").strip()
    except Exception:
        return None
