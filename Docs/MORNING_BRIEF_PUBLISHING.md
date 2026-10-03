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

The external cloud automation is enabled daily at 7:00 AM America/Chicago from October 4, targeting a 7:30 page without routine notifications. It invokes the Mac runner and includes connected inbox/calendar, built-in image generation with dated fallback, practical model-release checks and fresh-watch-feed use. No local cron/launchd job exists. First automated completion and these optional outputs remain unproven. Trello is deferred; free-generation/new-trial/paid mappings remain unverified. Missing sources stay explicit and unknown values stay null. Publication itself does not enable or alter scheduling.

## October 3 production proof and repeatable sequence

The approved hero and dated edition were published with the Mac signer on production commit `86dff85`, deployment `8b804e51-aa66-43a4-be75-6e8a64dc6bcd`. Receipts matched the image digest and edition date. A separate read-only transaction verified that the private database contains the exact validated edition and image bytes. Twelve live checks passed: same-edition publication, replay, forged/expired/future signatures, changed bytes, cross-route/query-path signatures, unsigned publication, signed read denial and anonymous page redirect. The private signing key was never emitted or transmitted. Owner browser readback and device persistence remain separate checks.

Repeat in order: refresh both queue sources, run `collect_inputs.py --live`, have the parent writer combine the fresh private inputs with connected Gmail/Calendar and write a new dated edition, validate it, optionally publish an approved image, then publish the edition and verify receipts. Never reuse the October 3 assembly script on later dates; its proof context is fixed. Exact Mac paths, argv sequences and receipts are recorded in private `daily-command-sequence.json` outside Git.

Measured one-run timings: queue refresh 7.42 seconds, local collection 14.28 seconds, image upload 2.54 seconds and edition upload 0.89 seconds. The 25.13-second sum excludes writer/model time, connected inbox/calendar intake, new image generation and external failures. It is not a guaranteed schedule runtime. The enabled 7:00 AM Central start leaves 30 minutes before desired 7:30 readiness; verify the first recurring completion. Mac must be online. Optional missing-source features do not block core text publication.

The writer reads private `cloud-routine-state.json`. An enabled edition sets `routineEnabled: true` and `routine: {kind: "cloud", startTime: "07:00", readyBy: "07:30", startsOn: "2026-10-04", confirmedAt: "<actual confirmation timestamp>", localCron: false, notifications: false}`. Do not copy the automation ID into page data. Legacy disabled editions remain readable. The page reports the recorded schedule's confirmation time and Mac dependency without asserting that every optional source is connected.
