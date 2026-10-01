DAN ROSE: 24-POST REVIEW BATCH
September 29, 2026

Status: Complete review batch. No scheduling or publishing authorized in this task.
Main review: index.html. Open it directly or serve this folder with Python's http.server.
Drive backup: https://drive.google.com/drive/folders/19en-2zvk9LWgeItK51A4pZeGzfP189Ih

DELIVERABLES
24 posts: three in each style 01-08.
18 single images and six five-slide carousels, totaling 48 sRGB JPEGs at 1080 x 1350.
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
The photo layer is taken from the original JPEG, with the existing cutout used only for alpha.
Style 01 retains the original studio background. Style 05 converts the original to grayscale.
Styles 02-04 use three generated environment plates, reused within each visual style.
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
Run build.py, outline.py, render.cjs, gallery.py and qa_contact.py in that order.
build.py needs access to the original photo library for changed photo sources.
Existing assets and self-contained SVGs are sufficient to re-export the delivered designs.
The raster exports are made from outlined SVGs because the default renderer substituted Impact.
Live-text SVGs remain editable. An editor may need to select the named fonts on another computer.

GENERATION
Built-in image_gen: three background-plate calls. No generated person pixels are used.
The tool does not expose a dollar cost. Reported cost: unavailable, not zero.
Exact prompts: generation-prompts.json. No alternate generation provider was used.

OWNER
This original-project task owns the final batch. A parallel task's files were isolated after a copy collision.
All 48 exports and this gallery were regenerated from this task's scripts afterward.
