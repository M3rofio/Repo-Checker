import time
import requests
from discord_webhook import DiscordWebhook
import logging
import sys
import os

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


def main():
    logger.info("Starting GitHub release notifier...")
    repositories = read_repository_file('repositories.txt')
    last_release_ids = {}

    # Fetch and store the latest release ID for each repository initially
    for owner, repo in repositories:
        repo_key = f"{owner}/{repo}"
        try:
            latest_release = get_latest_release(owner, repo)
            if latest_release:
                last_release_ids[repo_key] = latest_release['id']
                logger.info(f"Initial release ID for {repo_key}: {latest_release['id']}")
        except Exception as e:
            logger.error(f"Error in {repo_key}: {e}")

    # Monitor for new releases
    while True:
        for owner, repo in repositories:
            repo_key = f"{owner}/{repo}"
            try:
                latest_release = get_latest_release(owner, repo)
                if latest_release and latest_release['id'] != last_release_ids.get(repo_key):
                    send_discord_notification(DISCORD_WEBHOOK_URL, latest_release, (owner, repo))
                    last_release_ids[repo_key] = latest_release['id']
                    logger.info(f"New release detected for {repo_key}: {latest_release['id']}")
            except Exception as e:
                logger.error(f"Error in {repo_key}: {e}")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
