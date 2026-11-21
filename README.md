# Abs By AI

Live at **[absbyai.com](https://absbyai.com)**. One website serves all three platforms —
the iOS and Android apps are thin wrappers that load the same live site, so a push to
`main` updates web, iOS and Android at once.

## Where things live

### Start here
| Path | What it is |
|---|---|
| `AI_COORDINATION.md` | The shared task board. Current work, decisions, and what's verified. Read this first. |
| `CLAUDE.md` / `AGENTS.md` | Working rules for Claude Code and Codex. |
| `Handoffs/` | All 75 handoff documents, with an index in `Handoffs/README.md`. |
| `Docs/` | Project documentation — plans, audits, deployment and setup notes. |

### The app itself
| Path | What it is |
|---|---|
| `server.js` | The entire backend. Every API endpoint. |
| `db.js` | Postgres connection and schema. |
| `public/` | Everything served to the browser — `index.html` is the whole front end. |
| `assets/judge-exemplars/` | Reference images the AI judge compares against. Production — do not move. |
| `dashboard.html`, `admin.html` | Served from the root by name (`/dashboard`, `/admin`). Must stay in the root. |
| `*-data.json` | **These are the database** for credits, subscribers, todos and plans. The server reads and writes them by exact filename. Never move or rename them. |

### Apps and testing
| Path | What it is |
|---|---|
| `ios-app/` | iOS wrapper (Capacitor). |
| `android/` | Android wrapper (TWA) and signed build output. |
| `app-store-assets/` | Screenshots and listing copy for both stores. |
| `bakeoff/` | Model comparison harnesses and Dan's blind image labels. |
| `eval/` | Automated quality tests. |
| `scripts/` | Utility scripts, including the native smoke test. |

### Media and business (all kept out of git)
| Path | What it is |
|---|---|
| `Media/` | Working photos and video — B roll, source photos, edits, personal photos. |
| `YouTube Content/` | Finished videos ready for upload. |
| `social media graphics/`, `logos/` | Brand assets. |
| `Business/` | LLC formation documents and legal forms. |
| `ad-factory/` | AI-generated video ad production files. |
| `Archive/` | Retired files kept for reference. Nothing here is live. |

## Important

**This GitHub repository is public.** `Media/`, `Business/`, `YouTube Content/`,
`ad-factory/` and `_counsel_archive/` are excluded in `.gitignore` because they hold
personal photos, legal paperwork and private working files. Check `.gitignore` before
adding a new folder that contains anything private.

Only the `public/` folder is reachable over the web. Everything else in this repository
is on the server's disk but is not served to visitors.
