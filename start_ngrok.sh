#!/bin/bash
# Start ngrok tunnel for localhost:8000

echo "🚇 Starting ngrok tunnel..."
echo ""
echo "This will expose your local server at http://localhost:8000"
echo "to the internet via an ngrok URL."
echo ""
echo "⚠️  Keep this terminal open while testing Make.com!"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed!"
    echo ""
    echo "Install it with:"
    echo "  brew install ngrok"
    echo "  OR"
    echo "  Download from: https://ngrok.com/download"
    echo ""
    exit 1
fi

# Check if port 8000 is in use
if ! lsof -ti:8000 > /dev/null 2>&1; then
    echo "⚠️  Warning: Nothing is running on port 8000"
    echo "   Make sure your FastAPI server is running first!"
    echo "   Run: python -m app.main"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "✅ Starting ngrok..."
echo ""
echo "📋 Your ngrok URL will appear below."
echo "   Copy the HTTPS URL and use it in Make.com!"
echo ""
echo "   Example: https://abc123.ngrok-free.app"
echo ""
echo "─────────────────────────────────────────"
echo ""

# Start ngrok
ngrok http 8000

