from Add_new_post import add_post_to_json, save_all_articles_to_blob
from find_article_sources import findarticlesources
from flask import Blueprint, request, jsonify
import openai
import os
import random
#from dotenv import load_dotenv
import json
from newsapi import NewsApiClient
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import ClientSecretCredential
# Load environment variables from .env file
#load_dotenv()

# Your Azure details
tenant_id = os.getenv("YOUR_AZURE_TENANT_ID")
client_id = os.getenv("YOUR_AZURE_CLIENT_ID")
client_secret = os.getenv("YOUR_AZURE_CLIENT_SECRET")
storage_account_name = os.getenv("YOUR_STORAGE_ACCOUNT_NAME")
container_name = os.getenv("YOUR_CONTAINER_NAME")

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=credential
)

# Load existing posts from the JSON file
def load_existing_posts():
    blob_name = 'postsdata/posts.json'  # The name of the JSON file in blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    download_stream = blob_client.download_blob()
    posts = json.loads(download_stream.readall().decode('utf-8'))
    sorted_posts = sorted(posts, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return sorted_posts

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
source_url = ""

# Journalist personalities: each post is randomly assigned one. Name is shown as author; description shapes tone.
JOURNALIST_PERSONALITIES = [
    {
        "name": "Tommy Tennis",
        "description": "A highly professional tennis journalist who doesn't bring any external personality. Straightforward, factual, and neutral.",
    },
    {
        "name": "Prick Keergios",
        "description": "A prickly gay tennis journalist who is always on the attack. He loves Nick Kyrgios and tries to interject him into articles whenever possible. Sharp and combative tone.",
    },
    {
        "name": "Randy Murray",
        "description": "A very horny British tennis journalist who loves to make jokes about tennis players and the sport. Cheeky, double-entendre style with British humour.",
    },
    {
        "name": "Carlos Alcatraz",
        "description": "An eccentric Spanish convict who loves tennis, especially Spanish players. He brings a Spanish flair to his articles—dramatic, passionate, and a bit unhinged.",
    },
    {
        "name": "Novax Djokavic",
        "description": "A far right wing tennis journalist interested in conspiracy theories who likes to bring his political opinions into his articles. Skeptical, contrarian, and opinionated.",
    },
]


def pick_random_personality():
    """Return a randomly chosen journalist personality dict."""
    return random.choice(JOURNALIST_PERSONALITIES)


def is_article_tennis_related(article):
    """Use LLM to evaluate if the article is actually about tennis. Returns True only if tennis-related."""
    title = article.get('title', '')
    description = article.get('description', '')
    # Prefer full_content (full article text) when available; otherwise use API snippet
    content = article.get('full_content') or article.get('content', '')
    text = f"Title: {title}\n\nDescription: {description}\n\nContent: {content}".strip()
    if not text or text == "Title: \n\nDescription: \n\nContent:":
        # No meaningful text to evaluate; treat as not tennis-related to be safe
        return False
    prompt = (
        "You are a classifier. Based ONLY on the following news article title, description, and content snippet, "
        "determine if this article is genuinely about TENNIS (the sport)—e.g. players, tournaments, matches, rankings, "
        "or tennis-related news. Articles that merely mention the word 'tennis' in passing or are about other topics "
        "(e.g. a different sport, a person who happens to play tennis, or unrelated news) are NOT tennis-related. "
        "Reply with exactly one word: YES if the article is actually about tennis, or NO if it is not. "
        "Content below may be a snippet or the full article.\n\n"
        f"{text}"
    )
    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = (completion.choices[0].message.content or "").strip().upper()
        return answer.startswith("YES")
    except Exception as e:
        print(f"LLM tennis check failed for '{title}': {e}. Skipping article.")
        return False


def generate_post(source_url, personality):
    """Generate a headline and article body in the given journalist's voice. Returns (title, body)."""
    name = personality["name"]
    desc = personality["description"]
    instruction = (
        f"You are writing as the tennis journalist '{name}'. Their persona: {desc}\n\n"
        "Based ONLY on the data from the given website URL, write a short tennis news article "
        "in this journalist's distinct voice, style, and tone. The headline and body must sound like them.\n\n"
        "Reply with exactly two parts: "
        "1) A short, catchy headline (one line, no quotation marks) in their style. "
        "2) A blank line, then the article body (no title repeated in the body) in their voice.\n"
        "Format: first line is the headline, then a blank line, then the body."
    )
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"{instruction}\n\nWebsite: {source_url}"}
        ],
    )
    response = (completion.choices[0].message.content or "").strip()
    # First line = title, rest after first blank line = body
    parts = response.split("\n\n", 1)
    title = (parts[0].strip() or "Tennis News").replace("\n", " ")
    body = parts[1].strip() if len(parts) > 1 else response
    return (title, body)


articles_info = findarticlesources()
save_all_articles_to_blob(articles_info)
stories = []

# Load the existing posts to check for duplicates
existing_posts = load_existing_posts()
existing_titles = {post['title'] for post in existing_posts}  # set for fast lookup

for article in articles_info:
    # Check for matching title before calling the API
    if article['title'] in existing_titles:
        print(f"Duplicate title found. Skipping: {article['title']}")
        continue

    # LLM check: only proceed if the article is actually tennis-related
    if not is_article_tennis_related(article):
        print(f"Not tennis-related. Skipping (no post generated): {article['title']}")
        continue

    personality = pick_random_personality()
    generated_title, story = generate_post(article['url'], personality)
    print(f"Author: {personality['name']}\nTitle: {generated_title}\n{story}")
    date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    formatted_date = date.strftime("%Y-%m-%d")
    new_post = {
        "title": generated_title,
        "original_title": article["title"],
        "author": personality["name"],
        "date": formatted_date,
        "content": story,
        "source_url": article["url"]
    }
    restricted_phrases = [
        "I'm unable to access external websites",
        "external websites",
        "I can't access the content of the specified",
        "I can't access that URL"  # Add as many phrases as needed
    ]

    if any(phrase in new_post["content"] for phrase in restricted_phrases):
        print("Skipping next action as the content contains the restricted phrase.")
    else:
        add_post_to_json(new_post)
        existing_titles.add(article['title'])  # avoid duplicate in same run (by source title)
        print(f"Added new post: {new_post['title']}")

    stories.append(story)
#print(stories)
# Example usage:


