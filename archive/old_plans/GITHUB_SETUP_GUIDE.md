# GitHub Setup Guide - LEARNVIA Project

**Status**: ✅ Git repo initialized and first commit created
**Next Steps**: Push to GitHub and connect to Claude Code web

---

## 📋 What's Been Done

✅ Git repository initialized
✅ Directory reorganized (40 items → 5 in root)
✅ All files committed to local git
✅ .gitignore created (excludes sensitive files)
✅ README updated with new structure
✅ All tests passing

**Commit hash**: `24864ec` - "Reorganize project structure and prepare for GitHub"

---

## 🚀 Step-by-Step: Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon (top right) → **New repository**
3. Fill in repository details:
   - **Repository name**: `LEARNVIA` (or `learnvia-ai-review-system`)
   - **Description**: "AI-powered content revision system using 60 reviewers in consensus-based workflow"
   - **Visibility**:
     - Choose **Private** (recommended for internal project)
     - Or **Public** (if open-sourcing)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

### Step 2: Connect Your Local Repo to GitHub

GitHub will show you commands. Use these:

```bash
# Navigate to your project
cd /Users/michaeljoyce/Desktop/LEARNVIA

# Add GitHub as remote (replace YOUR-USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/LEARNVIA.git

# Verify remote was added
git remote -v

# Push your code to GitHub
git push -u origin main
```

**Example** (replace with your actual username):
```bash
git remote add origin https://github.com/mjoyceauthor/LEARNVIA.git
git push -u origin main
```

You'll be prompted for GitHub credentials (use Personal Access Token, not password).

### Step 3: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your files and folders
3. Verify README.md displays properly
4. Check that .gitignore is working (no .DS_Store, __pycache__, etc. in repo)

---

## 🌐 Connect to Claude Code on the Web

### Step 1: Access Claude Code Web

1. Go to https://claude.ai
2. Log in to your account
3. Look for Claude Code integration option (may be in sidebar or settings)

### Step 2: Connect GitHub Repository

**Option A: If Claude Code Web Has GitHub Integration**
1. Click "Connect Repository" or similar option
2. Authorize Claude to access your GitHub account
3. Select the `LEARNVIA` repository
4. Grant read/write permissions

**Option B: If Using Direct URL**
1. Copy your repository URL: `https://github.com/YOUR-USERNAME/LEARNVIA`
2. Paste it into Claude Code web interface
3. Follow prompts to grant access

### Step 3: Start Coding with Claude Code

Once connected, you can:
- Browse your code directly in Claude Code web
- Ask Claude to make changes
- Claude will create commits/PRs automatically
- Review and merge changes through GitHub

---

## 🔐 GitHub Personal Access Token (If Needed)

If you need to create a Personal Access Token for pushing:

### Create Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Give it a name: "LEARNVIA Project"
4. Select scopes:
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (if using GitHub Actions)
5. Click **Generate token**
6. **COPY THE TOKEN** (you won't see it again!)

### Use Token for Push:
```bash
# When prompted for password, paste your token instead
git push -u origin main
# Username: YOUR-GITHUB-USERNAME
# Password: [paste token here]
```

### Save Credentials (Optional):
```bash
# Cache credentials for 1 hour
git config --global credential.helper cache

# Or store permanently (macOS keychain)
git config --global credential.helper osxkeychain
```

---

## 📝 Alternative: Use GitHub Desktop (Easier)

If command line feels complex:

1. Download **GitHub Desktop**: https://desktop.github.com
2. Install and sign in to GitHub
3. Click **Add** → **Add Existing Repository**
4. Select `/Users/michaeljoyce/Desktop/LEARNVIA`
5. Click **Publish repository**
6. Choose visibility (Private/Public)
7. Click **Publish**

Done! Much simpler.

---

## 🎯 Recommended GitHub Settings

### Branch Protection (Optional, for team)

1. Go to repository → Settings → Branches
2. Add rule for `main` branch:
   - ✅ Require pull request before merging
   - ✅ Require approvals (1 person)
   - ✅ Require status checks to pass

### Secrets (If Using Actions)

1. Repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `OPENAI_API_KEY` (if automating tests)

### Topics (For Discoverability)

1. Go to repository main page
2. Click gear icon next to "About"
3. Add topics: `ai`, `education`, `content-review`, `python`, `machine-learning`

---

## 🔄 Common Git Workflows

### Making Changes After Push

```bash
# Make your changes to files
# ...

# Stage changes
git add .

# Commit
git commit -m "Add new feature: X"

# Push to GitHub
git push
```

### Creating a New Branch

```bash
# Create and switch to new branch
git checkout -b feature/new-review-algorithm

# Make changes, commit
git add .
git commit -m "Implement new algorithm"

# Push branch to GitHub
git push -u origin feature/new-review-algorithm

# Create Pull Request on GitHub web interface
```

### Pulling Latest Changes

```bash
# Get latest from GitHub
git pull origin main
```

---

## ⚠️ Important Notes

### Files That Are Ignored (Won't Push to GitHub)

These are in `.gitignore` and won't be committed:

- `__pycache__/` - Python compiled files
- `.DS_Store` - Mac system files
- `.claude/` - Claude Code settings
- `.pytest_cache/` - Test cache
- `reports/*.html` - Generated reports (dynamic)
- `feedback/*/*.json` - Feedback data (dynamic)
- `.env` - Environment variables (NEVER commit API keys!)

### Sensitive Data Warning

**NEVER commit**:
- API keys
- Passwords
- Personal tokens
- Private student data
- Confidential company information

If you accidentally commit sensitive data:
1. Remove from files
2. Use `git filter-repo` to remove from history
3. Rotate any exposed credentials immediately

---

## 🆘 Troubleshooting

### "Permission denied" when pushing

**Solution**: Set up SSH keys or use Personal Access Token

### "Repository not found"

**Solution**: Check remote URL: `git remote -v`
Update if needed: `git remote set-url origin https://github.com/USERNAME/LEARNVIA.git`

### "Failed to push refs"

**Solution**: Pull first, then push:
```bash
git pull origin main --rebase
git push origin main
```

### Large files rejected

**Solution**: GitHub has 100MB file limit. If you have large files:
1. Add to `.gitignore`
2. Use Git LFS: `git lfs track "*.large"`
3. Or store elsewhere (cloud storage)

---

## ✅ Success Checklist

After completing these steps, verify:

- [ ] Repository visible on GitHub
- [ ] All files present (check tree structure)
- [ ] README displays properly
- [ ] .gitignore working (no __pycache__, .DS_Store visible)
- [ ] Can clone repo to test: `git clone https://github.com/YOUR-USERNAME/LEARNVIA.git`
- [ ] Connected to Claude Code web (if applicable)

---

## 🎉 You're Done!

Your LEARNVIA project is now:
- ✅ Under version control
- ✅ Backed up on GitHub
- ✅ Ready for collaboration
- ✅ Accessible via Claude Code web
- ✅ Properly organized and documented

### Next Steps:

1. **Invite collaborators** (if team project):
   - Repository → Settings → Collaborators

2. **Set up CI/CD** (optional):
   - Add `.github/workflows/tests.yml` for automated testing

3. **Continue development**:
   - Use branches for features
   - Create Pull Requests for review
   - Let Claude Code help with changes!

---

## 📚 Resources

- **GitHub Docs**: https://docs.github.com
- **Git Basics**: https://git-scm.com/book/en/v2
- **GitHub Desktop**: https://desktop.github.com
- **Claude Code**: https://claude.ai

---

**Questions?** Check GitHub's documentation or ask Claude Code for help!

**Last Updated**: November 4, 2025
