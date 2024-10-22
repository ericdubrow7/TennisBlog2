from Add_new_post import add_post_to_json
from find_article_sources import findarticlesources
from flask import Blueprint, request, jsonify
import openai
import os
#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import ClientSecretCredential
from Is_tennis_story import tennis_stuff
# Load environment variables from .env file

source_urls = []
articlessource = tennis_stuff()
for article in articlessource:
    source_urls.append(article['url'])
print(source_urls)

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_post(source_urls):
    Instruction = "Write quick day in review of what happened in the world of tennis yesterday "
    
    # Call the OpenAI API with the user's question
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
             "content": f"{Instruction} using data from these websites {source_urls}"}
        ]
    )

    # Get the response from the API
    response = completion.choices[0].message.content
    # Send the response back to the front-end
    print(response)
    return (response)

generate_post(source_urls)