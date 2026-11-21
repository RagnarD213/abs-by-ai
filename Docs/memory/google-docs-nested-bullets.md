---
name: google-docs-nested-bullets
description: How to correctly extract and rebuild hierarchical/nested bullet lists when reorganizing an EXISTING Google Doc — never reconstruct nesting from the markdown-style text export.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: fd29755c-591b-497b-a994-aeeb84f3e071
  modified: 2026-08-14T22:59:55.116Z
---

When splitting, reorganizing, or rewriting an EXISTING Google Doc's content (e.g. moving some sections to a new document), **never reconstruct bullet nesting depth from `read_file_content`'s markdown-style text export.** That export (and any hand re-typed copy of it) flattens or loses real indentation in a large fraction of cases — it only reliably shows 2-3 extra leading spaces for SOME nested blocks and silently drops nesting for others (e.g. a "Deadlifts / Flat bench press / Squats" sub-list rendered at the exact same indent as its parent bullet, even though it is visually nested one level deeper in the real doc). Guessing depth from that text produces a document that "looks plausible" but is objectively wrong, and the error is invisible until a human looks at the rendered bullets.

**Why:** On 2026-08-14, asked to split an outlines doc into "shot" and "not yet shot" pieces while preserving the original hierarchy, the first two attempts both got the nesting wrong — first from a naive flat-list build, then from a "fixed" parser that still trusted the markdown export's indentation. Dan caught it visually ("the hierarchical bullet points on this are messed up"). The fix required going back to Google's real HTML export.

**How to apply — the reliable method:**
1. Get the REAL nested HTML, not the text export. Two ways:
   - If the doc still has its original "Imported .html file" revision in Version History, the "View original" link on that revision downloads the exact source HTML with genuine `<ul><li>` nesting — use that as ground truth if it matches the content you need.
   - Otherwise, open Version History, find the revision that matches the content you're working from (check timestamps against when you started — the doc may have been edited between creation and your first read), use "Make a copy" on that revision to spin off a static copy, then call Drive's `download_file_content` with `exportMimeType: "text/html"` on that copy. This is Google Docs' own HTML export and encodes true list depth in the CSS class suffix `lst-kix_list_XX-N` on each `<ul>` (N = nesting level, 0-indexed) — parse that number directly, don't infer from whitespace. Trash the temporary copy afterward.
2. Parse with a real HTML parser (Python `html.parser.HTMLParser`), walking `<ul>`/`<li>` start/end tags and reading the depth off the `<ul class="lst-kix_list_..-N">` attribute on entry. Build a proper node tree (stack keyed by depth number), then render nested `<ul><li>` HTML with each child `<ul>` placed INSIDE its parent `<li>` before the closing `</li>` tag — a flat string-builder that closes `</li>` before opening the child `<ul>` produces sibling lists, not nested ones, which silently breaks the hierarchy even when the depth numbers were read correctly.
3. Paste the rebuilt HTML into the target doc via the clipboard (`osascript` `set the clipboard to «data HTML...»`, both `«class HTML»` and `«class utf8»` flavors — see [[ad-outlines]] skill for the full paste mechanics and gotchas).
4. Verify visually afterward — screenshot the pasted result and compare bullet levels (●/○/■ or indentation) against the source doc's version history view for at least one deeply-nested section, not just the top of the doc.

**Extra gotcha hit during this task:** `cmd+a` immediately after a `navigate` to a Google Doc can select the DOCUMENT TITLE field instead of the body if the click before it landed too high on the page or the page hadn't finished settling focus — the title bar shows highlighted/selected text and Delete does nothing to the body. Always click well into the body (not near the top edge), then screenshot to confirm the body text is actually highlighted blue before pressing Delete.

See also [[ad-outlines]] for the outlines-as-HTML clipboard-paste delivery mechanics (used the same way for editing, not just adding new content).
