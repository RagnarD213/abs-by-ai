---
name: railway-graphql-and-cron
description: "How to create/configure a Railway service (cron schedule, start command, variables) from a session via GraphQL, plus two traps in the secrets cache that bite scripts running on Dan's Mac"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 7bf4d150-83e3-4ddf-8a18-8f9a0f91bef7
  modified: 2026-09-02T23:27:18.818Z
---

**Railway GraphQL works from a session** (verified 2026-09-02, used to create the `auto-boost` cron service):
endpoint `https://backboard.railway.com/graphql/v2`, header `Authorization: Bearer <accessToken>` where the
token is `user.accessToken` in `~/.railway/config.json` (NOT `user.token` — that one returns "Not Authorized").
Cloudflare 403s Python's default urllib user agent — send `User-Agent: curl/8.7.1` or use curl.
Mutations that matter: `serviceCreate(input:{projectId, environmentId, name})` (no source → nothing deploys),
`serviceInstanceUpdate(serviceId, environmentId, input:{startCommand, cronSchedule, restartPolicyType})`,
`variableCollectionUpsert(input:{projectId, environmentId, serviceId, variables:{…}, skipDeploys:true})`,
then `serviceConnect(id, input:{repo:"RagnarD213/abs-by-ai", branch:"main"})` LAST so the first build already
has the cron config. Project `f44b4c7e-78af-4c82-8138-37b035088dbf`, env `34c2df62-2119-4231-922d-8f736747d0e4`.
The CLI (`railway add`) cannot set a cron schedule or start command; only the GraphQL API / dashboard can.
Recipe script: it was written to the session scratchpad, and the flow is documented in `Docs/AUTO_BOOST.md`.

**Secrets-cache traps** (`~/.absbyai-secrets.env` is a dump of `railway variables --kv`):
- It contains `RAILWAY_ENVIRONMENT`, `RAILWAY_SERVICE_ID` etc., so a script cannot use those to tell
  "am I on Railway" from "am I on the Mac". Prefer `DATABASE_PUBLIC_URL` when set instead.
- `DATABASE_URL` in it is the INTERNAL host (`postgres.railway.internal`), which does not resolve from the Mac.
  `DATABASE_PUBLIC_URL` (from `railway variables --service Postgres --kv`) was added to the file 2026-09-02;
  scripts that run locally against prod Postgres should use it (`ssl: { rejectUnauthorized: false }`).

**Why:** creating the cron service through the dashboard would have meant a browser takeover; the API path is
scriptable and repeatable. See [[railway-deploy-workflow]].
**How to apply:** for any new scheduled job, reuse this order; give the cron service only `DATABASE_URL`
(internal) so scripts' "public URL wins when present" logic stays correct.
