import os
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

REPOSITORIES_FILE = "repositories.json"

discord_webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
check_interval = int(os.environ.get('CHECK_INTERVAL', '60'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        owner = request.form['owner']
        repo = request.form['repo']
        add_repository(owner, repo)
        return redirect(url_for('index'))
    repositories = load_repositories()
    return render_template('index.html', repositories=repositories)

def load_repositories():
    try:
        with open(REPOSITORIES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_repositories(repositories):
    with open(REPOSITORIES_FILE, 'w') as f:
        json.dump(repositories, f, indent=4)

def add_repository(owner, repo):
    repositories = load_repositories()
    repositories.append({"owner": owner, "repo": repo})
    save_repositories(repositories)

if __name__ == "__main__":
    # Listen on all network interfaces
    app.run(host='0.0.0.0', debug=True)
