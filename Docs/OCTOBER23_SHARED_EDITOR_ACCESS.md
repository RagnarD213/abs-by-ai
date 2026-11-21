# October 23: shared editing assets and queue

Dan finalized exercise names and Color C on October 25. Claude and Codex share159 checked native4K B-roll clips, including26 favorites. All usable takes/angles are retained, and originals are preserved. Read `.claude/skills/_shared/cliplib/README.md` before using the footage.

## Retrieve finished B-roll

From the main project folder:

```bash
python3 .claude/skills/_shared/cliplib/clip_library.py find "cable crunch" --favorite
python3 .claude/skills/_shared/cliplib/clip_library.py find "rear delt" --equipment machine
python3 .claude/skills/_shared/cliplib/clip_library.py show B0574
```

The private shared catalog is `Media/clip-library/catalog.json`. `show` resolves the master, original range, Drive ID and checks. Use the full-quality native master, not a small review proxy. The main library is `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed/`; verified copies exist on Expansion and Drive. Inspect the actual motion before choosing a rep. Unknown teaching intent remains unknown; correct-demonstration searches exclude it. Do not ask Dan to reconfirm names or Color C.

[Finished gallery](http://127.0.0.1:9205/) · [Shared Drive library](https://drive.google.com/drive/folders/1Hby8O4mB4HZS341qvrVKHSHyCGBgP8mi) · [Searchable Sheet](https://docs.google.com/spreadsheets/d/1MNzrN71RgrmU2-INsx-8nBD3GuX2PNJZMOxEhwGUBpQ/edit).

A cloud editor can retrieve `catalog.json` and `October-23-shared-library-usage.md` from that existing Drive library, then use the same permanent IDs and Drive masters. Do not create a competing catalog. A local editor uses the main project private catalog; an isolated Git checkout does not automatically contain ignored media/index files.

## See the filmed videos in Claude

[Existing Claude Edit Queue](https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs). Search `10/23`:30 Shorts DS-76..DS-105 and two long-forms RO-37..RO-38. The older artifact enumerates Dedicated Shorts subgroups, so these spoken Shorts use its supported **Talking** display group. Their actual shoot remains in `roll`, the master section and private intake maps. Unsupported `sub` values can be counted yet omitted from the display. The two long-forms appear under Organic long-form.

Each brief links its exact private source/take/mic/hook map under `Media/footage-index/shoot-20261023/queue-jobs/` and appropriate B-roll IDs. Every usable library take is available, even if the brief only names initial suggestions. Spoken working sources resolve verified Extreme copies; gym originals remain on Expansion. No edits were launched, unattended execution remains disabled and the dispatcher stays paused.

Both tools now default to the existing dedicated-client `gdrive_backup:` connection. Overrides are `EDIT_QUEUE_DRIVE_REMOTE` and `CLIPLIB_DRIVE_REMOTE`. Existing Drive file/folder IDs and sharing stay the same; the old shared Google client has returned rate-limit errors.

October26 checks: all32 jobs visibly present in the signed-in native Claude queue; all159 native masters readable locally and current Drive file sizes/MD5s verified;115 source sidecars and eight shared-library retrieval checks passed. The separate native fallback database was not written or marked synced. Its documented version-guarded mirror workflow remains available; live Drive display works independently.
