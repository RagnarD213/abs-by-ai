---
name: repo-is-public
description: github.com/RagnarD213/abs-by-ai is a PUBLIC repo — check before committing personal photos or anything sensitive
metadata: 
  node_type: memory
  type: project
  originSessionId: 23c04be3-2aa3-48dd-bef2-ef7b9c872099
  modified: 2026-07-25T23:22:58.984Z
---

The Abs By AI GitHub repo (`github.com/RagnarD213/abs-by-ai`, the one Railway auto-deploys from) is **public**. Verify with an unauthenticated `curl -s -o /dev/null -w "%{http_code}" https://api.github.com/repos/RagnarD213/abs-by-ai` — 200 means public.

Anything committed there is world-readable and permanent in git history, even when the server never serves it over HTTP (the server serves only `public/` — see [[static-serving-and-json-persistence]]).

**Why:** on 2026-07-25 the judge's few-shot exemplars needed 9 images committed to `assets/judge-exemplars/`, three of which were Dan's own shirtless photo plus AI-shredded edits of it. Dan was asked explicitly and chose to commit all nine as-is rather than make the repo private or drop his photo from the set.

**How to apply:** before committing images of real people, credentials, or customer data, say plainly that the repo is public and let Dan decide. Do not assume the previous approval covers a new case — it was granted for one specific set of files.
