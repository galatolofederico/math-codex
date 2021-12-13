import argparse
import os
import openai
import xxhash
import re
import time
from tqdm import tqdm
import json

from src.utils import read_jsonl, extract_answer
from src.openai import get_completion

parser = argparse.ArgumentParser()

parser.add_argument("--file", type=str, default="./datasets/gsm8k/test.jsonl")
parser.add_argument("--output-folder", type=str, default="./completions/gpt3/1")
parser.add_argument("--sleep", type=float, default=1)

parser.add_argument("--model", type=str, default="davinci")
parser.add_argument("--max-tokens", type=int, default=64)
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

    prompt = f"Question: \"{question}\"\nAnswer:"

    completion = get_completion(
        prompt=prompt,
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        stop=["\n"]
    )
        
    with open(answer_file, "w") as f:
        json.dump(dict(
            question=question,
            answer=answer,
            completion=completion
        ), f)
    
    time.sleep(args.sleep)
