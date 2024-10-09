from Add_new_post import add_post_to_json
from find_article_sources import findarticlesources
from flask import Blueprint, request, jsonify
import openai
import os
#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
from datetime import datetime
# Load environment variables from .env file
#load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
source_url = ""
def generate_post(source_url):
    Instruction = "Write a short article about recent tennis news. do Not include a title for the article, only include the body of the article "
    
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


articles_info = findarticlesources()
stories = []
for article in articles_info:
    story=generate_post(article['url'])
    print(story)
    date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    formatted_date= date.strftime("%Y-%m-%d")
    new_post = {
        "title": article['title'],
        "author": "Chat GPT",
        "date": formatted_date,
        "content": f"{story}"
    }
    file_path = 'posts.json'  # Path to your JSON file
    restricted_phrases = [
    "I'm unable to access external websites", 
    "from external websites"  # Add as many phrases as needed
    ]  

    if any(phrase in new_post["content"] for phrase in restricted_phrases):
        print("Skipping next action as the content contains the restricted phrase.")
    else:
        add_post_to_json(file_path, new_post)
    stories.append(story)
#print(stories)
# Example usage:


