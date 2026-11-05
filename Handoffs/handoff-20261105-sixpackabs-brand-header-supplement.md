# Supplement: apply the new SixPackAbs.com logo and black stripe sitewide

Written 2026-11-05 by the label session. **This supplements Dan's handoff for coding the shop and the new homepage. Read it alongside that handoff.** Where they differ on logo, header, colours or fonts, this one wins: Dan approved this look on 2026-11-05 ("Yes, apply it") after seeing the homepage mockup.

## What Dan approved

The mockup: https://claude.ai/artifact/JeDUY6MkwUxrXfgZHLFTKS (phone first, then desktop). It is the real current homepage with only the brand layer changed. Apply the same brand layer to **every page of sixpackabs.com and the shop**: the homepage, video pages, Shorts, the 165 legacy articles and 46 pages, product pages, cart and checkout. Every page wears the shared header and footer, so changing the theme's header and footer parts covers the whole site.

1. **Header: black stripe.** Background `#1C1A17` with a 2 px gold line under it (`#C9A766`) on every page, at every width.
2. **Logo.** The new gold horizontal logo on the left: the existing SixPackAbs.com abs-grid symbol plus SIXPACKABS.COM. Height 30 px on desktop and 22 px at phone width (760 px and below). It replaces `assets/img/sixpackabs-logo.webp` everywhere it appears: the header, the mobile menu panel and the footer.
3. **Menu and buttons.**
   - Menu links are gold `#C9A766`, weight 600; hover is white.
   - "Try the AI App" becomes a gold outline with gold text on a transparent background.
   - The hamburger lines are gold. The mobile menu panel is black with gold links.
   - **The red YouTube Subscribe button stays red** (Dan saw this and approved it).
4. **Font: Archivo everywhere**, replacing Manrope. Change `--spa-font` in `assets/css/site.css` and the `theme.json` font families.
   - Headings use Archivo at weight 800 to 900, letter-spacing -0.01em. Body text uses Archivo 400.
   - It is a variable font: weight 100 to 900, width 62% to 125%.
   - **Self-host it** in the theme (`assets/fonts/`), because the theme's fonts are same-origin. Do not load it from Google Fonts. Download the variable `Archivo[wdth,wght].ttf` from github.com/google/fonts (`ofl/archivo/`, OFL licence; keep `OFL.txt` beside it). A static SemiExpanded Bold copy is also in `sixpackabs/brand/logo/_build/fonts/`.
5. **Footer: black stripe too.** Background `#1C1A17`, gold links, body text `#D9D2C3`, gold logo.
6. **Gold only on dark backgrounds.** On white or light areas, links and accents stay dark (ink `#1C1A17`) or the existing link colour. Never light gold on white: it is too faint.
7. **Icons and sharing.**
   - Set the site icon / favicon to `sixpackabs/brand/logo/icons/favicon.ico` plus `sixpackabs-icon-32.png`, `-180.png` (Apple touch), `-192.png` and `-512.png`.
   - Use `sixpackabs/brand/logo/jpg/sixpackabs-og-1200x630.jpg` as the default Open Graph image wherever a page has no image of its own.

## Exact CSS from the approved mockup (theme classes, verified on the live markup)

```css
:root{--spa-gold:#C9A766;--spa-black:#1C1A17;--spa-font:"Archivo",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.spa-header{background:var(--spa-black);border-bottom:2px solid var(--spa-gold);box-shadow:none}
.spa-logo--header img{height:30px;width:auto}
@media (max-width:760px){.spa-logo--header img{height:22px}}
.spa-header .spa-nav a{color:var(--spa-gold);font-weight:600;font-stretch:112.5%}
.spa-header .spa-nav a:hover{color:#fff}
.spa-header .spa-header__app{color:var(--spa-gold);border-color:var(--spa-gold);background:transparent}
.spa-header .spa-burger span{background:var(--spa-gold)}
.spa-menu .spa-menu__panel{background:var(--spa-black)}
.spa-menu .spa-menu__nav a{color:var(--spa-gold)}
.spa-footer{background:var(--spa-black)}
.spa-footer, .spa-footer *{color:#D9D2C3}
.spa-footer a{color:var(--spa-gold)}
h1,h2,h3{font-weight:850;letter-spacing:-.01em}
```

Put this in the theme's own `assets/css/site.css`, not in a Customizer override. The mockup forced it with `!important`; the theme version should not need that. The logo image in `parts/header.html`, `parts/footer.html` and the menu markup points at the new file.

## Logo files (all built, in the repo)

`sixpackabs/brand/logo/`. `README.md` says which file to use where, and `logo-sheet.png` previews every version.
- Header and footer on black: `svg/sixpackabs-logo-horizontal-gold.svg` (inline it or copy it into `assets/img/`). There is a PNG fallback in `png-web/`.
- Light backgrounds (emails, white sections): `svg/sixpackabs-logo-horizontal-black.svg`.
- Square spots: `stacked` or `symbol` versions. Social avatar: `icons/sixpackabs-social-avatar-1080.png`.
- Colours: gold `#C9A766`, black `#1C1A17`, ivory `#F2ECDF`.

## Shop specifics

- Product images come **only** from `Contest/claude/labels-final-round1/mockups-web/` (or the `web front` / `web transparent` files in `Contest/approved/sixpackabs-labels-final-20261105/`). Never use `mockups/`, the flat label proofs, the print PDFs or the SVGs on a web page: their back panels contain Dan's home address. `Contest/` is local-only, so copy the needed web images into the theme or shop assets. Never commit `Contest/`.
- The label design is locked (`Contest/approved/LABELS-FINAL-LOCK-20261105.md`). Product names and the "what's in a serving" figures must match the labels.
- The shop design canvas from the website session already uses this logo and gold. Keep the header and footer identical between the content site and the shop, so it reads as one site.

## Deploy and verify (theme workflow in `sixpackabs/README.md`)

1. Build and check in the Playground preview (`preview_start` → `sixpackabs-playground`) at 390 px first, then 1440 px.
2. Run `sixpackabs/deploy.sh staging`, then `sixpackabs/url-check.sh https://<staging-host>`: every baseline URL returns 200.
3. Run `sixpackabs/deploy.sh prod`. Dan's "Yes, apply it" covers this look going live; the shop/homepage handoff's own go-live rules apply to anything else it ships.
4. Check live at 390 px and 1440 px:
   - the homepage, one video page, one legacy article, the mobile menu open, and the footer;
   - the header logo is crisp, the gold line shows, and nothing scrolls sideways;
   - Lighthouse or console shows no font or 404 errors.
5. Commit the theme changes with `scripts/git/safe-push.sh`. Never commit `Contest/` or `sixpackabs/brand/logo/homepage-mock/` (a scratch copy of the live page).

## Notes

- Untracked duplicates `theme/sixpackabs-child/assets/css/site 2.css` and `inc/head 2.php` are sync-conflict copies, not part of the theme. Leave them out of the deploy and the commit.
- The mockup files are in `sixpackabs/brand/logo/homepage-mock/`: `mock.html` (the live page plus the override CSS), `phone-full.png` and `desktop-full.png`. Use them as the visual target.
