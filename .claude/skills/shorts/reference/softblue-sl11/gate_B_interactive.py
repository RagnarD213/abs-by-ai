from full import R
import finish,renderq
# Dan selected the exact voice and is waiting for this batch's review copies.
# Supported interactive priority; same light pool, budgets, gates and actual file.
with renderq.slot('Vacuum B final interactive review delivery gate',pool='light',group='SL-11',priority=True):
 assert finish.gate('B')==0
