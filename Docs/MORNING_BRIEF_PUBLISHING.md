# Private morning brief publication

The approved publisher uses Ed25519 signatures. The private key stays on the Mac, outside Git, in a directory owned by its user with mode 0700. The key file is created exclusively with mode 0600. The signer rejects symlinked or permissive key files/directories and never emits private key material. Railway receives only `BRIEF_PUBLISH_PUBLIC_KEY`, the public SPKI DER key encoded as base64. No Google client secret or shared ingestion secret is needed.

Publication rights cover only `POST /api/brief/publish` and `POST /api/brief/image/publish`. They cannot read private content, establish owner sessions, change campaigns or post to social platforms. Google owner authentication continues protecting the page, data and image reads.

Each signature binds a version, method, exact path, SHA-256 body digest, timestamp, random nonce and public key ID. The server accepts timestamps no more than 300 seconds old or 30 seconds ahead. A persistent database primary key atomically claims each key-ID/nonce pair; replays remain rejected across process restarts and replicas. Expired records are removed only after their acceptance window. Failed validation/publication requires a new signed request. Signed bodies use dedicated bounded parsers before the product JSON parser can consume them.

## Local commands

Run from the repository. Choose a private directory outside every Git checkout. Key creation never overwrites an existing file:

```sh
node scripts/brief/mac_signer.js --create-key /private/directory/publish-key.pem
python3 scripts/brief/publish_brief.py /private/directory/edition.json
python3 scripts/brief/publish_brief.py /private/directory/edition.json --publish --key-file /private/directory/publish-key.pem
python3 scripts/brief/publish_image.py /private/directory/approved-image.png --publish --key-file /private/directory/publish-key.pem
```

Key creation returns only the public verification variable. Set that public value on the existing website service, then deploy the matching verifier. Keep private files, source evidence, imagery, prompts and receipts outside Git. The image publisher verifies a matching digest receipt before successful publication is claimed. It uploads an already-approved image; it does not generate one or incur an image API charge.

Revocation: remove or replace the website's public verification variable and deploy it. Rotation needs a separately created local key and public-key update. Never transmit the old or new private key. Retain Google owner publication at `/brief-publish` for manual recovery. Device files must be available on the device used for manual upload.

## Direct cloud image upload with local digest signing

When an authorized cloud executor already holds an approved image's original bytes and can make an HTTPS POST, those bytes need not pass through Library or the Mac. The Mac signs only their SHA-256 digest with its existing key. This is the same image publication protocol, not a new credential or persistent access grant. Local planning collection and signing still require the Mac. A cloud file being displayed as an artifact does not itself update the private website.

Prepare the upload before requesting authorization. Read the original PNG or JPEG as binary, check its MIME and size (more than 4 bytes, at most 8 MiB), and compute `hashlib.sha256(image_bytes).hexdigest()` or its exact equivalent. Send the resulting 64 lowercase hexadecimal characters to the Mac, with at most one trailing LF. Do not hash the filename, Library ID, URL, base64 text, JSON, multipart encoding or a re-encoded image. The digest signer rejects other input and has no selectable route:

```sh
umask 077
printf '%s\n' "$image_sha256" | node scripts/brief/mac_signer.js --sign-image-digest /private/directory/publish-key.pem > /private/directory/image-authorization.json
```

The command returns exactly `X-Brief-Key-Id`, `X-Brief-Timestamp`, `X-Brief-Nonce` and `X-Brief-Signature`. Treat this JSON as a short-lived authorization for one exact image upload; keep it outside Git and user-facing logs. It contains no private key. Coordinate immediately after preparation because the existing server accepts a timestamp only within 300 seconds, allowing at most 30 seconds ahead. The nonce can be claimed once across replicas and restarts.

The Ed25519 signature covers the following UTF-8 bytes, separated by LF and ending with one LF. The digest is lowercase SHA-256 of the exact HTTP body. Timestamp is Unix seconds; nonce is 32 lowercase hexadecimal characters; key ID is SHA-256 of the public SPKI DER bytes:

```text
absbyai-brief-v1
POST
/api/brief/image/publish
<64-character body digest>
<timestamp>
<nonce>
<key ID>
```

The cloud sends `POST https://absbyai.com/api/brief/image/publish`, with no query string or trailing slash. Add the four returned headers unchanged and `Content-Type: image/png` or `Content-Type: image/jpeg`. The HTTP body is the original binary image bytes, with no JSON, multipart wrapper, base64 encoding or compression. Do not export the Mac key, transfer an owner cookie, add CORS access, create a public image URL or use a website fetch-from-URL proxy. The existing endpoint recomputes the digest from received bytes and validates the image before storage.

A successful upload returns HTTP 200 with `{"ok":true,"sha256":"<same digest>","mime":"image/png","scheduleChanged":false}` (or JPEG MIME). Require both digest and MIME to match before reporting success. A 401 means authorization, exact-path or replay rejection; 400 means an invalid body; 413 means too large; 503 means publication unavailable. A retry requires new signing headers, not reuse of a consumed nonce. If a response is lost, first verify storage rather than assuming success. Signatures authorize publication only, never private reads or owner login.

After the image receipt, verify exact stored image bytes/digest and owner-only serving. Preserve the current text edition; update only its image provenance/date when separately coordinated, keeping a retained fallback's actual date. The present raw-image request does not carry an image date. Do not infer one from a download or upload timestamp. Anonymous image reads remain denied and owner responses remain `private, no-store`. This transport is not proven in production until a coordinated cloud upload and readback succeed.

## Verification and remaining work

Synthetic tests cover forged signatures, wrong keys, changed bytes, wrong methods/paths, expired/future timestamps, persistent replay rejection, concurrent nonce claims, unavailable database, bounded bodies and key-file permissions. They preserve the independent Google owner denial/session tests. Real signed publication and owner readback must be recorded separately; local test success alone is not production proof.

The external cloud automation is enabled daily at 7:00 AM America/Chicago from October 4, targeting a 7:30 page without routine notifications. It invokes the Mac runner and includes connected inbox/calendar, built-in image generation with dated fallback, practical model-release checks and fresh-watch-feed use. No local cron/launchd job exists. First automated completion and these optional outputs remain unproven. Trello is deferred; free-generation/new-trial/paid mappings remain unverified. Missing sources stay explicit and unknown values stay null. Publication itself does not enable or alter scheduling.

## October 3 production proof and repeatable sequence

The approved hero and dated edition were published with the Mac signer on production commit `86dff85`, deployment `8b804e51-aa66-43a4-be75-6e8a64dc6bcd`. Receipts matched the image digest and edition date. A separate read-only transaction verified that the private database contains the exact validated edition and image bytes. Twelve live checks passed: same-edition publication, replay, forged/expired/future signatures, changed bytes, cross-route/query-path signatures, unsigned publication, signed read denial and anonymous page redirect. The private signing key was never emitted or transmitted. Owner browser readback and device persistence remain separate checks.

Repeat in order: refresh both queue sources, run `collect_inputs.py --live`, have the parent writer combine the fresh private inputs with connected Gmail/Calendar and write a new dated edition, validate it, optionally publish an approved image, then publish the edition and verify receipts. Never reuse the October 3 assembly script on later dates; its proof context is fixed. Exact Mac paths, argv sequences and receipts are recorded in private `daily-command-sequence.json` outside Git.

Measured one-run timings: queue refresh 7.42 seconds, local collection 14.28 seconds, image upload 2.54 seconds and edition upload 0.89 seconds. The 25.13-second sum excludes writer/model time, connected inbox/calendar intake, new image generation and external failures. It is not a guaranteed schedule runtime. The enabled 7:00 AM Central start leaves 30 minutes before desired 7:30 readiness; verify the first recurring completion. Mac must be online. Optional missing-source features do not block core text publication.

The writer reads private `cloud-routine-state.json`. An enabled edition sets `routineEnabled: true` and `routine: {kind: "cloud", startTime: "07:00", readyBy: "07:30", startsOn: "2026-10-04", confirmedAt: "<actual confirmation timestamp>", localCron: false, notifications: false}`. Do not copy the automation ID into page data. Legacy disabled editions remain readable. The page reports the recorded schedule's confirmation time and Mac dependency without asserting that every optional source is connected.
