# use chatgpt in python
import requests
import os
import openai
import tomli
# response  = openai.
with open("../configs/yt_config.toml", mode="rb") as fp:
    config = tomli.load(fp)
    api_key = config["openai"]["api_key"]
    openai.api_key = api_key

    
# Generate a response using OpenAI GPT-3
def ask_chatGPT(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message