#!/bin/bash
# Setup git repository and prepare for GitHub push

set -e

echo "🚀 Setting up Git repository..."
echo ""

# Check if already a git repo
if [ -d ".git" ]; then
    echo "⚠️  Git repository already exists"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    # Initialize git
    echo "📦 Initializing git repository..."
    git init
fi

# Add all files
echo ""
echo "📝 Adding files to git..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --short

echo ""
read -p "Create initial commit? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git commit -m "Initial commit: AI Lead Intake & CRM Automation

- FastAPI backend with OpenAI integration
- Make.com scenario integration  
- Google Sheets CRM storage
- Website contact form
- Complete documentation and setup guides"
    
    echo ""
    echo "✅ Repository initialized and committed!"
    echo ""
    echo "📤 Next steps to push to GitHub:"
    echo ""
    echo "1. Create a new repository on GitHub:"
    echo "   → Go to https://github.com/new"
    echo "   → Don't initialize with README"
    echo ""
    echo "2. Add remote and push:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
else
    echo "⏭️  Skipped commit. Run 'git commit' manually when ready."
fi

