"""Integrate batch 2 after build_batch1.py; retain historical and batch-1 registers."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

P = Path(__file__).resolve().parents[1]
E = P / 'evidence'
R = P.parents[1] / 'report'
DATE = '2026-10-17'
parser = argparse.ArgumentParser()
parser.add_argument('--source-dir', type=Path)
args = parser.parse_args()

def read(name):
    with (E / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (E / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def save(name, rows):
    (E / name).write_text(json.dumps(rows, ensure_ascii=False, indent=None if name == 'workbook_source.json' else 2) + '\n')

def latex(s):
    esc = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}'}
    return ''.join(esc.get(c, c) for c in str(s))

accepted = json.loads((E / 'batch2_review_assessments.json').read_text())
excluded = json.loads((E / 'batch2_exclusions.json').read_text())
all_reviews = accepted + excluded
ids = {s['record_id'] for s in all_reviews}
assert len(accepted) == 3 and len(excluded) == 8 and len(ids) == 11
occ = {r['record_id']: r for r in read('new_export_occurrences.csv')}
baseline = json.loads((E / 'included_studies.json').read_text())
batch1 = json.loads((E / 'batch1_review_assessments.json').read_text())
assert len(baseline) == 21 and len(batch1) == 10
prior = baseline + batch1
assert len({s['doi'].lower() for s in prior + accepted if s['doi']}) == sum(bool(s['doi']) for s in prior + accepted)
assert len({s['study_id'] for s in prior + accepted}) == 34

for s in all_reviews:
    if args.source_dir:
        data = (args.source_dir / s['filename']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == s['sha256'] and len(data) == s['bytes']
    assert re.fullmatch('[0-9a-f]{64}', s['sha256'])
    if s in accepted:
        assert s['doi'].lower() == occ[s['record_id']]['doi'].lower()

receipts = []
quality = []
extraction = []
new_accepted = []
for s in accepted:
    total = sum(s['scores'])
    assert len(s['scores']) == len(s['qa_rationales']) == 10
    receipts.append({k: s[k] for k in ['record_id','report_id','study_id','filename','sha256','bytes']} | dict(received_date=DATE, source_format=s['source_type'], decision='accepted_new_study', qa_total=total))
    q = dict(study_id=s['study_id'], report_id=s['report_id'], reviewer='AI-CODEX', date=DATE,
             total=total, band='high' if total >= 8 else 'moderate' if total >= 6 else 'low', anchor=s['anchor'], source_url=s['publisher_url'])
    for n, score in enumerate(s['scores'], 1):
        q[f'Q{n}'], q[f'Q{n}_rationale'] = score, s['qa_rationales'][n-1]
    quality.append(q)
    extraction.append({k:v for k,v in s.items() if k not in ['scores','qa_rationales','sha256','bytes']}
                      | dict(retrieved_date=DATE, version=s['source_type'], qa=total,
                             untranscribed_fields='Missing chart coordinates or unspecified settings are NOT EXTRACTED.',
                             evidence_strength='Within-study direct evidence; local and system-level strata distinguished'))
    o = occ[s['record_id']]
    new_accepted.append(dict(record_id=s['record_id'], report_id=s['report_id'], study_id=s['study_id'],
                             title=s['title'], doi=s['doi'], publication_date=s['publication_date'],
                             database='ACM Digital Library', run_id=o['run_id'], record_route='formal_extension',
                             decision='accepted', stage='full_text', reason_code='', reason=s['eligibility'],
                             access='retrieved', reviewer='AI-CODEX', decision_date=DATE, url=s['publisher_url']))
write('batch2_paper_receipts.csv', receipts + [dict(record_id=s['record_id'],report_id='GA-PN'+s['record_id'][4:],study_id='',filename=s['filename'],sha256=s['sha256'],bytes=s['bytes'],received_date=DATE,source_format='User-supplied full-report Markdown conversion',decision='excluded_'+s['reason_code'],qa_total='') for s in excluded])
write('batch2_quality.csv', quality)
write('batch2_extraction.csv', extraction)
write('batch2_accepted.csv', new_accepted)
write('current_accepted.csv', read('accepted.csv') + read('batch1_accepted.csv') + new_accepted)
write('current_quality.csv', read('quality.csv') + read('batch1_quality.csv') + quality)
write('current_extraction.csv', read('extraction.csv') + read('batch1_extraction.csv') + extraction)
save('current_included_studies.json', prior + [{k:v for k,v in s.items() if k not in ['scores','qa_rationales','sha256','bytes']} for s in accepted])

assess = [r for r in read('new_fulltext_assessments.csv') if r['record_id'] not in ids]
for s in accepted:
    assess.append(dict(record_id=s['record_id'], doi=s['doi'], source_url=s['publisher_url'], access='user-supplied published full-report Markdown conversion',
                       publication_status=s['peer_review']+'; '+s['publication_date'], decision='accepted',reason_code='',study_link=s['study_id'],
                       reviewer='AI-CODEX', review_date=DATE,source_anchor=s['anchor'],mechanism=s['mechanism'],environment=s['environment'],
                       workload=s['workload'],comparator=s['comparator'],outcome=s['finding'],limitations=s['limitation']))
for s in excluded:
    o=occ[s['record_id']]
    assess.append(dict(record_id=s['record_id'],doi=o['doi'],source_url=o['url'],access='user-supplied full-report Markdown conversion',
                       publication_status=str(o['year'])+' publisher record; full text checked',decision='excluded',reason_code=s['reason_code'],study_link='',
                       reviewer='AI-CODEX',review_date=DATE,source_anchor=s['anchor'],mechanism='',environment='',workload='',comparator='',outcome='',limitations=s['reason']))
write('new_fulltext_assessments.csv', assess)
triage=read('new_screening_triage.csv')
for row in triage:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        incl=s in accepted
        row.update(stage='full_text',decision='accepted' if incl else 'exclude',reason_code='' if incl else s['reason_code'],
                   rationale=s['eligibility'] if incl else s['reason'],evidence_basis=s['anchor'],reviewer='AI-CODEX',review_date=DATE,
                   full_text_status='retrieved_and_assessed')
write('new_screening_triage.csv',triage)
queue=read('deduplicated_download_queue.csv')
for row in queue:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        incl=s in accepted
        row.update(download_status='received_assessed_accepted' if incl else 'received_assessed_excluded', local_filename=s['filename'],
                   cutoff_check='within cutoff; '+s['publication_date'] if incl else 'full-text eligibility assessed; publication-year within cutoff',
                   notes=(s['study_id']+f'; QA {sum(s["scores"]):g}/10' if incl else s['reason_code']+'; '+s['reason'])+'; hash in batch2_paper_receipts.csv')
write('deduplicated_download_queue.csv',queue)
pq=read('priority_fulltext_queue.csv')
for row in pq:
    if row['record_id'] in ids:
        s=next(v for v in all_reviews if v['record_id']==row['record_id'])
        row.update(full_text_status='retrieved_and_assessed',study_status='accepted: '+s['study_id'] if s in accepted else 'excluded: '+s['reason_code'],
                   date_check=s['publication_date']+'; within cutoff' if s in accepted else 'within year window',title_abstract_status='reconsidered_after_full_text')
write('priority_fulltext_queue.csv',pq)

counts=dict(date=DATE,scope='Accepted-set and received-report update, not reconciled four-database PRISMA flow',historical_accepted=21,
            batch1_accepted=10,batch2_assessed=11,batch2_accepted=3,batch2_excluded=8,current_accepted=34,
            extension_assessed=len(assess),extension_eligible_pending=sum(r['decision']=='eligible_pending_integration' for r in assess),
            supplied_queue=len(queue),queue_received=sum(r['download_status'].startswith('received_assessed_') for r in queue),
            queue_remaining=sum(not r['download_status'].startswith('received_assessed_') for r in queue))
assert counts['extension_assessed']==23 and counts['queue_received']==21 and counts['queue_remaining']==55
save('batch2_counts.json',counts)

bib=(R/'query_references.bib').read_text().strip()
for s in accepted:
    bib=re.sub(r'\n?@inproceedings\{'+s['key']+r',\n.*?\n\}', '', bib,flags=re.S).strip()
for s in accepted:
    fields=dict(title='{'+s['title']+'}',author=s['authors'],year=s['year'],booktitle=s['venue'],doi=s['doi'],url=s['publisher_url'])
    if s['pages']:fields['pages']=s['pages']
    if s['key']=='interference_deeper':fields['note']='Printed SoCC 2025 event; export year 2026'
    bib+='\n\n@inproceedings{'+s['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}'
(R/'query_references.bib').write_text(bib.strip()+'\n')

book=json.loads((E/'workbook_source.json').read_text())
allstudies=prior+accepted
book['Included']=[book['Included'][0]]+[[s[k] for k in ['study_id','key','mechanism','fulltext_url','anchor','finding','limitation']] for s in allstudies]
book['Quality']=[book['Quality'][0]]+[[q['study_id']]+[float(q[f'Q{n}']) for n in range(1,11)]+[float(q['total']),q['band'],q['anchor']] for q in read('current_quality.csv')]
base_receipts=read('uploaded_paper_receipts.csv')+read('batch1_paper_receipts.csv')+read('batch2_paper_receipts.csv')
book['Received']=[book['Received'][0]]+[[r[k] for k in ['record_id','study_id','filename','decision','qa_total','sha256']] for r in base_receipts]
book['Batch2']=[['Record','Study','Paper','Decision','QA /10','Reason / date basis','Source anchor']]+[[s['record_id'],s['study_id'] if s in accepted else '',s['filename'],'accepted' if s in accepted else 'excluded',sum(s['scores']) if s in accepted else '',s['publication_date'] if s in accepted else s['reason_code']+': '+s['reason'],s['anchor']] for s in all_reviews]
book['Current']=[['Current assessed evidence',DATE],['Scope','Accepted set; final PRISMA still pending'],
                 ['Historical accepted studies',21],['Batch 1 new studies',10],['Batch 2 new studies',3],['Current accepted studies',34],
                 ['Other extension eligible; integration pending',2],['Download queue still awaiting assessment',55],
                 ['Extension reports assessed',23],['Guideline 7-14 completion','Not complete; remaining records and flow need reconciliation']]
book={'Current':book.pop('Current'),**book}
book['DownloadQueue']=[list(queue[0])]+[[r[k] for k in queue[0]] for r in queue]
book['Triage']=[book['Triage'][0]]+[[r['record_id'],occ[r['record_id']]['run_id'],occ[r['record_id']]['title'],occ[r['record_id']]['year'],r['decision'],r['reason_code'],r['rationale'],r['canonical_record'],r['evidence_basis']] for r in triage]
for row in book.get('NewQueue',[])[1:]:
    if row[0] in ids:
        s=next(v for v in all_reviews if v['record_id']==row[0]); row[4:8]=['accepted' if s in accepted else 'exclude',s['publication_date'] if s in accepted else 'within year window','retrieved_and_assessed',s['study_id'] if s in accepted else s['reason_code']]
fields=['record_id','doi','publication_status','decision','source_url','source_anchor','mechanism','environment','workload','comparator','outcome','limitations']
book['AssessedNew']=[['Record','DOI','Publication','Decision','Source','Anchor','Mechanism','Environment','Workload','Comparator','Outcome','Limitations']]+[[r[f] for f in fields] for r in assess]
if 'Extension' in book:book['Extension'][-1][-2]='Batch 1: 10 accepted. Batch 2: 11 assessed, 3 accepted, 8 excluded. Current accepted 34; two older reports await integration; final PRISMA reconciliation open.'
save('workbook_source.json',book)

lines=[r'\section{Batch 2: full-text reassessment}\label{sec:batch2}',
       r'Eleven further user-supplied full-report conversions from the deduplicated queue were assessed on 17 October 2026 by the same single AI reviewer. Three add unique studies GA-S032--GA-S034; eight are excluded with principal full-text reasons. Prior rule-assisted title/abstract exclusions were reconsidered when the full texts arrived. The accepted set is now \textbf{34 unique studies (21 historical + 10 batch 1 + 3 batch 2)}; this does not complete merged database screening or PRISMA accounting.',
       r'The 76-entry download queue has 21 received reports (13 accepted, eight excluded) and 55 unassessed entries. The extension full-text ledger has 23 assessed reports, including two older eligible-pending-integration reports outside the 34. Source hashes, reasons and anchors are retained without committing paper bodies.',
       r'\subsection{Decisions and evidential bounds}',
       r'\begin{longtable}{P{0.16\linewidth}P{0.22\linewidth}P{0.52\linewidth}}\toprule Record & Decision & Primary reason or direct evidence\\\midrule\endhead']
for s in all_reviews:
    lines.append(latex(s['record_id'])+' & '+('Accept '+latex(s['study_id'])+r' \cite{'+s['key']+'}' if s in accepted else 'Exclude '+s['reason_code'])+' & '+latex(s['eligibility'] if s in accepted else s['reason'])+r'\\')
lines.append(r'\bottomrule\end{longtable}')
for s in accepted:
    lines.append(r'\paragraph{'+latex(s['study_id']+' '+s['key'])+r'.} '+latex(s['finding'])+' '+latex(s['limitation'])+r' \textit{Anchor:} '+latex(s['anchor'])+'.')
bands=Counter(q['band'] for q in read('current_quality.csv'))
lines.extend([r'\subsection{Appraisal and remaining reconciliation}',
              f'The three new studies score {sum(sum(s["scores"]) for s in accepted):g}/30; the combined 34 score {sum(float(q["total"]) for q in read("current_quality.csv")):g}/340, with {bands["high"]} high, {bands["moderate"]} moderate, and {bands["low"]} low. The same Q1--Q10 rubric applies only to included studies. Source-specific Q-item rationales and limitations are in '+r'\path{batch2_quality.csv} and \path{batch2_extraction.csv}.',
              r'The SoCC paper prints a November 2025 event date although the export lists 2026; both lie within the cutoff. It measures synthetic kernel co-tenants alongside LLM inference, not two production inference services. Guardian shows co-located training and standalone inference only; it therefore fails the adopted concurrent inference criterion despite useful memory-safety context.',
              r'\pending{Resolve 55 remaining queue entries, the two older eligible-pending-integration reports, report-version and occurrence links, and the four-database PRISMA flow. Excluded batch-2 reports are assessed full texts, not additions to the historical Flow A seven full-text exclusions.}'])
(R/'query_batch2.tex').write_text('\n\n'.join(lines)+'\n')
notes=['# Batch 2 full-text review — 17 October 2026','Single reviewer AI-CODEX; 11 full reports assessed, three accepted and eight excluded. No full-paper bodies committed. The historical Flow A is a separate dated checkpoint.']
for s in all_reviews:
    notes += ['## '+s['record_id']+' — '+s['filename'],s['eligibility'] if s in accepted else s['reason_code']+': '+s['reason'],
              'Anchor: '+s['anchor'],'SHA-256: '+s['sha256']]
(E/'batch2_review.md').write_text('\n\n'.join(notes)+'\n')
print(json.dumps(counts,indent=2))
