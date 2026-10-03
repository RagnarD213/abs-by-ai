# Mac-only morning brief publication

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

## Verification and remaining work

Synthetic tests cover forged signatures, wrong keys, changed bytes, wrong methods/paths, expired/future timestamps, persistent replay rejection, concurrent nonce claims, unavailable database, bounded bodies and key-file permissions. They preserve the independent Google owner denial/session tests. Real signed publication and owner readback must be recorded separately; local test success alone is not production proof.

Pending end-to-end features: cloud automation invoking the linked Mac and finishing by 7:30 AM America/Chicago; daily fresh image generation through an agreed supported capability; fresh YouTube watch-history actions; practical model-release applicability; Trello ranked inputs; verified free-generation, new-trial and paid-customer mappings. First newsletter captures are independently verified; Ads signal labels are not those outcomes. Missing sources remain explicit and unknown values stay null. Publication does not enable the routine, and neither CLI changes scheduling.
