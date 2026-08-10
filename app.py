from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'posts.json')

def load_posts():
    """Reads all posts from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts):
    """Writes the list of posts to the JSON file."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def get_next_id(posts):
    """Determines the next available ID."""
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1

@app.route('/')
def index():
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Extract form data
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load all posts, add new post
        posts = load_posts()
        new_post = {
            'id': get_next_id(posts),
            'author': author,
            'title': title,
            'content': content
        }
        posts.append(new_post)
        save_posts(posts)

        # Back to the homepage
        return redirect(url_for('index'))

    # GET: Display form
    return render_template('add.html')

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
