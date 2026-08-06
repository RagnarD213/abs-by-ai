# Abs By AI — Deployment Handoff

## Project Status: LIVE ✅

The Abs By AI fitness transformation app is fully deployed and operational on the custom domain **absbyai.com**.

## What Was Built

A complete backend infrastructure that handles all API calls server-side, eliminating the need for users to provide their own API keys. The backend proxies requests to Claude and Gemini APIs.

### Architecture

**Frontend:** Single HTML file (`index.html`) hosted on Netlify at absbyai.com
**Backend:** Node.js/Express server proxied through Netlify at ubiquitous-brioche-b456d1.netlify.app
**APIs:** 
- Claude (Anthropic) for photo validation and prompt generation
- Gemini (Google) for image transformation

### Three Backend Endpoints

1. **POST /api/check-photo** — Validates photo with Claude Haiku (~$0.001/check)
2. **POST /api/generate-prompt** — Creates image prompt with Claude Sonnet (~$0.01/generation)
3. **POST /api/generate-image** — Transforms image with Gemini (~$0.03–0.05/image)

Total cost per user: ~$0.05–0.07

## Deployment Details

### Domain Setup
- **Primary domain:** absbyai.com (purchased on Namecheap)
- **DNS:** CNAME record pointing to apex-loadbalancer.netlify.com
- **SSL:** Automatic via Netlify

### Hosting
- **Frontend:** Netlify (ubiquitous-brioche-b456d1.netlify.app)
- **Backend:** Same Netlify deployment
- Files deployed:
  - index.html (renamed from abs-by-ai.html to load at root)
  - server.js
  - package.json
  - vercel.json (for Vercel—can be removed if Netlify only)

### Environment Variables (Set in Netlify)
- `ANTHROPIC_API_KEY` — Your Claude API key from console.anthropic.com
- `GEMINI_API_KEY` — Your Gemini API key from aistudio.google.com

## File Structure

```
/Users/danielrose/Documents/Claude/Projects/Abs By AI/
├── index.html              # Frontend (loads at root)
├── abs-by-ai.html          # Old version (can delete)
├── abs-by-ai-updated.html  # Backup (can delete)
├── server.js               # Backend server
├── package.json            # Dependencies
├── vercel.json             # Vercel config (optional)
├── .env.example            # Template for env vars
├── .gitignore              # Git ignore rules
├── DEPLOYMENT.md           # Detailed deployment guide
├── QUICK_START.md          # Quick reference
├── README_BACKEND.md       # Backend documentation
├── WHAT_WAS_BUILT.md       # Architecture overview
└── HANDOFF.md              # This file
```

## User Flow

1. User goes to absbyai.com
2. Uploads a shirtless/sports-bra photo
3. Fills out form (gender, current condition, intensity, description)
4. Clicks "Generate My Future Self"
5. Backend:
   - Validates photo with Claude Haiku
   - Generates detailed prompt with Claude Sonnet
   - Transforms image with Gemini
6. Shows before/after transformation
7. User can adjust intensity or save image

## Cost Management

### Monthly Estimate (at scale)
- 100 users: $5–7
- 1,000 users: $50–70
- 10,000 users: $500–700

### Monitor Usage
- Claude: https://console.anthropic.com/account/billing/overview
- Gemini: https://console.cloud.google.com/billing

### Rate Limiting
Backend limits to 10 requests per minute per IP to prevent abuse.

## What's Not Yet Done

- Analytics/usage tracking
- User authentication
- Database for saving transformations
- Custom pricing tiers
- Email notifications
- Custom domain branding (content placeholder)
- Advanced features (workout plans, progress tracking—currently placeholder)

## For Next Chat

Reference this document and mention:
- The app is fully deployed at absbyai.com
- Backend is on Netlify with Claude/Gemini APIs
- API keys are stored server-side (users don't need their own)
- Monthly cost is ~$0.05–0.07 per user
- Three endpoints handle photo validation, prompt generation, and image generation

## Quick Links

- **Live app:** https://absbyai.com
- **Netlify project:** https://app.netlify.com/sites/ubiquitous-brioche-b456d1
- **Claude Console:** https://console.anthropic.com/account/billing/overview
- **Gemini Console:** https://console.cloud.google.com/billing
- **Namecheap domain:** https://ap.www.namecheap.com/dashboard/

## Important Notes

1. API keys are configured in Netlify environment variables—never commit them to git
2. DNS is set up via CNAME at Namecheap
3. The backend automatically scales with Netlify (free tier)
4. Rate limiting is in place to prevent abuse
5. All file handling is done server-side (secure)

---

**Last updated:** June 3, 2026
**Status:** Fully operational
**Users can access the app:** Yes, at https://absbyai.com
