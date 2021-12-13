import os
import argparse
import xxhash
import pandas as pd
import re
from tqdm import tqdm

from src.utils import read_jsonl, extract_answer

parser = argparse.ArgumentParser()

parser.add_argument("--programs-outputs", type=str, default="./results/codex/outputs.pkl")
parser.add_argument("--results-folder", type=str, default="./results/codex")
parser.add_argument("--file", type=str, default="./datasets/gsm8k/test.jsonl")

args = parser.parse_args()

dataset = read_jsonl(args.file)
outputs = pd.read_pickle(args.programs_outputs)
answers = dict()
questions = dict()

for elem in tqdm(dataset):
    question = elem["question"]
    answer = extract_answer(elem["answer"])[0]
    key = xxhash.xxh32(question.encode("utf-8")).hexdigest()
    answers[key] = answer
    questions[key] = question


outputs["solved"] = False
outputs["question"] = ""
outputs["target"] = ""

for idx, output in tqdm(outputs.iterrows()):
    target_answer = answers[output["key"]]
    output_numbers = [float(n) for n in re.findall("(-?\d+(?:\.\d+)?)", output["output"])]

    solved = target_answer in output_numbers

    outputs.at[idx, "solved"] = solved
    outputs.at[idx, "question"] = questions[output["key"]]
    outputs.at[idx, "target"] = target_answer
    

outputs["valid"] = outputs["valid"].astype(float)
outputs["halts"] = outputs["halts"].astype(float)
outputs["error"] = outputs["error"].astype(float)

outputs["solved"] = outputs["solved"].astype(float)

outputs.to_excel(os.path.join(args.results_folder, "outputs.xlsx"))

results = list()

for elem in tqdm(dataset):
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
results.to_excel(os.path.join(args.results_folder, "results.xlsx"))

top_keys = filter(lambda k: "top_" in k, results.keys())

results_avg = list()
for top_key in tqdm(top_keys):
    print(f"{top_key} solve rate: "+str(results[top_key].mean()))
    results_avg.append(dict(
        top=top_key,
        solve_rate=results[top_key].mean()
    ))

results_avg = pd.DataFrame(results_avg)
results_avg.to_excel(os.path.join(args.results_folder, "results_avg.xlsx"))

