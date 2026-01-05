#!/bin/bash
# Create GitHub repository and push code

set -e

echo "🚀 Creating GitHub Repository"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found"
    echo ""
    
    # Check if logged in
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI authenticated"
        echo ""
        
        read -p "Repository name (default: ai-lead-intake-crm-automation): " repo_name
        repo_name=${repo_name:-ai-lead-intake-crm-automation}
        
        read -p "Description (default: AI-powered lead intake automation): " repo_desc
        repo_desc=${repo_desc:-AI-powered lead intake automation with Make.com, OpenAI, and Google Sheets}
        
        read -p "Visibility (public/private, default: public): " visibility
        visibility=${visibility:-public}
        
        echo ""
        echo "📦 Creating repository: $repo_name"
        echo "   Description: $repo_desc"
        echo "   Visibility: $visibility"
        echo ""
        
        # Initialize git if not already
        if [ ! -d ".git" ]; then
            echo "Initializing git repository..."
            git init
            git add .
            git commit -m "Initial commit: AI Lead Intake & CRM Automation

- FastAPI backend with OpenAI integration
- Make.com scenario integration
- Google Sheets CRM storage
- Website contact form
- Complete documentation and setup guides"
        fi
        
        # Create repo on GitHub
        gh repo create "$repo_name" \
            --description "$repo_desc" \
            --$visibility \
            --source=. \
            --remote=origin \
            --push
        
        echo ""
        echo "✅ Repository created and pushed!"
        echo ""
        echo "🔗 View your repo:"
        gh repo view --web
        
    else
        echo "❌ Not logged in to GitHub CLI"
        echo ""
        echo "Login with: gh auth login"
        echo "Then run this script again."
        exit 1
    fi
else
    echo "❌ GitHub CLI (gh) not installed"
    echo ""
    echo "Option 1: Install GitHub CLI"
    echo "  brew install gh"
    echo "  gh auth login"
    echo "  Then run this script again"
    echo ""
    echo "Option 2: Create manually"
    echo "  1. Go to https://github.com/new"
    echo "  2. Create repository"
    echo "  3. Run: ./setup_git_repo.sh"
    echo "  4. Follow push instructions"
    exit 1
fi

