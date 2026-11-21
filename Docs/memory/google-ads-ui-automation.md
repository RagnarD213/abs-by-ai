---
name: google-ads-ui-automation
description: "Driving Google Ads in Dan's Chrome (claude-in-chrome) — refs/JS in the main app, ×1.112 coordinate clicks inside the Data Manager Flutter iframe; Scripts editor + API center facts; MCC ocid"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4ec90e49-ad4f-474e-afbe-9a1ceafc7944
  modified: 2026-09-03T15:52:07.915Z
---

Learned 2026-09-03 installing the YouTube engagement-champion Ads Script (`Docs/YTADS.md`).

- **Coordinate clicks land on the wrong element** in Google Ads (viewport 2111 px wide, screenshot 1558 px; clicks opened "Ask Advisor" / "Consult your expert" panels instead of the target). Use `find` → `ref` clicks and `javascript_tool` only.
- **Account ids:** Abs by AI client account `342-717-0837` = `ocid=8444849202`; **Daniel Rose Marketing MCC `324-458-6445` = `ocid=364714550`**. Account chooser page: `https://ads.google.com/nav/selectaccount` (search box accepts the CID). The MCC's API center (`/aw/apicenter?ocid=364714550`) now serves only the App Conversion Tracking API — Google Ads API access moved to the Cloud project (Explorer on `abs-by-ai`) and is used through `scripts/ads/api/client.js` ([[google-ads-api-client]]). ⚠ 342-717-0837 is NOT under this MCC (no manager link, verified by API 2026-09-10); Dan has direct access.
- **Scripts:** list at `/aw/bulk/scripts/management?ocid=…`; "New script" is a `menuitem` inside the + button's menu (the direct `/edit` URL is blank). Editor is **CodeMirror 5**: `document.querySelector('.CodeMirror').CodeMirror.setValue(code)`; Save is `material-button.save-button`; name field is the "Unnamed script" textbox. **Scheduling (Frequency pencil → Hourly) is refused until the script is authorized**, and Authorize is an OAuth grant = Dan's click.
- The Demand Gen ads table shows only the FIRST headline/long headline/description per ad ("+2 more"); full copy comes from a GAQL snapshot, not the UI. `get_page_text` sometimes returns the Ask Advisor chat panel instead of the table.
- Campaign name trap: the remarketing campaign's name also contains "geo tier 1" — never match tier 1 by name before excluding RMKTG.

**Data Manager (learned 2026-09-08, mapping the enhanced-conversions Email column):**
- The connection "Manage" side panel and the "Edit field mapping" wizard are a **Flutter canvas app in a cross-origin iframe** (`adsdataconnector.google.com`, `main.dart.js`). `find`/`read_page`/`javascript_tool` cannot see inside it. **Only coordinate clicks work there, and the frame coordinate = screenshot pixel × 1.112** (viewport 2111 wide, screenshot 1568, page content 1411 wide). Calibrate on "View details" before clicking anything that saves.
- Direct URL: `https://ads.google.com/aw/datamanager?ocid=8444849202` (the `/connections` path 404s; `datamanager.google.com` is an error page). Expand the HTTPS row via the "Show panel" ref; **the first click on it reloads the page** — wait ~8 s and click again. Open the connection by the short name button in the Connection column (a `find` ref works; it is in the top document).
- **"Edit mapping" cannot open while the feed is header-only**: it shows "Failed to load the list of imported fields … error 4000" and blank "Select a field" rows with Save disabled — the existing 4-field mapping is not even displayed. Do not save from that state. Mapping a new column waits for the first real row. Never seed one.

Related: [[meta-ads-instagram-identity]], [[ad-suspension-prevention]].

**Custom segments dialog (learned 2026-09-08, building the Demand Gen segments — full recipe in `Handoffs/handoff-20260908-google-ads-custom-segments.md` Execution notes):**
- Page: `/aw/audiences/management/customaudience?ocid=8444849202` (the guessed `/aw/audiences/custom` 404s). Name field takes the native setter; the type `material-radio` needs the pointerdown→…→click sequence; term/URL boxes take one comma-separated `computer type` + Return (all chips land at once); the websites/apps links are `span.add-url` / `span.add-app`; Save/Cancel are `material-button`s by text.
- **Renderer-hang trap:** dispatching pointer events on a `material-list-item` in the app picker, or `await`ing inside one `javascript_tool` call while the insights panel refreshes, froze the Ads renderer twice (needed a new tab; unsaved dialog lost). Use `find`→ref clicks or keyboard for picker rows, and keep JS calls synchronous.
- **Ads will not finish loading in an extension-driven tab while the Mac's load average is above ~40** (166 Claude Code processes + an ffmpeg render did it on 09-08), and once it enters the loading-shell state ("Google Ads" title, `document_idle` never reached) a fresh tab does not recover it in the same session. Check `uptime` before starting a long Ads drive.
