// AI cover clips placed over the joins, rev 3.
//
// Dan: "Cover that awkward cut with an AI-generated clip illustrating what's being said in the
// video at the time." One per join WE created by removing a pause or a clause - the picture
// cuts inherited from the source edit stay covered by the punch alternation, which he approved.
//
// An insert replaces PICTURE only, straddling the join: it takes `pre` seconds off the end of
// the outgoing shot and the rest off the start of the incoming one. Audio is continuous
// underneath and never touched, so nothing can drift.
//
// `afterPiece` is the index of the piece the join follows. Durations are deliberately short -
// long enough to bridge the cut and read as an illustration, short enough that the short stays
// a talking-head video and not a stock reel.
// `in` is the point inside the 8s generated clip where its content reads most clearly -
// chosen by looking at a frame strip of each, not by taking the head of the file.
module.exports = [
  // 4.6 is where the lit muscles are still in frame AND the brain begins to light, so the
  // insert shows both halves of the line it covers.
  { seg: 'H', afterPiece: 0, clip: 'h1', dur: 2.20, pre: 0.90, in: 4.60 },
  { seg: 'H', afterPiece: 1, clip: 'h2', dur: 1.80, pre: 0.75, in: 2.20 },
  { seg: 'C', afterPiece: 0, clip: 'c1', dur: 1.80, pre: 0.75, in: 0.80 },
  { seg: 'C', afterPiece: 1, clip: 'c2', dur: 1.90, pre: 0.80, in: 0.60 },
  { seg: 'J', afterPiece: 1, clip: 'j1', dur: 1.90, pre: 0.80, in: 0.80 },
  { seg: 'M', afterPiece: 0, clip: 'm1', dur: 2.00, pre: 0.85, in: 0.80 },
  { seg: 'D', afterPiece: 0, clip: 'd1', dur: 2.00, pre: 0.85, in: 1.80 },
  // ⚠ 0.2: this clip fills with steam after ~2s and the iron stops being readable. The head
  // is the only window where it reads as ironing rather than as haze.
  { seg: 'D', afterPiece: 1, clip: 'd2', dur: 2.00, pre: 0.85, in: 0.20 },
  { seg: 'E', afterPiece: 1, clip: 'e1', dur: 1.90, pre: 0.80, in: 1.60 },
];
