#!/bin/bash
# Guide for setting up ngrok authentication

echo "🔐 ngrok Authentication Setup"
echo ""
echo "ngrok requires a free account to use. Follow these steps:"
echo ""
echo "1. Sign up for free ngrok account:"
echo "   👉 https://dashboard.ngrok.com/signup"
echo ""
echo "2. After signing up, get your authtoken:"
echo "   👉 https://dashboard.ngrok.com/get-started/your-authtoken"
echo ""
echo "3. Once you have your authtoken, run:"
echo "   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE"
echo ""
echo "4. Then you can start ngrok with:"
echo "   ./start_ngrok.sh"
echo "   OR"
echo "   ngrok http 8000"
echo ""
echo "─────────────────────────────────────────"
echo ""
read -p "Do you already have an authtoken? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Enter your authtoken (it will be hidden):"
    read -s AUTHTOKEN
    echo ""
    echo "Configuring ngrok..."
    ngrok config add-authtoken "$AUTHTOKEN"
    if [ $? -eq 0 ]; then
        echo "✅ ngrok configured successfully!"
        echo ""
        echo "You can now run: ./start_ngrok.sh"
    else
        echo "❌ Failed to configure ngrok. Please check your authtoken."
    fi
else
    echo ""
    echo "📝 Steps to get your authtoken:"
    echo ""
    echo "1. Go to: https://dashboard.ngrok.com/signup"
    echo "2. Sign up (it's free)"
    echo "3. Go to: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "4. Copy your authtoken"
    echo "5. Run this script again, or run:"
    echo "   ngrok config add-authtoken YOUR_AUTHTOKEN"
    echo ""
fi

