import argparse
import os
import json
import re

from src.openai import get_completion
from src.execute import execute_program

def pipeline(apikey, problem, model, temperature=0.5, max_tokens=512):
    print(apikey, problem, model, temperature, max_tokens)
    if model == "Codex":
        for i in range(0, 5): # 5 maximum tries
            prompt = f"#Write a Python function that solves the problem: \"{problem}\"\ndef"

            completion = get_completion(
                apikey=apikey,
                prompt=prompt,
                model="davinci-codex",
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stop=["\n\n"]
            )

            tries = 0
            while "input(" in completion:
                print("Discarding input-using completion")
                completion = get_completion(
                    apikey=apikey,
                    prompt=prompt,
                    model="davinci-codex",
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=1,
                    stop=["\n\n"]
                )
                tries += 1
                if tries > args.max_tries:
                    return "Failed to generate input-free program", "No execution output available"
        
            code = prompt + completion

            functions = re.search(r"def (.+)\(", code)
            function_name = functions.group(1)

            code += f"\n#Call the function {function_name} to solve the problem: \"{problem}\"\n{function_name}"
            completion = get_completion(
                apikey=apikey,
                prompt=code,
                model="davinci-codex",
                temperature=temperature,
                max_tokens=32,
                top_p=1,
                stop=["\n"]
            )

            code += completion
            output = execute_program(code)
            
            if output["valid"] and not output["halts"] and not output["error"]:
                return [
                    code,
                    output["output"]
                ]
        
        return "Failed to generate a valid program", "No execution output available"
    
    elif model == "GPT-3":
        prompt = f"Question: \"{problem}\"\nAnswer:"
        completion = get_completion(
            apikey=apikey,
            prompt=prompt,
            model="davinci",
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stop=["\n"]
        )
        return [
            prompt+completion,
            "Execution output not available for GPT-3"
        ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--apikey", type=str, default="")
    parser.add_argument("--problem", type=str, required=True)
    parser.add_argument("--model", type=str, choices=["GPT-3", "Codex"], default="Codex")
    parser.add_argument("--temperature", type=float, default=0.5)
    parser.add_argument("--max-tokens", type=int, default=512)
    
    args = parser.parse_args()
    apikey = os.getenv("OPENAI_API_KEY") if args.apikey == "" else args.apikey

    generated_output, execution_output = pipeline(args.apikey, args.problem, args.model, args.temperature, args.max_tokens)

    print(f"Generated Output:\n{generated_output}\n")
    print(f"Execution Output:\n{execution_output}\n")
    