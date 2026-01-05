#!/bin/bash
# Test Make.com webhook connection

WEBHOOK_URL="https://hook.eu1.make.com/akkh2ku2d4y3okguu3qsp6iuovx3hctk"

echo "🧪 Testing Make.com Webhook"
echo "Webhook URL: $WEBHOOK_URL"
echo ""

echo "Sending test lead..."
curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Inc",
    "message": "We need an AI lead system. Budget 5k. ASAP",
    "source": "website_form"
  }' | python3 -m json.tool 2>/dev/null || curl -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Inc",
    "message": "We need an AI lead system. Budget 5k. ASAP",
    "source": "website_form"
  }'

echo ""
echo ""
echo "✅ Check Make.com scenario execution to see if it called your local API!"

