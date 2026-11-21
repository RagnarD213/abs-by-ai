"""Edit desk presentation records. Closed receipts identify one exact handoff."""
import copy
import re
from urllib.parse import urlsplit

# (job, register's handoff timestamp). A subsequent release has a new timestamp.
CLOSED = {
    ('EXDEMO-FLOW2', 1793993514.204297): 'Docs/EXERCISE_DEMO_FLOW_PILOT_20261105.md: both retry demos installed',
    ('EXDEMO-CODEX3', 1794345621.5863192): 'Docs/EXERCISE_DEMOS_CODEX_R3_20261110.md: stopped with no acceptable curl',
    ('REALDEMOS-B03', 1794758985.862941): 'Handoffs/real-demos/next-round-20261115.md: installed',
    ('REALDEMOS-B08', 1794783198.193829): 'Docs/REALDEMOS_B08_FLY_INSTALLED_20261115.md: five installed, swing on pickup list',
    ('REALDEMOS-B09', 1794808928.4621289): 'Docs/REALDEMOS_B09_INSTALLED_20261116.md: approved and installed',
    ('RO-24', 1794778200.15375): 'Docs/CELEBRITY_DIETS_R6_UPLOAD_RECEIPT_20261115.md: final approved and uploaded',
    ('SRM-JV-R2', 1794615244.2982929): 'Superseded by Joint Vigor round 4 production on M6',
}

def title(job, catalog, registered=None):
    if job == 'DS-98':
        return 'The Only 5 Machines You Need'
    if job.startswith('SRM-JV-R') and job[8:].isdigit():
        return 'Joint Vigor VSL · Round ' + job[8:]
    if job == 'SRM-GOLDENROOTS-JOINTVIGOR':
        return 'Joint Vigor VSL'
    if job == 'CLIPLIB-V2':
        return 'Vertical AI Dan Clip Library · Round 1'
    batch = re.fullmatch(r'REALDEMOS-B(\d+)', job)
    if batch:
        return 'Real Exercise Demos · Batch ' + str(int(batch[1]))
    name = catalog.get(job, {}).get('title') or registered
    if name and name.upper() != job:
        return name.split(' (RO-')[0] if job.startswith('SL-') else name
    return None

def review_fields(question, link):
    if not isinstance(question, str) or not question.strip() or not isinstance(link, str):
        return {}
    url = urlsplit(link)
    if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password:
        return {}
    return dict(question=question.strip(), link=link)

def batch_jobs(directory, read):
    """Read the dispatcher's own local ledgers on the M2, including closed rounds."""
    latest = {}
    for manifest in sorted(directory.glob('*/manifest.json')):
        state = read(manifest.parent/'state.json')
        for row in state['jobs'].values():
            ident = row['id']
            rank = (row['round'], row['queued_at'])
            if ident in latest and rank <= latest[ident][0]:
                continue
            outcome = row.get('outcome') or {}
            item = {k:row[k] for k in ('id','title','round','status','queued_at','placement')}
            item['owner'] = (row.get('claim') or {}).get('owner')
            item['enabled'] = state['enabled']
            item['ended'] = row.get('ended', 0)
            item.update(review_fields(outcome.get('question'), outcome.get('link')))
            latest[ident] = (rank, item)
    return [item for _, item in latest.values()]

def reconcile(hosts):
    """Merge independent observations for display, leaving scheduler state untouched."""
    hosts = copy.deepcopy(hosts)
    macs = {h:v.get('data') or {} for h,v in hosts.items()}
    lookup = {h:{j['id']:j for j in d.get('jobs',[])} for h,d in macs.items()}
    titles = {j['id']:j['title'] for jobs in lookup.values() for j in jobs.values()
              if j['title'] != j['id']}
    route = macs['m6'].get('route') or {}
    titles.update({k:v for k,v in route.get('titles',{}).items() if v})
    requests = {}
    pending = []
    shared = []
    for item in macs['m2'].get('batch',[]):
        ident = item['id']
        titles[ident] = item['title']
        host = item['owner'] or item['placement']
        matching = [jobs[ident] for jobs in lookup.values() if ident in jobs]
        for job in matching:
            if 'with-dan' in job['states'] and job.get('waitingSince',0) <= item['queued_at']:
                job['states'].remove('with-dan')
        status = item['status']
        round_title = item['title'] + ' · Round ' + str(item['round'])
        if status=='completed':
            for job in matching:
                if 'with-dan' in job['states'] and job.get('lastWork',0)<=item['ended']:
                    job['states'].remove('with-dan')
        if status=='needs-dan' and item.get('question') and item.get('link'):
            # A later edit registration is more recent than this handoff.
            if not any(j.get('lastWork',0)>item['ended'] for j in matching):
                requests[ident] = dict(id=ident,title=round_title,question=item['question'],link=item['link'])
        if status not in ('queued','claimed'):
            continue
        info = 'Waiting in production queue' if status=='queued' else 'Claimed by production worker'
        if not item['enabled']:
            info += ' · batch paused'
        if host not in lookup:
            shared.append(round_title+' · '+info)
            continue
        jobs = lookup[host]
        if ident not in jobs:
            jobs[ident] = dict(id=ident, title=item['title'], states=[], held=0,tickets=0,occupies=False,auxiliary=False)
            macs[host].setdefault('jobs',[]).append(jobs[ident])
        jobs[ident].update(title=round_title,batchStage=info)
    for h,jobs in lookup.items():
        for j in jobs.values():
            if j['title']==j['id']:
                j['title']=titles.get(j['id']) or 'Project name needs checking'
            if 'with-dan' in j['states'] and j['id'] not in requests:
                if j.get('question') and j.get('link'):
                    requests[j['id']] = j
                else:
                    pending.append(j['title']+' ('+h.upper()+')')
    assigned = {ident for jobs in lookup.values() for ident,j in jobs.items() if j.get('batchStage') or j['occupies']}
    shared.extend(titles.get(ident) or 'Project name needs checking' for ident in route.get('line',[]) if ident not in assigned)
    return hosts,list(requests.values()),pending,shared,titles
