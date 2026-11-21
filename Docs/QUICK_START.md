# Quick Start — Backend Deployment

**5-minute setup to deploy your backend and stop charging users for API keys.**

## Files You Have

- `server.js` — the backend (proxies API calls)
- `abs-by-ai.html` — updated frontend (calls your backend)
- `package.json` — dependencies
- `vercel.json` — deployment config

## Step 1: Get Your API Keys

1. **Claude:** https://console.anthropic.com → copy your API key (starts with `sk-ant-`)
2. **Gemini:** https://aistudio.google.com/apikey → copy your API key (starts with `AIza`)

Both need billing enabled.

## Step 2: Deploy to Vercel

1. Go to https://vercel.com/new
2. Click "Import Git Repository" and paste this repo URL (or upload via GitHub)
3. Add environment variables:
   - `ANTHROPIC_API_KEY` = your Claude key
   - `GEMINI_API_KEY` = your Gemini key
4. Click Deploy

Done. You get a URL like `https://abs-by-ai.vercel.app`

## Step 3: Update Frontend

In `abs-by-ai.html`, find this line:

```javascript
const BACKEND_URL = 'https://your-vercel-domain.vercel.app';
```

Replace `your-vercel-domain` with your actual Vercel domain.

## Step 4: Host the HTML File

Put `abs-by-ai.html` anywhere your users can access it:
- Same Vercel project (add static file routing)
- Netlify
- GitHub Pages
- Your own server
- S3

## That's It

Users now go to your HTML file, upload a photo, and the backend handles all API costs. No more API key entry.

## Verify It Works

1. Open the HTML file
2. Upload a photo
3. Fill the form and click "Generate"
4. Should see transformation in 15–30 seconds

If it fails, check:
- Backend URL in the HTML
- Environment variables in Vercel console
- API keys have billing enabled

---

See `DEPLOYMENT.md` for detailed docs.
