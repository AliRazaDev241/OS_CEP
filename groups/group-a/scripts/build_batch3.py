"""Integrate the third user supplied full text batch after build_batch2.py."""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
E = P / 'evidence'
R = P.parents[1] / 'report'
DATE = '2026-10-17'

def read(name):
    with (E / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (E / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def save(name, value):
    (E / name).write_text(json.dumps(value, ensure_ascii=False, indent=None if name == 'workbook_source.json' else 2) + '\n')

def latex(s):
    esc = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}'}
    return ''.join(esc.get(c, c) for c in str(s))

parser = argparse.ArgumentParser()
parser.add_argument('--source-dir', type=Path)
args = parser.parse_args()
accepted = json.loads((E / 'batch3_review_assessments.json').read_text())
excluded = json.loads((E / 'batch3_exclusions.json').read_text())
all_reviews = accepted + excluded
ids = {s['record_id'] for s in all_reviews}
assert len(accepted) == 9 and len(excluded) == 1 and len(ids) == 10
occ = {r['record_id']: r for r in read('new_export_occurrences.csv')}
prior = (json.loads((E / 'included_studies.json').read_text())
         + json.loads((E / 'batch1_review_assessments.json').read_text())
         + [{k:v for k,v in s.items() if k not in ['scores','qa_rationales','sha256','bytes']}
            for s in json.loads((E / 'batch2_review_assessments.json').read_text())])
assert len(prior) == 34
assert not ids.intersection({s['record_id'] for s in prior})
assert len({s['doi'].lower() for s in prior + accepted if s['doi']}) == sum(bool(s['doi']) for s in prior + accepted)
assert len({s['study_id'] for s in prior + accepted}) == 43

receipts, quality, extraction, new_accepted = [], [], [], []
for s in all_reviews:
    if args.source_dir:
        data = (args.source_dir / s['filename']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == s['sha256'] and len(data) == s['bytes']
    assert re.fullmatch('[0-9a-f]{64}', s['sha256'])
    assert s['doi'].lower() == occ[s['record_id']]['doi'].lower()
    included = s in accepted
    total = sum(s['scores']) if included else ''
    receipts.append(dict(record_id=s['record_id'],report_id=s['report_id'],study_id=s['study_id'] if included else '',
                         filename=s['filename'],sha256=s['sha256'],bytes=s['bytes'],received_date=DATE,
                         source_format='User-supplied full-report Markdown conversion',decision='accepted_new_study' if included else 'excluded_'+s['reason_code'],qa_total=total))
    if not included:
        continue
    assert len(s['scores']) == len(s['qa_rationales']) == 10
    q = dict(study_id=s['study_id'], report_id=s['report_id'], reviewer='AI-CODEX', date=DATE,
             total=total, band='high' if total >= 8 else 'moderate' if total >= 6 else 'low', anchor=s['anchor'],source_url=s['publisher_url'])
    for n, score in enumerate(s['scores'],1):
        assert score in [0,.5,1]
        q[f'Q{n}'],q[f'Q{n}_rationale'] = score,s['qa_rationales'][n-1]
    quality.append(q)
    extraction.append({k:v for k,v in s.items() if k not in ['scores','qa_rationales','sha256','bytes']}
                      | dict(retrieved_date=DATE,version=s['source_type'],qa=total,
                             untranscribed_fields='Unspecified setup and unreadable plot coordinates not extracted.',
                             evidence_strength='Direct within-study evidence, qualified by experimental scope'))
    o=occ[s['record_id']]
    new_accepted.append(dict(record_id=s['record_id'],report_id=s['report_id'],study_id=s['study_id'],title=s['title'],
                             doi=s['doi'],publication_date=s['publication_date'],database='ACM Digital Library',run_id=o['run_id'],
                             record_route='formal_extension',decision='accepted',stage='full_text',reason_code='',reason=s['eligibility'],
                             access='retrieved',reviewer='AI-CODEX',decision_date=DATE,url=s['publisher_url']))
write('batch3_paper_receipts.csv',receipts)
write('batch3_quality.csv',quality)
write('batch3_extraction.csv',extraction)
write('batch3_accepted.csv',new_accepted)
write('current_accepted.csv',read('accepted.csv')+read('batch1_accepted.csv')+read('batch2_accepted.csv')+new_accepted)
write('current_quality.csv',read('quality.csv')+read('batch1_quality.csv')+read('batch2_quality.csv')+quality)
write('current_extraction.csv',read('extraction.csv')+read('batch1_extraction.csv')+read('batch2_extraction.csv')+extraction)
save('current_included_studies.json',prior+[{k:v for k,v in s.items() if k not in ['scores','qa_rationales','sha256','bytes']} for s in accepted])

assess=[r for r in read('new_fulltext_assessments.csv') if r['record_id'] not in ids]
for s in all_reviews:
    included=s in accepted
    assess.append(dict(record_id=s['record_id'],doi=s['doi'],source_url=s['publisher_url'],
                       access='user-supplied published full-report Markdown conversion',publication_status=s['publication_date'],
                       decision='accepted' if included else 'excluded',reason_code='' if included else s['reason_code'],
                       study_link=s['study_id'] if included else '',reviewer='AI-CODEX',review_date=DATE,
                       source_anchor=s['anchor'],mechanism=s['mechanism'] if included else '',environment=s['environment'] if included else '',
                       workload=s['workload'] if included else '',comparator=s['comparator'] if included else '',
                       outcome=s['finding'] if included else '',limitations=s['limitation'] if included else s['reason']))
write('new_fulltext_assessments.csv',assess)
triage=read('new_screening_triage.csv')
for row in triage:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        included=s in accepted
        row.update(stage='full_text',decision='accepted' if included else 'exclude',reason_code='' if included else s['reason_code'],
                   rationale=s['eligibility'] if included else s['reason'],evidence_basis=s['anchor'],reviewer='AI-CODEX',
                   review_date=DATE,full_text_status='retrieved_and_assessed')
write('new_screening_triage.csv',triage)
queue=read('deduplicated_download_queue.csv')
for row in queue:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        included=s in accepted
        row.update(download_status='received_assessed_accepted' if included else 'received_assessed_excluded',
                   local_filename=s['filename'],cutoff_check=s['publication_date']+'; within cutoff',
                   notes=(s['study_id']+f'; QA {sum(s["scores"]):g}/10' if included else s['reason_code']+'; '+s['reason'])+'; hash in batch3_paper_receipts.csv')
write('deduplicated_download_queue.csv',queue)
pq=read('priority_fulltext_queue.csv')
for row in pq:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        row.update(full_text_status='retrieved_and_assessed',study_status='accepted: '+s['study_id'] if s in accepted else 'excluded: '+s['reason_code'],
                   date_check=s['publication_date']+'; within cutoff',title_abstract_status='reconsidered_after_full_text')
write('priority_fulltext_queue.csv',pq)

counts=dict(date=DATE,scope='Accepted-set update, not reconciled four-database PRISMA flow',historical_accepted=21,
            batch1_accepted=10,batch2_accepted=3,batch3_assessed=10,batch3_accepted=9,batch3_excluded=1,current_accepted=43,
            extension_assessed=len(assess),extension_eligible_pending=sum(r['decision']=='eligible_pending_integration' for r in assess),
            supplied_queue=len(queue),queue_received=sum(r['download_status'].startswith('received_assessed_') for r in queue),
            queue_remaining=sum(not r['download_status'].startswith('received_assessed_') for r in queue))
assert (counts['extension_assessed'],counts['queue_received'],counts['queue_remaining'])==(33,31,45)
save('batch3_counts.json',counts)

bib=(R/'query_references.bib').read_text().strip()
for s in accepted:
    bib=re.sub(r'\n?@\w+\{'+s['key']+r',\n.*?\n\}', '', bib,flags=re.S).strip()
    fields=dict(title=s['title'].replace('&',r'{\&}'),author=s['authors'],year=s['year'],doi=s['doi'],url=s['publisher_url'])
    fields['journal' if s['venue_type']=='journal' else 'booktitle']=s['venue']
    bib+='\n\n@'+('article' if s['venue_type']=='journal' else 'inproceedings')+'{'+s['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}'
(R/'query_references.bib').write_text(bib+'\n')

book=json.loads((E/'workbook_source.json').read_text())
allstudies=prior+accepted
book['Included']=[book['Included'][0]]+[[s[k] for k in ['study_id','key','mechanism','fulltext_url','anchor','finding','limitation']] for s in allstudies]
book['Quality']=[book['Quality'][0]]+[[q['study_id']]+[float(q[f'Q{n}']) for n in range(1,11)]+[float(q['total']),q['band'],q['anchor']] for q in read('current_quality.csv')]
allreceipts=read('uploaded_paper_receipts.csv')+read('batch1_paper_receipts.csv')+read('batch2_paper_receipts.csv')+receipts
book['Received']=[book['Received'][0]]+[[r[k] for k in ['record_id','study_id','filename','decision','qa_total','sha256']] for r in allreceipts]
book['Batch3']=[['Record','Study','Paper','Decision','QA /10','Reason / date basis','Source anchor']]+[[s['record_id'],s['study_id'] if s in accepted else '',s['filename'],'accepted' if s in accepted else 'excluded',sum(s['scores']) if s in accepted else '',s['publication_date'] if s in accepted else s['reason_code']+': '+s['reason'],s['anchor']] for s in all_reviews]
book['Current']=[['Current assessed evidence',DATE],['Scope','Accepted set; final PRISMA still pending'],['Historical accepted studies',21],['Batch 1 new studies',10],['Batch 2 new studies',3],['Batch 3 new studies',9],['Current accepted studies',43],['Other extension eligible; integration pending',2],['Download queue still awaiting assessment',45],['Extension reports assessed',33],['Guideline 7-14 completion','Not complete; remaining records and flow need reconciliation']]
book={'Current':book.pop('Current'),**book}
book['DownloadQueue']=[list(queue[0])]+[[r[k] for k in queue[0]] for r in queue]
book['Triage']=[book['Triage'][0]]+[[r['record_id'],occ[r['record_id']]['run_id'],occ[r['record_id']]['title'],occ[r['record_id']]['year'],r['decision'],r['reason_code'],r['rationale'],r['canonical_record'],r['evidence_basis']] for r in triage]
for row in book.get('NewQueue',[])[1:]:
    if row[0] in ids:
        s=next(v for v in all_reviews if v['record_id']==row[0]);row[4:8]=['accepted' if s in accepted else 'exclude',s['publication_date'],'retrieved_and_assessed',s['study_id'] if s in accepted else s['reason_code']]
fields=['record_id','doi','publication_status','decision','source_url','source_anchor','mechanism','environment','workload','comparator','outcome','limitations']
book['AssessedNew']=[['Record','DOI','Publication','Decision','Source','Anchor','Mechanism','Environment','Workload','Comparator','Outcome','Limitations']]+[[r[f] for f in fields] for r in assess]
if 'Extension' in book:book['Extension'][-1][-2]='Batches 1–3: 31 queue reports assessed, 22 accepted and nine excluded. Current accepted 43; two older reports await integration; final PRISMA reconciliation open.'
save('workbook_source.json',book)

lines=[r'\section{Batch 3: full-text review}\label{sec:batch3}',
       r'Ten further user-supplied full-report conversions were assessed by one AI reviewer on 17 October 2026. Nine add unique studies GA-S035--GA-S043; one is excluded. The accepted set is now \textbf{43 unique studies (21 historical + 10 batch 1 + 3 batch 2 + 9 batch 3)}. This is not a reconciled merged-database PRISMA inclusion count. The 76-entry queue has 31 assessed reports and 45 unassessed entries. Two older eligible-pending-integration reports remain outside the 43.',
       r'\begin{longtable}{P{0.16\linewidth}P{0.22\linewidth}P{0.52\linewidth}}\toprule Record & Decision & Reason or bounded finding\\\midrule\endhead']
for s in all_reviews:
    lines.append(latex(s['record_id'])+' & '+('Accept '+latex(s['study_id'])+r' \cite{'+s['key']+'}' if s in accepted else 'Exclude '+s['reason_code'])+' & '+latex(s['eligibility'] if s in accepted else s['reason'])+r'\\')
lines.append(r'\bottomrule\end{longtable}')
for s in accepted:
    lines.append(r'\paragraph{'+latex(s['study_id']+' '+s['key'])+r'.} '+latex(s['finding'])+' '+latex(s['limitation'])+r' \textit{Anchor:} '+latex(s['anchor'])+'.')
lines.append(r'\pending{The batch-3 reports extend the assessed evidence, not the historical Flow A boxes. Reconcile the remaining 45 queue entries, two older eligible reports, duplicate/version links, database searches and the combined PRISMA flow.}')
(R/'query_batch3.tex').write_text('\n\n'.join(lines)+'\n')
notes=['# Batch 3 full-text review — 17 October 2026','Single reviewer AI-CODEX; ten reports assessed, nine accepted and one excluded. Markdown conversions and full source bodies are not committed.']
for s in all_reviews:
    notes+=['## '+s['record_id']+' — '+s['filename'],s['eligibility'] if s in accepted else s['reason_code']+': '+s['reason'],'Anchor: '+s['anchor'],'SHA-256: '+s['sha256']]
(E/'batch3_review.md').write_text('\n\n'.join(notes)+'\n')
print(json.dumps(counts,indent=2))
