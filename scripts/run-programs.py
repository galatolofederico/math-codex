import os
import sys
import random
import argparse
import xxhash
import json
import pandas as pd
from tqdm import tqdm

from src.utils import read_jsonl, extract_answer
from src.execute import execute_program_fast


parser = argparse.ArgumentParser()

parser.add_argument("--completions-folder", type=str, default="./completions/codex")
parser.add_argument("--num-programs", type=int, default=10)
parser.add_argument("--file", type=str, default="./datasets/gsm8k/test.jsonl")
parser.add_argument("--output-folder", type=str, default="./results")

args = parser.parse_args()

output_folder = os.path.join(args.output_folder, "codex")
os.makedirs(output_folder, exist_ok=True)

completions_folders = [
    os.path.join(args.completions_folder, d) for d in os.listdir(args.completions_folder)
    if os.path.isdir(os.path.join(args.completions_folder, d)) 
]

codes = dict()
dataset = read_jsonl(args.file)
for elem in tqdm(dataset):
    question = elem["question"]
    answer = extract_answer(elem["answer"])[0]

    key = xxhash.xxh32(question.encode("utf-8")).hexdigest()
    
    programs = []
    for completions_folder in completions_folders:
        with open(os.path.join(completions_folder, f"{key}.json"), "r") as f:
            completions = json.load(f)
            program = completions["code"]
            output = execute_program_fast(program)
            output["program"] = program
            output["key"] = key
            if output["valid"] and not output["halts"] and not output["error"]:
                programs.append(output)
        if len(programs) == args.num_programs:
            break
    
    if len(programs) == args.num_programs:
        codes[key] = dict(
            question=question,
            answer=answer,
            programs=programs
        )
    else:
        print(f"Skipping element: {key}. Not enough programs")


outputs = []
for key, code in tqdm(codes.items()):
    for program in code["programs"]:
        outputs.append(program)

df = pd.DataFrame(outputs)
df.to_pickle(os.path.join(output_folder, "outputs.pkl"))
