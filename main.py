import requests
from discord_webhook import DiscordWebhook
import logging
import sys
import os
import time
from flask import Flask, render_template, request

# Configure logging to write to stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Time interval in seconds between release checks, defaults to 2 hours (7200 seconds).
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 2 * 60 * 60))
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

app = Flask(__name__)

def read_repository_file(file_path):
    repositories = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                owner, repo = line.strip().split(', ')
                repositories.append((owner, repo))
    except Exception as e:
        logger.error(f"Error reading repository file: {e}")
    return repositories


def get_latest_release(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    headers = {'Accept': 'application/vnd.github+json'}

    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    releases = response.json()
    return releases[0] if releases else None


def send_discord_notification(webhook_url, release, repo_info):
    owner, repo = repo_info
    release_name = release['name'] or release['tag_name']
    release_url = release['html_url']
    content = f"🚀 New release **{release_name}** in **{owner}/{repo}**\n{release_url}"
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()


@app.route('/')
def index():
    return "GitHub release notifier is running!"


@app.route('/start')
def start_notifier():
    main()
    return "GitHub release notifier started!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
