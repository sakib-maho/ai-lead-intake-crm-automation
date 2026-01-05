#!/bin/bash
# Setup script for AI Lead Intake project

set -e

echo "🚀 Setting up AI Lead Intake project..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  venv directory already exists. Removing it..."
    rm -rf venv
fi
python3 -m venv venv

# Activate virtual environment
echo ""
echo "✅ Virtual environment created!"
echo "🔧 Activating virtual environment..."

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Or use the venv's Python directly:"
echo "  venv/bin/python -m app.main"
echo ""

