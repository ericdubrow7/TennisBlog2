import openai
import os
from dotenv import load_dotenv

openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Write a short article about recent news from the ATP tour."
        }
    ]
)

print(completion)