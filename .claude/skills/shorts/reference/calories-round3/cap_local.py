import buildcap
original_worker=buildcap.is_worker
def _worker(p):
 return original_worker(p) or (buildcap._base(p)=='node' and 'hyperframes render ' in p['cmd'])
buildcap.is_worker=_worker
