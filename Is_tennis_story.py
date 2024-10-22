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

openai.api_key = os.getenv("OPENAI_API_KEY")

def isTennis(source_url):
    Instruction = "determine if this article is actually about tennis or not. Give the response as a one word answer either Yes or No. "
    
    # Call the OpenAI API with the user's question
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
             "content": f"{Instruction} {source_url}"}
        ]
    )

    # Get the response from the API
    response = completion.choices[0].message.content
    # Send the response back to the front-end
    return (response)

def tennis_stuff():
    source_urls = findarticlesources()
    for url in source_urls:
        url['about tennis'] = isTennis(url)


    pretty_data = json.dumps(source_urls, indent=4)
    #print(pretty_data)

    tennis_articles = [item for item in source_urls if item.get("about tennis") == "Yes"]

    pretty_data = json.dumps(tennis_articles, indent=4)
    #print(pretty_data)
    return tennis_articles

