import requests
from dotenv import load_dotenv
import os

def call_caveman_ai(text):
    load_dotenv()
    API_KEY = os.getenv("AWS_API_KEY")

    url = API_KEY

    response = requests.post(url, json={"text": text})

    data = response.json()

    text = data["response"]
    return text
