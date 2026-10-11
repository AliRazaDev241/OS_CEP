"""Publish paraphrased review notes and batch history, never source paper contents.

Optional --source-dir verifies/refreshes the private conversion receipt hashes.
Without sources the committed receipt ledger supports a portable rebuild.
"""
import argparse,csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parents[1];E=P/'evidence'
arg=argparse.ArgumentParser();arg.add_argument('--source-dir',type=Path);args=arg.parse_args()
reviews=json.loads((E/'uploaded_review_assessments.json').read_text())
def write(name,rows):
    with (E/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
if args.source_dir:
    receipts=[]
    for r in reviews:
        data=(args.source_dir/r['filename']).read_bytes()
        receipts.append(dict(record_id=r['record_id'],study_id=r['study_id'],filename=r['filename'],received_date='2026-10-11',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),decision='preferred_journal_version_same_study' if r['key']=='reef' else 'accepted_new_study',qa_total=sum(r['scores']),source_format='User-provided Markdown conversion; source file private',plot_status='Chart pixels not supplied; numerical prose/tables only'))
    write('uploaded_paper_receipts.csv',receipts)
records={r['record_id']:r for r in csv.DictReader((E/'studies.csv').open())}
priority=['GA-X005','GA-R0011','GA-R0004','GA-R0292','GA-R0006','GA-R0014','GA-X006','GA-X007','GA-R0009','GA-R0037']
received={r['record_id'] for r in reviews}
write('original_download_batch.csv',[dict(original_priority=i,record_id=rid,title=records[rid]['title'],url=records[rid]['url'],receipt_status='received_and_assessed' if rid in received else 'unavailable_no_repeat_request',active_request='no') for i,rid in enumerate(priority,1)])
notes='''# Six supplied papers — full-text review, 11 October 2026

This completes the six-paper review stage under the adopted Group A protocol. AI-CODEX is the sole reviewer. Source files are user-supplied Markdown conversions of published journal articles; their filenames and SHA-256 hashes are in uploaded_paper_receipts.csv. No licensed full text is committed. Assessments and source locations are reproducible from uploaded_review_assessments.json; the originals remain private.

Five new studies are included. The more complete REEF journal version replaces the OSDI2022 preferred report within GA-S001. The conference record remains a full-text E8 companion, not an eligibility rejection of REEF itself. companion_report_extraction.csv and companion_report_quality.csv preserve the former assessment. Six pending reports resolved plus the superseded conference classification increase full-text assessments from22 to28; unique studies rise16 to21, full-text exclusions6 to7, and pending cases102 to96. Discovery counts remain689 formal occurrences,10 duplicates and20 selected supplementary records.

| Record | Study | Paper | Decision | QA /10 |
|---|---|---|---|---:|
'''
for r in reviews:
    notes+=f"| {r['record_id']} | {r['study_id']} | {r['key']} | {'Preferred journal version; same study' if r['key']=='reef' else 'Include'} | {sum(r['scores']):g} |\n"
notes+='\nThe six conversions contain readable evidence for eligibility, but do not preserve original plot pixels. Missing chart points, CDF percentiles, damaged equations and uncertain labels are not reconstructed. Source line numbers refer to the supplied conversion; printed pages/sections/figure identifiers are preferred for later checking. NOT EXTRACTED is different from not reported in the original. No experimental code has been rerun.\n'
for r in reviews:
    notes+=f"\n## {r['study_id']} — {r['key']}\n\n{r['eligibility']}\n\n**Source:** {r['publisher_url']}; {r['anchor']}.\n\n**Setup:** {r['environment']}\n\n**Workload:** {r['workload']}\n\n**Comparators:** {r['comparator']}\n\n**Bounded outcome:** {r['finding']}\n\n**Limits:** {r['limitation']}\n\n**Isolation:** Performance: {r['performance_isolation']} Resource/memory: {r['resource_memory']}. Security: {r['security']}. Fault containment: {r['fault_containment']}.\n\n"
    notes+='QA: '+ '; '.join(f"Q{i}={score:g}: {r['qa_rationales'][i-1]}" for i,score in enumerate(r['scores'],1))+'.\n'
notes+='''
## What remains

The original shortlisting/report checkpoint was merged through PR3. This update completes the six supplied full-text decisions, QA, extraction and report-version assessment. The intermediate deliverable is updated; it is not the final CEP report. No remaining-four or replacement download batch is requested. Unavailable records stay pending/deferred.

Next work: recover formal ACM/ScienceDirect query exports through accessible routes, document unrecoverable coverage, continue already identified public manuscript leads, check relevant publication dates and versions, fill configuration/measurement gaps where readable, perform systematic citation chasing and transparent sensitivity synthesis. Then produce the final20-30-page CEP report with RQ answers, decision matrix, reconciled flow and appendices. Human audit remains useful for the disclosed single-AI-reviewer bias. The21-study eligible checkpoint exceeds the15-20 target; retain eligible evidence and justify any later narrowing rather than silently dropping papers.
'''
(E/'six_paper_review.md').write_text(notes)
