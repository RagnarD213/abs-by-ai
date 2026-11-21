import jwt, time, requests, os, json, sys

KEY_ID = "D7UC9KJD3B"
ISSUER_ID = "fc6c9b53-4b80-4d1c-b3e1-d4c1623a6385"
KEY_PATH = os.path.expanduser("~/.appstoreconnect/private_keys/AuthKey_D7UC9KJD3B.p8")

def token():
    with open(KEY_PATH) as f:
        key = f.read()
    payload = {
        "iss": ISSUER_ID,
        "iat": int(time.time()),
        "exp": int(time.time()) + 1200,
        "aud": "appstoreconnect-v1",
    }
    return jwt.encode(payload, key, algorithm="ES256", headers={"kid": KEY_ID, "typ": "JWT"})

def api(path, params=None, method="GET", body=None):
    url = path if path.startswith("http") else "https://api.appstoreconnect.apple.com" + path
    h = {"Authorization": "Bearer " + token(), "Content-Type": "application/json"}
    r = requests.request(method, url, headers=h, params=params, json=body)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, r.text

if __name__ == "__main__":
    sc, data = api("/v1/builds", {"filter[app]": "6794097836", "limit": 5,
                                  "sort": "-uploadedDate"})
    print(sc)
    for b in data.get("data", []):
        a = b["attributes"]
        print(json.dumps({
            "id": b["id"],
            "version": a.get("version"),
            "processingState": a.get("processingState"),
            "uploadedDate": a.get("uploadedDate"),
            "expired": a.get("expired"),
        }, indent=2))
