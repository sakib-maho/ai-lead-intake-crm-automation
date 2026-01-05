# Make.com Scenario Setup - Step by Step

## Step 1: Create New Scenario

1. Go to https://www.make.com
2. Click **"Create a new scenario"** (or **"Scenarios"** → **"Create a new scenario"**)
3. Give it a name: "AI Lead Intake Automation"

## Step 2: Add Webhook Module (Trigger)

1. Click **"Add a module"** or drag from the left panel
2. Search for **"Webhooks"**
3. Select **"Custom webhook"**
4. Click **"Add"** button (this creates the webhook)
5. **IMPORTANT**: 
   - The webhook URL will appear (e.g., `https://hook.eu1.make.com/...`)
   - **Copy this URL** - you'll use it to send test requests
   - **DO NOT close this module yet**

## Step 3: Add HTTP Module (Call Your API)

1. Click **"Add a module"** again (or the **"+"** button after the webhook)
2. Search for **"HTTP"**
3. Select **"Make a request"**
4. Configure:
   - **Method**: `POST`
   - **URL**: `https://axenic-santo-unstartled.ngrok-free.dev/lead`
   - **Headers**: Click "Add header"
     - **Name**: `Content-Type`
     - **Value**: `application/json`
   - **Body type**: Select **"Raw"**
   - **Request content**: 
   ```json
   {
     "name": "{{name}}",
     "email": "{{email}}",
     "company": "{{company}}",
     "message": "{{message}}",
     "source": "{{source}}"
   }
   ```
   - Note: The `{{name}}`, `{{email}}` etc. are data from the webhook module

## Step 4: TURN ON THE SCENARIO ⚠️ CRITICAL!

1. Look for the **toggle switch** at the top of the scenario (usually says "OFF")
2. Click it to turn it **"ON"** (it should turn green/blue)
3. **This is essential!** The scenario must be ON to listen for webhooks

## Step 5: Test the Webhook

Once the scenario is ON:

1. Copy the webhook URL from Step 2
2. Test it from your terminal:

```bash
curl -X POST "YOUR-WEBHOOK-URL" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "company": "Acme Inc",
    "message": "We need an AI lead system. Budget 5k. ASAP",
    "source": "website_form"
  }'
```

3. Go back to Make.com and check:
   - You should see a new execution appear
   - Click on it to see the flow
   - Verify the HTTP module called your API successfully

## Common Issues

### Issue: "No scenario listening for this webhook"
**Solution**: 
- Make sure the scenario is **turned ON** (toggle switch at top)
- Verify you're using the correct webhook URL
- Check that the webhook module is the first module in the scenario

### Issue: HTTP module fails
**Solution**:
- Verify ngrok is still running
- Check the URL is correct: `https://axenic-santo-unstartled.ngrok-free.dev/lead`
- Verify your local server is running
- Check ngrok dashboard: http://127.0.0.1:4040

### Issue: Data not mapping correctly
**Solution**:
- In the HTTP module, make sure you're using `{{name}}`, `{{email}}`, etc.
- These should auto-populate from the webhook module
- If not, click the field and select from the webhook's output

## Visual Flow

```
[Webhook] → Receives lead data
    ↓
[HTTP Request] → POST to your ngrok URL
    ↓
[Your Local API] → Processes with AI
    ↓
[Response back to Make.com]
```

## Next Steps After Testing

Once the basic flow works, you can add:
- Google Sheets module (to store leads)
- Router module (to check for duplicates)
- Slack/Gmail modules (for notifications)

See `make/scenario_blueprint.md` for the complete setup.

