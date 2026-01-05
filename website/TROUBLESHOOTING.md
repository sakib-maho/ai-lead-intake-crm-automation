# Troubleshooting Form Submission Errors

## Common Issues and Solutions

### Error: "Something went wrong"

This usually means one of the following:

#### 1. Make.com Scenario is OFF
**Solution:**
- Go to Make.com
- Open your scenario
- Make sure the toggle switch at the top is **ON** (green/blue)
- The scenario must be ON to receive webhooks

#### 2. Wrong Webhook URL
**Solution:**
- Open `index.html` in a text editor
- Find line with `const WEBHOOK_URL = '...'`
- Verify it matches your Make.com webhook URL exactly
- Make.com webhook URLs look like: `https://hook.eu1.make.com/...`

#### 3. CORS Issues (Less Common)
**Solution:**
- Make.com webhooks handle CORS automatically
- If you see CORS errors in console, check Make.com scenario settings
- Try opening browser console (F12) to see detailed error

#### 4. Network/Firewall Issues
**Solution:**
- Check your internet connection
- Try from a different network
- Check if corporate firewall is blocking requests

## Debugging Steps

### Step 1: Check Browser Console
1. Open the form in browser
2. Press `F12` (or right-click → Inspect → Console)
3. Submit the form
4. Look for error messages in red
5. Check what it says - this will tell you the exact problem

### Step 2: Verify Webhook URL
1. In browser console, you should see: `Webhook URL: https://...`
2. Copy that URL
3. Test it directly with curl:
   ```bash
   curl -X POST "YOUR-WEBHOOK-URL" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test","email":"test@test.com","message":"Test"}'
   ```
4. If curl works but form doesn't, it's a browser/CORS issue

### Step 3: Check Make.com
1. Go to Make.com scenario
2. Check "Operations" or "Executions"
3. See if the webhook was received
4. If no execution appears, the scenario is OFF or URL is wrong

### Step 4: Test Payload
Check browser console for:
```
Submitting payload: {name: "...", email: "...", ...}
```
Verify all fields are present and correct.

## Quick Test

Run this in terminal to test webhook directly:

```bash
curl -X POST "https://hook.eu1.make.com/akkh2ku2d4y3okguu3qsp6iuovx3hctk" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "company": "Test Corp",
    "message": "This is a test",
    "source": "website_form"
  }'
```

If this works but the form doesn't, the issue is in the browser/form code.

## Most Common Fix

**90% of the time, the issue is:**
- Make.com scenario is turned OFF

**Fix:**
1. Go to Make.com
2. Turn scenario ON
3. Try form again

