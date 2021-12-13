import os
import openai

def get_completion(prompt, model, temperature, max_tokens, top_p, stop, apikey=None):
    openai.api_key = os.getenv("OPENAI_API_KEY") if apikey is None else apikey
    assert openai.api_key != "", "You have to set the OpenAI API Key. You can use the OPENAI_API_KEY environment variable"
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
