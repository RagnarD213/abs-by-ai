"""Normalize fresh owner API observations; native scheduling grants no approval."""
import re
from master_queue import identity, stamp, longform_errors


def native_records(snapshot):
    if snapshot.get('status') != 'ok': return []
    records=[]
    for v in snapshot['videos']:
        at=v.get('status',{}).get('publishAt')
        if not at or v['status'].get('privacyStatus') != 'private': continue
        snippet=v['snippet']; description=snippet.get('description','')
        thumbs=snippet.get('thumbnails',{})
        cover=next((thumbs[k]['url'] for k in ('maxres','standard','high','medium','default') if k in thumbs),None)
        kind='short' if 'utm_medium=short' in description else 'longform' if 'utm_campaign=longform' in description else 'unknown'
        payload={'accountId':snapshot['channel']['id'],'content':{'platform':'youtube','text':description,'mediaUrls':[]},
                 'target':{'targetType':'youtube','title':snippet['title'],'nativeVideoId':v['id']}}
        r={'payload':payload,'scheduledAt':stamp(at).isoformat(),'platform':'youtube','account':snapshot['channel']['id'],
           'title':snippet['title'],'caption':description,'media':[],'cover':cover,'kind':kind,
           'nativeVideoId':v['id'],'nativeObserved':True,'scheduleId':'native:'+v['id'],
           'approval':{'status':'scheduled_observed','reference':'youtube:'+v['id'],'quote':'Observed owner API schedule; original approval not inferred'},
           'provenance':[{'source':'youtube_native','sourceId':v['id'],'checkedAt':snapshot['checkedAt']}],
           'publicPostUrl':'https://studio.youtube.com/video/'+v['id']+'/edit'}
        r['id']=identity(payload,at);records.append(r)
    return records


def add_native_rows(queue, records, checks):
    rules=longform_errors(records)
    for r in records:
        if not stamp(queue['windowFrom']) <= stamp(r['scheduledAt']) < stamp(queue['windowTo']): continue
        links=[u.rstrip('.,!;') for u in re.findall(r'https://[^\s<>"\)]+',r['caption'])]
        def state(url):
            c=checks.get(url,{})
            try: age=(stamp(queue['checkedAt'])-stamp(c['checkedAt'])).total_seconds()
            except (KeyError,ValueError,TypeError): return 'unverified'
            if not 0 <= age <= 43200:return 'unverified'
            return 'verified' if c.get('status') in (200,206) else 'broken' if c.get('status') in (404,410) else 'unverified'
        states=[state(u) for u in links]
        notes=rules.get(r['id'],[]) + ['Native YouTube schedule observed; private video playback requires the Studio link']
        queue['rows'].append({'id':r['id'],'platform':'youtube','account':r['account'],'scheduledAt':r['scheduledAt'],
                             'title':r['title'][:220],'caption':r['caption'][:1000],'coverReviewUrl':r['cover'],'mediaUrl':None,
                             'reviewUrl':r['publicPostUrl'],'notes':notes,
                             'preflight':{'cover':state(r['cover']) if r['cover'] else 'missing','description':'verified' if r['caption'] else 'missing',
                                          'links':'not_applicable' if not links else 'broken' if 'broken' in states else 'verified' if all(s=='verified' for s in states) else 'unverified',
                                          'duplicates':'verified','assetMatch':'unverified','cadence':'mismatch' if r['id'] in rules else 'unverified' if r['kind']=='unknown' else 'verified','crop':'unverified'}})
    # Counts combine Blotato and native owner schedules for the same channel/time.
    for r in queue['rows']:
        if r['platform']=='youtube' and sum(v['platform']=='youtube' and stamp(v['scheduledAt'])==stamp(r['scheduledAt']) for v in queue['rows'])>1:
            r['preflight']['duplicates']='duplicate';r['notes'].append('More than one YouTube schedule at this exact time; identity review required')
    queue['rows'].sort(key=lambda r:r['scheduledAt'])
