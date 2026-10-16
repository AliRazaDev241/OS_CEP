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
T=(P.parents[1]/'report/query_report.tex').read_text();B=(P.parents[1]/'report/query_references.bib').read_text()
keys=set(re.findall(r'@\w+\{([^,]+),',B))
T+='\n'+(P.parents[1]/'report/query_batch1.tex').read_text()
T+='\n'+(P.parents[1]/'report/query_batch2.tex').read_text()
cited={k for block in re.findall(r'\\cite\{([^}]+)\}',T) for k in block.split(',')}
assert keys==cited=={s['key'] for s in json.loads((E/'current_included_studies.json').read_text())}
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

# Current views are separate from the immutable historical Flow A.
B1=json.loads((E/'batch1_review_assessments.json').read_text())
BA=rows('batch1_accepted.csv'); CA=rows('current_accepted.csv')
assert len(B1)==len(BA)==10 and len(CA)==34
assert len({r['study_id'] for r in CA})==len(CA)
assert {r['study_id'] for r in CA}=={r['study_id'] for r in A}|{r['study_id'] for r in BA}|{r['study_id'] for r in rows('batch2_accepted.csv')}
for name in ['current_quality.csv','current_extraction.csv']:
    assert {r['study_id'] for r in rows(name)}=={r['study_id'] for r in CA}
for q in rows('current_quality.csv'):
    assert sum(float(q[f'Q{n}']) for n in range(1,11))==float(q['total'])
    assert all(float(q[f'Q{n}']) in [0,.5,1] and q[f'Q{n}_rationale'] for n in range(1,11))
receipts=rows('batch1_paper_receipts.csv')
assert len(receipts)==10 and all(re.fullmatch('[0-9a-f]{64}',r['sha256']) for r in receipts)
new={r['record_id']:r for r in rows('new_fulltext_assessments.csv')}
triage={r['record_id']:r for r in rows('new_screening_triage.csv')}
for s in B1:
    assert new[s['record_id']]['decision']==triage[s['record_id']]['decision']=='accepted'
    assert new[s['record_id']]['study_link']==s['study_id']
    assert s['anchor'] and len(s['qa_rationales'])==10
queue=rows('deduplicated_download_queue.csv')
assert len(queue)==76 and sum(r['download_status']=='received_assessed_accepted' for r in queue)==13
assert sum(r['download_status']=='received_assessed_excluded' for r in queue)==8
assert len(new)==23 and sum(r['decision']=='eligible_pending_integration' for r in new.values())==2
book=json.loads((E/'workbook_source.json').read_text())
assert len(book['Included'])==len(book['Quality'])==35
assert len(book['Received'])==28 and len(book['Batch1'])==11 and len(book['Batch2'])==12
assert {r[0] for r in book['Included'][1:]}=={r['study_id'] for r in CA}
assert book['Current'][5][1]==34 and book['Current'][7][1]==55
assert len(keys)==34
assert len(rows('batch2_paper_receipts.csv'))==11 and len(rows('batch2_quality.csv'))==3
B2=json.loads((E/'batch2_review_assessments.json').read_text());X2=json.loads((E/'batch2_exclusions.json').read_text())
assert {r['record_id'] for r in rows('batch2_paper_receipts.csv')}=={r['record_id'] for r in B2+X2}
assert {r['study_id'] for r in rows('batch2_quality.csv')}=={s['study_id'] for s in B2}
for s in B2:
    assert new[s['record_id']]['decision']==triage[s['record_id']]['decision']=='accepted'
    assert new[s['record_id']]['study_link']==s['study_id']
    assert sum(s['scores'])==8 and len(s['qa_rationales'])==10
for s in X2:
    assert new[s['record_id']]['decision']=='excluded' and new[s['record_id']]['reason_code']==s['reason_code']
    assert triage[s['record_id']]['decision']=='exclude' and triage[s['record_id']]['stage']=='full_text'
    assert new[s['record_id']]['source_anchor']==s['anchor'] and s['reason']
assert all(re.fullmatch('[0-9a-f]{64}',r['sha256']) for r in rows('batch2_paper_receipts.csv'))
print('PASS: batch1 10 accepted; batch2 3 accepted/8 excluded; current 34 unique studies; 23 extension reports assessed; 55 queue entries remain; 34 bibliography keys; historical flow unchanged.')
