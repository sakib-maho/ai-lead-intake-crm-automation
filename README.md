# AI Lead Intake & CRM Automation

A portfolio-ready demo project that automates lead processing using **Make.com**, **OpenAI**, **Google Sheets**, and **Gmail/Slack** notifications.

## 🎯 What Problem Does This Solve?

This system automates the entire lead intake workflow:
- **Captures** leads from web forms, landing pages, or any source via webhook
- **Validates & normalizes** lead data (email formatting, deduplication)
- **AI-powered classification** using OpenAI to extract intent, urgency, budget, and generate summaries
- **Stores** leads in Google Sheets (acting as a lightweight CRM)
- **Notifies** your team via Slack/Gmail for high-priority leads
- **Prevents duplicates** using intelligent deduplication keys

Perfect for small teams who want enterprise-level lead processing without complex CRM setup.

---

## 🚀 Quick Start (60 Seconds)

### Prerequisites
- Python 3.11+
- OpenAI API key
- Make.com account (free tier works)
- Google Sheets (free)
- Slack workspace (optional, for notifications)

### Step 1: Clone & Setup

```bash
# Navigate to project directory (after clone)
git clone https://github.com/sakib-maho/ai-lead-intake-crm-automation.git
cd ai-lead-intake-crm-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### Step 3: Run the Server

```bash
# Run locally
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Step 4: Test It

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test lead processing (from examples directory)
cd examples
chmod +x curl_test.sh
./curl_test.sh
```

Or test manually:

```bash
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Inc",
    "message": "We need an AI lead system. Budget 5k. ASAP",
    "source": "website_form"
  }'
```

---

## 📋 Environment Variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional (defaults shown)
PORT=8000
HOST=0.0.0.0
DRY_RUN=false          # Set to true to skip OpenAI calls (uses mock data)
LOG_LEVEL=INFO         # DEBUG, INFO, WARNING, ERROR
```

---

## 🧪 Testing

### Test with Sample Payload

```bash
# Using the provided sample
curl -X POST http://localhost:8000/lead \
  -H "Content-Type: application/json" \
  -d @examples/sample_lead.json | jq '.'
```

### Expected Response

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Inc",
  "message": "We need an AI lead system. Budget 5k. ASAP",
  "source": "website_form",
  "dedupe_key": "john@example.com",
  "intent": "seeking AI automation services",
  "urgency": "high",
  "budget_range": "5k",
  "summary": "Lead is interested in AI lead system with budget of 5k. Requires ASAP implementation.",
  "lead_score": 75,
  "next_action": "schedule discovery call to discuss requirements",
  "raw_payload_json": "{\"name\":\"John Doe\",\"email\":\"JOHN@EXAMPLE.COM\",...}"
}
```

### DRY_RUN Mode

Set `DRY_RUN=true` in `.env` to test without calling OpenAI (uses mock AI responses):

```bash
# In .env
DRY_RUN=true

# Restart server and test - will return mock analysis
```

---

## 🔗 Make.com Setup

### Step 1: Create Google Sheets

1. Create a new Google Sheet
2. Name the first sheet: `Leads`
3. Add headers in row 1:
   ```
   timestamp | name | email | company | message | source | intent | urgency | budget_range | summary | lead_score | next_action | dedupe_key | raw_payload_json
   ```
4. (Optional) Create a second sheet named `Errors` with headers:
   ```
   timestamp | error_message | error_code | original_payload
   ```

### Step 2: Create Make.com Scenario

Follow the detailed blueprint in [`make/scenario_blueprint.md`](make/scenario_blueprint.md)

**Quick summary:**
1. **Webhook trigger** → receives lead data
2. **HTTP request** → POST to your FastAPI `/lead` endpoint
3. **Google Sheets search** → check if lead exists (by `dedupe_key`)
4. **Router** → if exists → update row, else → add row
5. **Router** → if `urgency=high` OR `lead_score>=80` → send Slack/Gmail
6. **Error handler** → log errors to Errors sheet

### Step 3: Deploy FastAPI (for Production)

#### Option A: Railway

1. Install Railway CLI: `npm i -g @railway/cli`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`
5. Set environment variables in Railway dashboard
6. Get your Railway URL: `https://your-app.railway.app`

#### Option B: Render

1. Connect GitHub repo to Render
2. Create new Web Service
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables in Render dashboard

#### Option C: Local Testing with ngrok

```bash
# Install ngrok
brew install ngrok  # or download from ngrok.com

# Expose local server
ngrok http 8000

# Use the ngrok URL in Make.com (e.g., https://abc123.ngrok.io)
```

### Step 4: Configure Make.com Webhook

1. In Make.com scenario, copy the webhook URL
2. Update your web form/landing page to POST to this URL
3. Or test manually using curl:

```bash
curl -X POST "YOUR_MAKE_COM_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @examples/sample_lead.json
```

---

## 📊 API Endpoints

### `POST /lead`

Process a new lead and return AI-analyzed structured data.

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "company": "Acme Inc",
  "message": "We need an AI lead system. Budget 5k. ASAP",
  "source": "website_form"
}
```

**Response:**
See "Expected Response" section above.

**Validation Rules:**
- `message` is required (min 1 char, max 4000 chars)
- At least one of `email` or `name` must be provided
- Email is normalized (lowercased, validated)
- All strings are trimmed

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎬 60-Second Demo Script (for Loom/Recording)

**Script:**
1. (0-5s) "This is an AI-powered lead intake system that processes leads automatically."
2. (5-15s) Show the FastAPI server running, test with curl command
3. (15-25s) Show the structured JSON response with AI analysis (intent, urgency, score)
4. (25-35s) Open Make.com scenario, show webhook receiving the lead
5. (35-45s) Show Google Sheets being updated with the lead data
6. (45-55s) Show Slack notification for high-priority leads
7. (55-60s) "The system handles deduplication, validation, and AI classification automatically."

**Key Points to Highlight:**
- ✅ Automatic email normalization and deduplication
- ✅ AI-powered lead scoring and classification
- ✅ Seamless integration with Google Sheets (CRM)
- ✅ Smart notifications for high-priority leads

---

## 🔧 Troubleshooting

### Issue: "OpenAI API key not found"

**Solution:**
- Ensure `.env` file exists in project root
- Check `OPENAI_API_KEY` is set correctly
- Restart the server after changing `.env`

### Issue: "JSON parsing error from OpenAI"

**Solution:**
- The system automatically attempts one repair
- Check OpenAI API status
- Try setting `DRY_RUN=true` to test without OpenAI

### Issue: "Make.com webhook not receiving data"

**Solution:**
- Verify webhook URL is correct
- Check webhook payload matches expected schema
- Test webhook directly in Make.com's webhook test tool
- Ensure FastAPI is accessible (deployed or ngrok running)

### Issue: "Google Sheets not updating"

**Solution:**
- Verify Make.com has Google Sheets connection authorized
- Check column names match exactly (case-sensitive)
- Ensure `dedupe_key` column exists
- Test Google Sheets module separately in Make.com

### Issue: "Notifications not sending"

**Solution:**
- Check router conditions: `urgency === "high"` (triple equals)
- Verify Slack/Gmail connections are authorized in Make.com
- Check lead_score is >= 80 for high-priority route
- Test notification modules separately

### Issue: "Port already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it or change PORT in .env
PORT=8001
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── settings.py      # Environment configuration
│   ├── schemas.py       # Pydantic models
│   ├── ai.py            # OpenAI integration
│   └── utils.py         # Validation, normalization, dedupe
├── examples/
│   ├── sample_lead.json # Sample test payload
│   └── curl_test.sh     # Test script
├── make/
│   ├── scenario_blueprint.md  # Detailed Make.com setup
│   ├── data_mapping.md        # Google Sheets column mapping
│   └── prompts.md             # OpenAI prompts
├── .env.example         # Environment template
├── .gitignore
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

---

## 🔐 Security Considerations

- **API Keys:** Never commit `.env` file to git
- **Webhooks:** In production, add webhook secret validation
- **CORS:** Restrict CORS origins to Make.com IPs in production
- **Rate Limiting:** Consider adding rate limiting for production use
- **Input Validation:** All inputs are validated and sanitized

---

## 🚢 Deployment Checklist

- [ ] Set `DRY_RUN=false` in production
- [ ] Add OpenAI API key to deployment platform
- [ ] Update Make.com HTTP module with production URL
- [ ] Test end-to-end flow with real lead
- [ ] Verify Google Sheets permissions
- [ ] Test error handling (break API temporarily)
- [ ] Set up monitoring/alerts
- [ ] Document webhook URL for your team

---

## 📝 License

This is a portfolio demo project. Feel free to use and modify as needed.

---

## 🤝 Contributing

This is a demo project, but suggestions are welcome! Common improvements:
- Add more AI models (Claude, Gemini)
- Add webhook authentication
- Add rate limiting
- Add database backup option
- Add lead enrichment (company data APIs)

---

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review Make.com scenario blueprint
3. Check FastAPI logs for detailed error messages
4. Test endpoints individually to isolate issues

---

**Built with:** FastAPI, OpenAI, Make.com, Google Sheets, Python 3.11+

