# Setting Up Make.com with Localhost

Since Make.com runs in the cloud, it can't directly access `localhost`. We need to expose your local server to the internet using a tunneling service like **ngrok**.

## Step 1: Install and Authenticate ngrok

### Install ngrok

### Option A: Using Homebrew (macOS)
```bash
brew install ngrok
```

### Option B: Download from ngrok.com
1. Go to https://ngrok.com/download
2. Download for macOS
3. Extract and add to PATH, or use directly

### Option C: Using npm
```bash
npm install -g ngrok
```

### Authenticate ngrok (REQUIRED)

ngrok requires a free account:

1. **Sign up**: https://dashboard.ngrok.com/signup (free account)
2. **Get authtoken**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure**:
   ```bash
   ngrok config add-authtoken YOUR_AUTHTOKEN_HERE
   ```

Or use the helper script:
```bash
./setup_ngrok_auth.sh
```

## Step 2: Start Your Local Server

Make sure your FastAPI server is running:

```bash
cd /Users/sakib/Project/Make.com
source venv/bin/activate
python -m app.main
```

The server should be running on `http://localhost:8000`

## Step 3: Start ngrok Tunnel

In a **new terminal window**, run:

```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok-free.app`)

⚠️ **Important**: Keep this terminal open! Closing it will stop the tunnel.

## Step 4: Configure Make.com

### A. Create Webhook in Make.com

1. Go to https://www.make.com
2. Create a new scenario
3. Add **Webhooks > Custom webhook** module
4. Click "Add" to create a new webhook
5. Copy the webhook URL (you'll use this to send test requests)

### B. Add HTTP Module to Call Your API

1. Add **HTTP > Make a request** module
2. Configure:
   - **Method**: POST
   - **URL**: `https://YOUR-NGROK-URL.ngrok-free.app/lead`
     - Replace `YOUR-NGROK-URL` with your actual ngrok URL
   - **Headers**:
     - `Content-Type: application/json`
   - **Body type**: Raw
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

### C. Test the Connection

1. In Make.com, click "Run once" on the webhook module
2. Copy the webhook URL
3. Test it from your terminal:

```bash
curl -X POST "YOUR-MAKECOM-WEBHOOK-URL" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "company": "Test Corp",
    "message": "This is a test lead",
    "source": "make_test"
  }'
```

4. Check Make.com scenario execution - it should call your local API!

## Step 5: Handle ngrok Browser Warning (Free Tier)

If you see an ngrok browser warning page:
- Click "Visit Site" button
- Or upgrade to ngrok paid plan to remove warnings
- Or use ngrok's `--host-header` flag (see below)

## Alternative: ngrok with Custom Domain (No Browser Warning)

```bash
ngrok http 8000 --host-header=localhost:8000
```

## Troubleshooting

### Issue: ngrok URL changes every time
**Solution**: 
- Sign up for free ngrok account: https://dashboard.ngrok.com/signup
- Get authtoken: `ngrok config add-authtoken YOUR_TOKEN`
- Use static domain (paid feature) or update Make.com URL each time

### Issue: "Tunnel not found" error
**Solution**: 
- Make sure ngrok is still running
- Check the ngrok URL is correct in Make.com
- Verify your local server is running on port 8000

### Issue: CORS errors
**Solution**: 
- The FastAPI app already has CORS enabled for all origins
- If issues persist, check `app/main.py` CORS settings

### Issue: Connection timeout
**Solution**:
- Check ngrok is running
- Verify local server is accessible: `curl http://localhost:8000/health`
- Check ngrok dashboard: https://dashboard.ngrok.com/status/tunnels

## Quick Reference

```bash
# Terminal 1: Start local server
cd /Users/sakib/Project/Make.com
source venv/bin/activate
python -m app.main

# Terminal 2: Start ngrok
ngrok http 8000

# Terminal 3: Test webhook
curl -X POST "YOUR-MAKECOM-WEBHOOK-URL" \
  -H "Content-Type: application/json" \
  -d @examples/sample_lead.json
```

## Production Deployment

For production, deploy to:
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Fly.io**: https://fly.io

Then use the production URL directly in Make.com (no ngrok needed).

