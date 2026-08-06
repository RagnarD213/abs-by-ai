# Abs By AI — Backend Deployment Guide

This guide walks you through deploying the Abs By AI backend to Vercel. Your users will no longer need API keys — you'll handle all costs.

## What You're Deploying

- **server.js** — Node.js/Express backend that proxies API calls to Claude and Gemini
- **Three endpoints:**
  - `/api/check-photo` — validates photos (Claude Haiku)
  - `/api/generate-prompt` — creates image prompt (Claude Sonnet)
  - `/api/generate-image` — generates image (Gemini)
- **Rate limiting:** 10 requests/minute per IP to prevent abuse
- **abs-by-ai.html** — updated app that calls your backend instead of APIs directly

## Prerequisites

1. **Vercel account** — sign up at https://vercel.com
2. **Claude API key** — get one at https://console.anthropic.com
3. **Gemini API key** — get one at https://aistudio.google.com/apikey (linked to a billing account)
4. **Git installed** (optional, but easiest deployment method)

## Deployment Steps

### Step 1: Prepare Your Environment

Copy `.env.example` to `.env.local` and fill in your API keys:
```bash
cp .env.example .env.local
```

Edit `.env.local` and add:
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
GEMINI_API_KEY=AIzaxxxxx
```

**Keep `.env.local` private — never commit it to git.**

### Step 2: Deploy to Vercel

#### Option A: Via Vercel CLI (recommended)

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. When prompted, link to your Vercel account and project
4. Enter your API keys when asked for environment variables (or set them via Vercel dashboard later)

#### Option B: Via GitHub + Vercel Dashboard

1. Create a git repository and push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/abs-by-ai-backend.git
git push -u origin main
```

2. Go to https://vercel.com/new and connect your GitHub repo
3. Set environment variables in Vercel dashboard:
   - `ANTHROPIC_API_KEY` — your Claude API key
   - `GEMINI_API_KEY` — your Gemini API key
4. Click Deploy

### Step 3: Configure Your Frontend

After deployment, you'll get a Vercel URL (e.g., `https://abs-by-ai.vercel.app`).

Update the `BACKEND_URL` in **abs-by-ai.html**:
```javascript
const BACKEND_URL = 'https://your-vercel-domain.vercel.app';
```

### Step 4: Host Your Frontend

Host `abs-by-ai.html` on any static hosting:
- **Vercel:** deploy it as a static file alongside your backend
- **Netlify:** free static hosting
- **GitHub Pages:** free
- **S3:** AWS
- **Your own domain:** upload the HTML file anywhere

## Vercel.json Explained

The `vercel.json` file configures how Vercel deploys your app:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "server.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "server.js"
    }
  ],
  "env": {
    "ANTHROPIC_API_KEY": "@anthropic_api_key",
    "GEMINI_API_KEY": "@gemini_api_key"
  }
}
```

This tells Vercel to:
- Use Node.js runtime for `server.js`
- Route all requests to the server (no static files at this URL)
- Reference environment variables you set in the Vercel dashboard

## Environment Variables in Vercel

To add/update API keys in Vercel dashboard:

1. Go to your project → Settings → Environment Variables
2. Add:
   - **Name:** `ANTHROPIC_API_KEY` | **Value:** `sk-ant-xxxxx`
   - **Name:** `GEMINI_API_KEY` | **Value:** `AIzaxxxxx`
3. Redeploy: Vercel → Deployments → Re-run on the latest commit

## Testing Locally

Test before deploying:

```bash
# Install dependencies
npm install

# Start server
npm start
```

Server runs on `http://localhost:3000`. Update the BACKEND_URL in abs-by-ai.html to `http://localhost:3000` for testing.

## API Endpoint Reference

### POST /api/check-photo
**Validates a photo with Claude Haiku**

Request:
```javascript
{
  "photoBase64": "iVBORw0KGgo...",
  "photoMime": "image/jpeg"
}
```

Response:
```javascript
{
  "code": "OK" // or CLOTHED, SUGGESTIVE, EXPLICIT, ILLEGAL, MINOR
}
```

### POST /api/generate-prompt
**Generates an image prompt with Claude Sonnet**

Request:
```javascript
{
  "systemPrompt": "You are the prompt-engineering layer...",
  "userJson": "{\"user_description\": \"...\", \"subject_gender\": \"male\", ...}"
}
```

Response:
```javascript
{
  "prompt": "Reduce the subject to 9-11% body fat..."
}
```

### POST /api/generate-image
**Generates an image with Gemini**

Request:
```javascript
{
  "prompt": "Reduce the subject to 9-11% body fat...",
  "photoBase64": "iVBORw0KGgo...",
  "photoMime": "image/jpeg"
}
```

Response:
```javascript
{
  "imageBase64": "iVBORw0KGgo..."
}
```

## Cost Management

Monitor your API usage and costs:

- **Claude API** — https://console.anthropic.com/account/billing/overview
- **Gemini API** — https://console.cloud.google.com/billing

### Estimated Costs Per User
- Photo check (Haiku): ~$0.001
- Prompt generation (Sonnet): ~$0.01
- Image generation (Gemini): ~$0.03–0.05
- **Total per session:** ~$0.05–0.07

### Rate Limiting
The backend limits to 10 requests per minute per IP to prevent abuse. Adjust in `server.js` if needed:
```javascript
const limiter = rateLimit({
  windowMs: 60 * 1000,
  max: 10, // change this number
});
```

## Troubleshooting

### "Backend returned an error"
- Check your Vercel logs: `vercel logs`
- Ensure API keys are correct and have billing enabled
- Verify Claude key starts with `sk-ant-`
- Verify Gemini key starts with `AIza`

### "Too many requests"
- Rate limiting kicked in. Wait a minute and retry
- Adjust rate limits in `server.js` if needed for your use case

### "Image generation was blocked"
- User's photo was flagged as inappropriate
- Suggest users upload a clear, neutral shirtless/sports-bra photo

### CORS errors in browser
- Verify `BACKEND_URL` in abs-by-ai.html is correct
- Check that your Vercel domain is set in the HTML

## Next Steps

1. ✅ Deploy backend to Vercel
2. ✅ Host abs-by-ai.html (Vercel, Netlify, GitHub Pages, etc.)
3. ✅ Monitor API costs
4. 📊 Add analytics to track usage
5. 🔐 Consider authentication if you want to limit access
6. 💳 Set spending limits on Claude + Gemini API consoles

---

Questions? Check the repo or contact support.
