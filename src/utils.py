import re
import json

def read_jsonl(path):
    with open(path) as fh:
        return [json.loads(line) for line in fh.readlines() if line]

def extract_answer(*args):
    ret = []
    for a in args:
        match = re.compile(r"#### (\-?[0-9\.\,]+)").search(a)
        if match:
            match_str = match.group(1).strip()
            match_str = match_str.replace(",", "")
            ret.append(float(match_str))
        else:
            raise Exception("Dataset Error")
    return ret
