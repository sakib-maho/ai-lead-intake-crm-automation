#!/bin/bash
# Quick start script for the AI Lead Intake API

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: ./setup_py314.sh first"
    exit 1
fi

# Use venv's Python directly (no need to activate)
echo "🚀 Starting AI Lead Intake API server..."
echo "   Press Ctrl+C to stop"
echo ""

venv/bin/python -m app.main

