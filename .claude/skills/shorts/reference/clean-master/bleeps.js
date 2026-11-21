// No bleeps in this batch.
//
// Dan's eight picks contain no profanity. The two candidates that did - [I] "I just
// uncontrollably shit myself" and [F]'s Zepbound mention - are not in the selection, [I]
// on its flags and [F] because Dan did not rule on the drug name. If either is added later,
// the bleep mechanism is intact: windows in SOURCE time here, shifted into piece-local time
// at render, and qc.js asserts the tone is really there and the word is not in the captions.
const BLEEPS = {};
const BLEEP_WORDS = {};
module.exports = { BLEEPS, BLEEP_WORDS };
