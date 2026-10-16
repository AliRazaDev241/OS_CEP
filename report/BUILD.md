# Report files and builds

All Group A deliverables are collected in this root `report/` directory:

- `SLR_protocol.tex` and `SLR_protocol.pdf`: original submitted protocol, renamed without changing contents.
- `query_report.tex` and `query_report.pdf`: intermediate search, shortlisting and evidence report.
- `query_review_workbook.xlsx`: filterable evidence review workbook; CSV/JSON records under `groups/group-a/evidence/` remain authoritative.
- `query_references.bib` and `IEEEtran.bst`: query report bibliography and its unmodified LPPL bibliography style.

Compile the query report from this directory with `latexmk -pdf -interaction=nonstopmode -halt-on-error query_report.tex`; the output is directly `query_report.pdf`. There is no copy/rename step. The protocol's bibliography is embedded in its source; use `latexmk -pdf SLR_protocol.tex` if you need to rebuild it. The preserved protocol PDF was moved byte-for-byte, not regenerated.

From the repository root, rebuild evidence with `python groups/group-a/scripts/build_evidence.py`, then `python groups/group-a/scripts/build_uploaded_review.py`, then `python groups/group-a/scripts/build_report.py`. The report builder preserves the manually maintained `query_report.tex` marked `GROUP_A_MANUAL_REPORT`; reconcile its text and interim counts against changed ledgers explicitly. Regenerate the 21-study evidence cards with `python groups/group-a/scripts/build_query_appendix.py` and the Group A QA matrix with `python groups/group-a/scripts/build_query_qa.py` before compiling. Validate with `python groups/group-a/scripts/validate_evidence.py`. Regenerate the workbook using the existing `groups/group-a/scripts/build_workbook.mjs` builder and the Codex primary runtime Node; its destination is `report/query_review_workbook.xlsx`. The report inputs `query_method_detail.tex`, `query_step_status.tex`, `query_qa_detail.tex` and `query_evidence_appendix.tex`; keep them beside the main TeX file when compiling. References intentionally follow the appendix.

The 17 October Step 3--5 notes are supplementary review inputs. Their individual decisions are not yet reflected in `new_screening_triage.csv` or the workbook. The report distinguishes the note-level 78 advanced/assessed occurrences from the older first-pass CSV until the row-level reconciliation is performed.

The query PDF uses12-point Times-compatible text with numerical IEEEtran citations. It remains an intermediate deliverable; final20-30-page CEP submission and incomplete database coverage are separate outstanding work. The original protocol contents and Group B evidence are preserved.
