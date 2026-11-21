// Audio bleeps, in SOURCE time. Dan's call 2026-08-10: short C keeps the bubble-gut
// explanation but the word "steroids" is bleeped.
//
// Windows are the Whisper word spans padded by 50ms each side. The neighbouring words are
// contiguous ("of|steroids|they", "by|steroids|It's"), so the padding clips ~50ms off each
// neighbour -- imperceptible, and under-covering the target word is the worse failure.
const BLEEPS = {
  C: [
    [353.69, 354.13],   // "...guys who are on a lot of [steroids] they get what's called bubble gut"
    [373.67, 374.41],   // "...bubble gut caused by [steroids]. It's effective at reducing..."
  ],
};

// Words masked in the burned-in captions for those same segments.
const BLEEP_WORDS = { C: ['steroids'] };

module.exports = { BLEEPS, BLEEP_WORDS };
