#!/usr/bin/env python3
"""Daily date-preserving top-up of a privately authorized frozen cohort."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, build_opener

from master_queue import Inventory, locked, _reconcile_locked, plan_topup
from social_daily import load_module, private_json, NoRedirect


class AuthorizedInventory:
    def __init__(self, inventory, policy, require_enabled=False):
        if (policy.get('version') != 1 or not isinstance(policy.get('enabled'),bool)
                or policy.get('windowDays') != 30 or policy.get('cap') != 200
                or not policy.get('authorizedBy') or not isinstance(policy.get('placementIds'), list)):
            raise ValueError('Invalid bounded authorization')
        if require_enabled and policy['enabled'] is not True:
            raise ValueError('Scheduling activation is disabled pending explicit human confirmation')
        self.inventory = inventory
        self.allowed = set(policy['placementIds'])

    def records(self):
        # Identity binds every payload field and exact authorized date. A changed
        # caption, asset, account, platform or date cannot inherit authorization.
        return [r for r in self.inventory.records() if r['id'] in self.allowed and r['approval']['status'] == 'approved']

    def submission(self, key):
        return self.inventory.submission(key)

    def submitted(self, *args):
        return self.inventory.submitted(*args)


def single_create(api, key, body):
    # Do not use the legacy adapter's POST retry policy. Even a timeout is an
    # uncertain submission, recorded before this one request by reconciliation.
    request = Request(api.BASE + '/posts', data=json.dumps(body).encode(), method='POST',
                      headers={'blotato-api-key': key, 'Content-Type': 'application/json'})
    with build_opener(NoRedirect()).open(request, timeout=30) as response:
        return json.loads(response.read())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', type=Path, required=True)
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--authorization-file', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.authorization_file.stat().st_mode & 0o077:
        parser.error('Authorization file must be private')
    with locked(args.state_dir) as directory:
        inventory = Inventory(directory)
        scoped = AuthorizedInventory(inventory, json.loads(args.authorization_file.read_text()), require_enabled=args.apply)
        api = load_module('existing_blotato', args.project_root / 'scripts/blotato/danrosefit_migration.py')
        guard = load_module('existing_guard', args.project_root / 'scripts/blotato/ad_guard.py')
        checks = json.loads((directory / 'social-url-checks.json').read_text())
        key = api.api_key()
        fetch = lambda: api.fetch_schedules(key)
        now = datetime.now(timezone.utc)
        plan = plan_topup(scoped, fetch(), now, guard.assert_organic, checks)
        private_json(directory / 'daily-topup-plan.json', plan)
        before = {r['id']: inventory.submission(r['id']) for r in scoped.records()}
        if args.apply:
            _reconcile_locked(scoped, fetch, lambda body: single_create(api, key, body), now,
                              guard.assert_organic, plan['planDigest'], checks)
        created = [r['id'] for r in scoped.records() if before[r['id']] != 'confirmed' and inventory.submission(r['id']) == 'confirmed']
        receipt = {'checkedAt': now.isoformat(), 'apply': args.apply, 'authorization': 'frozen_approved_cohort',
                   'planDigest': plan['planDigest'], 'existingCount': plan['existingCount'], 'cap': 200,
                   'created': created, 'held': plan['held'], 'overflow': plan['overflow'],
                   'scheduleChanged': bool(created), 'deleted': 0, 'rescheduled': 0}
        private_json(directory / 'daily-topup-receipt.json', receipt)
        print(json.dumps(receipt))


if __name__ == '__main__':
    main()
