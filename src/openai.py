import os
import openai

def get_completion(prompt, model, temperature, max_tokens, top_p, stop):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return openai.Completion.create(
        engine=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop
    )["choices"][0]["text"]
