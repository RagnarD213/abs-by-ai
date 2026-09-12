# Corpus plan fixtures

A delivery-gate row that needs to know what the build INTENDED reads a `plan.json`. For a corpus
entry the build's own plan is usually long gone (it lived in `Media/`, which is gitignored), so the
minimum a given row needs is reconstructed here.

**These files are INPUTS, never verdicts.** A plan may say where a graphic sits or which recording
contains a banned screen. It may never say whether the file passes. If you find yourself writing a
number here to make a row go green, you are relaxing a bound — stop, and read
`../README.md`.

Each fixture records how its values were obtained.
