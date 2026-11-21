'use strict';
// Map verified tag signals, without silently relabeling them as business totals.
const DEFINITIONS = {
  first_image_response: {
    id: '7704441548', name: 'Free Generation Started', label: 'KqDxCMzl4dkcEJvEqLNE',
    display: 'First image-response conversion (Ads)',
    definition: 'Tag fires after a successful image response, including locked/chooser responses. Browser dedupe lasts 400 days. Billing/free status is not checked.',
    evidence: ['public/index.html:11457', 'public/index.html:3706', 'Docs/DGEN_CONVERSION_CAMPAIGN.md:19'],
  },
  membership_checkout: {
    id: '7704441545', name: 'Trial Signup', label: 'AqLTCMnl4dkcEJvEqLNE',
    display: 'Membership checkout conversion (Ads)',
    definition: 'Client reports non-restore membership checkout completion. Returning-member checkouts can be counted, so this is not a verified new-trial total.',
    evidence: ['public/index.html:8452', 'public/index.html:8592', 'server.js:6686'],
  },
  website_paid_reporting: {
    id: '7703335439', name: 'Subscribe', label: 'dQUqCI-kntkcEJvEqLNE',
    display: 'Paid membership website reporting (Ads)',
    definition: 'Website attribution signal after the server marks a paid membership conversion. Excludes the offline channel and is not the total number of paying customers.',
    evidence: ['public/index.html:8081', 'server.js:7139', 'server.js:7201'],
  },
};

function tagTargets(action) {
  return [...new Set((action.tagSnippets || []).flatMap(snippet =>
    [...(snippet.eventSnippet || '').matchAll(/AW-\d+\/[A-Za-z0-9_-]+/g)].map(match => match[0])))];
}

function verified(actions) {
  const output = {};
  for (const [name, definition] of Object.entries(DEFINITIONS)) {
    const action = actions.find(item => String(item.id) === definition.id);
    if (!action || action.name !== definition.name || action.type !== 'WEBPAGE'
        || !tagTargets(action).includes('AW-18361229851/' + definition.label)) continue;
    output[name] = {status: 'verified_tag', actionIds: [definition.id],
      label: definition.display, definition: definition.definition, evidence: definition.evidence};
  }
  return output;
}

function attach(campaigns, definitions) {
  for (const campaign of campaigns) {
    campaign.stageSignals = {};
    for (const [name, definition] of Object.entries(definitions)) {
      const matched = campaign.observedActions.filter(action => definition.actionIds.includes(action.id));
      campaign.stageSignals[name] = {...definition, yesterday: matched.reduce((sum, item) => sum + item.yesterday, 0),
        last7d: matched.reduce((sum, item) => sum + item.last7d, 0)};
    }
  }
  return campaigns;
}

module.exports = {verified, attach, tagTargets};
