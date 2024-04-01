# pip install transformers
from transformers import pipeline
import os
import contextlib
import openai
from dotenv import load_dotenv
from typing import Final

load_dotenv()
OPENAI_KEY: Final[str] = os.getenv('OPEN_AI_API_KEY')

@contextlib.contextmanager
def suppress_print():
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        yield

async def analyze_output(input: str):
    with suppress_print():
        pipe = pipeline("text-classification", model="Titeiiko/OTIS-Official-Spam-Model")
    x = pipe(input)[0]
    spam_prob_score = x["score"] if x["label"] == "LABEL_1" else 1 - x["score"]
    
    # Label 1 is spam, label 0 is not spam
    res = await generate_phisherman_response(spam_prob_score, input)
    return res

async def generate_phisherman_response(spam_score, discord_message):
    prompt = f'A user received the following message on Discord: "{discord_message}" and the message was given a spam probability score of {spam_score} (scale of 0.0 to 1.0 where 1.0 indicates that it is a spam message). Please respond with a message to the user that restates the spam probability score and explains why the message is or is not spam.'

    openai.api_key = OPENAI_KEY  # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key

    completion = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use a different model if you prefer
        messages=[
            {"role": "system", "content": "You are a cybersecurity expert."},
            {"role": "user", "content": prompt},
        ]
    )

    return completion.choices[0].message['content']