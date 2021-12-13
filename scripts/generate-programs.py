import argparse
import os
import xxhash
import re
import time
from tqdm import tqdm
import json

from src.utils import read_jsonl, extract_answer
from src.openai import get_completion

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="./datasets/gsm8k/test.jsonl")
parser.add_argument("--output-folder", type=str, default="./completions/codex/1")
parser.add_argument("--max-tries", type=int, default=3)
parser.add_argument("--sleep", type=float, default=1)

parser.add_argument("--model", type=str, default="davinci-codex")
parser.add_argument("--max-tokens", type=int, default=256)
parser.add_argument("--temperature", type=int, default=0.5)
parser.add_argument("--top-p", type=int, default=1)

args = parser.parse_args()

os.makedirs(args.output_folder, exist_ok=True)

dataset = read_jsonl(args.file)
for elem in tqdm(dataset):
    question = elem["question"]
    answer = extract_answer(elem["answer"])[0]

    key = xxhash.xxh32(question.encode("utf-8")).hexdigest()
    answer_file = os.path.join(args.output_folder, f"{key}.json")
    
    if os.path.exists(answer_file):
        continue

    prompt = f"#Write a Python function that solves the problem: \"{question}\"\ndef"

    completion = get_completion(
        prompt=prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        stop=["\n\n"]
    )
    tries = 0
    while "input(" in completion:
        print("Discarding input-using completion")
        completion = get_completion(
            prompt=prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            top_p=args.top_p,
            stop=["\n\n"]
        )
        tries += 1
        if tries > args.max_tries:
            print("Failed to generate an input-free completion")
            break
    
    code = prompt + completion

    functions = re.search(r"def (.+)\(", code)
    function_name = functions.group(1)

    code += f"\n#Call the function {function_name} to solve the problem: \"{question}\"\n{function_name}"
    completion = get_completion(
        prompt=code,
        model=args.model,
        temperature=args.temperature,
        max_tokens=32,
        top_p=args.top_p,
        stop=["\n"]
    )
    code += completion
    
    with open(answer_file, "w") as f:
        json.dump(dict(
            question=question,
            answer=answer,
            code=code
        ), f)
    
    time.sleep(args.sleep)
