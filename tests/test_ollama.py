import re
from llama_cpp import Llama
import os
os.environ["GGML_LOG_LEVEL"] = "ERROR"
os.environ["LLAMA_LOG_LEVEL"] = "ERROR"
os.environ["LLAMA_CPP_LOG_LEVEL"] = "ERROR"
MODEL_PATH = os.path.join("models", "qwen2.5-1.5b-instruct-q4_k_m.gguf")
llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4
)

import random
import re

def extract_tags(text: str):
    # split per righe e pulizia base
    candidates = []

    for line in text.split("\n"):
        t = line.strip().lower()

        # pulizia caratteri strani
        t = re.sub(r"[^a-zA-Z\- ]", "", t).strip()

        if not t:
            continue

        # max 2 parole
        if 1 <= len(t.split()) <= 2:
            candidates.append(t)

    # dedup mantenendo ordine
    seen = set()
    unique = []
    for c in candidates:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    if not unique:
        return []

    # scegli random 2 o 3
    k = random.choice([2, 3])
    k = min(k, len(unique))

    return random.sample(unique, k)

def generate_tags(text: str):
    prompt = f"""
You are a tag generator.
Rules:
- Output ONLY 2 or 3 English tags
- English only.
- One or two words maximum per tag.
- comma separated
- no explanation
- No numbering.
Input:
{text}
Output:
"""
    output = llm(
        prompt,
        max_tokens=30,
        temperature=0.2,
        stop=["\n\n"]
    )
    result = output["choices"][0]["text"]
    print("ORIGINAL-------->", result)
    return extract_tags(result)

print("------------------------->" , generate_tags("Porsche Racing"))
print("------------------------->" , generate_tags("Oggi ho voglia di mare"))

