# Make.com Scenario Blueprint

This document provides a detailed step-by-step guide for setting up the Make.com automation scenario that processes leads through the FastAPI endpoint and stores them in Google Sheets.

## Scenario Overview

**Trigger:** Webhook receives new lead
**Flow:** Validate → AI Analysis → Google Sheets (with dedupe) → Notifications
**Error Handling:** Log errors to separate sheet

## Module-by-Module Setup

### Module 1: Webhook Trigger

**Type:** Webhooks > Custom webhook

**Configuration:**
- **Webhook name:** `Lead Intake Webhook`
- **Note the webhook URL** - you'll use this to send test requests

**Output:**
- Receives JSON payload with: `name`, `email`, `company`, `message`, `source`

---

### Module 2: HTTP Request to FastAPI

**Type:** HTTP > Make a request

**Configuration:**
- **Method:** POST
- **URL:** 
  - **For localhost testing:** `https://YOUR-NGROK-URL.ngrok-free.app/lead`
    - Get ngrok URL by running: `ngrok http 8000` (see SETUP_MAKECOM_LOCAL.md)
  - **For production:** `https://your-app.railway.app/lead` (or your deployed URL)
- **Headers:**
  - `Content-Type: application/json`
- **Body type:** Raw
- **Request content:** 
```json
{
  "name": "{{name}}",
  "email": "{{email}}",
  "company": "{{company}}",
  "message": "{{message}}",
  "source": "{{source}}"
}
```

**Error handling:**
- Enable error handling
- Set error handler to route to Module 7 (Error Handler)

**Output:**
- Receives structured JSON response with all lead analysis fields

---

### Module 3: Google Sheets - Search for Existing Lead

**Type:** Google Sheets > Search rows

**Configuration:**
- **Spreadsheet:** Select your Google Sheets spreadsheet
- **Sheet:** `Leads`
- **Search criteria:**
  - **Column:** `dedupe_key`
  - **Value:** `{{dedupe_key}}` (from Module 2 response)

**Output:**
- If row found: `rows` array contains the row
- If not found: `rows` array is empty

---

### Module 4: Router - Check if Lead Exists

**Type:** Flow control > Router

**Configuration:**
- **Route 1 (Lead exists):**
  - **Condition:** `{{rows.length}} > 0`
  - **Route to:** Module 5a (Update Row)
- **Route 2 (New lead):**
  - **Condition:** `{{rows.length}} === 0` (or default route)
  - **Route to:** Module 5b (Add Row)

---

### Module 5a: Google Sheets - Update Existing Row

**Type:** Google Sheets > Update a row

**Configuration:**
- **Spreadsheet:** Same as Module 3
- **Sheet:** `Leads`
- **Row number:** `{{rows[0].row}}` (from Module 3)
- **Map all fields from Module 2 response:**
  - `timestamp` → `timestamp`
  - `name` → `name`
  - `email` → `email`
  - `company` → `company`
  - `message` → `message`
  - `source` → `source`
  - `intent` → `intent`
  - `urgency` → `urgency`
  - `budget_range` → `budget_range`
  - `summary` → `summary`
  - `lead_score` → `lead_score`
  - `next_action` → `next_action`
  - `dedupe_key` → `dedupe_key`
  - `raw_payload_json` → `raw_payload_json`

---

### Module 5b: Google Sheets - Add New Row

**Type:** Google Sheets > Add a row

**Configuration:**
- **Spreadsheet:** Same as Module 3
- **Sheet:** `Leads`
- **Map all fields from Module 2 response** (same mapping as Module 5a)

---

### Module 6: Router - Check Notification Criteria

**Type:** Flow control > Router

**Configuration:**
- **Route 1 (High priority):**
  - **Condition:** `{{urgency}} === "high" OR {{lead_score}} >= 80`
  - **Route to:** Module 6a (Send Notifications)
- **Route 2 (Low priority):**
  - **Default route (no condition)
  - **Route to:** End (or optional low-priority notification)

---

### Module 6a: Send Slack Notification

**Type:** Slack > Create a message

**Configuration:**
- **Channel:** `#leads` (or your channel)
- **Text:**
```
🚨 New High-Priority Lead

*Name:* {{name}}
*Company:* {{company}}
*Email:* {{email}}
*Urgency:* {{urgency}}
*Lead Score:* {{lead_score}}
*Budget:* {{budget_range}}
*Summary:* {{summary}}
*Next Action:* {{next_action}}
```

---

### Module 6b: Send Gmail Notification (Optional)

**Type:** Gmail > Send an email

**Configuration:**
- **To:** `sales@yourcompany.com`
- **Subject:** `New High-Priority Lead: {{name}} from {{company}}`
- **Content type:** HTML
- **Body:**
```html
<h2>New High-Priority Lead</h2>
<p><strong>Name:</strong> {{name}}<br>
<strong>Company:</strong> {{company}}<br>
<strong>Email:</strong> {{email}}<br>
<strong>Urgency:</strong> {{urgency}}<br>
<strong>Lead Score:</strong> {{lead_score}}<br>
<strong>Budget:</strong> {{budget_range}}</p>
<p><strong>Summary:</strong> {{summary}}</p>
<p><strong>Next Action:</strong> {{next_action}}</p>
```

---

### Module 7: Error Handler - Log to Error Sheet

**Type:** Google Sheets > Add a row

**Configuration:**
- **Spreadsheet:** Same as Module 3
- **Sheet:** `Errors`
- **Map error data:**
  - `timestamp` → Current timestamp
  - `error_message` → `{{error.message}}`
  - `error_code` → `{{error.code}}`
  - `original_payload` → Stringified original webhook payload

**Error Sheet Columns:**
- `timestamp`
- `error_message`
- `error_code`
- `original_payload`

---

## Complete Flow Diagram

```
[Webhook] 
    ↓
[HTTP: POST to FastAPI /lead]
    ↓ (on error → Error Handler)
[Google Sheets: Search by dedupe_key]
    ↓
[Router: Check if exists]
    ├─→ [Update Row] ──┐
    └─→ [Add Row] ──────┘
         ↓
[Router: Check urgency/score]
    ├─→ [Send Slack] ──┐
    ├─→ [Send Gmail] ──┘
    └─→ [End]
```

## Testing Steps

1. **Test Webhook:**
   - Use Make.com's webhook test feature
   - Or send POST request to webhook URL with sample payload

2. **Verify FastAPI Response:**
   - Check Module 2 output to ensure all fields are present

3. **Test Deduplication:**
   - Send same lead twice (same email)
   - Verify it updates instead of creating duplicate

4. **Test Notifications:**
   - Send lead with `urgency: "high"` or `lead_score: 85`
   - Verify Slack/Gmail notifications are sent

5. **Test Error Handling:**
   - Temporarily break FastAPI URL
   - Verify error is logged to Errors sheet

## Common Issues & Solutions

**Issue:** FastAPI returns 400 error
- **Solution:** Check webhook payload mapping matches expected schema

**Issue:** Google Sheets search not finding existing leads
- **Solution:** Ensure `dedupe_key` column exists and is being searched correctly

**Issue:** Notifications not sending
- **Solution:** Check router conditions match exactly (`urgency === "high"` not `urgency == "high"`)

**Issue:** JSON parsing errors
- **Solution:** Ensure FastAPI response is valid JSON (check Module 2 output)

## Production Considerations

1. **Webhook Security:**
   - Add webhook secret validation
   - Restrict webhook to specific IPs if possible

2. **Rate Limiting:**
   - Add rate limiting in FastAPI if needed
   - Make.com has built-in rate limits

3. **Monitoring:**
   - Set up Make.com scenario monitoring
   - Add alerts for error rate spikes

4. **Backup:**
   - Regularly export Google Sheets data
   - Consider adding database backup

