from flask import Flask, render_template
from flask import Flask, jsonify
from QuestionresponseAPI import ask_bp
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
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    posts = load_posts()
    post = posts[post_id]
    return render_template('post.html', post=post)

@app.route('/abouttheauthor')
def abouttheauthor():
    return render_template('abouttheauthor.html')

@app.route('/questionspage')
def questionspage():
    return render_template('questionspage.html')

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

app.register_blueprint(ask_bp)

if __name__ == '__main__':
    app.run(debug=True)
