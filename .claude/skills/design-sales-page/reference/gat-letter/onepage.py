"""Great Again T one-page order form (Healthy Back's layout), its thank-you page and the account page.

Used only by build_live.py. The order page carries BOTH flows in one template:
  classic   options, order summary, terms, "Continue To Secure Checkout" (hands off to Shopify checkout)
  one page  options, 1 shipping, 2 order summary, 3 payment (Stripe card fields), terms, "Complete My Order"
The body class `op` (set before first paint by the layout, from CFG['onePage'] and the address) picks which shows.
Card fields are Stripe Elements mounted by live/gat-pay.js; the server side is gat-checkout.js in the app repo.
"""

STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'),
          ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'),
          ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'),
          ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
          ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
          ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
          ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
          ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'),
          ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]


def inp(i, label, auto, half=False, req=True, typ='text', mode=None, ph=''):
    star = '<i>*</i>' if req else ''
    return (f'<label class="field{" half" if half else ""}" for="{i}"><span>{label}{star}</span>'
            f'<input id="{i}" name="{i}" type="{typ}" autocomplete="{auto}"' + (f' inputmode="{mode}"' if mode else '')
            + (f' placeholder="{ph}"' if ph else '') + (' required' if req else '') + '></label>')


def state_select(i, auto, half=True):
    opts = '<option value="">Select</option>' + ''.join(f'<option value="{c}">{n}</option>' for c, n in STATES)
    return (f'<label class="field{" half" if half else ""}" for="{i}"><span>State<i>*</i></span>'
            f'<select id="{i}" name="{i}" autocomplete="{auto}" required>{opts}</select></label>')


def card_field(i, label, half=False):
    return f'<div class="field{" half" if half else ""}" id="{i}-f"><span>{label}<i>*</i></span><div class="input stripe" id="{i}"></div></div>'


def helps(gen):
    mock = gen.checkout()
    return mock[mock.index('<section class="co-more">'):mock.index('<footer>')]   # the approved benefits and guarantee block, unchanged


def order_body(gen):
    A, LOCK, ARROW, S, L = gen.A, gen.LOCK, gen.ARROW, gen.SUPPORT, gen.LINKS
    choose = ('<div class="choose" role="radiogroup" aria-label="Choose your order">'
              '<label class="opt on"><input type="radio" name="gat-option" value="trial" checked><span class="radio"></span>'
              f'<img src="{A}bottle-transparent.png" alt="">'
              '<div><b>Free Month’s Supply</b><span>60 tablets. Just pay $9.99 shipping today</span><span class="then">Then $67 a month, cancel any time</span></div><em>$0.00</em></label>'
              '<label class="opt"><input type="radio" name="gat-option" value="single"><span class="radio"></span>'
              f'<img src="{A}bottle-transparent.png" alt="">'
              '<div><b>One bottle, one time</b><span>60 tablets. No monthly shipments</span></div><em>$97.00</em></label></div>')
    note = ('<p class="newonly trial-only">Your first bottle is free. You pay only $9.99 shipping today.</p>'
            '<p class="newonly single-only">One bottle, one time. $97 today with free shipping, and no monthly shipments.</p>')
    ship = ('<div class="op-only">' + gen.step(1, 'Shipping information') + '<div class="fields">'
            + inp('op-first', 'First name', 'given-name', half=True) + inp('op-last', 'Last name', 'family-name', half=True)
            + inp('op-email', 'Email', 'email', typ='email', mode='email') + inp('op-phone', 'Phone', 'tel', typ='tel', mode='tel')
            + '<label class="toggle"><input type="checkbox" id="op-sms"><span class="sw"></span><span>Text me order updates and exclusive offers</span></label>'
            + '<label class="field" for="op-country"><span>Country<i>*</i></span><select id="op-country" name="op-country" autocomplete="country"><option value="US" selected>United States</option></select></label>'
            + inp('op-addr1', 'Address', 'address-line1') + inp('op-addr2', 'Apt, suite, building', 'address-line2', req=False)
            + inp('op-city', 'City', 'address-level2') + state_select('op-state', 'address-level1')
            + inp('op-zip', 'ZIP code', 'postal-code', half=True, mode='numeric') + '</div>'
            + '<label class="check"><input type="checkbox" id="op-billdiff"><span class="box"></span><span>My billing address is different from my shipping address</span></label>'
            + '<div class="fields op-bill" id="op-bill" hidden>'
            + inp('op-b-addr1', 'Billing address', 'billing address-line1') + inp('op-b-addr2', 'Apt, suite, building', 'billing address-line2', req=False)
            + inp('op-b-city', 'City', 'billing address-level2') + state_select('op-b-state', 'billing address-level1')
            + inp('op-b-zip', 'ZIP code', 'billing postal-code', half=True, mode='numeric') + '</div></div>')
    summary = ('<table class="sum trial-only"><tr><td>Great Again T, free month’s supply</td><td>$0.00</td></tr>'
               '<tr><td>Subtotal</td><td>$0.00</td></tr><tr><td>Shipping and handling</td><td>$9.99</td></tr>'
               '<tr><td>Sales tax</td><td>$0.00</td></tr><tr class="tot"><td>Order total</td><td>$9.99</td></tr></table>'
               '<table class="sum single-only"><tr><td>Great Again T, one bottle</td><td>$97.00</td></tr>'
               '<tr><td>Subtotal</td><td>$97.00</td></tr><tr><td>Shipping and handling</td><td>$0.00</td></tr>'
               '<tr><td>Sales tax</td><td>$0.00</td></tr><tr class="tot"><td>Order total</td><td>$97.00</td></tr></table>')
    cards = ('<div class="cardlogos" aria-label="We accept Visa, Mastercard, American Express and Discover">'
             '<span>VISA</span><span>Mastercard</span><span>AMEX</span><span>DISCOVER</span></div>')
    pay = ('<div class="op-only">' + gen.step(3, 'Payment information') + f'<p class="secure-row">{LOCK}Secure checkout, 256-bit encryption</p>' + cards
           + '<div class="fields">' + inp('op-name', 'Name on card', 'cc-name') + card_field('op-card-number', 'Card number')
           + card_field('op-card-exp', 'Expiration', half=True) + card_field('op-card-cvc', 'CVV', half=True) + '</div></div>')
    terms = ('<div class="trial trial-only"><h3>How this FREE Trial Offer Works</h3>'
             '<p>With your order today, you will receive a full 60-count bottle of Great Again T at no cost… you just pay $9.99 shipping &amp; handling plus any applicable tax.</p>'
             '<p>You will automatically be enrolled in our Monthly Savings program and will have 30 days to try Great Again T. If you choose to continue after the first free bottle we will ship you a fresh bottle every 30 days (beginning 30 days from your initial order date). Any future bottles will be billed $67 plus tax per bottle, shipping included, until you decide to cancel.</p>'
             f'<p>You can pause, change the frequency or cancel your Monthly Savings subscription quickly and easily anytime by emailing {S}.</p></div>'
             '<label class="check agree trial-only"><input type="checkbox" id="agree"><span class="box"></span>'
             '<span>By checking this box, you are agreeing to the terms of the offer stated above.</span></label>'
             '<p class="co-err" id="co-err" role="alert" hidden></p>'
             f'<button type="button" class="cta cta-order classic-only" id="co-go">Continue To Secure Checkout{ARROW}<small>{LOCK}Secure 256-bit encryption</small></button>'
             '<p class="co-next classic-only">Next: enter your shipping address and payment details on our secure checkout page.</p>'
             f'<button type="submit" class="cta cta-order op-only" id="op-pay"><span id="op-pay-label">Complete My Order</span>{ARROW}<small>{LOCK}Secure 256-bit encryption</small></button>'
             f'<p class="policy-links"><a href="{L["terms"]}">Terms and Conditions</a><a href="{L["privacy"]}">Privacy Policy</a><a href="{L["shipping"]}">Shipping and Returns</a></p>'
             f'<p class="support"><b>Ask Questions By Email</b><br><a href="mailto:{S}">{S}</a></p>'
             f'<p class="legal trial-only">By requesting your free bottle today, you agree to our <a href="{L["terms"]}">terms and conditions</a>. Charge will appear as “SIXPACKABS.COM” on your credit card/bank statement.</p>'
             f'<p class="legal single-only">By placing your order today, you agree to our <a href="{L["terms"]}">terms and conditions</a>. Charge will appear as “SIXPACKABS.COM” on your credit card/bank statement.</p>'
             '<p class="fine">Important: Please read all supporting material before use.</p>'
             '<p class="fine">†These statements have not been evaluated by the Food and Drug Administration. Individual results may vary. '
             'This product is not intended to diagnose, treat, cure, or prevent any disease.</p>')
    steps_sum = ('<h2 class="step classic-only"><span>1</span>Order summary</h2><h2 class="step op-only"><span>2</span>Order summary</h2>')
    step_review = '<h2 class="step classic-only"><span>2</span>Review and continue</h2>'
    return (gen.header(False, checkout=True) + '<main class="co is-trial"><div class="co-grid">'
            '<div class="co-left">' + choose + note + '</div>'
            '<form class="co-right" id="op-form" novalidate>' + ship + steps_sum + summary + step_review + pay + terms
            + '</form></div></main>' + helps(gen) + gen.footer())


def thanks_body(gen):
    S, L = gen.SUPPORT, gen.LINKS
    return (gen.header(False, checkout=True) + '<main class="co ty is-trial" id="ty"><div class="ty-in">'
            '<p class="ty-wait" id="ty-wait" role="status">One moment. We are confirming your order.</p>'
            '<div id="ty-done" hidden><p class="ty-kicker">Order confirmed</p>'
            '<h1 id="ty-title">Thank you. Your order is confirmed.</h1>'
            '<p class="ty-num">Order number: <b id="ty-order"></b></p>'
            '<table class="sum trial-only"><tr><td>Great Again T, free month’s supply</td><td>$0.00</td></tr>'
            '<tr><td>Shipping and handling</td><td>$9.99</td></tr><tr class="tot"><td>Charged today</td><td>$9.99</td></tr></table>'
            '<table class="sum single-only"><tr><td>Great Again T, one bottle</td><td>$97.00</td></tr>'
            '<tr><td>Shipping and handling</td><td>$0.00</td></tr><tr class="tot"><td>Charged today</td><td>$97.00</td></tr></table>'
            '<div class="trial trial-only"><h3>What Happens Next</h3>'
            '<p>Your free bottle ships within 2 to 5 business days. We will email you a tracking link when it leaves.</p>'
            '<p>Your first $67 charge is on <b id="ty-first"></b>. We will email you a reminder at least 7 days before it. '
            'After that, a fresh bottle ships every 30 days at $67, shipping included, until you cancel.</p>'
            f'<p>You can cancel, skip a month or update your card at any time. Use the account page link in your confirmation email, or email {S}. '
            'If you cancel before your first $67 charge, you keep your free bottle and you are not billed again.</p></div>'
            '<div class="trial single-only"><h3>What Happens Next</h3>'
            '<p>Your bottle ships within 2 to 5 business days. We will email you a tracking link when it leaves.</p>'
            '<p>This is a one time order. There are no monthly shipments and you will not be charged again.</p></div>'
            '<p class="legal">A confirmation email is on its way to you. The charge appears on your statement as “SIXPACKABS.COM”.</p>'
            '<div id="gat-upsell" hidden></div></div>'
            '<div id="ty-miss" hidden><h1>We could not find that order</h1>'
            f'<p class="ty-p">If you just paid, your confirmation email is on its way and your order is safe. If you have a question, email <a href="mailto:{S}">{S}</a>.</p>'
            f'<p class="ty-p"><a href="{L["sales"]}">Back to Great Again T</a></p></div>'
            f'<p class="support"><b>Ask Questions By Email</b><br><a href="mailto:{S}">{S}</a></p>'
            '</div></main>' + helps(gen) + gen.footer())


def account_body(gen):
    S, L = gen.SUPPORT, gen.LINKS
    return (gen.header(False, checkout=True) + '<main class="co ty acct" id="ac"><div class="ty-in">'
            '<p class="ty-kicker">Your account</p><h1>Your Great Again T Monthly Delivery</h1>'
            '<p class="ty-wait" id="ac-wait" role="status">One moment. We are loading your details.</p>'
            '<div id="ac-on" hidden><p class="ty-p" id="ac-hello"></p>'
            '<table class="sum"><tr><td>Monthly delivery</td><td id="ac-status">Active</td></tr>'
            '<tr><td>Next bottle ships, and your card is charged</td><td id="ac-next"></td></tr>'
            '<tr><td>Amount</td><td>$67.00, shipping included</td></tr></table>'
            '<p class="co-ok" id="ac-ok" role="status" hidden></p>'
            '<button type="button" class="acct-btn" id="ac-skip">Skip My Next Month</button>'
            '<p class="acct-note" id="ac-skipnote"></p>'
            '<button type="button" class="acct-btn" id="ac-card">Update My Card</button>'
            '<button type="button" class="acct-btn quiet" id="ac-cancel">Cancel My Monthly Delivery</button>'
            '<div class="acct-confirm" id="ac-confirm" hidden><p><b>Cancel your monthly delivery?</b> You will not be charged again and no more bottles will ship. '
            'Any order that was already charged will still ship.</p>'
            '<button type="button" class="acct-btn stop" id="ac-yes">Yes, Cancel My Monthly Delivery</button>'
            '<button type="button" class="acct-btn" id="ac-no">Keep My Monthly Delivery</button></div></div>'
            '<div id="ac-off" hidden><div class="trial"><h3>Your Monthly Delivery Is Cancelled</h3>'
            '<p>You will not be charged again and no more bottles will ship. Any order that was already charged will still ship, '
            'and it is covered by our one year money back guarantee on unopened bottles.</p>'
            f'<p>Want to start again? Email {S} or <a href="{L["order"]}">place a new order</a>.</p></div></div>'
            '<div id="ac-single" hidden><div class="trial"><h3>One Time Order</h3>'
            '<p>Your order was a one time order. There are no monthly shipments and nothing to cancel.</p></div></div>'
            '<div id="ac-miss" hidden><div class="trial"><h3>This Link Did Not Work</h3>'
            f'<p>Please use the account page link in your order email. If you cannot find it, email {S} and we will help you right away.</p></div></div>'
            '<p class="co-err" id="ac-err" role="alert" hidden></p>'
            f'<p class="support"><b>Ask Questions By Email</b><br><a href="mailto:{S}">{S}</a></p>'
            '</div></main>' + gen.footer())


CSS = '''
/* ---------- one-page order form, thank-you and account pages (onepage.py) ---------- */
body:not(.op) .op-only,body.op .classic-only{display:none!important}
.field input,.field select{height:50px;width:100%;border:1px solid #d9c8a2;background:#fffaf0;border-radius:6px;padding:0 12px;color:var(--ink);font:inherit;font-size:16px;-webkit-appearance:none;appearance:none;margin:0}
.field select{padding-right:38px;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='none' stroke='%236b6f68' stroke-width='2'%3E%3Cpath d='M5 8l5 5 5-5'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;background-size:18px}
.field select:invalid,.field input::placeholder{color:#9b9a92}
.field input:focus,.field select:focus,.field .input.focus{outline:3px solid var(--gold);outline-offset:1px;border-color:var(--gold-d)}
.field .input.stripe{display:block;padding:15px 12px;color:var(--ink)}
.field.bad input,.field.bad select,.field.bad .input{border-color:#c23b2f;background:#fff6f4}
.field .ferr{color:#a8281c;font-size:13.5px;font-weight:600;line-height:1.35}
.toggle{cursor:pointer;position:relative}
.toggle input{position:absolute;opacity:0;width:1px;height:1px;margin:0}
.toggle .sw{transition:background .15s}
.toggle .sw::after{transition:transform .15s}
.toggle input:checked+.sw{background:var(--win)}
.toggle input:checked+.sw::after{transform:translateX(18px)}
.toggle input:focus-visible+.sw{outline:3px solid var(--gold);outline-offset:2px}
.op-bill{margin-top:14px}
.op-bill[hidden]{display:none}
#op-pay.busy{opacity:.75;cursor:wait}
#op-pay.busy .chev{display:none}
.op-test{background:#8f2f25;color:#fff;text-align:center;font-size:14px;font-weight:700;line-height:1.4;padding:9px 14px}
.op-test span{font-weight:500;white-space:nowrap}
.ty-in{max-width:660px;margin:0 auto;padding:28px 18px 44px}
.ty h1{font-size:27px;line-height:1.22;color:var(--ink);margin:4px 0 12px}
.ty-kicker{font-size:13px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:var(--gold-d)}
.ty-num{font-size:17px;margin-bottom:14px;color:var(--ink)}
.ty-p{font-size:17px;margin:10px 0}
.ty-wait{font-size:18px;font-weight:600;color:var(--ink);padding:26px 0}
.ty .legal{margin-top:18px}
.ty .trial a,.ty-p a{color:var(--ink);font-weight:600}
.ty .sum{margin-top:6px}
.co.is-trial .single-only,.co.is-single .trial-only{display:none}
.acct-btn{display:block;width:100%;min-height:54px;margin-top:14px;border:2px solid var(--green);border-radius:8px;background:var(--green);color:#fff;font:inherit;font-size:18px;font-weight:700;cursor:pointer;padding:10px 14px}
.acct-btn.quiet{background:#fff;color:var(--ink);border-color:#aeb5ae;font-weight:600}
.acct-btn.stop{background:#8f2f25;border-color:#8f2f25}
.acct-btn[disabled]{opacity:.6;cursor:wait}
.acct-btn:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
.acct-note{font-size:14.5px;color:var(--muted);margin-top:6px}
.acct-confirm{margin-top:16px;padding:16px;border:1px solid #ecc9c3;background:#fdf5f3;border-radius:8px;font-size:16px;line-height:1.5}
.acct-confirm[hidden]{display:none}
.co-ok{margin-top:14px;padding:12px 14px;border-radius:6px;background:#eef6ee;border:1px solid #c5dcc6;color:#274d31;font-weight:600;font-size:15px;line-height:1.45}
.co-ok[hidden]{display:none}
@media (min-width:768px){.ty h1{font-size:32px}.ty-in{padding-top:40px}}
'''
