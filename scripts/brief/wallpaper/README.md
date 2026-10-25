# Private Mac wallpaper reader

Activation requires Dan's explicit approval for this separate persistent credential
and grant. The implementation alone does not enroll a Mac or grant access.

- Owner-only web favorites retain exact original bytes and image provenance.
- A separate Ed25519 key lives in the login Keychain, never a browser token or
  publishing key. Only its public key is configured as BRIEF_WALLPAPER_PUBLIC_KEY.
- Its signed, replay-protected requests can fetch active favorite metadata/bytes
  and submit an integration receipt. They cannot read the brief or mutate favorites,
  publish content, or access product data. Removing the variable revokes the grant.
- A user LaunchAgent runs once per minute, making outbound HTTPS requests only.
  No listener, public feed, new paid service or Full Disk Access is required.
- Originals are digest-verified in a private local cache and never deleted by removal.
  Removed favorites stop being eligible after the next successful sync. Cached
  favorites can keep rotating while offline; the website marks stale sync pending.
- Each connected screen has its own 30-minute deadline and random choice, with
  distinct choices where possible and immediate repeats avoided where reasonable.
  Mac readback, three screens, the current manifest and 1800-second configuration
  are required before a signed receipt is submitted. An empty collection stays pending.

After approval, from this trusted checkout:

1. `python3 scripts/brief/wallpaper/install.py install` compiles and installs the
   helper, enrolls the Keychain key, backs up current wallpaper paths and prepares
   the LaunchAgent without starting it. Capture only the public-key output.
2. Configure that public key on the existing site service using Railway.
3. `python3 scripts/brief/wallpaper/install.py start` starts the reader.
4. On the owner-authenticated brief, save the actual displayed hero. Verify exact
   original digests in the local cache, all three AppKit wallpaper paths and the
   signed status. Observe the next 30-minute transition on each screen before
   reporting complete end-to-end rotation.

Stop with `python3 scripts/brief/wallpaper/install.py stop`, revoke the Railway
public-key variable, and use `wallpapers-before.json` to restore prior settings if
requested. Keep originals and archived provenance. Do not remove the Keychain
entry, cache or backups without an explicit deletion request.
