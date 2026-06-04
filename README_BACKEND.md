# Abs By AI Backend

Backend for the Abs By AI fitness transformation app. Proxies API calls to Claude and Gemini so users don't need their own API keys — you pay the costs.

## What Changed

### Before (User-Managed Keys)
- Users entered Claude API key in the app
- Users entered Gemini API key in the app
- App made direct API calls from the browser
- Users charged directly or needed billing setup

### After (Backend-Managed Keys)
- No API key inputs in the app
- Backend holds API keys (secure, server-side)
- App calls three backend endpoints instead
- You control all costs, rate limiting, and usage

## Architecture

```
[Browser] → abs-by-ai.html
    ↓
    └─→ [Your Backend on Vercel]
            ├─ /api/check-photo    → Claude Haiku
            ├─ /api/generate-prompt → Claude Sonnet
            └─ /api/generate-image  → Gemini
```

**Flow:**
1. User uploads photo → backend validates it with Claude Haiku
2. User fills form → backend generates detailed prompt with Claude Sonnet
3. User clicks Generate → backend passes photo + prompt to Gemini to create image
4. Backend returns image → displayed in browser

## What's Inside

### Files

| File | Purpose |
|------|---------|
| `server.js` | Express backend with three API endpoints |
| `package.json` | Node dependencies (express, cors, rate-limiting) |
| `vercel.json` | Vercel deployment config |
| `.env.example` | Template for environment variables |
| `abs-by-ai.html` | Updated frontend (calls backend instead of APIs) |
| `DEPLOYMENT.md` | Step-by-step Vercel deployment guide |
| `QUICK_START.md` | 5-minute setup summary |

### Environment Variables

```
ANTHROPIC_API_KEY  = your Claude API key (starts with sk-ant-)
GEMINI_API_KEY     = your Gemini API key (starts with AIza)
```

Store these in Vercel's environment variable settings. Never hardcode them.

## Cost Control

### Rate Limiting
- **10 requests per minute per IP** — prevents abuse
- Adjust in `server.js` line ~19 if needed

### Monitoring
- **Claude usage:** https://console.anthropic.com/account/billing/overview
- **Gemini usage:** https://console.cloud.google.com/billing

### Estimated Costs
| Operation | Cost | Notes |
|-----------|------|-------|
| Photo check (Haiku) | $0.001 | Fast, cheap validation |
| Prompt generation (Sonnet) | $0.01 | High-quality prompt |
| Image generation (Gemini) | $0.03–0.05 | Bulk of cost |
| **Per user session** | **$0.05–0.07** | One generate cycle |

## How to Deploy

**Fastest way (5 minutes):**
1. Copy API keys
2. Go to https://vercel.com/new
3. Import this repo
4. Set environment variables
5. Click Deploy

See `QUICK_START.md` for details.

## Endpoints Reference

### 1. POST `/api/check-photo`
Validates photo using Claude Haiku.

**Request:**
```json
{
  "photoBase64": "iVBORw0KGgo...",
  "photoMime": "image/jpeg"
}
```

**Response (OK):**
```json
{ "code": "OK" }
```

**Response (Blocked):**
```json
{ "code": "CLOTHED" }
```

Valid codes: `OK`, `CLOTHED`, `SUGGESTIVE`, `EXPLICIT`, `ILLEGAL`, `MINOR`

---

### 2. POST `/api/generate-prompt`
Generates image-editing prompt using Claude Sonnet.

**Request:**
```json
{
  "systemPrompt": "You are the prompt-engineering layer...",
  "userJson": "{\"user_description\": \"...\", \"subject_gender\": \"male\", ...}"
}
```

**Response:**
```json
{
  "prompt": "Reduce the subject to 9-11% body fat. The body in the output image MUST look unmistakably and dramatically different..."
}
```

---

### 3. POST `/api/generate-image`
Generates transformed image using Gemini.

**Request:**
```json
{
  "prompt": "Reduce the subject to 9-11% body fat...",
  "photoBase64": "iVBORw0KGgo...",
  "photoMime": "image/jpeg"
}
```

**Response:**
```json
{
  "imageBase64": "iVBORw0KGgo..."
}
```

## Troubleshooting

### Vercel shows "Internal Server Error"
- Check that both API keys are set in environment variables
- Verify API keys are correct (Claude: starts with `sk-ant-`, Gemini: starts with `AIza`)
- Check both APIs have billing enabled

### App says "Backend error (HTTP 500)"
- See logs: go to Vercel → your project → Deployments → Logs
- Common issue: missing or incorrect API keys

### Rate limiting kicks in
- User/IP exceeded 10 requests/minute
- Wait 60 seconds and retry
- To allow more: edit `server.js` line 19

### CORS error in browser console
- The frontend's `BACKEND_URL` doesn't match your Vercel domain
- Update `abs-by-ai.html` line ~2:
  ```javascript
  const BACKEND_URL = 'https://YOUR-VERCEL-DOMAIN.vercel.app';
  ```

## Next Steps

1. **Deploy backend** → Vercel (docs: `DEPLOYMENT.md`)
2. **Update frontend** → set correct `BACKEND_URL` in abs-by-ai.html
3. **Host HTML** → Netlify, GitHub Pages, or your domain
4. **Test** → upload photo, fill form, generate image
5. **Monitor** → watch API usage in Claude + Gemini consoles
6. **Optimize** → adjust rate limits, add analytics, tweak prompts

## Local Testing

```bash
# Install dependencies
npm install

# Start server
npm start

# Server runs on http://localhost:3000
# Update abs-by-ai.html:
# const BACKEND_URL = 'http://localhost:3000';
```

---

**Questions?** See `DEPLOYMENT.md` for detailed setup or check the code comments.
