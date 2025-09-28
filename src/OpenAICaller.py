import openai
import os
from dotenv import load_dotenv

class OpenAICaller:
    def __init__(self):
        load_dotenv()
        openai.api_type = os.getenv("OPENAI_API_TYPE")
        openai.api_base = os.getenv("OPENAI_API_BASE")
        openai.api_version = os.getenv("OPENAI_API_VERSION")
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def chat_completion(self, messages, engine="gpt4", temperature=0.7, top_p=0.95, frequency_penalty=0.5, presence_penalty=0.1, stop=None):
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop
        )
        return response.choices[0].message.content
