import os
import sys
import argparse
import xxhash
import json
import pandas as pd
import re
from tqdm import tqdm

from src.utils import read_jsonl, extract_answer


parser = argparse.ArgumentParser()

parser.add_argument("--completions-folder", type=str, default="./completions/gpt3")
parser.add_argument("--ignore-folders", type=str, nargs="+", default=[])
parser.add_argument("--file", type=str, default="./datasets/gsm8k/test.jsonl")
parser.add_argument("--results-folder", type=str, default="./results")

args = parser.parse_args()

results_folder = os.path.join(args.results_folder, "gpt3")
os.makedirs(results_folder, exist_ok=True)

completions_folders = [
    os.path.join(args.completions_folder, d) for d in os.listdir(args.completions_folder)
    if os.path.isdir(os.path.join(args.completions_folder, d)) and d not in args.ignore_folders 
]

outputs = list()
dataset = read_jsonl(args.file)
for elem in dataset:
    question = elem["question"]
    answer = extract_answer(elem["answer"])[0]

    key = xxhash.xxh32(question.encode("utf-8")).hexdigest()
    
    elem_completions = []
    for completions_folder in completions_folders:
        with open(os.path.join(completions_folder, f"{key}.json"), "r") as f:
            gpt3_output = json.load(f)
            output_numbers = [float(n) for n in re.findall("(-?\d+(?:\.\d+)?)", gpt3_output["completion"])]
            outputs.append(dict(
                key=key,
                question=question,
                answer=answer,
                completion=gpt3_output["completion"],
                solved=int(answer in output_numbers)
            ))
    

outputs = pd.DataFrame(outputs)
completions_numbers = outputs.groupby("key").count()["completion"]
assert max(completions_numbers) == min(completions_numbers), "Missing some completions"
completions_number = max(completions_numbers)

print(f"[!] Using {completions_number} completion per question")

results = list()
for elem in dataset:
    question = elem["question"]
    answer = extract_answer(elem["answer"])[0]
    key = xxhash.xxh32(question.encode("utf-8")).hexdigest()

    elem_outputs = outputs[outputs["key"] == key]
    top_solved = elem_outputs["solved"].cummax()

    result = dict(
        question=question,
        answer=answer,
    )

    for i, t in enumerate(top_solved.tolist()): result[f"top_{i+1}"] = t
    
    results.append(result)


results = pd.DataFrame(results)
results.to_excel(os.path.join(results_folder, "results.xlsx"))
outputs.to_excel(os.path.join(results_folder, "outputs.xlsx"))

top_keys = filter(lambda k: "top_" in k, results.keys())

results_avg = list()
for top_key in tqdm(top_keys):
    print(f"{top_key} solve rate: "+str(results[top_key].mean()))
    results_avg.append(dict(
        top=top_key,
        solve_rate=results[top_key].mean()
    ))

results_avg = pd.DataFrame(results_avg)
results_avg.to_excel(os.path.join(results_folder, "results_avg.xlsx"))

