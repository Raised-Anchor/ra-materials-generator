import openai
from pathlib import Path
import pyjson5 as json

gptModel = "gpt-4"

openai.api_key_path = (Path().cwd() / 'chatgpt.apikey.txt').resolve()

def getChatResponse(messages: list[str]) -> str:
    response = openai.ChatCompletion.create(
        model=gptModel,
        messages=messages
    )
    return __parseResponse__(response, 'choices', 0, 'message', 'content')


def __parseResponse__(response, *args):
    value = response
    for arg in args:
        value = value[arg] or None
        if(value is None): return None

    return value