#!/usr/bin/env python3
"""Builds the review page for the Great Again T one-page order form from the proof screenshots and the six order emails.

    python3 scripts/gat/build-review.py <review folder with the .jpg files and emails.json> <out.html>

The page is published as an Artifact. Phone first, then the account page, tablet, desktop, the emails, what was proven.
"""
import base64, html, json, pathlib, sys

src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
STATUS = json.loads((src / 'status.json').read_text()) if (src / 'status.json').exists() else {}


def img(name, alt):
    b = base64.b64encode((src / f'{name}.jpg').read_bytes()).decode()
    return f'<img src="data:image/jpeg;base64,{b}" alt="{html.escape(alt)}" loading="lazy">'


def shot(name, cap, alt, cls='phone'):
    return f'<figure class="shot {cls}"><div class="frame" tabindex="0">{img(name, alt)}</div><figcaption>{cap}</figcaption></figure>'


emails = json.loads((src / 'emails.json').read_text())
mail = ''.join(f'<details class="mail"{" open" if i == 0 else ""}><summary><span class="mlabel">{html.escape(e["label"])}</span>'
               f'<span class="msub">Subject: {html.escape(e["subject"])}</span></summary><div class="paper">{e["html"]}</div></details>' for i, e in enumerate(emails))

proof = STATUS.get('proof', [])
rows = ''.join(f'<tr><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>' for a, b in proof)
left = ''.join(f'<li>{x}</li>' for x in STATUS.get('left', []))
hosted = STATUS.get('hosted', '')

page = f'''<title>Great Again T One-Page Checkout</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap">
<style>
/* Layout: one reading column; screenshots sit in scroll frames sized like the device, phone first. Shop colours. */
:root {{ --bg:#fbf9f3; --panel:#ffffff; --ink:#172322; --body:#35403d; --muted:#5f6965; --line:#dfe3db; --gold:#8f7438; --green:#172322; --on-green:#f3ead3;
  --ok:#2f6a40; --warn:#8f2f25; --paper:#ffffff; --paper-ink:#1f2a27; --frame:#e9ece5; --font:Archivo,Arial,sans-serif }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#111a19; --panel:#18231f; --ink:#f1ecdd; --body:#d3d7cf; --muted:#9aa49d; --line:#2c3a35;
  --gold:#d2b473; --green:#0c1413; --on-green:#f3ead3; --ok:#8fc79d; --warn:#f0a195; --frame:#0c1413; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#111a19; --panel:#18231f; --ink:#f1ecdd; --body:#d3d7cf; --muted:#9aa49d; --line:#2c3a35;
  --gold:#d2b473; --green:#0c1413; --on-green:#f3ead3; --ok:#8fc79d; --warn:#f0a195; --frame:#0c1413; color-scheme:dark }}
* {{ box-sizing:border-box }}
body {{ background:var(--bg); color:var(--body); font-family:var(--font); font-size:17px; line-height:1.55 }}
.wrap {{ max-width:1180px; margin:0 auto; padding-block:26px 60px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)) }}
.col {{ max-width:720px }}
h1 {{ font-size:30px; line-height:1.18; color:var(--ink); margin:6px 0 10px; text-wrap:balance }}
h2 {{ font-size:22px; line-height:1.25; color:var(--ink); margin:44px 0 6px; text-wrap:balance }}
h3 {{ font-size:17px; color:var(--ink); margin:0 0 4px }}
p {{ margin:8px 0 }}
.kick {{ font-size:13px; font-weight:800; letter-spacing:.09em; text-transform:uppercase; color:var(--gold); margin:0 }}
.state {{ display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 4px; padding:0; list-style:none }}
.state li {{ font-size:14px; font-weight:700; padding:5px 11px; border-radius:99px; border:1px solid var(--line); background:var(--panel); color:var(--ink) }}
.state li.t {{ border-color:var(--warn); color:var(--warn) }}
.try {{ background:var(--green); color:var(--on-green); border-radius:10px; padding:20px; margin:22px 0 0 }}
.try h2 {{ color:var(--on-green); margin:0 0 8px; font-size:20px }}
.try a {{ color:var(--on-green); font-weight:700; word-break:break-all }}
.try ol {{ margin:10px 0 0; padding-left:22px }}
.try li {{ margin:6px 0 }}
.card {{ font-variant-numeric:tabular-nums; font-weight:700; user-select:all; background:rgba(255,255,255,.12); padding:2px 7px; border-radius:5px; white-space:nowrap }}
.note {{ font-size:15px; color:var(--muted) }}
.shots {{ display:flex; flex-wrap:wrap; gap:22px 20px; margin-top:16px; align-items:flex-start }}
.shot {{ margin:0; min-width:0 }}
.shot.phone {{ flex:0 1 300px }}
.shot.wide {{ flex:1 1 100% }}
.frame {{ border:1px solid var(--line); border-radius:12px; overflow:auto; max-height:640px; background:var(--frame) }}
.shot.wide .frame {{ max-height:760px }}
.frame:focus-visible, summary:focus-visible {{ outline:3px solid var(--gold); outline-offset:2px }}
.frame img {{ display:block; width:100%; height:auto }}
figcaption {{ font-size:14.5px; color:var(--muted); margin-top:8px; line-height:1.4 }}
figcaption b {{ color:var(--ink) }}
.mail {{ border:1px solid var(--line); border-radius:10px; background:var(--panel); margin-top:12px; overflow:hidden }}
.mail summary {{ cursor:pointer; padding:13px 16px; display:flex; flex-direction:column; gap:2px }}
.mlabel {{ font-weight:700; color:var(--ink) }}
.msub {{ font-size:14.5px; color:var(--muted) }}
.paper {{ background:var(--paper); color:var(--paper-ink); padding:18px 16px; border-top:1px solid var(--line) }}
.paper a {{ pointer-events:none }}
.tablewrap {{ overflow-x:auto; margin-top:12px }}
table {{ border-collapse:collapse; width:100%; font-size:15.5px; min-width:520px }}
td {{ padding:10px 12px 10px 0; border-bottom:1px solid var(--line); vertical-align:top }}
td:first-child {{ font-weight:700; color:var(--ink); width:38% }}
.left {{ padding-left:22px; margin:10px 0 }}
.left li {{ margin:9px 0 }}
code {{ font-size:.92em; background:var(--panel); border:1px solid var(--line); border-radius:4px; padding:1px 5px }}
@media (max-width:520px) {{ h1 {{ font-size:26px }} .shot.phone {{ flex-basis:100% }} }}
</style>
<div class="wrap">
<div class="col">
<p class="kick">Great Again T</p>
<h1>One-Page Checkout</h1>
<p>The buyer picks an option, types shipping and card details, ticks the terms box and pays, all on the order page. There is no second Shopify checkout step. It follows Healthy Back's order form: options, 1 Shipping, 2 Order summary, 3 Payment, the terms box, the tick box, one button.</p>
<ul class="state"><li class="t">Test mode: no real charges</li><li>Hidden from visitors</li><li>Two-step flow still live</li><li>Not reviewed yet</li></ul>
<div class="try"><h2>Try it on your phone</h2>
<p><a href="https://shop.sixpackabs.com/pages/great-again-t-order?onepage=1">shop.sixpackabs.com/pages/great-again-t-order?onepage=1</a></p>
<ol><li>Use the test card <span class="card">4242 4242 4242 4242</span>, any future date, any CVV. Nothing is charged.</li>
<li>To see a declined card, use <span class="card">4000 0000 0000 0002</span>, then fix it with the first card.</li>
<li>Use your own email to get the order email. It has the link to the account page (cancel, skip a month, update card).</li></ol>
<p class="note" style="color:var(--on-green);opacity:.85">{hosted}</p></div>
</div>

<h2>Phone</h2>
<p class="col note">Scroll inside each picture. These are from real test orders placed through the form in a phone-size browser.</p>
<div class="shots">
{shot('phone-form', '<b>The order form, filled in.</b> Options, shipping, order summary, card fields, terms box, tick box, one button.', 'The one-page order form on a phone')}
{shot('phone-declined', '<b>Declined card.</b> The bank&rsquo;s message shows above the button. The next try pays on the same order.', 'Declined card message on a phone')}
{shot('phone-thanks', '<b>Thank-you page, free month.</b> Order number, what was charged, the date of the first $67 charge.', 'Thank-you page for the free month')}
{shot('phone-thanks-single', '<b>Thank-you page, one bottle.</b>', 'Thank-you page for one bottle')}
</div>

<h2>Account page</h2>
<p class="col note">The link is in every order email. This is the &ldquo;account page&rdquo; the Questions, Terms and How It Works pages promise.</p>
<div class="shots">
{shot('phone-account-1', '<b>Monthly delivery.</b> Next charge date, skip, update card, cancel.', 'Account page')}
{shot('phone-account-2', '<b>After Skip My Next Month.</b> The next bottle and charge move 30 days.', 'Account page after skipping a month')}
{shot('phone-account-3', '<b>Cancel asks once.</b>', 'Account page cancel confirmation')}
{shot('phone-account-4', '<b>Cancelled.</b> A cancel email is sent too.', 'Account page after cancelling')}
</div>

<h2>Tablet</h2>
<div class="shots">{shot('tablet-form', '<b>One bottle chosen, 768 wide.</b>', 'The order form on a tablet', 'wide')}</div>

<h2>Desktop</h2>
<div class="shots">
{shot('desktop-form', '<b>Free month with a separate billing address, 1440 wide.</b> On a real screen the options column stays beside the form as you scroll.', 'The order form on a desktop', 'wide')}
{shot('desktop-thanks', '<b>Thank-you page.</b>', 'Thank-you page on a desktop', 'wide')}
</div>

<div class="col">
<h2>The six emails</h2>
<p class="note">Order emails only, sent to the buyer. Tap one to open it. The wording is mine and is yours to change.</p>
{mail}

<h2>What was proven in test mode</h2>
<div class="tablewrap"><table>{rows}</table></div>

<h2>What is left</h2>
<ol class="left">{left}</ol>
</div>
</div>
'''
out.write_text(page)
print('review page', out, len(page) // 1024, 'KB')
