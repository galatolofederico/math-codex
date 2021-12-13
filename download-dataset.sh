#!/bin/sh

mkdir -p ./datasets

rm -rf /tmp/math-codex-gsm8k
rm -rf ./datasets/gsm8k

git clone https://github.com/openai/grade-school-math.git /tmp/math-codex-gsm8k
cp -r /tmp/math-codex-gsm8k/grade_school_math/data ./datasets/gsm8k