import openai
from pathlib import Path
import json

gptModel = "gpt-4"

openai.api_key_path = (Path().cwd() / 'chatgpt.apikey.txt').resolve()
