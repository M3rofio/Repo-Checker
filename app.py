from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

REPOSITORIES_FILE = "repositories.json"

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
    app.run(debug=True)
