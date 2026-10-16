"""Integrate recorded batch-1 decisions without rewriting the historical Flow A.

The assessment JSON contains the reviewer's decisions, not source full texts.
Run after the baseline builders; all outputs are deterministic and ID keyed.
"""
import argparse
import csv
import hashlib
import json
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

def write(name, data):
    fields = list(dict.fromkeys(k for row in data for k in row))
    with (E / name).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(data)

def save(name, data):
    (E / name).write_text(json.dumps(data, ensure_ascii=False, indent=None if name=='workbook_source.json' else 2) + '\n')

def tex(value):
    changes = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
               '^': r'\textasciicircum{}'}
    return ''.join(changes.get(c, c) for c in str(value))

reviews = json.loads((E / 'batch1_review_assessments.json').read_text())
byid = {s['record_id']: s for s in reviews}
occ = {r['record_id']: r for r in read('new_export_occurrences.csv')}
baseline = json.loads((E / 'included_studies.json').read_text())
assert len(reviews) == 10 and len(byid) == 10 and len(baseline) == 21
assert not ({s['doi'].lower() for s in baseline if s['doi']} & {s['doi'].lower() for s in reviews})
assert len({s['doi'].lower() for s in reviews}) == 10
assert len({s['study_id'] for s in baseline + reviews}) == 31
receipts, quality, extraction, accepted = [], [], [], []
for s in reviews:
    assert s['doi'].lower() == occ[s['record_id']]['doi'].lower()
    if args.source_dir:
        data = (args.source_dir / s['filename']).read_bytes()
        assert hashlib.sha256(data).hexdigest() == s['sha256']
        assert len(data) == s['bytes']
    receipts.append({k: s[k] for k in ['record_id', 'report_id', 'study_id', 'filename', 'sha256', 'bytes']}
                    | {'received_date': DATE, 'source_format': s['source_type'],
                       'decision': 'accepted_new_study', 'qa_total': sum(s['scores'])})
    total = sum(s['scores'])
    q = dict(study_id=s['study_id'], report_id=s['report_id'], reviewer='AI-CODEX', date=DATE,
             total=total, band='high' if total >= 8 else 'moderate' if total >= 6 else 'low',
             anchor=s['anchor'], source_url=s['publisher_url'])
    for n, score in enumerate(s['scores'], 1):
        q[f'Q{n}'], q[f'Q{n}_rationale'] = score, s['qa_rationales'][n-1]
    quality.append(q)
    extraction.append({k: v for k, v in s.items() if k not in ['scores', 'qa_rationales', 'sha256', 'bytes']}
                      | dict(retrieved_date=DATE, version=s['source_type'], qa=total,
                             untranscribed_fields='Unspecified settings remain NOT EXTRACTED; damaged plots/tables not reconstructed.',
                             evidence_strength='Direct within-study evidence; local and system-level strata kept separate'))
    o = occ[s['record_id']]
    accepted.append(dict(record_id=s['record_id'], report_id=s['report_id'], study_id=s['study_id'],
                         title=s['title'], doi=s['doi'], publication_date=s['publication_date'],
                         database='ACM Digital Library' if o['run_id'].startswith('ACM') else 'ScienceDirect', run_id=o['run_id'], record_route='formal_extension',
                         decision='accepted', stage='full_text', reason_code='', reason=s['eligibility'],
                         access='retrieved', reviewer='AI-CODEX', decision_date=DATE, url=s['publisher_url']))
write('batch1_paper_receipts.csv', receipts)
write('batch1_quality.csv', quality)
write('batch1_extraction.csv', extraction)
write('batch1_accepted.csv', accepted)
write('current_accepted.csv', read('accepted.csv') + accepted)
write('current_quality.csv', read('quality.csv') + quality)
write('current_extraction.csv', read('extraction.csv') + extraction)
save('current_included_studies.json', baseline + [{k:v for k,v in s.items() if k not in ['scores','sha256','bytes']} for s in reviews])

# New full-text register is the extension decision authority. Preserve Pantheon
# and Jormungandr exactly; they still need version integration and Q-item scores.
assess = [r for r in read('new_fulltext_assessments.csv') if r['record_id'] not in byid]
for s in reviews:
    assess.append(dict(record_id=s['record_id'], doi=s['doi'], source_url=s['publisher_url'],
                       access='user-supplied published full-report Markdown conversion',
                       publication_status=s['peer_review'] + '; ' + s['publication_date'], decision='accepted',
                       reason_code='', study_link=s['study_id'], reviewer='AI-CODEX', review_date=DATE,
                       source_anchor=s['anchor'], mechanism=s['mechanism'], environment=s['environment'],
                       workload=s['workload'], comparator=s['comparator'], outcome=s['finding'], limitations=s['limitation']))
write('new_fulltext_assessments.csv', assess)
triage = read('new_screening_triage.csv')
for row in triage:
    if row['record_id'] in byid:
        s = byid[row['record_id']]
        row.update(stage='full_text', decision='accepted', reason_code='', rationale=s['eligibility'],
                   evidence_basis=s['anchor'], reviewer='AI-CODEX', review_date=DATE,
                   full_text_status='retrieved_and_assessed')
write('new_screening_triage.csv', triage)

queue = read('deduplicated_download_queue.csv')
for row in queue:
    if row['record_id'] in byid:
        s = byid[row['record_id']]
        row.update(download_status='received_assessed_accepted', local_filename=s['filename'],
                   cutoff_check='within cutoff; '+s['publication_date'],
                   notes=f"{s['study_id']}; QA {sum(s['scores']):g}/10; private source hash in batch1_paper_receipts.csv")
write('deduplicated_download_queue.csv', queue)
for name in ['priority_fulltext_queue.csv']:
    rows = read(name)
    for row in rows:
        if row['record_id'] in byid:
            s = byid[row['record_id']]
            row.update(full_text_status='retrieved_and_assessed', study_status='accepted: '+s['study_id'],
                       date_check=s['publication_date']+'; within cutoff', title_abstract_status='accepted_after_full_text')
    write(name, rows)

counts = dict(date=DATE, scope='Current assessed set; not a reconciled four-database PRISMA flow',
              baseline_unique_studies=len(baseline), batch1_new_unique_studies=len(reviews),
              current_accepted_unique_studies=len(baseline)+len(reviews),
              batch1_assessed_reports=len(reviews), batch1_exclusions=0,
              extension_assessed_reports=len(assess), extension_eligible_pending_integration=len(assess)-len(reviews),
              supplied_download_queue=len(queue), received_from_queue=len(reviews),
              queue_remaining=sum(r['record_id'] not in byid for r in queue))
save('batch1_counts.json', counts)

# Rebuild bibliography from the immutable baseline result plus ten new entries.
bib = (R / 'query_references.bib').read_text()
import re
bib = re.sub(r'\n?@(?:article|inproceedings)\{(?:'+'|'.join(s['key'] for s in reviews)+r'),\n.*?\n\}\n?', '', bib, flags=re.S)
bib = bib.strip()
for s in reviews:
    fields = dict(title='{'+s['title']+'}', author=s['authors'], year=s['year'],
                  url=s['publisher_url'], doi=s['doi'], pages=s['pages'])
    fields['journal' if s.get('journal') else 'booktitle'] = s['venue']
    for k in ['volume', 'number']:
        if s.get(k): fields[k] = s[k]
    if s.get('article_number'): fields['note'] = 'Art. no. '+s['article_number']
    if s['key']=='deft': fields['note']='WoC 2023 event; export publication year 2024; printed reference year 2023'
    bib += '\n\n@'+('article' if s.get('journal') else 'inproceedings')+'{'+s['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}'
(R / 'query_references.bib').write_text(bib.strip()+'\n')

book = json.loads((E / 'workbook_source.json').read_text())
book['Summary'][0] = ['Historical Flow A checkpoint', '2026-10-11; see Current for later accepted set']
book['Included'] = [book['Included'][0]] + [[s[k] for k in ['study_id','key','mechanism','fulltext_url','anchor','finding','limitation']] for s in baseline+reviews]
allq = read('current_quality.csv')
book['Quality'] = [book['Quality'][0]] + [[q['study_id']]+[float(q[f'Q{n}']) for n in range(1,11)]+[float(q['total']),q['band'],q['anchor']] for q in allq]
base_receipts = read('uploaded_paper_receipts.csv')
book['Received'] = [book['Received'][0]] + [[r[k] for k in ['record_id','study_id','filename','decision','qa_total','sha256']] for r in base_receipts+receipts]
book['Batch1'] = [['Record','Study','Paper','Decision','QA /10','Publication date basis','Source anchor']]+[[s['record_id'],s['study_id'],s['key'],'accepted',sum(s['scores']),s['publication_date'],s['anchor']] for s in reviews]
book['Current'] = [['Current assessed evidence','2026-10-17'], ['Scope','Accepted set; final PRISMA still pending'],
                   ['Historical accepted studies',21], ['Batch 1 new studies',10], ['Current accepted studies',31],
                   ['Other extension eligible; integration pending',2], ['Download queue still awaiting assessment',counts['queue_remaining']],
                   ['Extension reports assessed',len(assess)], ['Guideline 7-14 completion','Not complete; remaining records and flow need reconciliation']]
book = {'Current':book.pop('Current'), **book}
book['DownloadQueue'] = [list(queue[0])] + [[r[k] for k in queue[0]] for r in queue]
book['Triage'] = [book['Triage'][0]]+[[r['record_id'],occ[r['record_id']]['run_id'],occ[r['record_id']]['title'],occ[r['record_id']]['year'],r['decision'],r['reason_code'],r['rationale'],r['canonical_record'],r['evidence_basis']] for r in triage]
for row in book.get('NewQueue', [])[1:]:
    if row[0] in byid:
        s = byid[row[0]]
        row[4],row[5],row[6],row[7]='accepted',s['publication_date'],'retrieved_and_assessed',s['study_id']
fields=['record_id','doi','publication_status','decision','source_url','source_anchor','mechanism','environment','workload','comparator','outcome','limitations']
book['AssessedNew'] = [['Record','DOI','Publication','Decision','Source','Anchor','Mechanism','Environment','Workload','Comparator','Outcome','Limitations']]+[[a[f] for f in fields] for a in assess]
if 'Extension' in book:
    book['Extension'][-1][-2] = 'Batch 1: ten full texts accepted with QA/extraction; 31 current studies; two earlier extension assessments still await integration. Other screening reconciliation remains open.'
save('workbook_source.json', book)

out=[r'\section{Batch 1: full-text decisions and current accepted set}\label{sec:batch1}',
     r'Ten user-supplied full-report conversions were received and assessed on 17 October 2026 by AI-CODEX. All ten satisfy the adopted eligibility rules and add distinct studies, GA-S022--GA-S031. The current accepted evidence set therefore contains \textbf{31 unique studies (21+10)}. This is an accepted-set update, not a claim that four-database screening or the final PRISMA flow is complete. Pantheon and Jormungandr retain their earlier eligible-pending-integration status and are outside the 31.',
     r'The supplied 76-record deduplicated download queue now records ten received and assessed reports and 66 still awaiting assessment. The extension full-text register contains twelve assessed reports: the ten accepted here and the two earlier preliminary assessments. Received files are not re-requested. Occurrences, reports, and unique studies remain separate counting units.',
     r'\subsection{Eligibility, publication window and report identity}',
     r'The first-page DOI/title matches were checked against the occurrence ledger, the prior 21-study set, and the other reports in this batch. No duplicate study was identified. MIGER, BOER and MMK describe distinct designs and evaluations despite related mechanisms and citations. EnerTune cites an earlier workshop precursor; it is a version lead, not a second included study. All four 2026 reports have printed publication or conference dates before 11 October: MMK (July), MIGServe and AdMix (28 September--1 October), and EnerTune (29 September--2 October). Exact online dates remain distinct from event/issue dates. Deft retains export publication year 2024 and printed WoC 2023 event/reference dates; this discrepancy does not change eligibility.',
     r'Deft and AdMix are full original workshop proceedings reports with implemented evaluations, not poster abstracts. Their limited experiment breadth is reflected in appraisal and transfer caveats. Mixed inference/training studies qualify only for their explicit inference-specific local sharing evidence. Multi-GPU aggregate improvements remain separately labelled.',
     r'\begin{longtable}{P{0.14\linewidth}P{0.22\linewidth}P{0.44\linewidth}r}',
     r'\toprule Study & Report & Eligible evidence stratum & QA\\\midrule\endhead']
for s in reviews:
    out.append(tex(s['study_id'])+' & '+tex(s['key'])+r' \cite{'+s['key']+'} & '+tex(s['mechanism'])+' & '+f"{sum(s['scores']):g}"+r'\\')
out += [r'\bottomrule\end{longtable}', r'\subsection{Bounded extraction and contradictory evidence}']
for s in reviews:
    out += [r'\paragraph{'+tex(s['study_id']+' '+s['key'])+r'.} '+tex(s['finding'])+' '+tex(s['limitation'])+r' \textit{Source:} '+tex(s['anchor'])+'.']
bands=Counter(q['band'] for q in allq); total=sum(float(q['total']) for q in allq)
out += [r'\subsection{Quality, isolation and sensitivity}',
        f'The ten batch scores total {sum(sum(s["scores"]) for s in reviews):g}/100. Across the current 31-study set, the total is {total:g}/310 (mean {total/31:.2f}); {bands["high"]} high, {bands["moderate"]} moderate and {bands["low"]} low. The original Q1--Q10 rubric is unchanged. Each new item score has a rationale and source anchor in '+r'\path{batch1_quality.csv}; \path{current_quality.csv} combines the historical and batch registers. The current study-level evidence cards include all 31 studies.',
        r'Excluding moderate-QA reports removes Deft and FaST-GShare from this batch as well as the four moderate reports in the earlier set. This weakens adaptive synchronization and serverless quota evidence; it does not establish that all remaining studies have comparable or complete measurement controls. No numerical effect is pooled across studies.',
        r'SGDRC explicitly cannot contain co-located GPU runtime faults in its shared context (section 10). MIG-based partition descriptions do not establish adversarial security or fault-injection results. AdMix and EnerTune show why higher throughput or utilization is insufficient: protected-service latency and energy can worsen under particular sharing configurations. These are conditional trade-offs, not universal rankings.',
        r'\subsection{Evidence and remaining work}',
        r'The historical 11 October registers and flow remain available unchanged. Extension decisions are authoritative in \path{new_fulltext_assessments.csv}, supported by \path{batch1_review_assessments.json}, per-item QA, extraction and SHA-256 receipts. The combined accepted views are \path{current_accepted.csv}, \path{current_extraction.csv}, \path{current_quality.csv} and \path{current_included_studies.json}. The workbook Included and Quality tabs show 31 studies; its Summary tab is explicitly historical and Current shows the later accepted set. The bibliography contains 31 preferred reports.',
        r'\pending{Complete the remaining retrieval/eligibility records, reconcile the supplied Step 3--5 decisions and duplicate/version links, integrate or resolve the two earlier extension assessments, and derive a complete four-database PRISMA flow. The 66 remaining download-queue entries are candidate reports, not guaranteed additions. No unavailable chart data, reviewer consensus, or screening outcome is invented.}']
chapter='\n\n'.join(out)+'\n'
chapter=chapter.replace('current accepted set', 'batch-1 accepted checkpoint').replace('The current accepted evidence set therefore contains', 'At this batch checkpoint, the accepted evidence set contained').replace('now records ten', 'recorded ten at the batch-1 checkpoint').replace('66 still awaiting', '66 then awaiting').replace('Across the current 31-study set', 'At the 31-study batch-1 checkpoint').replace('The current study-level evidence cards include all 31 studies.', 'The evidence cards included 31 studies at this checkpoint; batch 2 later updates the combined cards.').replace('The workbook Included and Quality tabs show 31 studies;', 'The workbook Included and Quality tabs showed 31 studies at this checkpoint;').replace('The bibliography contains 31 preferred reports.', 'The bibliography contained 31 preferred reports at this checkpoint.').replace('The 66 remaining download-queue entries', 'The 66 entries remaining at this checkpoint')
(R/'query_batch1.tex').write_text(chapter)
notes=['# Batch 1 full-text review — 17 October 2026',
       'Single reviewer: AI-CODEX. Ten supplied Markdown conversions were read for eligibility, original Q1–Q10 appraisal, and source-anchored extraction. Source bodies remain private; only metadata, SHA-256 receipts, scores and paraphrases are committed.',
       'Current accepted set: 31 unique studies (21 historical + 10 new). The extension full-text register contains 12 assessed reports: 10 accepted here and 2 earlier eligible-pending-integration reports. The supplied 76-entry download queue has 10 received and 66 unassessed. These are not a completed PRISMA flow.',
       'The historical Flow A registers remain reproducible. Current combined accepted/quality/extraction registers use the `current_` prefix; extension decisions remain in `new_fulltext_assessments.csv`. Do not add 10 to the historical Flow A PRISMA boxes.']
for s in reviews:
    notes += [f"## {s['study_id']} — {s['key']}",s['eligibility'],f"DOI: {s['doi']}. Publication basis: {s['publication_date']}. QA: {sum(s['scores']):g}/10.",s['finding'],s['limitation'],f"Anchor: {s['anchor']}"]
(E/'batch1_review.md').write_text('\n\n'.join(notes)+'\n')
print(json.dumps(counts, indent=2))
