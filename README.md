# 💾 GitHub Backup

> **Back up every GitHub repository you own — public and private — to your local machine with a single command.**

Never worry about losing years of code again.

---

## ✨ Why I Built This

I once lost access to a GitHub account and with it, years of code.

Whether an account is accidentally deleted, suspended, hacked, or you simply lose access, your repositories shouldn't disappear with it.

This tool lets you create a **local backup of every repository** in your GitHub account, giving you peace of mind that your code is always yours.

> **A backup takes minutes. Rebuilding years of work can take years.**

---

# 🚀 Features

- 📦 Clone **all public repositories**
- 🔒 Clone **all private repositories**
- ⚡ Uses the **official GitHub REST API**
- 🌳 Preserves the **complete Git history** (commits, branches, and tags)
- 📂 Saves everything into a single local backup folder
- ⏭️ Skips repositories that have already been downloaded
- 🔄 Safe to run again anytime
- 📊 Beautiful terminal progress bar
- 📋 Clean summary table after completion

---

# 📦 What Gets Backed Up

Each repository is cloned locally using Git, including:

- 📁 Source code
- 📝 Complete commit history
- 🌿 Branches
- 🏷️ Tags

Each repository remains a normal Git repository that you can use immediately.

---

# ❌ What Is NOT Backed Up

This tool clones Git repositories only.

The following GitHub-specific features are **not included**:

- Issues
- Pull Requests
- Discussions
- Wikis
- Releases & release assets
- GitHub Actions
- Project boards
- Repository settings
- Secrets
- Environment variables

---

# 🛠 Installation

## 1️⃣ Clone this repository

```bash
git clone https://github.com/NeuralFalconYT/GitHub-Backup.git
cd GitHub-Backup
```

---

## 2️⃣ Install Python dependencies

```bash
pip install rich requests
```

---

## 3️⃣ Install Git

Git must already be installed because it is used to clone repositories.

### Windows

https://git-scm.com/downloads

### macOS

```bash
brew install git
```

### Linux

```bash
sudo apt install git
```

---

# ▶️ Usage

Run:

```bash
python github_backup.py
```

The program will ask for:

1. 👤 GitHub Username
2. 🔑 GitHub Personal Access Token

---

# 🔑 Creating a Personal Access Token

Go to:

https://github.com/settings/tokens

## Classic Personal Access Token

Enable the following scope:

```
repo
```

This allows the tool to access both public and private repositories.

---

## Fine-Grained Personal Access Token

Configure:

**Repository access**

```
All repositories
```

**Repository permissions**

```
Contents → Read-only
```

Without these permissions, private repositories cannot be backed up.

---

# 📁 Backup Location

All repositories are stored inside:

```text
./your_username_backup/
```

Example:

```text
john_backup/
├── Portfolio/
├── AI-Projects/
├── Website/
├── Discord-Bot/
└── Machine-Learning/
```

Each repository becomes its own local Git repository.

---

# 🔄 Running It Again

You can safely run the tool whenever you want.

If a repository folder already exists inside the backup directory, it is skipped automatically.

This makes it ideal for:

- Daily backups
- Weekly backups
- Monthly backups
- Before switching computers
- Before transferring repositories
- Before deleting an account

---

# 🔒 Privacy

Your Personal Access Token is:

- ✅ Used only to authenticate with GitHub
- ✅ Used only during the current backup
- ✅ Never stored on disk
- ✅ Never logged by this program
- ✅ Never sent anywhere except GitHub

---

# 📊 Example Output

```text
Fetching repositories...

██████████████████████████████████ 100%

✔ Cloned : 42
↷ Skipped: 17
✘ Failed : 0
```

---

# 💡 Why Backups Matter

GitHub is an excellent hosting platform but **it is not a backup strategy.**

Accounts can become inaccessible due to:

- Accidental deletion
- Account suspension
- Lost credentials
- Security incidents
- Human error

Keeping a local copy of your repositories ensures your code remains under your control.

---

# ⭐ Support

If you find this project useful:

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest new features
- 🤝 Contribute improvements

---

# 📄 License

Released under the **MIT License**.

---

# ❤️ Final Note

Your code represents countless hours of learning and hard work.

Don't rely on a single cloud account to keep it safe.

**Run a backup today—and keep a copy of your work that you truly own.**
