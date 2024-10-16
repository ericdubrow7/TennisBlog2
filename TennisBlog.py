from flask import Flask, render_template
from flask import Flask, jsonify
from QuestionresponseAPI import ask_bp
from Load_Rankings import load_rankings, load_WTArankings
import json
from datetime import datetime
import os
app = Flask(__name__)

# Sample blog posts
def load_posts():
    with open('posts.json', 'r') as file:
        posts = json.load(file)
    # Sort the posts by date
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
