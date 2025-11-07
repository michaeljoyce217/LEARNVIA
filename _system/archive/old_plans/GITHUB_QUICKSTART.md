# GitHub Quick Start - 5 Steps

**Goal**: Push LEARNVIA to GitHub and use with Claude Code web

---

## ✅ What's Already Done

- Git initialized
- Files committed locally
- .gitignore created
- README updated

---

## 🚀 5 Steps to GitHub

### 1️⃣ Create GitHub Repo

1. Go to https://github.com → Click **+** → **New repository**
2. Name: `LEARNVIA`
3. **Private** (recommended) or Public
4. **Don't** check any initialization boxes
5. Click **Create repository**

### 2️⃣ Link Local to GitHub

```bash
cd /Users/michaeljoyce/Desktop/LEARNVIA

# Replace YOUR-USERNAME with your GitHub username
git remote add origin https://github.com/YOUR-USERNAME/LEARNVIA.git
```

### 3️⃣ Push to GitHub

```bash
git push -u origin main
```

Enter your GitHub username and **Personal Access Token** (not password).

### 4️⃣ Verify

Go to https://github.com/YOUR-USERNAME/LEARNVIA and check files are there!

### 5️⃣ Use with Claude Code Web

1. Go to https://claude.ai
2. Look for GitHub integration or repository connection
3. Select your `LEARNVIA` repository
4. Start coding!

---

## 🔑 Need Personal Access Token?

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select `repo` scope
4. Copy token (save it somewhere!)
5. Use token as password when pushing

---

## 🖥️ Or Use GitHub Desktop (Easier!)

1. Download: https://desktop.github.com
2. Add existing repo: `/Users/michaeljoyce/Desktop/LEARNVIA`
3. Click **Publish repository**
4. Done!

---

## 🆘 Help

**Can't push?** Check: `git remote -v` shows correct URL

**Permission denied?** Use Personal Access Token as password

**Full guide**: See `GITHUB_SETUP_GUIDE.md`

---

**That's it!** Your project will be on GitHub in 5 minutes.
