DAN ROSE: 27-POST REVIEW BATCH
Revised October 2, 2026

Status: Complete review batch. No scheduling or publishing authorized in this task.
Main review: index.html. Open it directly or serve this folder with Python's http.server.
Drive backup: https://drive.google.com/drive/folders/19en-2zvk9LWgeItK51A4pZeGzfP189Ih

DELIVERABLES
27 posts: three in each style 01-09.
21 single images and six five-slide carousels, totaling 51 sRGB JPEGs at 1080 x 1350.
Image filenames are post ID plus two-digit slide number. A carousel is one post.
Captions: captions.txt and posts.json.
Editable layouts: templates/*.svg, with separate embedded photographs and live text.
Font-stable layouts: outlined/*.svg, with text converted to vector outlines for export.
Reusable cropped person layers and backgrounds: assets/.
Source photo filenames, SHA256 hashes and crop coordinates: source-map.json.
Proposed slot order: proposed-rotation.csv. No dates are assigned.
Blank post results: results-ledger.csv. Do not fill unavailable metrics with guesses.

PHOTOGRAPHY AND CROP NOTES
Every person layer is an existing shirtless source. No shirt removal or body generation.
The photo layer is taken from the finalized studio JPEG, with the existing cutout used only for alpha. S01-C has a localized cheek repair, limited to pixels (598,293)-(614,319) in its 1080x1350 photo layer. The rest of that photo is pixel-identical to the previous photo layer.
Style 01 retains the original studio background. Style 05 converts the original to grayscale.
Styles 02-04 use three generated environment plates, reused within each visual style. Style 09 uses three new topic-specific background plates inspired by the Jelly Beans cover.
No claim is made that Dan was photographed in those settings. Captions and images disclose the AI backgrounds.
S01-C, S06-C and S08-C use conservative waist-level crops. The bottom stops at the waistband, with no leg opening visible.
The other sources visibly wear real shorts or jeans. No seated or lying briefs photographs are used.
Full captured hair is retained. Text stays clear of face, hair and abs.

COPY GROUNDING
Source: Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md, section s4_maketime.
Verified personal facts used: Dan has a home gym and a gym membership; Dan uses a meal-prep service.
Other copy is practical planning advice, not an invented personal story or a promised result.
No numerical health outcomes, fabricated testimonials, free-preview funnel or keyword CTA.
The initial 01-08 references determine design direction; their generated people are not used.

TEST PLAN
Use the next available existing image-post slots after batch approval; keep existing queued content intact.
Mix all eight styles in each block of eight. Vary weekdays across a style's three attempts where slots allow.
Observe every post for seven days before comparing it. Educational content: saves/reach and shares/reach.
Photography: reach, profile visits and follows. Leave missing private metrics blank.
Only attribute product trials and paying customers when actual tracking supports it.
This is a directional creative test, not a controlled causal experiment.

REVIEW
Click an image to open the full-size viewer. Use previous/next or keyboard arrows.
Scroll sideways on carousel cards. Per-post status and notes are stored only in the current browser.
Use Download review notes to save them. This does not send them anywhere.

REBUILD
Requirements: Python with Pillow and fontTools; Node with sharp; macOS Arial, Arial Narrow, Arial Black and Impact.
Run revision2/apply-cheek-repair.py, build.py, outline.py, render.cjs, gallery.py, qa_contact.py and validate.py in that order.
build.py needs access to the original photo library for changed photo sources.
Existing assets and self-contained SVGs are sufficient to re-export the delivered designs.
The raster exports are made from outlined SVGs because the default renderer substituted Impact.
Live-text SVGs remain editable. An editor may need to select the named fonts on another computer.

GENERATION
Original batch: built-in image_gen, three background-plate calls.
Round 2: codex-image.sh on the Codex subscription, gpt-6.1-sol high, three background calls and one localized cheek repair. No face or physique redraw is used beyond the requested tiny blemish repair. Exact round-2 prompts: revision2/prompts/. Recorded usage: 92,568 Codex tokens across the four calls. No paid API was used.
The original built-in tool did not expose a dollar cost. Round 2 used the subscription allowance.
Original prompts: generation-prompts.json.

OWNER
This original-project task owns the final batch. A parallel task's files were isolated after a copy collision.
All 48 exports and this gallery were regenerated from this task's scripts afterward.

ROUND 2 CHANGES
S02-A and S03-B: titles and full captions exchanged; image exports unchanged.
S04-C: title and caption now explain martial arts conditioning plus weight training; image unchanged.
S05-A: same hands-behind-head pose in yellow shorts, source studio-blue-201.
S05-A/B/C: post title is the magazine masthead, with three short sidebar points.
S01-C: tiny dark cheek blemish removed; original source file retained.
S09-A/B/C: three additional portrait designs with real shirtless studio photos.
All 44 other original image exports remain byte-identical.
Current download: studio-posts-27-review-r2.zip. The old 24-post ZIP is retained as an archive.
Review server: com.absbyai.studio-posts-review LaunchAgent, loopback port 8791.
Nothing is scheduled or published. The three additions have no assigned test slots.
