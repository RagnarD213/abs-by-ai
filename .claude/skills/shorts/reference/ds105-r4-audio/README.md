# DS-105 R4: selected gentle cleanup B

Dan chose B from R3 and requested it on the full64s Short. R4 reuses the prepared fullB PCM; never denoise that processed PCM again. The original naturalwarmth EQ and expander remain; no new compressor/dereverb. Source-specific choice, not a new house default.

Master061deb744eb1e83cf1917727095214c8e4ea68ffebf56d9f85042d80694eebe2; review91764be9410c4293de29e5815c801ce4cc4097c78f341cf06df9f5be79d16730. Both picture packet streams are byte-identical to R2 originals. One new AAC encode is shared by bothcopies. B audition to fullPCM correlation exceeds.9999999 with constant auditiongain only. No further FFTdelay correction was applied; existing1200sample correction is retained and finalrelative delay0samples.

Canonical work `/Volumes/Extreme/_edit_work/DS-105/round4`. These scripts are archival source-specific recipes and expect that external working-tree layout, soleowner controller and immutabledecisions. Do not run the archival copies in place or rebuild delivered media. Source decisions/provenance and complete gates are in the canonical folder.

Default reviewplayer muted; task-driven playback verifies muted state before each action and leavespaused/muted. Exported audio is intact.
