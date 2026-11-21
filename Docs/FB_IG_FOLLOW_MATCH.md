# Facebook followers → Instagram follow-back review (Dan, 2026-10-22)

Dan's personal Facebook profile (facebook.com/danroseninja) cannot be a Meta ad audience (Meta builds audiences only
from Pages and Instagram business accounts). Instead, a daily routine finds which of his Facebook followers have an
Instagram account and opens **5 matches every morning** in Chrome. Dan confirms each one is the same person and decides
himself whether to follow them from @danrosefit, so they see his content and may follow back.

- Routine: scheduled task `fb-ig-follow-matches-daily`, 6:45 AM every day (runs when the Claude app is open).
- Helper: `scripts/social/fbig_match.py` (`load`, `next`, `record`, `review`, `stats`).
- Ledger: `~/.absbyai-fbig/ledger.json`, **outside the repo** on purpose: it holds other people's names and profile
  links, and the repo may be public. Never copy it into the repo, a commit, an artifact or a Drive file.
- The list: 584 followers scraped 2026-10-22 from facebook.com/danroseninja/followers (Facebook shows only these, not
  the 2.8K header count). Many are pending friend requests; a good share are new spam accounts.

## Hard rules

1. **Read only.** Never click Follow, Message, Like, Confirm/Delete request, or anything else that acts, on Facebook or
   Instagram. Dan does every follow himself.
2. **Only `match` reaches Dan.** A match needs the same person (or same personal logo/brand) visible in the profile photo
   or posts on both sides, **plus** at least one more signal agreeing: name or nickname, city, workplace, school, a
   handle built from the Facebook name, or "Followed by" people Dan knows. Anything weaker is `unsure` and stays out.
3. Look only at what both profiles show publicly to Dan's logged-in accounts. Do not dig further (no tagged photos of
   other people, no friends lists, no other sites), and keep no photos.
4. Pace like a person: one search at a time, a 3 to 5 second pause between searches, **at most 30 followers checked per
   run**. Stop at 5 matches.

## Steps per run

Chrome extension tools (`mcp__claude-in-chrome__*`), Dan's Chrome is signed in to his Facebook and to @danrosefit.

1. `python3 scripts/social/fbig_match.py next 30` gives the next unchecked followers.
2. For each follower:
   - **Facebook:** open their profile URL, wait 3 s, take a 0.5-scale screenshot (photo, name, nickname in brackets,
     city, work, school, mutual friends). An obvious spam or business account, or one with no photo and no details:
     `record` as `skip` and move on.
   - **Instagram search:** on `https://www.instagram.com/explore/` click the search box at the top (about x=780, y=35 in
     the 1564-wide frame), type the full name, wait 3 s, read the results with:
     ```js
     [...new Set([...document.querySelectorAll('a[href^="/"]')].filter(a=>/^\/[A-Za-z0-9._]+\/$/.test(a.getAttribute('href'))&&a.innerText.trim()).map(a=>a.innerText.replace(/\n+/g,' | ')))].slice(0,8)
     ```
     Nothing plausible: triple-click the box and try first + last name, then the nickname or a distinctive piece of the
     Facebook vanity URL (e.g. `oletsky` from `julie.oletskykatz`). A result that says "Followed by …" is a strong lead.
   - **Candidates:** open at most 3 plausible profiles. Read the header text (`document.querySelector('header').innerText`).
     The button reads `Following` or `Requested`: record `already_following`. Otherwise take a 0.6-scale screenshot and
     compare against the Facebook photo and details under rule 2.
   - **Record** one line per follower, always:
     ```bash
     python3 scripts/social/fbig_match.py record '{"u":"<facebook url>","result":"match","ig":"<handle>","why":"<one plain sentence: what matched>","confidence":"high|likely"}'
     ```
     `result` is one of `match`, `no_account`, `unsure`, `already_following`, `skip`.
3. When 5 matches are recorded today, or 30 followers are checked: `python3 scripts/social/fbig_match.py review`
   prints the review page path. Open it and each match in Dan's normal Chrome with Bash (the extension cannot open
   local files, and normal tabs stay open for him):
   ```bash
   open -a "Google Chrome" "<review page path>"
   open -a "Google Chrome" "https://www.instagram.com/<handle>/"   # once per match
   ```
4. Close the extension tabs you worked in. Nothing is committed (the ledger is outside the repo).
5. Report one or two plain lines: how many matches are open, how many followers checked, how many left
   (`fbig_match.py stats`). No em dashes.

## Traps (2026-10-22 pilot)

- Instagram's search API (`/api/v1/web/search/topsearch/`) returns an HTML page to a script; use the search box.
- Followers list: run long scroll loops in the background (`window.__…` state, poll it), or `javascript_tool` times out
  at 45 s. The Followers tab ends above "Check-ins"; drop those place links. Download the result as a JSON file from the
  page (a blob link) rather than returning it, which truncates.
- To refresh the list later (new followers): scrape again and `fbig_match.py load <file>`; only new links are added.
