#!/bin/bash
# Setup script for Python 3.14 compatibility

set -e

echo "🚀 Setting up with Python 3.14..."
echo ""

# Check Python version
echo "📋 Python version:"
python3 --version
echo ""

# Remove old venv if exists
if [ -d "venv" ]; then
    echo "🧹 Removing old venv..."
    rm -rf venv
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate and upgrade pip
echo "🔧 Activating and upgrading pip..."
source venv/bin/activate
pip install --upgrade pip

# Install latest versions (not pinned) to avoid build issues
echo ""
echo "📥 Installing latest package versions (for Python 3.14 compatibility)..."
echo "   This may take a few minutes..."
pip install fastapi uvicorn[standard] pydantic pydantic-settings httpx python-dotenv

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Then start the server:"
echo "  python -m app.main"
echo ""

