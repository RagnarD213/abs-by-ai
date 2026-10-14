"""RA-05 round 2: THE OPENING CARD's segment table (Dan, 2026-10-14: "in the first 3 seconds, I want to show the full
generation functionality, but very sped up, so that the after shows for a full second at the end. It goes through adding
the photo and then loading in less than 2 seconds").

Read frame by frame from B0049 (1320x2868, 29.97): 0-2.5 s the photo-crop screen (NEVER, ad-edit lesson 15); 3.0 s the photo
in place on "Visualize Yourself With Abs"; 7.35 s "Peak" selected; 7.90 s the Generate button pressed; 8.0-24.4 s loading
(29 % to 91 %); 25.0-27.6 s "Meet the new you" BEFORE/AFTER (NEVER); 28.0 s on, the result alone (confetti to about 29 s);
the email form sits below y 1770 and every window ends at or above it.
A plain fast cut through five moments (not one smooth ramp): each step reads at its own speed, and the loading bar visibly
runs. Rows: (source in, source out, output frames, crop y of the 1320x1600 window, what it shows).
"""
SEGS = [
    (3.05, 3.45, 12, 600,  "photo added: 'Visualize Yourself With Abs' with his photo in place (real time)"),
    (7.25, 7.98, 16, 1200, "options: 'Peak' is tapped, then 'Generate my future self' is pressed (1.4x)"),
    (9.65, 12.40, 10, 520, "loading 40 % -> 64 % (8.2x)"),
    (13.20, 24.40, 20, 340, "loading 76 % -> 91 % (16.8x)"),
]
RESULT_T0 = 28.0          # after 'Meet the new you' (to about 27.6 s); round 1's trap
RESULT_Y = 170            # round 1's window: title + result picture, email form out
RESULT_F = sum(s[2] for s in SEGS)     # the AI result starts at this card frame (58 = 1.935 s)
SCAN_X0, SCAN_W = 150, 1620            # A0044: the four callouts span x 160-1740 of 1920
SCAN_T0 = 1.0                          # all four callouts are up by 1.0 s; natural speed from there
