# SixPackAbs.com logo kit

Built 2026-11-05 from the lockup on Dan's approved, locked supplement labels (`Contest/approved/LABELS-FINAL-LOCK-20261105.md`). Preview of every version: `logo-sheet.png`.

- **Symbol:** the existing SixPackAbs.com abs-grid shield with the swoosh, redrawn as clean vector art from `public/img/sixpackabs-icon-192.png`.
- **Wordmark:** SIXPACKABS.COM in Archivo SemiExpanded Bold (free font, OFL), letter-spaced +3.5%. All text is converted to shapes, so no font is needed to use the files.
- **Colours:** gold `#C9A766`, black `#1C1A17`, ivory `#F2ECDF`, white `#FFFFFF`.

## Which file to use

| Need | Use |
|---|---|
| Website header on a dark background | `svg/sixpackabs-logo-horizontal-gold.svg` (or `png-web/` version) |
| Website header on a light background | `svg/sixpackabs-logo-horizontal-black.svg` |
| Over a photo or video | `-white` (dark photos) or `-black` (light photos) |
| Print, packaging, a designer | `pdf/` or `svg/` (vector, any size) |
| Slides, documents, anywhere that wants a big image | `png/` (high resolution, transparent unless the name says `-on-`) |
| Email, simple web use where a background is fine | `jpg/` (small files, solid background) |
| Square spots (profile pictures, app tiles) | `stacked` or `symbol` |
| Favicon / browser tab | `icons/favicon.ico` + `icons/sixpackabs-icon-32.png`, `-180.png` (Apple touch), `-192.png`, `-512.png` |
| Instagram, TikTok, YouTube, Facebook profile picture | `icons/sixpackabs-social-avatar-1080.png` (safe inside a round crop) |
| Link preview image (Open Graph / Twitter card) | `jpg/sixpackabs-og-1200x630.jpg` |

**Layouts:** `horizontal` (symbol + name, the main logo), `stacked` (symbol above the name), `symbol` (icon only), `wordmark` (name only).
**Colours in file names:** `gold`, `black`, `white` = transparent background. `gold-on-black`, `black-on-white`, `black-on-ivory` = solid background.

## Rules

- Gold goes on black or dark backgrounds. On white or light backgrounds use black. Light gold on white is too faint to read.
- Leave clear space around the logo at least the height of the letters.
- Smallest size: horizontal logo 120 px wide on screen (1 in in print); symbol alone 16 px.
- Never stretch, recolour outside these colours, add effects, or set the name in another font.

## Rebuild

`python3 sixpackabs/brand/logo/_build/make_logo.py` regenerates every file from `_build/symbol-master.json` and `_build/fonts/`.
