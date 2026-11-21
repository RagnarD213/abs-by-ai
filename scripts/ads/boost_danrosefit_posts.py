#!/usr/bin/env python3
"""
Attach the two existing @danrosefit Instagram posts to the paused IG profile-visits ad set,
as PAUSED ads, under the @danrosefit identity.

WHY THIS EXISTS (2026-09-02): Ads Manager has NO Instagram-identity control for this ad set
(the Identity card is a "Read only page field"), and it silently runs the ad as @abs.by.ai, so
boosting a @danrosefit post fails with #2238052. The Marketing API accepts the identity when the
creative is built with the TOP-LEVEL shape below (object_id + instagram_user_id +
source_instagram_media_id, NO object_story_spec, NO call_to_action). That shape passed the
identity check and was stopped only by:

    (#100, subcode 1885183) "Ads creative post was created by an app that is in development
    mode. It must be in public to create this ad."

So the ONE precondition is: app 1598463548528030 switched to LIVE in developers.facebook.com
(App settings → Basic: privacy https://absbyai.com/privacy, terms https://absbyai.com/terms,
app domain absbyai.com, a category → Save → Publish → Live). Claude cannot edit app settings
(platform restriction on account-setting changes) — Dan does that, then runs:

    python3 scripts/ads/boost_danrosefit_posts.py            # dry run: creates nothing
    python3 scripts/ads/boost_danrosefit_posts.py --apply    # creates 2 creatives + 2 PAUSED ads

Everything it creates is PAUSED and the campaign/ad set stay PAUSED. Nothing spends until Dan
flips the campaign on in Ads Manager.

Handoff: Handoffs/handoff-20260902-ig-engagement-ad-identity.md
"""
import hashlib
import hmac
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0/"
ACT = "act_2143998876461525"
ADSET_ID = "120250753601020682"           # IG profile visits - danrosefit v2 (PAUSED)
PAGE_ID = "1380236418500031"              # Daniel Rose Fitness (keeper, red "D")
IG_USER_ID = "17841401601139982"          # @danrosefit
POSTS = [
    # (ig media id, ad name) — MUST be these existing posts: ManyChat listens on their comments.
    ("18188183254395331", "danrosefit - channel intro reel (existing post)"),
    ("18192762022391478", "danrosefit - 3-min total body (existing post)"),
]
SECRETS = os.path.expanduser("~/.absbyai-secrets.env")


def secret(key):
    if os.environ.get(key):
        return os.environ[key]
    env = open(SECRETS).read()
    m = re.search(r"^(?:export )?%s=(.*)$" % re.escape(key), env, re.M)
    if not m:
        sys.exit(f"{key} not found in env or {SECRETS}")
    return m.group(1).strip().strip('"').strip("'")


TOKEN = secret("META_ADS_TOKEN")
PROOF = hmac.new(secret("META_APP_SECRET").encode(), TOKEN.encode(), hashlib.sha256).hexdigest()


def call(method, path, **params):
    params.update(access_token=TOKEN, appsecret_proof=PROOF)
    body = urllib.parse.urlencode(params).encode()
    url = API + path + ("?" + body.decode() if method == "GET" else "")
    req = urllib.request.Request(url, data=None if method == "GET" else body, method=method)
    try:
        return json.loads(urllib.request.urlopen(req).read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())


def main():
    apply = "--apply" in sys.argv

    adset = call("GET", ADSET_ID, fields="name,status,effective_status,promoted_object")
    print("ad set:", json.dumps(adset))
    if adset.get("status") != "PAUSED":
        sys.exit("refusing: ad set is not PAUSED")

    existing = call("GET", f"{ADSET_ID}/ads", fields="id,name,status").get("data", [])
    print(f"ads already in ad set: {len(existing)}")
    for a in existing:
        print("  ", a)

    for media_id, name in POSTS:
        media = call("GET", media_id, fields="id,caption,permalink,owner,timestamp")
        owner = (media.get("owner") or {}).get("id")
        print(f"\npost {media_id}: {media.get('timestamp','?')[:10]} {media.get('permalink')}")
        if owner and owner != IG_USER_ID:
            sys.exit(f"refusing: post {media_id} is owned by {owner}, not @danrosefit")
        if any(a["name"] == name for a in existing):
            print("  ad with this name already exists — skipping")
            continue
        if not apply:
            print("  dry run — would create creative + PAUSED ad:", name)
            continue

        creative = call(
            "POST", f"{ACT}/adcreatives",
            name=name,
            object_id=PAGE_ID,
            instagram_user_id=IG_USER_ID,
            source_instagram_media_id=media_id,
        )
        print("  creative:", json.dumps(creative))
        if "id" not in creative:
            err = creative.get("error", {})
            if err.get("error_subcode") == 1885183:
                sys.exit("STOP: app 1598463548528030 is still in Development mode — switch it to Live first.")
            sys.exit("creative creation failed")

        ad = call(
            "POST", f"{ACT}/ads",
            name=name,
            adset_id=ADSET_ID,
            creative=json.dumps({"creative_id": creative["id"]}),
            status="PAUSED",
        )
        print("  ad:", json.dumps(ad))
        if "id" not in ad:
            sys.exit("ad creation failed")

        check = call("GET", ad["id"], fields="id,name,status,effective_status,creative{instagram_user_id,source_instagram_media_id}")
        print("  read-back:", json.dumps(check))

    if apply:
        final = call("GET", f"{ADSET_ID}/ads", fields="id,name,status,effective_status")
        print("\nfinal ads in ad set:", json.dumps(final))
        print("Campaign and ad set are still PAUSED. Dan flips the campaign on in Ads Manager when ready.")


if __name__ == "__main__":
    main()
