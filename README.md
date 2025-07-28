# 🔄 GitHub Repository Backup Tool

This python script allows you to **automatically backup all your GitHub repositories** (both public and private) into a local folder (`./backup/`), including all source code, folders, and Git history.

---

## ✅ Features

- Clones all **public** and **private** repositories from your account
- Stores each repo in its own folder inside `./backup/`
- Preserves full Git history
- Uses GitHub **Personal Access Token (PAT)** for authentication

---

## 🚀 How to Use

### 1. 🔐 Generate a GitHub Personal Access Token

1. Go to: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Give it a name like `RepoBackup`
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:org` (if backing up organization repos)
5. Click **Generate token**
6. Copy the token and save it securely.

> 📸 Example:
>
> ![token](https://github.com/user-attachments/assets/93652252-fb94-417e-9af1-45c31b6ba33b)

---

### 2. 🧠 Set Your Credentials

Open the Python script and replace:

```python
GITHUB_USERNAME = "YourGitHubUsername"
GITHUB_TOKEN = "YourGitHubToken"
