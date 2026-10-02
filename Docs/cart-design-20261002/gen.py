# Cart Mockups FINAL (approved 2026-10-02: deep navy, yellow callout and yellow underline): builds the Design canvas boards (five cart designs, notes, extras, compare table).
# Usage: gen.py measure <dir>   -> plain pages for headless-Chrome height measuring
#        gen.py build <root> <live-canvas.json> -> <root>/project/*.dc.html + canvas.json (needs heights.json)
import re, json, sys, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get('ABS_REPO', os.getcwd())  # repo root; used only to find local copies of the images when measuring

IMG = {
    'logo': '/_blob/16c1606d8fac5520dbaf90def0e38b9b',
    'lock': '/_blob/af89bd0ca72f42ba28044caf640695cc',
    'workout': '/_blob/8b53ae5af7adf422fe4ab6af0cc51fb8',
    'head': '/_blob/45ec7610b4db87e50d8c7799f6362632',
    'danfull': '/_blob/7885411de78f4dcc70518559438f5e18',
}
LOCAL = {
    IMG['logo']: PROJ + '/public/img/logo.png',
    IMG['lock']: PROJ + '/public/img/letter/goal-lock-screen.jpg',
    IMG['workout']: PROJ + '/public/img/letter/app-workout-day.jpg',
    IMG['head']: PROJ + '/Media/research/cart-mockups-r2/dan-head.jpg',
    IMG['danfull']: PROJ + '/public/img/letter/dan-note.jpg',
}

TOK = {
    '@INK@': '#1b1a18', '@BG@': '#f6f5f2', '@CARD@': '#ffffff', '@LINE@': '#e4e1db', '@MUTE@': '#5f5c56',
    '@ACC@': '#2f5fe0', '@ACCSOFT@': '#f1f5fe', '@GREEN@': '#15803D', '@RED@': '#C9302D',
    '@FONT@': "'Manrope', sans-serif",
    '@LOGO@': IMG['logo'], '@LOCK@': IMG['lock'], '@WORKOUT@': IMG['workout'], '@HEAD@': IMG['head'], '@DANFULL@': IMG['danfull'],
}

ICON = {
    'check': '<polyline points="20 6 9 17 4 12"></polyline>',
    'shield': '<path d="M12 3l8 3v6c0 4.5-3.2 8.3-8 9-4.8-.7-8-4.5-8-9V6z"></path><polyline points="9 12 11.5 14.5 15.5 10"></polyline>',
    'lock': '<rect x="4" y="11" width="16" height="10" rx="2"></rect><path d="M8 11V7a4 4 0 0 1 8 0v4"></path>',
    'back': '<path d="M15 18l-6-6 6-6"></path>',
    'arrow': '<line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>',
    'clock': '<circle cx="12" cy="12" r="9"></circle><polyline points="12 7 12 12 15.5 14"></polyline>',
    'mail': '<rect x="3" y="5" width="18" height="14" rx="2"></rect><polyline points="3 7 12 13 21 7"></polyline>',
    'star': '<polygon points="12 3 14.8 8.9 21 9.7 16.5 14.1 17.6 20.5 12 17.5 6.4 20.5 7.5 14.1 3 9.7 9.2 8.9"></polygon>',
    'user': '<circle cx="12" cy="8" r="4"></circle><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"></path>',
    'slide': '<polyline points="9 6 3 12 9 18"></polyline><polyline points="15 6 21 12 15 18"></polyline>',
}


def ic(name, size=18, color='currentColor', sw=2.2):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round" aria-hidden="true" style="flex-shrink: 0">%s</svg>' % (size, size, color, sw, ICON[name]))


def tok(s):
    for k, v in TOK.items():
        s = s.replace(k, v)
    return s


def render(s, mode):
    def do_if(m):
        name, dflt, inner = m.group(1), m.group(2), m.group(3)
        if mode == 'build':
            return '<sc-if value="{{ %s }}" hint-placeholder-val="{{ %s }}">%s</sc-if>' % (name, dflt, inner)
        return inner if dflt == 'true' else ''
    s = re.sub(r'\[\[#if (\w+)\|(true|false)\]\](.*?)\[\[/if\]\]', do_if, s, flags=re.S)

    def do_hole(m):
        return '{{%s}}' % m.group(1) if mode == 'build' else m.group(2)
    return re.sub(r'\[\[(\w+)\|([^\]]*)\]\]', do_hole, s)


# ---------------------------------------------------------------- shared pieces

def eyebrow(t, color='@MUTE@'):
    return '<div style="font-size: 11.5px; font-weight: 800; letter-spacing: 0.7px; text-transform: uppercase; color: %s">%s</div>' % (color, t)


def h2(t, size=19, align='left'):
    return '<h2 style="margin: 0; font-size: %dpx; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2; text-align: %s">%s</h2>' % (size, align, t)


def chip(t, bg, color='#ffffff', pos='left: 8px; top: 8px'):
    return ('<span style="position: absolute; %s; font-size: 10.5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; '
            'padding: 4px 8px; border-radius: 999px; background: %s; color: %s">%s</span>' % (pos, bg, color, t))


def photo(src, alt, chips='', radius=14):
    return ('<div style="position: relative; border-radius: %dpx; overflow: hidden; background: #e9e6df">'
            '<img src="%s" alt="%s" style="display: block; width: 100%%; aspect-ratio: 3 / 4; object-fit: cover; object-position: top">%s</div>'
            % (radius, src, alt, chips))


def stat(label, value, color='@INK@'):
    return ('<div style="display: flex; flex-direction: column; gap: 1px"><span style="font-size: 12px; font-weight: 600; color: @MUTE@">%s</span>'
            '<span style="font-size: 17px; font-weight: 800; letter-spacing: -0.2px; color: %s">%s</span></div>' % (label, color, value))




def ph(label, sub='', minh=0):
    """A clearly marked empty slot."""
    sub_html = '<div style="font-size: 12px; font-weight: 600; color: @MUTE@">%s</div>' % sub if sub else ''
    mh = ' min-height: %dpx;' % minh if minh else ''
    return ('<div style="border: 1.5px dashed #a8a297; border-radius: 12px; background: #efece6; padding: 14px;%s display: flex; flex-direction: column; '
            'gap: 4px; justify-content: center"><div style="font-size: 13.5px; font-weight: 700; color: #45423d">%s</div>%s</div>' % (mh, label, sub_html))


def ph_quote(extra='Member name, verified member since 2026'):
    return ('<div style="border: 1.5px dashed #a8a297; border-radius: 12px; background: #efece6; padding: 14px; display: flex; gap: 12px; align-items: center">'
            '<div style="width: 44px; height: 44px; border-radius: 50%; border: 1.5px dashed #a8a297; display: flex; align-items: center; justify-content: center; color: #6e6b64; flex: none">'
            + ic('user', 20) + '</div><div style="display: flex; flex-direction: column; gap: 3px; min-width: 0">'
            '<div style="font-size: 13.5px; font-weight: 700; color: #45423d">Member quote goes here</div>'
            '<div style="font-size: 12px; font-weight: 600; color: @MUTE@">' + extra + '</div></div></div>')


def checks(items, size=14.5, color='#1e9e5a', gap=9):
    rows = ''.join('<li style="display: flex; gap: 10px; align-items: flex-start; font-size: %spx; line-height: 1.4; font-weight: 600">%s<span>%s</span></li>'
                   % (size, ic('check', 18, color, 3), t) for t in items)
    return '<ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: %dpx">%s</ul>' % (gap, rows)


def buy(label, sub='', attrs='', bg='@GREEN@', h=58, size=18):
    sub_html = '<span style="font-size: 11.5px; font-weight: 700; letter-spacing: 0.6px; opacity: 0.92">%s</span>' % sub if sub else ''
    return ('<button type="button" %s style="width: 100%%; min-height: %dpx; border: none; border-radius: 12px; background: %s; color: #ffffff; font-family: inherit; '
            'font-size: %dpx; font-weight: 800; letter-spacing: -0.2px; cursor: pointer; display: flex; flex-direction: column; align-items: center; justify-content: center; '
            'gap: 2px; padding: 8px 14px; box-shadow: 0 8px 22px rgba(21,128,61,0.28)"><span>%s</span>%s</button>' % (attrs, h, bg, size, label, sub_html))


def apple_pay(h=54):
    return ('<button type="button" style="width: 100%%; min-height: %dpx; border: none; border-radius: 12px; background: #000000; color: #ffffff; font-family: inherit; '
            'font-size: 18px; font-weight: 700; cursor: pointer">Apple Pay</button>' % h)



def tick(label, id_):
    return ('<label for="%s" style="display: flex; gap: 12px; align-items: flex-start; font-size: 14px; font-weight: 700; line-height: 1.4; cursor: pointer">'
            '<input type="checkbox" id="%s" style="width: 26px; height: 26px; margin: 0; flex: none; accent-color: #15803D"><span>%s</span></label>' % (id_, id_, label))


def radio_dot(bd, dot):
    return ('<span style="width: 22px; height: 22px; border-radius: 50%%; border: 2px solid %s; box-sizing: border-box; display: flex; align-items: center; '
            'justify-content: center; flex: none; background: #ffffff"><span style="width: 10px; height: 10px; border-radius: 50%%; background: %s"></span></span>' % (bd, dot))


def badge(t, bg='@RED@', color='#ffffff'):
    return ('<span style="align-self: flex-start; font-size: 10.5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; padding: 3px 8px; '
            'border-radius: 999px; background: %s; color: %s">%s</span>' % (bg, color, t))


SEL_JS = '''
    const on = '#2f5fe0', off = '#d9d5cd';
    const sel = (yes) => ({ bd: yes ? on : off, bg: yes ? '#f1f5fe' : '#ffffff', dot: yes ? on : 'transparent' });
'''



# ================================================================ ROUND 3: Design B (Healthy Back Institute structure), revised
# Dan picked B. Content changes (2026-10-02): no "Questions?" line at the top; new top-box copy; no benefits box on
# the phone (desktop keeps it); no card-brand chips; a Pay with Link button; no member comments, expert slot or
# founder quote; the founder photo at the bottom is the upper-body picture from the sales page.
# Then three looks that keep the structure and content but use the /start sales-page branding.

K = '#05070B'       # sales-page ink
PAPER = '#F6F4F0'
HAIR = '#E4E1DB'
BODY = '#1D2127'
SOFT = '#3F444C'
R = '#C9302D'
G = '#15803D'

HEAD_1 = 'See yourself with abs, then get an AI fitness plan to make it real.'
HEAD_2 = 'Claim your free 7-day trial today!'
NOTICE = 'This special, one time offer is only available to new Abs By AI members.'
BENEFITS = ['An AI picture of yourself with the exact body and abs you want',
            'A personalized AI workout plan built from your photo',
            'AI calorie tracking: snap a picture of your food',
            'Meal prep recipes built around the foods you like',
            'AI sleep coaching that works with Oura, Whoop and Apple Watch',
            'Unlimited goal pictures and Supplement Audits']
BIO = ('Dan Rose is the founder of Abs By AI. His first channel, SixPackAbs.com, was one of the most viewed fitness channels in the history of YouTube. '
       'He built Abs By AI after using AI to get six pack abs at 40.')
TERMS = ['With your order today, you get the full Abs By AI membership free for 7 days. You pay $0 today.',
         'You will automatically be enrolled as a monthly member and will have 7 days to try everything. If you love it, do nothing and you stay a member at the Members Only price of $19.99 a month. Your card is billed $19.99 on day 7 and every month after that until you decide to cancel.',
         'You can cancel quickly and easily anytime in two taps (Manage membership, then Cancel) or by emailing dan@absbyai.com. Cancel before day 7 and you pay nothing.']
TICK = 'By checking this box, you are agreeing to the terms of the offer stated above.'


def phone(key, alt, w):
    return ('<img src="%s" alt="%s" style="display: block; width: %dpx; aspect-ratio: 621 / 1302; border-radius: 14.5%% / 6.9%%; flex: none">' % (key, alt, w))


def link_btn(h=54, bd=K):
    return ('<button type="button" style="width: 100%%; min-height: %dpx; border: 2px solid %s; border-radius: 12px; background: #ffffff; color: %s; font-family: inherit; '
            'font-size: 17px; font-weight: 800; cursor: pointer">Pay with Link</button>' % (h, bd, bd))


def hl(t, dark=False):
    return '<span style="box-shadow: inset 0 -9px 0 rgba(201,48,45,%s)">%s</span>' % ('0.6' if dark else '0.22', t)


def title_head(dark=False):
    return 'See Yourself With Abs, Then Get An AI Fitness Plan To ' + hl('Make It Real.', dark)


def free_tag():
    return ('<span style="position: absolute; right: -12px; top: -6px; background: ' + R + '; color: #ffffff; font-size: 11px; font-weight: 800; line-height: 1.1; '
            'padding: 6px 8px; border-radius: 4px; text-align: center">FREE<br>7 days</span>')


# ---------------------------------------------------------------- B0: the original look, revised

def b0_parts():
    P = {}
    P['header'] = '''<div style="display: flex; flex-wrap: wrap; gap: 10px 20px; align-items: center; justify-content: space-between; padding: 16px 0 0">
<img src="@LOGO@" alt="Abs By AI" style="height: 30px; width: auto; display: block">
<div style="display: flex; align-items: center; gap: 8px">''' + ic('lock', 22, '#2f5fe0') + '''<div style="display: flex; flex-direction: column; line-height: 1.15"><span style="font-size: 14px; font-weight: 800; letter-spacing: 0.4px">SECURE CHECKOUT</span><span style="font-size: 11.5px; font-weight: 700; color: @ACC@">256-BIT ENCRYPTION</span></div></div>
</div>'''
    P['banner'] = '''<div style="background: #ebe8e2; border-radius: 6px; padding: 14px 16px; display: flex; gap: 20px; align-items: center">
<div style="position: relative; width: 74px; flex: none">
''' + phone('@WORKOUT@', 'App screenshot: the AI workout plan', 74) + free_tag() + '''
</div>
<h1 style="margin: 0; flex: 1; font-size: 18px; font-weight: 800; letter-spacing: -0.3px; line-height: 1.3; text-align: center">''' + HEAD_1 + '''<br>''' + HEAD_2 + '''</h1>
</div>'''
    P['yellow'] = '<div style="background: #FFEB3B; padding: 16px 14px; text-align: center; font-size: 15px; font-weight: 800; line-height: 1.3">' + NOTICE + '</div>'
    P['benefits'] = '''<div style="background: #ebe8e2; padding: 16px; display: flex; flex-direction: column; gap: 12px">
<div style="font-size: 20px; font-weight: 700; line-height: 1.25">How Abs By AI gets you to your goal:</div>
''' + checks(BENEFITS, 15, '#2f5fe0', 11) + '''
</div>'''

    def step(n, t):
        return ('<div style="position: relative; background: @ACC@; color: #ffffff; height: 52px; display: flex; align-items: center; justify-content: center; margin-top: 6px">'
                '<span style="position: absolute; left: 8px; top: -6px; width: 60px; height: 60px; border-radius: 50%%; background: #24479f; border: 3px solid #ffffff; box-sizing: border-box; '
                'display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 800">%d</span>'
                '<span style="font-size: 22px; font-weight: 800; letter-spacing: -0.2px; padding-left: 40px">%s</span></div>' % (n, t))

    def field(label, id_, ph_='', typ='text'):
        return ('<div style="display: flex; flex-direction: column; gap: 5px; flex: 1; min-width: 0"><label for="%s" style="font-size: 13px; font-weight: 600">%s <span style="color: @RED@">*</span></label>'
                '<input type="%s" id="%s" placeholder="%s" style="width: 100%%; height: 46px; box-sizing: border-box; border: 2px solid #e6d9b4; border-radius: 5px; background: #fffaf0; padding: 0 12px; '
                'font-family: inherit; font-size: 16px; color: @INK@"></div>' % (id_, label, typ, id_, ph_))

    def sumrow(l, r, strong=False):
        return ('<div style="display: flex; justify-content: space-between; font-size: %spx; font-weight: %d"><span>%s</span><span>%s</span></div>'
                % (19 if strong else 15, 800 if strong else 700, l, r))

    P['step1'] = lambda pre: step(1, 'Your Email') + '''
<div style="display: flex; flex-direction: column; gap: 8px">
''' + field('Email', pre + 'email', '', 'email') + '''
<div style="font-size: 13px; color: @MUTE@">Your email becomes your login. No password needed today.</div>
</div>'''
    P['step2'] = step(2, 'Order Summary') + '''
<div style="display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; align-items: baseline; gap: 12px; font-size: 15px; padding-bottom: 14px; border-bottom: 1px solid #cfcac0">
<span style="flex: 1; font-weight: 600">Abs By AI Membership, Free 7-Day Trial</span>
<s style="color: @MUTE@">$19.99</s>
<span style="font-weight: 800">FREE!</span>
</div>
''' + sumrow('Subtotal', '$0.00') + sumrow('Sales Tax', '$0.00') + '''
<div style="border-top: 1px solid #cfcac0; padding-top: 12px">''' + sumrow('Order Total', '$0.00', True) + '''</div>
</div>'''
    P['step3'] = lambda pre: step(3, 'Payment Information') + '''
<div style="display: flex; flex-direction: column; gap: 14px">
''' + apple_pay(50) + link_btn(50, '#1b1a18') + '''
<div style="text-align: center; font-size: 13px; font-weight: 700; color: @MUTE@">or pay by card</div>
''' + field('Name on Card', pre + 'name') + field('Credit Card Number', pre + 'card', 'Credit Card #') + '''
<div style="display: flex; gap: 14px">''' + field('Expiration', pre + 'exp', 'MM / YY') + field('CVV', pre + 'cvv', 'CVV') + '''</div>
</div>'''
    P['terms'] = lambda pre: '''<div style="display: flex; flex-direction: column; gap: 14px; padding-top: 6px">
<h2 style="margin: 0; font-size: 17px; font-weight: 800; text-align: center">How this FREE Trial Offer Works</h2>
''' + ''.join('<p style="margin: 0; font-size: 15px; line-height: 1.55">%s</p>' % t for t in TERMS) + '''
''' + tick(TICK, pre + 'agree') + '''
''' + buy('START MY FREE TRIAL', 'SECURE 256-BIT ENCRYPTION', '', '@GREEN@', 84, 27) + '''
<div style="display: flex; flex-direction: column; gap: 10px; text-align: center; padding-top: 4px">
<div style="font-size: 15px; font-weight: 800">Questions Before You Order?</div>
<div style="font-size: 15px"><a href="mailto:dan@absbyai.com">dan@absbyai.com</a></div>
<div style="font-size: 12.5px; font-weight: 700; line-height: 1.45">Your purchase will appear on your statement under the name: [STATEMENT NAME]</div>
<div style="font-size: 12.5px; font-weight: 700; line-height: 1.45">Goal pictures are AI visualizations, not real results. Individual results vary.</div>
</div>
</div>'''
    P['guarantee'] = '''<div style="border: 2px solid #e6d9b4; background: #fffaf0; border-radius: 6px; padding: 16px; display: flex; flex-direction: column; gap: 12px">
<div style="display: flex; gap: 14px; align-items: center">
<div style="width: 76px; height: 76px; border-radius: 50%; background: @GREEN@; color: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: none; border: 3px double #ffffff; outline: 2px solid @GREEN@; line-height: 1"><span style="font-size: 28px; font-weight: 800">90</span><span style="font-size: 11px; font-weight: 800; letter-spacing: 1px">DAY</span></div>
<div style="font-size: 17px; font-weight: 800; line-height: 1.3; text-align: center; flex: 1">90-Day No Risk<br>100% Money Back Guarantee</div>
</div>
<div style="font-size: 13px; line-height: 1.5; text-align: center">We guarantee you'll love Abs By AI or we'll refund your money.</div>
<div style="font-size: 13px; line-height: 1.5; text-align: center">If you're not happy for any reason, email us within 90 days of your first payment for a full refund. No questions asked.</div>
</div>'''
    P['bio'] = '''<div style="display: flex; gap: 16px; align-items: flex-start">
<img src="@DANFULL@" alt="Dan Rose, founder of Abs By AI" style="width: 112px; height: 145px; object-fit: cover; object-position: center top; border: 2px solid #ffffff; flex: none">
<div style="font-size: 14px; line-height: 1.55; color: #ffffff">''' + BIO + '''</div>
</div>'''
    P['footer'] = '''<div style="display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: space-between; font-size: 13px; color: #45423d">
<span>Copyright &copy; 2026 Abs By AI</span>
<span><a href="#top">Terms of Service</a> &nbsp; <a href="#top">Privacy Policy</a></span>
</div>'''
    return P


STATIC = 'class Component extends DCLogic {\n  renderVals() { return {}; }\n}'


def b0_phone():
    P = b0_parts()
    body = '''<div id="top" style="background: #ffffff; padding: 0 16px 22px; display: flex; flex-direction: column; gap: 18px">
''' + P['header'] + P['banner'] + P['yellow'] + P['step1']('b0p-') + P['step2'] + P['step3']('b0p-') + P['terms']('b0p-') + P['guarantee'] + '''
</div>
<div style="background: @ACC@; padding: 16px">''' + P['bio'] + '''</div>
<div style="background: #ebe8e2; padding: 18px 16px 22px; flex-grow: 1">''' + P['footer'] + '''</div>'''
    return body, STATIC


def b0_desktop():
    P = b0_parts()
    banner = P['banner'].replace('font-size: 18px', 'font-size: 27px').replace('padding: 14px 16px', 'padding: 20px 28px').replace('width: 74px', 'width: 86px')
    body = '''<div id="top" style="max-width: 976px; margin: 0 auto; padding: 0 24px 40px; box-sizing: border-box; display: flex; flex-direction: column; gap: 22px">
''' + P['header'] + banner + '''
<div style="display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start">
<div style="flex: 999 1 460px; min-width: 0; display: flex; flex-direction: column; gap: 18px">
''' + P['yellow'] + P['step1']('b0d-') + P['step2'] + P['step3']('b0d-') + P['terms']('b0d-') + '''
</div>
<div style="flex: 1 1 340px; min-width: 0; display: flex; flex-direction: column; gap: 22px">
''' + P['benefits'] + P['guarantee'] + '''
</div>
</div>
</div>
<div style="background: @ACC@"><div style="max-width: 976px; margin: 0 auto; padding: 16px 24px; box-sizing: border-box">''' + P['bio'] + '''</div></div>
<div style="background: #ebe8e2"><div style="max-width: 976px; margin: 0 auto; padding: 22px 24px 30px; box-sizing: border-box">''' + P['footer'] + '''</div></div>'''
    return body, STATIC


# ---------------------------------------------------------------- shared brand pieces (sales-page look)

def stripe(D):
    pad = '0 40px' if D else '0 16px'
    inner = 'max-width: 1040px; margin: 0 auto; ' if D else ''
    return ('<div id="top" style="background: ' + K + '; color: #ffffff; height: ' + ('64' if D else '60') + 'px; padding: ' + pad + '; display: flex; flex-shrink: 0">'
            '<div style="' + inner + 'display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%">'
            '<img src="@LOGO@" alt="Abs By AI" style="height: ' + ('34' if D else '26') + 'px; width: auto; display: block; filter: invert(1)">'
            '<div style="display: flex; align-items: center; gap: 8px">' + ic('lock', 18, '#ffffff') +
            '<div style="font-size: 13px; font-weight: 800; line-height: 1.25; text-align: right">Secure checkout<br><span style="font-weight: 600; color: #C9CDD3">256-bit encryption</span></div></div>'
            '</div></div>')


def bfield(label, id_, ph_='', typ='text', bg='#ffffff', bd='#C9CDD3'):
    return ('<div style="display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 0"><label for="%s" style="font-size: 13px; font-weight: 700; color: #2B2F36">%s <span style="color: %s">*</span></label>'
            '<input type="%s" id="%s" placeholder="%s" style="width: 100%%; height: 52px; box-sizing: border-box; border: 1.5px solid %s; border-radius: 12px; background: %s; padding: 0 14px; '
            'font-family: inherit; font-size: 16px; color: %s"></div>' % (id_, label, R, typ, id_, ph_, bd, bg, K))


def email_block(pre, **kw):
    return ('<div style="display: flex; flex-direction: column; gap: 8px">' + bfield('Email', pre + 'email', '', 'email', **kw) +
            '<div style="font-size: 13px; line-height: 1.45; color: ' + SOFT + '">Your email becomes your login. No password needed today.</div></div>')


def bsum(thumb=False, rule=HAIR):
    def row(l, r, strong=False):
        return ('<div style="display: flex; justify-content: space-between; font-size: %spx; font-weight: %d; color: %s"><span>%s</span><span>%s</span></div>'
                % (20 if strong else 15, 800 if strong else 700, K if strong else '#2B2F36', l, r))
    th = phone('@WORKOUT@', 'App screenshot: the AI workout plan', 40) if thumb else ''
    return ('<div style="display: flex; flex-direction: column; gap: 12px">'
            '<div style="display: flex; align-items: center; gap: 12px; font-size: 15px; padding-bottom: 14px; border-bottom: 1px solid ' + rule + '">' + th +
            '<span style="flex: 1; font-weight: 700; line-height: 1.35">Abs By AI Membership, Free 7-Day Trial</span>'
            '<s style="color: ' + SOFT + '">$19.99</s><span style="font-weight: 800; color: ' + R + '">FREE!</span></div>' +
            row('Subtotal', '$0.00') + row('Sales Tax', '$0.00') +
            '<div style="border-top: 1px solid ' + rule + '; padding-top: 12px">' + row('Order Total', '$0.00', True) + '</div></div>')


def bpay(pre, **kw):
    return ('<div style="display: flex; flex-direction: column; gap: 12px">' + apple_pay(54) + link_btn(54) +
            '<div style="display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; color: ' + SOFT + '"><span style="flex: 1; height: 1px; background: ' + HAIR + '"></span>'
            '<span>or pay by card</span><span style="flex: 1; height: 1px; background: ' + HAIR + '"></span></div>' +
            bfield('Name on Card', pre + 'name', **kw) + bfield('Credit Card Number', pre + 'card', 'Credit Card #', **kw) +
            '<div style="display: flex; gap: 12px">' + bfield('Expiration', pre + 'exp', 'MM / YY', **kw) + bfield('CVV', pre + 'cvv', 'CVV', **kw) + '</div></div>')


def bterms_text(size=15):
    return ''.join('<p style="margin: 0; font-size: %spx; line-height: 1.55; color: %s">%s</p>' % (size, BODY, t) for t in TERMS)


def bcta(label='Start My Free Trial'):
    return ('<button type="button" style="width: 100%; min-height: 58px; padding: 0 18px; border: 0; border-radius: 12px; background: ' + G + '; color: #ffffff; font-family: inherit; '
            'font-size: 18px; font-weight: 800; cursor: pointer; box-shadow: 0 8px 18px rgba(5,7,11,0.16)">' + label + '</button>'
            '<div style="display: flex; align-items: center; justify-content: center; gap: 6px; font-size: 12px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; color: ' + SOFT + '">'
            + ic('lock', 14, SOFT, 2.4) + '<span>Secure 256-bit encryption</span></div>')


def bcontact(color=K, soft=SOFT):
    return ('<div style="display: flex; flex-direction: column; gap: 8px; text-align: center">'
            '<div style="font-size: 16px; font-weight: 800; color: ' + color + '">Questions Before You Order?</div>'
            '<div style="font-size: 15px; font-weight: 700"><a href="mailto:dan@absbyai.com">dan@absbyai.com</a></div>'
            '<div style="font-size: 13px; line-height: 1.5; color: ' + soft + '">Your purchase will appear on your statement under the name: [STATEMENT NAME]</div>'
            '<div style="font-size: 13px; line-height: 1.5; color: ' + soft + '">Goal pictures are AI visualizations, not real results. Individual results vary.</div></div>')


def bguarantee(card):
    return ('<div style="' + card + ' display: flex; flex-direction: column; gap: 12px">'
            '<div style="display: flex; gap: 14px; align-items: center">'
            '<div style="width: 72px; height: 72px; border-radius: 50%; background: ' + K + '; color: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: none; line-height: 1; '
            'box-shadow: 0 0 0 3px #ffffff, 0 0 0 5px ' + K + '"><span style="font-size: 26px; font-weight: 800">90</span><span style="font-size: 10.5px; font-weight: 800; letter-spacing: 1px">DAY</span></div>'
            '<div style="font-size: 18px; font-weight: 800; line-height: 1.3; flex: 1">90-Day No Risk<br>100% Money Back Guarantee</div></div>'
            '<p style="margin: 0; font-size: 14.5px; line-height: 1.55; color: ' + SOFT + '">We guarantee you\'ll love Abs By AI or we\'ll refund your money.</p>'
            '<p style="margin: 0; font-size: 14.5px; line-height: 1.55; color: ' + SOFT + '">If you\'re not happy for any reason, email us within 90 days of your first payment for a full refund. No questions asked.</p></div>')


def bbenefits(card, check=R):
    return ('<div style="' + card + ' display: flex; flex-direction: column; gap: 14px">'
            '<div style="font-size: 20px; font-weight: 800; line-height: 1.3">How Abs By AI gets you to your goal:</div>' + checks(BENEFITS, 15, check, 11) + '</div>')


def bfounder(text_color, sub_color, name_color):
    return ('<div style="display: flex; gap: 16px; align-items: flex-start">'
            '<img src="@DANFULL@" alt="Dan Rose, founder of Abs By AI" style="width: 126px; height: 147px; border-radius: 14px; object-fit: cover; object-position: center top; flex: none">'
            '<div style="display: flex; flex-direction: column; gap: 8px; min-width: 0"><div style="display: flex; flex-direction: column; gap: 1px"><span style="font-size: 17px; font-weight: 800; color: ' + name_color + '">Dan Rose</span>'
            '<span style="font-size: 13px; font-weight: 600; color: ' + sub_color + '">Founder, Abs By AI</span></div>'
            '<div style="font-size: 14.5px; line-height: 1.55; color: ' + text_color + '">' + BIO + '</div></div></div>')


def bfooter(D, top_rule=False):
    rule = 'border-top: 1px solid #2A2F38; ' if top_rule else ''
    inner = 'max-width: 1040px; margin: 0 auto; ' if D else ''
    return ('<div class="foot" style="' + rule + 'background: ' + K + '; color: #A9AEB6; font-size: 12px; line-height: 1.6; padding: ' + ('28px 40px 32px' if D else '24px 20px 28px') + '; flex-grow: 1">'
            '<div style="' + inner + 'display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: space-between">'
            '<span>Copyright &copy; 2026 Abs By AI</span><span><a href="#top" style="color: #D5D8DD">Terms of Service</a> &nbsp; <a href="#top" style="color: #D5D8DD">Privacy Policy</a></span></div></div>')


def terms_head(size=20, align='center'):
    return '<h2 style="margin: 0; font-size: %dpx; font-weight: 800; letter-spacing: -0.01em; line-height: 1.25; text-align: %s">How This Free Trial Offer Works</h2>' % (size, align)


def cols(left, right):
    return ('<div style="display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start">'
            '<div style="flex: 999 1 480px; min-width: 0; display: flex; flex-direction: column; gap: 20px">' + left + '</div>'
            '<div style="flex: 1 1 340px; min-width: 0; display: flex; flex-direction: column; gap: 20px">' + right + '</div></div>')



# ================================================================ ROUND 4: B1 (Brand bars) in three blues
# Dan, 2026-10-02: likes B1 but not the black. Stripe, step headers and the Apple Pay button go blue, in three shades
# (Healthy Back Institute's blue, a deeper navy, one of my choice). The New Members Only outline and label and the
# underline under "Make It Real" take the same blue. Guarantee is 365 days. The Annual option is back: picking it
# makes the order a one-time charge (no subscription), so the free-trial copy and the tick box disappear and his
# sentence appears: "One-time charge of $69.99 for lifetime access. No recurring billing."

THEMES = [
    dict(key='HBIBlue', label='Blue 1 · Healthy Back blue', main='#2C75C8', rgb='44,117,200', tint='#EEF5FC'),
    dict(key='Navy', label='Blue 2 · Deep navy', main='#12306B', rgb='18,48,107', tint='#EEF1F8'),
    dict(key='AppBlue', label='Blue 3 · Abs By AI app blue', main='#2F5FE0', rgb='47,95,224', tint='#EFF3FE'),
]
ANNUAL_LINE = '7 days free, then a one-time charge of $69.99 for lifetime access, no recurring billing.'
QUOTE = ("I know you'll love Abs By AI. It's changed thousands of guys' lives, and it will change yours too. That's why I'm offering you the chance to try it completely free for seven days. "
         "And after that, you can use Abs By AI for a full YEAR at my risk. So try Abs By AI at my risk - it could be the key to getting the body you've always wanted.")


def blue_board(T, D, start, tagc='red'):
    M, TINT, RGB = T['main'], T['tint'], T['rgb']
    pre = ('d' if D else 'p') + T['key'].lower() + start[0] + '-'
    mono = start == 'monthly'
    IFM, IFA = ('true', 'false') if mono else ('false', 'true')
    paper_card = 'background: ' + PAPER + '; border-radius: 16px; padding: 20px;'
    tag_html = free_tag() if tagc == 'red' else free_tag().replace('background: ' + R + '; color: #ffffff', 'background: #FFD23F; color: ' + K)
    assert tagc == 'red' or '#FFD23F' in tag_html

    def sel(on):
        return (M if on else '#C9CDD3', TINT if on else '#ffffff', M if on else 'transparent')

    def plan(p, on, name, bdg, sub, right):
        bd, bg, dot = sel(on)
        hbd, hbg, hdot = '[[%sBd|%s]]' % (p, bd), '[[%sBg|%s]]' % (p, bg), '[[%sDot|%s]]' % (p, dot)
        return ('<button type="button" onClick="[[' + p + 'Pick|]]" style="display: flex; align-items: center; gap: 12px; width: 100%; text-align: left; padding: 12px 14px; '
                'border: 2px solid ' + hbd + '; border-radius: 12px; background: ' + hbg + '; font-family: inherit; color: ' + K + '; cursor: pointer">'
                '<span style="width: 22px; height: 22px; border-radius: 50%; border: 2px solid ' + hbd + '; box-sizing: border-box; display: flex; align-items: center; justify-content: center; flex: none; background: #ffffff">'
                '<span style="width: 10px; height: 10px; border-radius: 50%; background: ' + hdot + '"></span></span>'
                '<span style="flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px"><span style="display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 800">' + name + bdg + '</span>'
                '<span style="font-size: 13px; line-height: 1.4; color: ' + SOFT + '">' + sub + '</span></span>'
                '<span style="font-size: 16px; font-weight: 800; white-space: nowrap">' + right + '</span></button>')

    def bar(n, t):
        return ('<div style="background: ' + M + '; color: #ffffff; min-height: 52px; border-radius: 12px; display: flex; align-items: center; gap: 12px; padding: 0 12px">'
                '<span style="width: 34px; height: 34px; border-radius: 50%; background: #ffffff; color: ' + M + '; display: flex; align-items: center; justify-content: center; font-size: 17px; font-weight: 800; flex: none">' + str(n) + '</span>'
                '<span style="font-size: 19px; font-weight: 800; letter-spacing: -0.01em">' + t + '</span></div>')

    def row(l, r, strong=False):
        return ('<div style="display: flex; justify-content: space-between; font-size: ' + ('20' if strong else '15') + 'px; font-weight: ' + ('800' if strong else '700') + '; color: ' + (K if strong else '#2B2F36') + '"><span>' + l + '</span><span>' + r + '</span></div>')

    top = ('<div id="top" style="background: ' + M + '; color: #ffffff; height: ' + ('64' if D else '60') + 'px; padding: ' + ('0 40px' if D else '0 16px') + '; display: flex; flex-shrink: 0">'
           '<div style="' + ('max-width: 1040px; margin: 0 auto; ' if D else '') + 'display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%">'
           '<img src="@LOGO@" alt="Abs By AI" style="height: ' + ('34' if D else '26') + 'px; width: auto; display: block; filter: invert(1)">'
           '<div style="display: flex; align-items: center; gap: 8px">' + ic('lock', 18, '#ffffff') +
           '<div style="font-size: 13px; font-weight: 800; line-height: 1.25; text-align: right">Secure checkout<br><span style="font-weight: 700; color: #ffffff">256-bit encryption</span></div></div>'
           '</div></div>')
    head_line = 'See Yourself With Abs, Then Get An AI Fitness Plan To <span style="box-shadow: inset 0 -9px 0 ' + ('rgba(' + RGB + ',0.3)' if tagc == 'red' else '#FFD23F') + '">Make It Real.</span>'
    hero = ('<div style="background: ' + PAPER + '; border-radius: 16px; padding: ' + ('24px 32px' if D else '16px') + '; display: flex; gap: ' + ('32' if D else '20') + 'px; align-items: center">'
            '<div style="position: relative; width: ' + ('86' if D else '74') + 'px; flex: none">' + phone('@WORKOUT@', 'App screenshot: the AI workout plan', 86 if D else 74) + tag_html + '</div>'
            '<div style="flex: 1; display: flex; flex-direction: column; gap: ' + ('10' if D else '8') + 'px; text-align: center">'
            '<h1 style="margin: 0; font-size: ' + ('34' if D else '20') + 'px; font-weight: 800; letter-spacing: -0.015em; line-height: 1.2">' + head_line + '</h1>'
            '<div style="font-size: ' + ('19' if D else '15') + 'px; font-weight: 700; line-height: 1.4; color: #2B2F36">Claim Your Free 7-Day Trial Today!</div></div></div>')
    notice = ('<div style="border: 1.5px solid ' + M + '; border-radius: 12px; padding: 12px 14px; display: flex; flex-direction: column; gap: 3px; text-align: center">'
              '<span style="font-size: 12px; font-weight: 800; letter-spacing: 0.09em; text-transform: uppercase; color: ' + M + '">New members only</span>'
              '<span style="font-size: 15px; font-weight: 700; line-height: 1.4">' + NOTICE + '</span></div>')
    pay_once = ('<span style="font-size: 10.5px; font-weight: 800; letter-spacing: 0.5px; text-transform: uppercase; padding: 3px 8px; border-radius: 999px; background: ' + M + '; color: #ffffff">Pay once</span>')
    summary = ('<div style="display: flex; flex-direction: column; gap: 12px">'
               '<div style="font-size: 13px; font-weight: 700; color: #2B2F36">Choose your plan</div>' +
               plan('m', mono, 'Monthly', '', '7 days free, then $19.99 a month', '$0 today') +
               plan('a', not mono, 'Lifetime', pay_once, ANNUAL_LINE, '$0 today') +
               '<div style="display: flex; align-items: baseline; gap: 12px; font-size: 15px; padding: 6px 0 14px; border-bottom: 1px solid ' + HAIR + '">'
               '<span style="flex: 1; font-weight: 700; line-height: 1.35">[[item|' + ('Abs By AI Membership, Free 7-Day Trial' if mono else 'Abs By AI Lifetime Access, Free 7-Day Trial') + ']]</span>'
               '<s style="color: ' + SOFT + '">[[struck|' + ('$19.99' if mono else '$69.99') + ']]</s><span style="font-weight: 800; color: ' + R + '">[[price|FREE!]]</span></div>' +
               row('Subtotal', '$0.00') + row('Sales Tax', '$0.00') +
               '<div style="border-top: 1px solid ' + HAIR + '; padding-top: 12px">' + row('Order Total', '$0.00', True) + '</div></div>')
    pay = ('<div style="display: flex; flex-direction: column; gap: 12px">'
           '<button type="button" style="width: 100%; min-height: 54px; border: none; border-radius: 12px; background: ' + M + '; color: #ffffff; font-family: inherit; font-size: 18px; font-weight: 700; cursor: pointer">Apple Pay</button>'
           '<button type="button" style="width: 100%; min-height: 54px; border: 2px solid ' + M + '; border-radius: 12px; background: #ffffff; color: ' + M + '; font-family: inherit; font-size: 17px; font-weight: 800; cursor: pointer">Pay with Link</button>'
           '<div style="display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; color: ' + SOFT + '"><span style="flex: 1; height: 1px; background: ' + HAIR + '"></span>'
           '<span>or pay by card</span><span style="flex: 1; height: 1px; background: ' + HAIR + '"></span></div>' +
           bfield('Name on Card', pre + 'name') + bfield('Credit Card Number', pre + 'card', 'Credit Card #') +
           '<div style="display: flex; gap: 12px">' + bfield('Expiration', pre + 'exp', 'MM / YY') + bfield('CVV', pre + 'cvv', 'CVV') + '</div></div>')
    trial_terms = ('<div style="display: flex; flex-direction: column; gap: 14px">' + terms_head() + bterms_text() + tick(TICK, pre + 'agree') + '</div>')
    once_terms = ('<div style="border: 2px solid ' + M + '; background: ' + TINT + '; border-radius: 14px; padding: 18px 16px; text-align: center; font-size: 17px; font-weight: 800; line-height: 1.45">' + ANNUAL_LINE[0].upper() + ANNUAL_LINE[1:] + '</div>')
    close = ('<div style="display: flex; flex-direction: column; gap: 14px; padding-top: 8px">'
             '<div>[[#if monthly|' + IFM + ']]' + trial_terms + '[[/if]][[#if annual|' + IFA + ']]' + once_terms + '[[/if]]</div>' +
             bcta('Start My Free Trial') + '</div>')
    contact = ('<div style="display: flex; flex-direction: column; gap: 8px; text-align: center">'
               '<div style="font-size: 16px; font-weight: 800">Questions Before You Order?</div>'
               '<div style="font-size: 15px; font-weight: 700"><a href="mailto:dan@absbyai.com" style="color: ' + M + '">dan@absbyai.com</a></div>'
               '<div style="font-size: 13px; line-height: 1.5; color: ' + SOFT + '">Your purchase will appear on your statement under the name: [STATEMENT NAME]</div>'
               '<div style="font-size: 13px; line-height: 1.5; color: ' + SOFT + '">Goal pictures are AI visualizations, not real results. Individual results vary.</div></div>')
    guarantee = ('<div style="' + paper_card + ' display: flex; flex-direction: column; gap: 12px">'
                 '<div style="display: flex; gap: 14px; align-items: center">'
                 '<div style="width: 72px; height: 72px; border-radius: 50%; background: ' + M + '; color: #ffffff; display: flex; flex-direction: column; align-items: center; justify-content: center; flex: none; line-height: 1; '
                 'box-shadow: 0 0 0 3px #ffffff, 0 0 0 5px ' + M + '"><span style="font-size: 23px; font-weight: 800">365</span><span style="font-size: 10.5px; font-weight: 800; letter-spacing: 1px">DAY</span></div>'
                 '<div style="font-size: 18px; font-weight: 800; line-height: 1.3; flex: 1">365-Day No Risk<br>100% Money Back Guarantee</div></div>'
                 '<p style="margin: 0; font-size: 14.5px; line-height: 1.55; color: ' + SOFT + '">We guarantee you\'ll love Abs By AI or we\'ll refund your money.</p>'
                 '<p style="margin: 0; font-size: 14.5px; line-height: 1.55; color: ' + SOFT + '">If you\'re not happy for any reason, email us within 365 days of your first payment for a full refund. No questions asked.</p></div>')
    benefits = ('<div style="' + paper_card + ' display: flex; flex-direction: column; gap: 14px">'
                '<div style="font-size: 20px; font-weight: 800; line-height: 1.3">How Abs By AI gets you to your goal:</div>' + checks(BENEFITS, 15, M, 11) + '</div>')
    founder = ('<div style="display: flow-root">'
               '<img src="@DANFULL@" alt="Dan Rose, founder of Abs By AI" style="float: left; width: 126px; height: 147px; margin: 4px 16px 8px 0; border-radius: 14px; object-fit: cover; object-position: center top">'
               '<p style="margin: 0; font-size: ' + ('17' if D else '15.5') + 'px; line-height: 1.6; color: ' + BODY + '">&ldquo;' + QUOTE + '&rdquo;</p>'
               '<div style="display: flex; flex-direction: column; gap: 1px; padding-top: 12px"><span style="font-size: 17px; font-weight: 800">Dan Rose</span>'
               '<span style="font-size: 13px; font-weight: 600; color: ' + SOFT + '">Founder, Abs By AI</span></div></div>')
    foot = ('<div style="background: ' + M + '; color: #ffffff; font-size: 12px; line-height: 1.6; padding: ' + ('28px 40px 32px' if D else '24px 20px 28px') + '; flex-grow: 1">'
            '<div style="' + ('max-width: 1040px; margin: 0 auto; ' if D else '') + 'display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: space-between">'
            '<span>Copyright &copy; 2026 Abs By AI</span><span><a href="#top" style="color: #ffffff">Terms of Service</a> &nbsp; <a href="#top" style="color: #ffffff">Privacy Policy</a></span></div></div>')
    form = bar(1, 'Your Email') + email_block(pre) + bar(2, 'Order Summary') + summary + bar(3, 'Payment Information') + pay + close + contact
    if D:
        body = (top + '<div style="max-width: 1040px; margin: 0 auto; padding: 28px 40px 48px; box-sizing: border-box; display: flex; flex-direction: column; gap: 24px">' + hero +
                cols(notice + form, benefits + guarantee) + '</div>'
                '<div style="background: ' + PAPER + '"><div style="max-width: 1040px; margin: 0 auto; padding: 36px 40px; box-sizing: border-box"><div style="max-width: 720px">' + founder + '</div></div></div>' + foot)
    else:
        body = (top + '<section style="background: #ffffff; padding: 18px 20px 30px; display: flex; flex-direction: column; gap: 18px">' + hero + notice + form + guarantee + '</section>'
                '<section style="background: ' + PAPER + '; padding: 28px 20px">' + founder + '</section>' + foot)

    logic = '''class Component extends DCLogic {
  renderVals() {
    const plan = (this.state && this.state.plan) || '@START@';
    const m = plan === 'monthly';
    const on = '@MAIN@', off = '#C9CDD3';
    const sel = (yes) => ({ bd: yes ? on : off, bg: yes ? '@TINT@' : '#ffffff', dot: yes ? on : 'transparent' });
    const sm = sel(m), sa = sel(!m);
    return {
      mPick: () => this.setState({ plan: 'monthly' }),
      aPick: () => this.setState({ plan: 'annual' }),
      mBd: sm.bd, mBg: sm.bg, mDot: sm.dot, aBd: sa.bd, aBg: sa.bg, aDot: sa.dot,
      monthly: m,
      annual: !m,
      item: m ? 'Abs By AI Membership, Free 7-Day Trial' : 'Abs By AI Lifetime Access, Free 7-Day Trial',
      struck: m ? '$19.99' : '$69.99',
      price: 'FREE!'
    };
  }
}'''.replace('@START@', start).replace('@MAIN@', M).replace('@TINT@', TINT)
    return body, logic



# ---------------------------------------------------------------- the approved design (locked by Dan, 2026-10-02)

def final_notes():
    def block(title, items):
        lis = ''.join('<li style="font-size: 14px; line-height: 1.5">%s</li>' % i for i in items)
        return ('<div style="display: flex; flex-direction: column; gap: 8px">' + eyebrow(title, '@RED@') +
                '<ul style="margin: 0; padding: 0 0 0 20px; display: flex; flex-direction: column; gap: 7px">' + lis + '</ul></div>')
    body = '''<section style="padding: 24px; display: flex; flex-direction: column; gap: 18px; flex-grow: 1">
<div style="display: flex; flex-direction: column; gap: 4px">''' + eyebrow('Approved 2026-10-02') + '''<span style="font-size: 22px; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2">The final cart</span></div>
''' + block('What is locked', [
        'Structure: the Healthy Back Institute cart. Top box, new-members notice, three numbered steps on one page, terms with a tick box above the button, guarantee, your photo and quote at the bottom.',
        'Entry: straight from the /start buy button. No photo, goal picture or body numbers.',
        'Colour: deep navy <b>#12306B</b> for the stripe, step headers, pay buttons, outlines, seal and footer.',
        'The "FREE 7 days" callout and the underline under "Make It Real" are yellow <b>#FFD23F</b>.',
        'Guarantee: 365 days.',
        'Plans: Monthly (7 days free, then $19.99 a month, pre-selected) and Lifetime (7 days free, then a one-time charge of $69.99, no recurring billing).',
        'Picking Lifetime removes the free-trial terms and the tick box.',
        'The phone has no bullet box. Desktop keeps it in the right column with the guarantee.']) + '''
''' + block('The three boards', [
        'Phone, Monthly picked. Press Play to tap between the plans.',
        'Phone, Lifetime picked.',
        'Desktop.']) + '''
''' + block('Still open for the build', [
        '[STATEMENT NAME] is filled in from Stripe during the build.',
        "Stripe draws the Apple Pay and Link buttons, so those two will look like Stripe's own."]) + '''
</section>'''
    return body, STATIC


NAVY = THEMES[1]
NOTES_FILE = 'Final-Notes.dc.html'
PHONES = ['Final-Cart-Phone.dc.html', 'Final-Cart-Phone-Lifetime.dc.html']
DESK = 'Final-Cart-Desktop.dc.html'


def boards():
    B = []

    def add(path, title, W, fn, fluid=False, bg='#ffffff', brand=True):
        body, logic = fn()
        B.append(dict(path=path, title=title, W=W, body=body, logic=logic, fluid=fluid, bg=bg, brand=brand))
    add(PHONES[0], 'FINAL · phone, Monthly picked', 390, lambda: blue_board(NAVY, False, 'monthly', 'yellow'))
    add(PHONES[1], 'FINAL · phone, Lifetime picked', 390, lambda: blue_board(NAVY, False, 'annual', 'yellow'))
    add(DESK, 'FINAL · desktop', 1200, lambda: blue_board(NAVY, True, 'monthly', 'yellow'), True)
    add(NOTES_FILE, 'Approved design notes', 560, final_notes, False, '#ffffff', False)
    return B


def root_open(b, H=None):
    ink = K if b['brand'] else '@INK@'
    base = "background: %s; color: %s; font-family: @FONT@; -webkit-font-smoothing: antialiased" % (b['bg'], ink)
    if b['fluid']:
        return '<div style="%s">' % base
    hh = 'height: %dpx; ' % H if H else ''
    return '<div style="width: %dpx; %sbox-sizing: border-box; display: flex; flex-direction: column; %s">' % (b['W'], hh, base)


FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&amp;display=swap" rel="stylesheet">'
LINK_CSS = 'a{color:#12306B}a:hover{color:#0B1F47}'


def measure_page(b):
    html = tok(root_open(b) + '\n' + b['body'] + '\n</div>')
    html = render(html, 'measure')
    for k, v in LOCAL.items():
        html = html.replace(k, 'file://' + v.replace(' ', '%20'))
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">' + FONT_LINK +
            '<style>body{margin:0}' + LINK_CSS + '</style></head><body><div id="root" style="width:%dpx">%s</div>'
            '<script>document.fonts.ready.then(function(){setTimeout(function(){var h=Math.ceil(document.getElementById("root").getBoundingClientRect().height);'
            'var p=document.createElement("pre");p.textContent="MEASURE["+h+"]END";document.body.appendChild(p);},400);});</script></body></html>' % (b['W'], html))


def dc_page(b, H):
    html = tok(root_open(b, H) + '\n' + b['body'] + '\n</div>')
    html = render(html, 'build')
    props = json.dumps({'$preview': {'width': b['W'], 'height': H}})
    title = b['title'].replace('·', '-')
    return '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>''' + title + '''</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
''' + FONT_LINK + '''
<style>
body{margin:0}
''' + LINK_CSS + '''
</style>
</helmet>
''' + html + '''
</x-dc>
<script type="text/x-dc" data-dc-script data-props=\'''' + props + '''\'>
''' + b['logic'] + '''
</script>
</body>
</html>
'''



def main():
    mode, out = sys.argv[1], sys.argv[2]
    B = boards()
    if mode == 'measure':
        os.makedirs(out, exist_ok=True)
        for b in B:
            open(os.path.join(out, b['path'].replace('.dc.html', '.html')), 'w').write(measure_page(b))
        print(len(B), 'measure pages')
        return
    heights = json.load(open(os.path.join(HERE, 'heights.json')))
    live = json.load(open(sys.argv[3]))  # the canvas index as last read from the artifact
    proj = os.path.join(out, 'project')
    os.makedirs(proj, exist_ok=True)
    H = {}
    by = {b['path']: b for b in B}
    for b in B:
        H[b['path']] = heights[b['path']] + 8
        open(os.path.join(proj, b['path']), 'w').write(dc_page(b, H[b['path']]))
    canvas = dict(live)  # keep every key and every earlier board exactly as read
    canvas['pages'] = [p for p in live.get('pages', []) if p.get('id') != 'final'] + [{'id': 'final', 'name': 'APPROVED: final cart'}]
    canvas['launch'] = {'view': 'canvas', 'page': 'final'}
    cb = {k: dict(v) for k, v in live['boards'].items() if k not in by}
    notes = {k: dict(v) for k, v in live.get('notes', {}).items() if not k.startswith('final')}
    cb[PHONES[0]] = dict(x=0, y=0, w=390, h=H[PHONES[0]], title=by[PHONES[0]]['title'], page='final', is_interactive=True)
    cb[PHONES[1]] = dict(x=470, y=0, w=390, h=H[PHONES[1]], title=by[PHONES[1]]['title'], page='final')
    cb[DESK] = dict(x=940, y=0, w=1200, h=H[DESK], title=by[DESK]['title'], page='final', expand='fill', is_interactive=True)
    cb[NOTES_FILE] = dict(x=2220, y=0, w=560, h=H[NOTES_FILE], title='Approved design notes', page='final')
    notes['finalt1'] = {'x': 0, 'y': -300, 'text': 'Approved cart, locked 2026-10-02', 'kind': 'title1', 'maxW': 2780, 'page': 'final'}
    canvas['boards'] = cb
    canvas['order'] = [p for p in live['order'] if p not in by] + PHONES + [DESK, NOTES_FILE]
    canvas['notes'] = notes
    json.dump(canvas, open(os.path.join(proj, 'canvas.json'), 'w'), indent=1, ensure_ascii=False)
    print('built', len(B), 'boards')
    for p in PHONES + [DESK, NOTES_FILE]:
        print(' ', p, cb[p]['w'], 'x', cb[p]['h'], '@', cb[p]['x'], cb[p]['y'])


main()
