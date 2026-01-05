# Website Contact Form

A production-ready HTML contact form that submits lead data directly to your Make.com webhook.

## 🎯 What This Does

This form replaces manual testing (like `curl` commands) with a real website form that:
- Collects lead information from website visitors
- Validates input on the client side
- Sends data directly to your Make.com webhook
- Triggers your existing automation (AI analysis → Google Sheets)

## 🔗 How It Connects to Make.com

```
Website Form → Make.com Webhook → HTTP Module → Your FastAPI API → AI Analysis → Google Sheets
```

1. **User fills out form** on your website
2. **Form submits** to Make.com webhook URL
3. **Make.com scenario** receives the data
4. **HTTP module** forwards to your FastAPI endpoint
5. **AI processes** the lead (intent, urgency, score, etc.)
6. **Data saved** to Google Sheets

## 🚀 Setup Instructions

### Step 1: Update Webhook URL

Open `index.html` and find this line (around line 200):

```javascript
const WEBHOOK_URL = 'https://hook.eu1.make.com/akkh2ku2d4y3okguu3qsp6iuovx3hctk';
```

Replace with your Make.com webhook URL.

### Step 2: Deploy

#### Option A: Netlify (Recommended - Easiest)

1. Go to https://www.netlify.com
2. Drag and drop the `website` folder
3. Your form is live! (e.g., `https://your-site.netlify.app`)

#### Option B: Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel` in the `website` directory
3. Follow prompts

#### Option C: GitHub Pages

1. Create a GitHub repository
2. Upload `index.html` to the repository
3. Go to Settings → Pages
4. Enable GitHub Pages
5. Your form will be at: `https://yourusername.github.io/repo-name`

#### Option D: Local Testing

Just open `index.html` in a web browser (works locally too!)

## 📋 Form Fields

- **Name** (required) - Text input
- **Email** (required) - Email validation
- **Company** (optional) - Text input
- **Message** (required) - Textarea

The form automatically adds `"source": "website_form"` to the payload.

## ✨ Features

- ✅ Client-side validation (required fields, email format)
- ✅ Real-time error messages
- ✅ Success/error feedback
- ✅ Loading state during submission
- ✅ Mobile-responsive design
- ✅ Modern, professional UI
- ✅ No external dependencies (pure HTML/CSS/JS)

## 🎨 Customization

### Change Colors

Edit the CSS gradient in the `<style>` section:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Change Form Title

Edit the `<h1>` tag:

```html
<h1>Your Custom Title</h1>
```

### Add More Fields

1. Add HTML input in the form
2. Add to the `payload` object in JavaScript
3. Update Make.com scenario to map the new field

## 🔍 Testing

1. Open `index.html` in a browser
2. Fill out the form
3. Submit
4. Check Make.com scenario execution
5. Verify data appears in Google Sheets

## 📱 Real-World Usage

### For Clients:

1. **Deploy** the form to their website (Netlify/Vercel)
2. **Update** the webhook URL in `index.html`
3. **Embed** on their landing page or create a dedicated contact page
4. **Leads automatically flow** into their CRM (Google Sheets)

### Example Workflow:

```
Website Visitor → Fills Form → Submits
    ↓
Make.com Webhook Receives Data
    ↓
AI Analyzes Lead (intent, urgency, score)
    ↓
High-Priority Lead? → Slack/Gmail Alert
    ↓
All Leads → Saved to Google Sheets
```

## 🛠️ Troubleshooting

### Form not submitting?

- Check browser console for errors (F12)
- Verify webhook URL is correct
- Check Make.com scenario is ON
- Verify Make.com webhook is active

### Data not appearing in Google Sheets?

- Check Make.com scenario execution logs
- Verify HTTP module URL is correct
- Check your FastAPI server is running
- Verify ngrok is running (if testing locally)

### CORS errors?

- Make.com webhooks handle CORS automatically
- If issues persist, check Make.com scenario settings

## 📝 Notes

- This is a **static HTML file** - no backend needed
- Works with your **existing Make.com scenario** (no changes required)
- **No API keys** exposed (webhook URL is safe to use client-side)
- **Production-ready** - can be deployed immediately

## 🔐 Security Considerations

- Webhook URLs are safe to use in client-side code (they're designed for public access)
- Consider rate limiting in Make.com if needed
- For production, you may want to add:
  - reCAPTCHA (to prevent spam)
  - Rate limiting (in Make.com scenario)
  - IP filtering (in Make.com)

---

**Ready to use!** Just update the webhook URL and deploy. 🚀

