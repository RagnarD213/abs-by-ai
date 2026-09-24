#!/usr/bin/env node
/* eslint-disable no-console */
//
// BRAND TIGHTEN (Dan, 2026-09-24). The Brand - Search - US campaign spent $142.94 in 30 days and
// not one search contained "abs by ai": Google's exact-match close variants read "abs by ai" as
// "ai abs" and served it to "ai six pack", "abs editor", "ai ab generator". Dan's decisions:
//   1. Brand shows only for Abs By AI searches -> generic negatives on the brand ad group
//      (campaign-level negatives moved down so they cannot block the name group).
//   2. New "Brand - Dan Rose" ad group: his name + something unmistakably his, never the bare name,
//      with heavy negatives for the other Dan/Daniel Roses (chef, NYC developer, Facebook VP...).
//   3. The 7 generic terms that converted move to Non-Brand (AI Abs Generator group).
//   4. Brand bidding -> Maximize Clicks with a $2.00 CPC ceiling.
// scripts/ads/brand-guard.js then negates, every run, any search term that slips through.
//
//   node scripts/ads/oneoff/brand-tighten-20260924.js [--dry-run]
//
const ads = require('../api/client.js');

const CID = '3427170837';
const CAMPAIGN = '24086091285';                // Brand - Search - US
const BRAND_AG = '204012081332';               // "Ad group 1" -> "Brand - Abs By AI"
const NONBRAND_AG = '194615821330';            // Non-Brand: AI Abs Generator
const camp = `customers/${CID}/campaigns/${CAMPAIGN}`;
const ag = (id) => `customers/${CID}/adGroups/${id}`;
const NEW_AG = `customers/${CID}/adGroups/-1`;

const kw = (group, text, matchType, negative = false) => ({
  adGroupCriterionOperation: { create: { adGroup: group, status: 'ENABLED', negative, keyword: { text, matchType } } },
});

// ---- 1. the brand ad group
const EXISTING_CAMPAIGN_NEGATIVES = ['6 pack', 'ab generator', 'abs generator', 'abs ai', 'give me abs', 'ai ab', 'abs creator', 'ai abs'];
const CAMPAIGN_NEG_IDS = ['260570474', '36714172529', '368867247316', '560402698209', '813793717857', '1392514459422', '1966364946842', '2476063742764'];
// Single words a real "abs by ai" search never contains. Broad negatives match the word anywhere.
const BRAND_BROAD_NEG = ['generator', 'generate', 'generated', 'editor', 'edit', 'editing', 'maker', 'creator', 'create',
  'filter', 'photoshop', 'sixpack', '6pack', 'fake', 'amy', 'bodyfit', 'workout', 'workouts', 'exercise', 'exercises'];
const BRAND_PHRASE_NEG = ['six pack', 'six abs', 'dan rose', 'daniel rose', 'danrose', 'danielrose', 'danrosefit'];
const BRAND_EXACT_NEG = ['abi', 'abs edit', 'abs', 'ai'];

// ---- 2. the Dan Rose ad group
const NAMES = ['dan rose', 'daniel rose'];
const MODIFIERS = ['abs by ai', 'absbyai', 'sixpackabs', 'sixpackabs.com', 'six pack abs', '6 pack abs', 'six pack',
  'six pack shortcuts', 'sixpackshortcuts', 'abs', 'fitness', 'social response marketing', 'youtube marketing',
  '15 steps to profitable youtube marketing'];
const NAME_EXTRA_PHRASE = ['danrosefit', 'dan rose fit'];
const NAME_EXACT = ['danrosefit', 'danrose abs by ai', 'danielrose abs by ai', 'danrose absbyai', 'danielrose absbyai',
  'danrose sixpackabs', 'danielrose sixpackabs', 'danielrose sixpackabs.com', 'danrose sixpackabs.com',
  'danrose sixpackshortcuts', 'danielrose sixpackshortcuts', 'danrose abs', 'danielrose abs'];
// The other Dan / Daniel Roses: the chef (Le Coucou, Spring, La Bourse et la Vie in Paris), the NYC real-estate
// developer (Rose Associates), the ex-Facebook VP (Coatue), athletes, musicians, lawyers, doctors, obituaries.
const NAME_BROAD_NEG = ['chef', 'restaurant', 'restaurants', 'coucou', 'bourse', 'spring', 'recipe', 'recipes', 'cook',
  'cooking', 'cuisine', 'menu', 'reservation', 'reservations', 'michelin', 'food', 'obituary', 'obituaries', 'funeral',
  'died', 'death', 'attorney', 'lawyer', 'law', 'esq', 'realtor', 'realty', 'developer', 'associates', 'md', 'doctor',
  'dr', 'physician', 'dentist', 'dds', 'orthodontist', 'surgeon', 'nurse', 'professor', 'phd', 'university', 'linkedin',
  'facebook', 'coatue', 'amazon', 'vp', 'venture', 'ventures', 'investor', 'actor', 'film', 'movie', 'imdb', 'music',
  'band', 'singer', 'guitar', 'song', 'lyrics', 'album', 'golf', 'golfer', 'baseball', 'basketball', 'football',
  'hockey', 'soccer', 'nba', 'nfl', 'mlb', 'derrick', 'pete', 'jalen', 'axl', 'amber', 'justin', 'ruby', 'judge',
  'court', 'arrest', 'arrested', 'mugshot', 'sheriff', 'police', 'pastor', 'church', 'rabbi', 'architect', 'painter',
  'artist', 'photographer', 'wedding', 'florist', 'flowers', 'garden', 'wine', 'hotel', 'paris', 'nyc', 'brooklyn',
  'manhattan', 'chicago', 'london', 'wikipedia', 'wiki', 'wife', 'married', 'jobs', 'hiring'];
const NAME_PHRASE_NEG = ['real estate', 'new york', 'net worth', 'rose associates'];

// ---- 3. converters that move to Non-Brand (each converted once in Brand, Aug 25 - Sep 23)
const CONVERTERS = ['six pack ai', 'ai six pack', 'ai sixpack', 'give me abs ai', 'abs editor ai', 'abs creator ai', 'six pack generator'];

const ops = [];

// 4. bidding: Maximize Clicks, $2.00 ceiling
ops.push({ campaignOperation: { update: { resourceName: camp, targetSpend: { cpcBidCeilingMicros: '2000000' } }, updateMask: 'target_spend.cpc_bid_ceiling_micros' } });

// rename the brand ad group
ops.push({ adGroupOperation: { update: { resourceName: ag(BRAND_AG), name: 'Brand - Abs By AI' }, updateMask: 'name' } });

// move campaign negatives down to the brand ad group
for (const id of CAMPAIGN_NEG_IDS) ops.push({ campaignCriterionOperation: { remove: `customers/${CID}/campaignCriteria/${CAMPAIGN}~${id}` } });
for (const t of EXISTING_CAMPAIGN_NEGATIVES) ops.push(kw(ag(BRAND_AG), t, 'PHRASE', true));
for (const t of BRAND_BROAD_NEG) ops.push(kw(ag(BRAND_AG), t, 'BROAD', true));
for (const t of BRAND_PHRASE_NEG) ops.push(kw(ag(BRAND_AG), t, 'PHRASE', true));
for (const t of BRAND_EXACT_NEG) ops.push(kw(ag(BRAND_AG), t, 'EXACT', true));

// the name ad group
ops.push({ adGroupOperation: { create: { resourceName: NEW_AG, campaign: camp, name: 'Brand - Dan Rose', status: 'ENABLED', type: 'SEARCH_STANDARD' } } });
for (const n of NAMES) for (const m of MODIFIERS) ops.push(kw(NEW_AG, `${n} ${m}`, 'PHRASE'));
for (const t of NAME_EXTRA_PHRASE) ops.push(kw(NEW_AG, t, 'PHRASE'));
for (const t of NAME_EXACT) ops.push(kw(NEW_AG, t, 'EXACT'));
for (const t of NAME_BROAD_NEG) ops.push(kw(NEW_AG, t, 'BROAD', true));
for (const t of NAME_PHRASE_NEG) ops.push(kw(NEW_AG, t, 'PHRASE', true));
// the bare name must never serve on its own
for (const t of ['dan rose', 'daniel rose', 'danrose', 'danielrose']) ops.push(kw(NEW_AG, t, 'EXACT', true));

const H = (text, pinnedField) => (pinnedField ? { text, pinnedField } : { text });
ops.push({ adGroupAdOperation: { create: { adGroup: NEW_AG, status: 'ENABLED', ad: {
  finalUrls: ['https://absbyai.com/start'],
  responsiveSearchAd: {
    path1: 'Dan-Rose',
    headlines: [
      H("Dan Rose's Abs By AI", 'HEADLINE_1'),
      H('Abs By AI by Dan Rose'),
      H('Built By Dan Rose'),
      H('Abs By AI - Official Site'),
      H('See Yourself With Abs'),
      H('Visualize Yourself with Abs'),
      H('AI Six-Pack Preview Tool'),
      H('See Your Goal Before You Start'),
      H('Upload a Photo. See Your Abs.'),
      H('Make AI Image Of You With Abs'),
    ],
    descriptions: [
      H('Dan Rose built Abs By AI to show you with abs before you start training.'),
      H('Upload a photo, get an AI preview of a leaner you in seconds. Free to try.'),
      H('Visualize yourself with six pack abs, then get an AI workout and nutrition plan.'),
      H('The official Abs By AI site from Dan Rose. See your goal, then get the plan.'),
    ],
  },
} } } });

// converters into Non-Brand
for (const t of CONVERTERS) { ops.push(kw(ag(NONBRAND_AG), t, 'EXACT')); ops.push(kw(ag(NONBRAND_AG), t, 'PHRASE')); }

(async () => {
  const dryRun = process.argv.includes('--dry-run');
  console.log(`${ops.length} operations${dryRun ? ' (validate only)' : ''}`);
  const res = await ads.mutate(ops, { dryRun, note: 'Brand tighten + Dan Rose name group + converters to Non-Brand (Dan 2026-09-24)' });
  console.log(JSON.stringify(res, null, 1).slice(0, 3000));
})().catch((e) => { console.error(e.message || e); process.exit(1); });
