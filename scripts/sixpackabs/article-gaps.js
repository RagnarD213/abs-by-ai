'use strict';
/**
 * SixPackAbs.com article gaps — the early warning.
 *
 * Every public video gets a page on sixpackabs.com, and every page should get a
 * real article (sixpackabs/articles/README.md). The daily routine and
 * `python3 sixpackabs/articles/gap.py` are what actually close a gap; gap.py
 * checks the LIVE pages and is the authority.
 *
 * This module only makes a new gap visible within minutes instead of at the next
 * daily run: after each five-minute feed refresh the server calls `check()`, and
 * a public video with no `sixpackabs/articles/<id>.md` and no entry in
 * `skips.json` is logged once per process:
 *
 *   sixpackabs article gap: <id> "<title>" (short|long) public since <time> ...
 *
 * Find them with `railway logs --service abs-by-ai | grep "article gap"`.
 * The folder is read on every check, so a deploy that adds the file ends the gap.
 *
 * Tests: node scripts/sixpackabs/article-gaps.test.js
 */

const fs = require('fs');
const path = require('path');

// Pure: which public videos have neither an article file nor a recorded skip.
function findArticleGaps(videos, articleIds, skipIds) {
  return (videos || []).filter((v) => v && v.id && !articleIds.has(v.id) && !skipIds.has(v.id));
}

function readArticleFolder(dir) {
  // A YouTube id is 11 characters, so README.md and the TBD-*.md drafts drop out.
  const articleIds = new Set(
    fs.readdirSync(dir).filter((f) => /^[A-Za-z0-9_-]{11}\.md$/.test(f)).map((f) => f.slice(0, -3)),
  );
  let skipIds = new Set();
  try {
    skipIds = new Set(Object.keys(JSON.parse(fs.readFileSync(path.join(dir, 'skips.json'), 'utf8'))));
  } catch (e) { /* no skip list is the same as an empty one */ }
  return { articleIds, skipIds };
}

function createArticleGapLogger({ dir, log = console, readFolder = readArticleFolder } = {}) {
  const logged = new Set();

  // `channel` is the feed document ({ videos: [...] }). Never throws: a broken
  // warning must not break the feed refresh that called it.
  function check(channel) {
    try {
      if (!channel || !Array.isArray(channel.videos)) return [];
      const { articleIds, skipIds } = readFolder(dir);
      const gaps = findArticleGaps(channel.videos, articleIds, skipIds);
      for (const v of gaps) {
        if (logged.has(v.id)) continue;
        logged.add(v.id);
        log.warn(`sixpackabs article gap: ${v.id} "${v.title}" (${v.type}) public since ${v.publishedAt} has no article file. Run: python3 sixpackabs/articles/gap.py`);
      }
      return gaps;
    } catch (e) {
      log.error(`sixpackabs article gap check failed: ${e.message}`);
      return [];
    }
  }

  return { check };
}

module.exports = { createArticleGapLogger, findArticleGaps, readArticleFolder };
