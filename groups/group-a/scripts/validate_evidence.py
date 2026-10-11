"""Check research-register identities, count reconciliation, and citation integrity."""
import csv,json,re,hashlib
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parents[1];E=P/'evidence'
def rows(name):return list(csv.DictReader((E/name).open()))
R=rows('studies.csv');A=[r for r in R if r['decision']=='accepted'];D=rows('duplicates.csv')
C=json.loads((E/'prisma_counts.json').read_text());I=json.loads((E/'imported_records.json').read_text())
assert len({r['record_id'] for r in R})==len(R)
assert len(I)==689
assert Counter(r['run_id'] for r in I)=={'SPR-MASTER':587,'IEEE-MPS':25,'IEEE-MIG':23,'IEEE-TEMPORAL':45,'IEEE-API':9}
assert len({r['study_id'] for r in A})==len(A)==C['accepted_unique_studies']==21
assert len({r['report_id'] for r in A})==len(A)
byid={r['record_id']:r for r in I}
for d in D:
    a,b=byid[d['record_id']],byid[d['canonical_record_id']]
    assert a['url']==b['url'] or (a['doi'] and a['doi']==b['doi']), 'Distinct DOI/report incorrectly removed'
assert len(D)==C['formal_duplicates']==10
assert C['formal_occurrences']-len(D)+C['supplementary_selected']==C['excluded_before_fulltext']+C['fulltext_assessed']+C['pending']==699
assert C['fulltext_assessed']==len(A)+C['fulltext_excluded']==28
assert C['acm_hits'] is None and C['sciencedirect_hits'] is None
for name in ['quality.csv','extraction.csv']:
    Q=rows(name);assert len(Q)==len(A) and {q['study_id'] for q in Q}=={a['study_id'] for a in A}
for q in rows('quality.csv'):
    assert all(float(q[f'Q{n}']) in [0,.5,1] for n in range(1,11))
    assert sum(float(q[f'Q{n}']) for n in range(1,11))==float(q['total'])
    assert q['source_url'] and q['anchor'] and q['reviewer']=='AI-CODEX'
for r in R:
    assert r['reason']
    if r['decision']=='excluded':assert re.fullmatch('E(10|[1-9])',r['reason_code'])
    if r['decision']=='pending':assert r['access']=='not_retrieved'
T=(P/'report/main.tex').read_text();B=(P/'report/references.bib').read_text()
keys=set(re.findall(r'@\w+\{([^,]+),',B))
cited={k for block in re.findall(r'\\cite\{([^}]+)\}',T) for k in block.split(',')}
assert keys==cited=={s['key'] for s in json.loads((E/'included_studies.json').read_text())}
assert '[12pt,' in T
assert len(rows('download_requests.csv'))==C['pending']==96
assert sum(r['priority']=='requested_max10' for r in rows('download_requests.csv'))==0
assert all(r['platform'] in ['IEEE Xplore','ACM DL','Springer Nature Link','ScienceDirect'] for r in rows('download_requests.csv'))
received=rows('uploaded_paper_receipts.csv'); assert len(received)==6
registered={r['record_id']:r for r in R}
assert {r['record_id'] for r in received}.isdisjoint({r['record_id'] for r in rows('download_requests.csv')})
for r in received:
    assert registered[r['record_id']]['decision']=='accepted'
    assert re.fullmatch('[0-9a-f]{64}',r['sha256'])
    assert registered[r['record_id']]['study_id']==r['study_id']
assert registered['GA-X007']['study_id']==registered['GA-SUP001']['study_id']=='GA-S001'
assert registered['GA-SUP001']['decision']=='excluded' and registered['GA-SUP001']['reason_code']=='E8'
assert next(q for q in rows('extraction.csv') if q['study_id']=='GA-S001')['record_id']=='GA-X007'
assert len(rows('original_download_batch.csv'))==10
assert sum(r['receipt_status']=='received_and_assessed' for r in rows('original_download_batch.csv'))==6
assert sum(r['receipt_status']=='unavailable_no_repeat_request' for r in rows('original_download_batch.csv'))==4
print('PASS:689 imports;10 duplicates;699 captured nonduplicate records;28 assessed;21 studies;96 pending;21 resolving BibTeX keys;6 receipts;0 active download requests;REEF counted once.')
