from Add_new_post import add_post_to_json
from find_article_sources import findarticlesources
from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
source_url = ""
def generate_post(source_url):
    Instruction = "Write a short article about recent tennis news"
    
    # Call the OpenAI API with the user's question
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
             "content": f"{Instruction} using data from this website {source_url}"}
        ]
    )

    # Get the response from the API
    response = completion.choices[0].message.content
    # Send the response back to the front-end
    #print(response)
    return (response)


urls = findarticlesources()
stories = []
for url in urls:
    story=generate_post(url)
    print(story)
    new_post = {
        "title": "TBD",
        "author": "Chat GPT",
        "date": "October 08, 2024",
        "content": f"{story}"
    }
    file_path = 'posts.json'  # Path to your JSON file
    add_post_to_json(file_path, new_post)
    stories.append(story)
#print(stories)
# Example usage:


