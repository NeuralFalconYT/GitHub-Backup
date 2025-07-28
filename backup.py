import os
import requests
import subprocess

# Replace with your credentials
GITHUB_USERNAME = "YourGitHubUsername"
GITHUB_TOKEN = "YourGitHubToken"

# Create backup folder
backup_dir = "./backup"
os.makedirs(backup_dir, exist_ok=True)

# GitHub API URL to fetch all repos (private and public)
url = "https://api.github.com/user/repos"
headers = {"Accept": "application/vnd.github+json"}
auth = (GITHUB_USERNAME, GITHUB_TOKEN)

page = 1
while True:
    print(f"🔄 Fetching page {page} of repositories...")
    response = requests.get(f"{url}?per_page=100&type=all&page={page}", auth=auth, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to fetch repositories:", response.text)
        break

    repos = response.json()
    if not repos:
        break  # No more repos

    for repo in repos:
        repo_name = repo["name"]
        clone_url = repo["clone_url"].replace("https://", f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@")
        repo_path = os.path.join(backup_dir, repo_name)

        if os.path.exists(repo_path):
            print(f"✅ Repo '{repo_name}' already exists. Skipping...")
            continue

        print(f"⬇️ Cloning '{repo_name}' into '{repo_path}'")
        result = subprocess.run(["git", "clone", clone_url, repo_path])
        if result.returncode != 0:
            print(f"❌ Failed to clone {repo_name}")

    page += 1

print("🎉 All repositories cloned with source code into ./backup/")
