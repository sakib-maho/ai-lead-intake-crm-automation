#!/bin/bash
# Test script for the /lead endpoint

# Set your API URL (default: localhost:8000)
API_URL="${API_URL:-http://localhost:8000}"

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Testing health endpoint..."
curl -X GET "${API_URL}/health" | jq '.'

echo -e "\n\nTesting /lead endpoint..."
curl -X POST "${API_URL}/lead" \
  -H "Content-Type: application/json" \
  -d @"${SCRIPT_DIR}/sample_lead.json" | jq '.'

echo -e "\n\nTest complete!"

