from flask import Flask, render_template, request
from flask import jsonify
from Load_Rankings import load_rankings, load_WTArankings
import json
from datetime import datetime
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from azure.identity import ClientSecretCredential
app = Flask(__name__)


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


# Journalist names for News dropdown; must match post['author'] from Create_new_post
JOURNALIST_NAMES = [
    "Tommy Tennis",
    "Prick Queergios",
    "Randy Murray",
    "Carlos Alcatraz",
    "Novax Djokavic",
]

# Team page: journalists with bio and optional headshot URL (None = placeholder)
TEAM_MEMBERS = [
    {
        "name": "Tommy Tennis",
        "bio": "A veteran tennis journalist with a no-nonsense approach. Tommy keeps coverage factual and balanced, giving readers the story without the spin.",
        "headshot": None,
    },
    {
        "name": "Prick Queergios",
        "bio": "Prick brings an unapologetically sharp perspective to the beat. A longtime fan of Nick Kyrgios, he’s never shy about calling out what he sees on and off the court.",
        "headshot": None,
    },
    {
        "name": "Randy Murray",
        "bio": "British correspondent with a knack for finding the lighter side of the tour. Randy’s been covering tennis for years and still finds new ways to make readers laugh.",
        "headshot": None,
    },
    {
        "name": "Carlos Alcatraz",
        "bio": "Spanish tennis obsessive with a flair for drama. Carlos lives for the clay season and Spanish players, and his pieces bring that passion to every story.",
        "headshot": None,
    },
    {
        "name": "Novax Djokavic",
        "bio": "Contrarian commentator with a taste for the controversial. Novax isn’t afraid to question the mainstream narrative and stir the pot.",
        "headshot": None,
    },
]


@app.context_processor
def inject_journalists():
    return dict(journalist_names=JOURNALIST_NAMES)


# Sample blog posts
def load_posts():

    blob_name = 'postsdata/posts.json'  # The name of the JSON file in blob storage
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)    
    
    download_stream = blob_client.download_blob()
    posts = json.loads(download_stream.readall().decode('utf-8'))
    sorted_posts = sorted(posts, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True)
    return sorted_posts

@app.route('/')
def index():
    posts = load_posts()
    return render_template('home.html', posts=posts[:3])

@app.route('/baseline-brief')
def baseline_brief():
    return render_template('baseline_brief.html')


@app.route('/tennis-lab')
def tennis_lab():
    return render_template('tennis_lab.html')


@app.route('/articles')
def articles():
    all_posts = load_posts()
    author = request.args.get('author')
    if author:
        post_list = [(p, i) for i, p in enumerate(all_posts) if p.get('author') == author]
    else:
        post_list = [(p, i) for i, p in enumerate(all_posts)]
    return render_template('articles.html', post_list=post_list, author_filter=author)

@app.route('/post/<int:post_id>')
def post(post_id):
    posts = load_posts()
    post = posts[post_id]
    return render_template('post.html', post=post)

@app.route('/abouttheauthor')
def abouttheauthor():
    return render_template('abouttheauthor.html')


@app.route('/our-team')
def our_team():
    return render_template('our_team.html', team_members=TEAM_MEMBERS)


@app.route('/rankings')
def rankings():
    rankings,last_modified_date = load_rankings()
    rankings = rankings['rankings']
    return render_template('rankings.html', rankings=rankings, last_modified_date=last_modified_date)

@app.route('/WTArankings')
def WTArankings():
    rankings, last_modified_date = load_WTArankings()
    rankings = rankings['rankings']
    return jsonify(rankings=rankings, last_modified_date = last_modified_date)

if __name__ == '__main__':
    app.run(debug=True)
