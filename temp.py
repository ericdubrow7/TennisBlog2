from Add_new_post import add_post_to_json
from find_article_sources import findarticlesources
from flask import Blueprint, request, jsonify
import openai
import os
from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
# Load environment variables from .env file


new_post = {
    "title": "French Open 2024: Nadal Returns",
    "author": "Emily Clark",
    "date": "June 1, 2024",
    "content": "Rafael Nadal makes his much-anticipated return to Roland Garros after a year-long absence..."
}

file_path = 'posts.json'  # Path to your JSON file
add_post_to_json(file_path, new_post)