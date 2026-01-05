# Fix HTTP 410 Error - Webhook URL Gone

## What HTTP 410 Means

**HTTP 410 "Gone"** means the webhook URL no longer exists. This happens when:
- The Make.com webhook was deleted
- The scenario was deleted
- The webhook module was removed and re-added
- The webhook expired (rare, but possible)

## Solution: Create New Webhook

### Step 1: Go to Make.com

1. Open your Make.com scenario
2. Find the **Webhook** module (first module)

### Step 2: Create New Webhook

**Option A: If webhook module shows "Add" button:**
1. Click **"Add"** button
2. This creates a new webhook URL
3. Copy the new URL (it will look like: `https://hook.eu1.make.com/...`)

**Option B: If webhook module exists but URL is old:**
1. Click on the webhook module
2. Click **"Remove"** or delete the module
3. Add a new **"Custom webhook"** module
4. Click **"Add"** to create new webhook
5. Copy the new URL

### Step 3: Update Form

1. Open `website/index.html` in a text editor
2. Find this line (around line 200):
   ```javascript
   const WEBHOOK_URL = 'https://hook.eu1.make.com/akkh2ku2d4y3okguu3qsp6iuovx3hctk';
   ```
3. Replace with your NEW webhook URL:
   ```javascript
   const WEBHOOK_URL = 'https://hook.eu1.make.com/YOUR-NEW-WEBHOOK-ID';
   ```
4. Save the file
5. Refresh the form in browser

### Step 4: Verify

1. Make sure Make.com scenario is **ON**
2. Test the form again
3. Check Make.com executions to see if it worked

## Quick Checklist

- [ ] Make.com scenario is ON
- [ ] New webhook created in Make.com
- [ ] New webhook URL copied
- [ ] `index.html` updated with new URL
- [ ] Form refreshed in browser
- [ ] Test submission

## Alternative: Use Environment Variable (Advanced)

If you deploy to Netlify/Vercel, you can use environment variables:

1. Set `WEBHOOK_URL` as environment variable
2. Update form to read from `window.WEBHOOK_URL` or similar
3. This way you don't need to edit HTML each time

But for now, just update the URL in `index.html` - it's simpler!

