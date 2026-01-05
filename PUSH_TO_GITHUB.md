# Push to GitHub - Step by Step

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `ai-lead-intake-crm-automation` (or your preferred name)
3. Description: "AI-powered lead intake automation with Make.com, OpenAI, and Google Sheets"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Add Remote and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/sakib/Project/Make.com

# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Or if using SSH:
# git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify

1. Go to your GitHub repository
2. You should see all your files
3. Check that `.env` is NOT there (it's in .gitignore)

## Important Notes

### Files NOT pushed (protected by .gitignore):
- `.env` - Contains your OpenAI API key (sensitive!)
- `venv/` - Virtual environment (not needed in repo)
- `__pycache__/` - Python cache files
- `MAKECOM_URL.txt` - Contains webhook URLs

### Files that ARE pushed:
- All source code
- Documentation
- Configuration examples
- Website form

## Quick Commands Reference

```bash
# Check status
git status

# See what will be committed
git status --short

# Add all files
git add .

# Commit
git commit -m "Your commit message"

# Push
git push

# View remote
git remote -v
```

## After Pushing

Your repository is now on GitHub! You can:
- Share it with clients
- Deploy from GitHub (Railway, Render, etc.)
- Collaborate with others
- Use GitHub Pages for the website form

