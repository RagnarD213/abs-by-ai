# QA for the /start video test (two films, one per browser). Real Chrome, headless, phone and desktop sizes.
# Every PostHog post the page makes is caught and decoded here, and the ad pixels are blocked.
#   python3 qa_video_test.py http://localhost:3000 --hold    local: nothing reaches PostHog
#   python3 qa_video_test.py https://absbyai.com             live: the forced ?vid= views do reach PostHog (they are
#                                                            marked video_forced and never counted); the coin views are held
#   --quick skips the 4x watch run (about 40 seconds per case). --only forced | coin | other runs one group.
import base64, gzip, json, sys, time, urllib.parse
from playwright.sync_api import sync_playwright

BASE = sys.argv[1].rstrip('/')
HOLD = '--hold' in sys.argv
QUICK = '--quick' in sys.argv
PIXELS = ('googletagmanager.com', 'google-analytics.com', 'doubleclick.net', 'googleadservices.com', 'google.com/pagead',
          'google.com/ccm', 'connect.facebook.net', 'facebook.com/tr', 'analytics.tiktok.com', 'googlesyndication.com')
FILMS = {'a': {'phone': '/video/wv01-a-720.mp4', 'desk': '/video/wv01-a-1080.mp4', 'opening': 142.14, 'dur': 627.6},
         'b': {'phone': '/video/wv01-b-720.mp4', 'desk': '/video/wv01-b-1080.mp4', 'opening': 212.45, 'dur': 717.2}}
SIZES = {'desk': dict(viewport=dict(width=1280, height=800), user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'),
         'phone': dict(viewport=dict(width=390, height=844), device_scale_factor=3, is_mobile=True, has_touch=True,
                       user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1')}
results = []


def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('  ok   ' if ok else '  FAIL ') + name + (f'  [{detail}]' if detail and not ok else ''))


def decode(req):
    body = req.post_data_buffer or b''
    q = urllib.parse.parse_qs(urllib.parse.urlparse(req.url).query)
    try:
        if q.get('compression', [''])[0] == 'gzip-js' or body[:2] == b'\x1f\x8b':
            body = gzip.decompress(body)
        elif body.startswith(b'data='):
            body = base64.b64decode(urllib.parse.unquote(body[5:].decode()))
        d = json.loads(body)
    except Exception:
        return []
    if isinstance(d, dict) and 'batch' in d: d = d['batch']
    return d if isinstance(d, list) else [d]


class Session:
    def __init__(self, browser, size, init=None, hold=HOLD):
        self.hold = hold  # unforced views are always held, so QA never lands in the test's numbers
        self.cx = browser.new_context(**SIZES[size])
        # PostHog drops events from automated browsers; look like a normal one so the events can be read.
        self.cx.add_init_script("Object.defineProperty(Navigator.prototype, 'webdriver', { get: function () { return false; } });")
        if init: self.cx.add_init_script(init)
        self.posts = 0
        self.events, self.media = [], []
        self.cx.route('**/*', self.route)
        self.page = self.cx.new_page()
        self.page.on('request', lambda r: self.media.append(urllib.parse.urlparse(r.url).path) if ('/video/' in r.url or 'poster' in r.url) else None)

    def route(self, route):
        req = route.request
        u = req.url
        if any(p in u for p in PIXELS):
            return route.abort()
        if 'i.posthog.com' in u and req.method == 'POST' and 'flags' not in u and 'decide' not in u:
            self.posts += 1
            self.events += decode(req)
            if self.hold:
                return route.fulfill(status=200, content_type='application/json', body='{"status":1}')
        return route.continue_()

    def ev(self, name):
        return [e for e in self.events if e.get('event') == name]

    def wait_ev(self, name, n=1, secs=12):
        t = time.time()
        while time.time() - t < secs:
            if len(self.ev(name)) >= n: return True
            self.page.wait_for_timeout(250)
        return False

    def v(self, expr):
        return self.page.evaluate(f"(function(){{var v=document.getElementById('vsl');return {expr}}})()")

    def close(self):
        self.cx.close()


def forced_arm(browser, size, arm):
    print(f'\n== {size} ?vid={arm}')
    film = FILMS[arm]; other = FILMS['b' if arm == 'a' else 'a']
    want = film[size]
    s = Session(browser, size)
    s.page.goto(f'{BASE}/start?vid={arm}&utm_source=qa&utm_campaign=vsl-video-test&gclid=QA123', wait_until='load')
    s.page.wait_for_timeout(3500)
    st = s.v("{arm: VSL.video, forced: VSL.videoForced, sticky: VSL.videoSticky, src: v.currentSrc, poster: v.poster, paused: v.paused, muted: v.muted, t: v.currentTime, dur: v.duration, w: v.videoWidth, stored: localStorage.getItem('absbyai_vsl_video'), hidden: document.hidden, controls: v.controls}")
    check('arm picked from ?vid', st['arm'] == arm and st['forced'] is True, st)
    check('forced view is not stored', st['stored'] is None, st['stored'])
    check(f'plays {want}', st['src'].endswith(want), st['src'])
    check('video size matches the file', st['w'] == (1920 if size == 'desk' else 1280), st['w'])
    check('film length is this arm\'s', abs((st['dur'] or 0) - film['dur']) < 1, st['dur'])
    check('muted preview autoplays', (not st['paused']) and st['muted'] and st['t'] > 0.3 and not st['controls'], st)
    vids = sorted(set(m for m in s.media if '/video/' in m))
    check('only this arm\'s one film is requested', vids == [want], vids)
    check('nothing of the other arm is requested', not any(m in (other['phone'], other['desk']) for m in s.media), s.media)
    check('poster requested', any('video-poster-wv01.jpg' in m for m in s.media), s.media)
    # load-time events
    s.wait_ev('vsl_landing_seen'); s.wait_ev('vsl_video_play')
    print('     posthog posts caught:', s.posts, 'events:', sorted(set(e.get('event') for e in s.events)))
    seen = s.ev('vsl_landing_seen'); flag = s.ev('$feature_flag_called'); play = s.ev('vsl_video_play')
    p = seen[0]['properties'] if seen else {}
    check('vsl_landing_seen once, with the arm', len(seen) == 1 and p.get('video_variant') == arm and p.get('video_forced') is True and p.get('video_sticky') is True, p and {k: p.get(k) for k in ('video_variant', 'video_forced', 'video_sticky')})
    check('page variant unchanged (letter-v1)', p.get('landing_variant') == 'letter-v1' and p.get('variant') == 'letter-v1' and p.get('landing') == 'vsl')
    fl = [e for e in flag if e['properties'].get('$feature_flag') == 'vsl-video-variant']
    check('exposure event once, with the arm', len(fl) == 1 and fl[0]['properties'].get('$feature_flag_response') == arm and fl[0]['properties'].get('forced') is True, len(fl))
    check('vsl_video_play (muted autoplay) once', len(play) == 1 and play[0]['properties'].get('video_variant') == arm and play[0]['properties'].get('muted') is True, len(play))
    # the muted preview pauses when scrolled away and resumes when back
    s.page.evaluate('window.scrollTo(0, 3000)'); s.page.wait_for_timeout(900)
    away = s.v('v.paused')
    s.page.evaluate('window.scrollTo(0, 0)'); s.page.wait_for_timeout(900)
    back = s.v('v.paused')
    check('muted preview pauses when scrolled away, resumes when back', away is True and back is False, (away, back))
    # sound on: restart from 0:00 with sound and controls
    before = s.v('v.currentTime')
    s.page.click('#soundBox'); s.page.wait_for_timeout(1200)
    on = s.v("{t: v.currentTime, muted: v.muted, controls: v.controls, paused: v.paused, live: document.getElementById('vbox').classList.contains('live'), box: getComputedStyle(document.getElementById('soundBox')).display}")
    check('sound on restarts from 0:00, unmuted, with controls', on['t'] < before and on['t'] < 2.5 and on['muted'] is False and on['controls'] and not on['paused'] and on['live'] and on['box'] == 'none', (before, on))
    check('vsl_sound_on once', s.wait_ev('vsl_sound_on') and len(s.ev('vsl_sound_on')) == 1 and s.ev('vsl_sound_on')[0]['properties'].get('video_variant') == arm)
    if not QUICK:
        # 4x playback: about 36 film seconds in 9 real seconds, so the 30 second mark fires and the 60 does not
        s.v('(v.playbackRate = 4, 1)'); s.page.wait_for_timeout(9000)
        s.v('(v.playbackRate = 1, 1)')
        s.wait_ev('vsl_video_watch'); s.page.wait_for_timeout(3300)
        w = [e['properties'].get('sec') for e in s.ev('vsl_video_watch')]
        check('vsl_video_watch fires at 30 seconds watched (and not yet at 60)', w == [30], w)
        check('opening not done yet', len(s.ev('vsl_opening_done')) == 0)
        # skip ahead to 2 seconds before this arm's opening ends: the skip adds no watch time
        s.v(f"(v.currentTime = {film['opening'] - 2}, 1)"); s.page.wait_for_timeout(1200)
        early = s.v('v.currentTime') < film['opening'] and not s.page.evaluate('!!window.__od')
        s.wait_ev('vsl_opening_done'); s.page.wait_for_timeout(3300)
        od = s.ev('vsl_opening_done')
        check('not before the opening ends', early)
        check('vsl_opening_done fires once when playback passes this arm\'s opening', len(od) == 1 and od[0]['properties'].get('video_variant') == arm, [e['properties'] for e in od][:1] and {k: od[0]['properties'].get(k) for k in ('video_variant', 'watched_sec')})
        w2 = [e['properties'].get('sec') for e in s.ev('vsl_video_watch')]
        check('a skip ahead adds no watch seconds', w2 == [30], w2)
        check('no percent mark from a short watch... 25% only after the skip', all(e['properties'].get('pct') in (25,) for e in s.ev('vsl_video_progress')) , [e['properties'].get('pct') for e in s.ev('vsl_video_progress')])
    # the checkout link carries the arm and the ad click ids
    href = s.page.evaluate("document.querySelector('.js-cta').getAttribute('href')")
    q = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
    check('checkout link: join, from=vsl, v=letter-v1, vid=arm, vf=1, utm and gclid kept',
          q.get('join') == ['1'] and q.get('from') == ['vsl'] and q.get('v') == ['letter-v1'] and q.get('vid') == [arm] and q.get('vf') == ['1'] and q.get('utm_source') == ['qa'] and q.get('gclid') == ['QA123'], href)
    n_btn = s.page.evaluate("Array.prototype.filter.call(document.querySelectorAll('.js-cta'), function(a){return a.getAttribute('href') === document.querySelector('.js-cta').getAttribute('href')}).length")
    check('all 8 buy links carry it (stripe + 7 buttons)', n_btn == 8, n_btn)
    s.page.wait_for_timeout(3600)  # let the page's events flush
    s.events.clear()
    clicks = []
    s.page.expose_function('qaCap', lambda j: clicks.append(json.loads(j)))
    s.page.evaluate("(function(){var o=posthog.capture.bind(posthog);posthog.capture=function(e,p){try{window.qaCap(JSON.stringify([e,p]))}catch(x){}return o.apply(null,arguments)}})()")
    s.page.evaluate("document.querySelector('.cta.js-cta').click()")
    s.page.wait_for_load_state('load'); s.wait_ev('cart_viewed', secs=15)
    check('button opens the cart', '/?' in s.page.url and 'join=1' in s.page.url, s.page.url)
    cv = s.ev('cart_viewed'); cp = cv[0]['properties'] if cv else {}
    check('cart_viewed carries the arm', len(cv) >= 1 and cp.get('video_variant') == arm and cp.get('video_forced') is True and cp.get('landing_variant') == 'letter-v1', cp and {k: cp.get(k) for k in ('video_variant', 'video_forced', 'landing_variant', 'landing')})
    click = [c for c in clicks if c[0] == 'vsl_trial_cta_clicked']
    check('vsl_trial_cta_clicked fires once and carries the arm', len(click) == 1 and click[0][1].get('video_variant') == arm and click[0][1].get('position'), click)
    sent = [e for e in s.events if e.get('event') == 'vsl_trial_cta_clicked']
    print('     (click event caught on the wire as the page left:', len(sent), ')')
    s.close()


def coin(browser, size):
    print(f'\n== {size} coin (no ?vid)')
    s = Session(browser, size, hold=True)
    arms = []
    for i in range(4):
        s.page.goto(f'{BASE}/start', wait_until='load'); s.page.wait_for_timeout(3600)  # long enough for the page's events to flush
        arms.append(s.v("[VSL.video, VSL.videoForced, VSL.videoSticky, localStorage.getItem('absbyai_vsl_video'), v.currentSrc]"))
    first = arms[0]
    check('coin picks a or b, not forced, stored', first[0] in ('a', 'b') and first[1] is False and first[2] is True and first[3] == first[0], first)
    check('same arm on every reload', all(a[0] == first[0] for a in arms), [a[0] for a in arms])
    check('plays the stored arm\'s film', all(a[4].endswith(FILMS[first[0]][size]) for a in arms), [a[4] for a in arms])
    s.wait_ev('vsl_landing_seen', n=4)
    ps = [e['properties'] for e in s.ev('vsl_landing_seen')]
    check('events say unforced and sticky', len(ps) == 4 and all(p.get('video_variant') == first[0] and p.get('video_forced') is False and p.get('video_sticky') is True for p in ps), len(ps))
    # ?vid= on a browser that already has an arm: forced view, stored arm untouched
    other = 'b' if first[0] == 'a' else 'a'
    s.page.goto(f'{BASE}/start?vid={other}', wait_until='load'); s.page.wait_for_timeout(800)
    f = s.v("[VSL.video, VSL.videoForced, localStorage.getItem('absbyai_vsl_video')]")
    check('?vid= overrides without changing the stored arm', f == [other, True, first[0]], f)
    s.close()
    return first[0]


def blocked_storage(browser):
    print('\n== storage blocked')
    s = Session(browser, 'phone', hold=True, init="try { Object.defineProperty(window, 'localStorage', { get: function () { throw new Error('blocked'); } }); } catch (e) {}")
    s.page.goto(f'{BASE}/start', wait_until='load'); s.page.wait_for_timeout(2500)
    st = s.v('[VSL.video, VSL.videoForced, VSL.videoSticky, v.currentSrc, v.paused]')
    check('page still works: an arm is picked and its film plays', st[0] in ('a', 'b') and st[1] is False and st[3].endswith(FILMS[st[0]]['phone']) and st[4] is False, st)
    check('marked not sticky', st[2] is False, st)
    s.wait_ev('vsl_landing_seen')
    p = (s.ev('vsl_landing_seen') or [{'properties': {}}])[0]['properties']
    check('event says sticky: false', p.get('video_sticky') is False and p.get('video_variant') == st[0], {k: p.get(k) for k in ('video_variant', 'video_sticky')})
    s.close()


def in_app(browser):
    print('\n== inside the Android app (purchase UI hidden)')
    s = Session(browser, 'phone', init="try { sessionStorage.setItem('absbyai_twa', '1'); } catch (e) {}")
    s.page.goto(f'{BASE}/start?vid=b', wait_until='load'); s.page.wait_for_timeout(2500)
    st = s.page.evaluate("(function(){var v=document.getElementById('vsl');var c=document.querySelector('.cta.js-cta');return [document.documentElement.classList.contains('native-app'), VSL.nativeApp, VSL.video, v.currentSrc, v.paused, getComputedStyle(c).display, getComputedStyle(document.querySelector('.app-only-note')).display]})()")
    check('app mode unchanged: buy buttons hidden, Open Abs By AI shown', st[0] and st[1] and st[5] == 'none' and st[6] != 'none', st)
    check('the arm\'s film still plays in the app', st[2] == 'b' and st[3].endswith(FILMS['b']['phone']) and st[4] is False, st)
    s.close()


with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', headless=True, args=['--autoplay-policy=document-user-activation-required', '--disable-blink-features=AutomationControlled'])
    only = sys.argv[sys.argv.index('--only') + 1] if '--only' in sys.argv else None  # forced | coin | other
    if only in (None, 'forced'):
        for size in ('desk', 'phone'):
            for arm in ('a', 'b'):
                forced_arm(b, size, arm)
    if only in (None, 'coin'):
        coin(b, 'desk'); coin(b, 'phone')
    if only in (None, 'other'):
        blocked_storage(b)
        in_app(b)
    b.close()

bad = [r for r in results if not r[1]]
print(f'\n{len(results) - len(bad)} of {len(results)} checks passed')
for name, ok, detail in bad: print('FAILED:', name, detail)
sys.exit(1 if bad else 0)
