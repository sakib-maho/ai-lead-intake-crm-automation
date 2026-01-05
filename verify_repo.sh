#!/bin/bash
# Verify what files are in the git repository

echo "🔍 Checking Git Repository Status"
echo ""

if [ ! -d ".git" ]; then
    echo "❌ Not a git repository yet!"
    echo ""
    echo "Run: ./setup_git_repo.sh"
    exit 1
fi

echo "✅ Git repository found"
echo ""

echo "📊 Repository Status:"
git status --short
echo ""

echo "📁 Files tracked by git:"
git ls-files | wc -l | xargs echo "Total:"
echo ""

echo "📋 Important files check:"
echo ""

# Check for key files
files_to_check=(
    "README.md"
    "requirements.txt"
    "app/main.py"
    "app/ai.py"
    "app/schemas.py"
    "app/utils.py"
    "app/settings.py"
    "website/index.html"
    "make/scenario_blueprint.md"
    "make/prompts.md"
    "make/data_mapping.md"
    "examples/sample_lead.json"
    ".gitignore"
)

missing_files=()

for file in "${files_to_check[@]}"; do
    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
        missing_files+=("$file")
    fi
done

echo ""

# Check for sensitive files that should NOT be tracked
echo "🔒 Security check (should NOT be tracked):"
sensitive_files=(
    ".env"
    "venv/"
    "__pycache__"
    "MAKECOM_URL.txt"
)

for file in "${sensitive_files[@]}"; do
    if git ls-files | grep -q "^$file"; then
        echo "  ⚠️  WARNING: $file is tracked (should be in .gitignore)"
    else
        echo "  ✅ $file is NOT tracked (good)"
    fi
done

echo ""

if [ ${#missing_files[@]} -eq 0 ]; then
    echo "✅ All important files are tracked!"
else
    echo "⚠️  Missing files detected. Add them with:"
    echo "   git add ${missing_files[*]}"
    echo "   git commit -m 'Add missing files'"
fi

echo ""
echo "📤 To check what's on GitHub:"
echo "   git remote -v"
echo "   git log --oneline -5"

