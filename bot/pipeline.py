# pip install transformers
from transformers import pipeline
import os
import contextlib

@contextlib.contextmanager
def suppress_print():
    with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
        yield

def analyze_output(input: str):
    with suppress_print():
        pipe = pipeline("text-classification", model="Titeiiko/OTIS-Official-Spam-Model")
    x = pipe(input)[0]
    
    # Label 1 is spam, label 0 is not spam
    return (1, x["score"]) if x["label"] == "LABEL_1" else (0, x["score"])