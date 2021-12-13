#!/bin/sh

if [ -z "${OPENAI_API_KEY}" ]; then
    echo "Please set your OpenAI API Key using the environment variable OPENAI_API_KEY"
    exit 1;
fi


mkdir -p ./completions
mkdir -p ./completions/codex
mkdir -p ./completions/gpt3

for i in $(seq 15); do
    python -m scripts.generate-programs --output-folder "./completions/codex/$i"
done

python -m scripts.generate-gpt3 --output-folder ./completions/gpt3/1