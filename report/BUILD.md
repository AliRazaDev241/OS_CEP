# Report files and builds

All Group A deliverables are collected in this root `report/` directory:

- `SLR_protocol.tex` and `SLR_protocol.pdf`: original submitted protocol, renamed without changing contents.
- `query_report.tex` and `query_report.pdf`: intermediate search, shortlisting and evidence report.
- `query_review_workbook.xlsx`: filterable evidence review workbook; CSV/JSON records under `groups/group-a/evidence/` remain authoritative.
- `query_references.bib` and `IEEEtran.bst`: query report bibliography and its unmodified LPPL bibliography style.

Compile the query report from this directory with `latexmk -pdf -interaction=nonstopmode -halt-on-error query_report.tex`; the output is directly `query_report.pdf`. There is no copy/rename step. The protocol's bibliography is embedded in its source; use `latexmk -pdf SLR_protocol.tex` if you need to rebuild it. The preserved protocol PDF was moved byte-for-byte, not regenerated.

From the repository root, rebuild evidence with `python groups/group-a/scripts/build_evidence.py`, then `python groups/group-a/scripts/build_uploaded_review.py`, then `python groups/group-a/scripts/build_report.py`. The report builder preserves the manually maintained `query_report.tex` marked `GROUP_A_MANUAL_REPORT`; reconcile its text and interim counts against changed ledgers explicitly. Regenerate the current evidence cards with `python groups/group-a/scripts/build_query_appendix.py` and the Group A QA matrix with `python groups/group-a/scripts/build_query_qa.py` before compiling. Validate with `python groups/group-a/scripts/validate_evidence.py`. Regenerate the workbook using the existing `groups/group-a/scripts/build_workbook.mjs` builder and the Codex primary runtime Node; its destination is `report/query_review_workbook.xlsx`. The report inputs `query_method_detail.tex`, `query_step_status.tex`, `query_qa_detail.tex` and `query_evidence_appendix.tex`; keep them beside the main TeX file when compiling. References intentionally follow the appendix.

The 17 October Step 3--5 notes are supplementary review inputs. Their individual decisions are not yet reflected in `new_screening_triage.csv` or the workbook. The report distinguishes the note-level 78 advanced/assessed occurrences from the older first-pass CSV until the row-level reconciliation is performed.

The report also includes `query_prisma_interim.tex`, an interim four-source stage map. Run `python groups/group-a/scripts/build_interim_prisma.py` from the root to validate its stage arithmetic and refresh `groups/group-a/evidence/interim_four_source_prisma.json` before compiling. Four additional links and Step 5 exclusions still need canonical row-level reconciliation; the figure does not claim final PRISMA completion.

The query PDF uses12-point Times-compatible text with numerical IEEEtran citations. It remains an intermediate deliverable; final20-30-page CEP submission and incomplete database coverage are separate outstanding work. The original protocol contents and Group B evidence are preserved.


## Batch 1 update (17 October 2026)

The original 21-study Flow A is a historical checkpoint. The current accepted set is 31. Extension decisions are in `new_fulltext_assessments.csv`; `batch1_review_assessments.json` contains the ten recorded full-text assessments. `current_accepted.csv`, `current_quality.csv`, `current_extraction.csv` and `current_included_studies.json` combine those with the baseline. `batch1_counts.json` reports accepted-set progress, not a final PRISMA flow. Do not use the historical count JSON as the current included-study total.

After the existing baseline evidence/report builders, run:

```bash
python groups/group-a/scripts/build_batch1.py
python groups/group-a/scripts/build_query_appendix.py
python groups/group-a/scripts/build_query_qa.py
python groups/group-a/scripts/validate_evidence.py
```

Optional `--source-dir PRIVATE_SOURCE_DIRECTORY` on `build_batch1.py` checks the original ten conversion hashes/byte sizes without publishing source files. The same script is safe to rerun; its updates use stable IDs. It refreshes the ten affected Triage/NewQueue/AssessedNew rows and the Included/Quality/Received views, plus Current, Batch1 and the supplied 76-entry DownloadQueue. Summary is explicitly historical. Unintegrated Step 3--5 decisions remain a separate work item.

Then run `build_workbook.mjs` with the Codex primary runtime and compile from `report/` using the command above. Copy the MJS builder into a writable temporary directory with the runtime `node_modules` symlink and set `OS_CEP_GROUP_A_ROOT` to the absolute `groups/group-a` directory. The script needs the `query_batch1.tex` and `query_batch2.tex` inputs beside the other report inputs. The report's QA/evidence cards use the current 34-study registers after both batch builders. Re-running the baseline report builder preserves extension workbook views; run the batch builder afterward to refresh current values.

## Batch 2 update (17 October 2026)

After `build_batch1.py`, run `python groups/group-a/scripts/build_batch2.py` (optionally `--source-dir PRIVATE_SOURCE_DIRECTORY` to verify all eleven source hashes). Then regenerate appendix/QA, validate, rebuild the workbook and compile the PDF. Batch 2 assesses eleven reports: three accepted (GA-S032–GA-S034), eight excluded. The combined accepted set is 34; 21 of the 76 queue reports are assessed and 55 remain. `batch2_review_assessments.json`, `batch2_exclusions.json`, `batch2_paper_receipts.csv`, `batch2_quality.csv` and `batch2_extraction.csv` record source-linked decisions without paper bodies. The historical 21-study checkpoint and PRISMA diagram remain distinct.

## Batch 3 update (17 October 2026)

After `build_batch2.py`, run `python groups/group-a/scripts/build_batch3.py` (optionally `--source-dir PRIVATE_SOURCE_DIRECTORY` for the ten conversion hashes). Regenerate appendix/QA and validate, rebuild the workbook, then compile the PDF. Nine studies GA-S035–GA-S043 are added, one report is excluded. The 43-study accepted set and 45 remaining queue entries are current progress, separate from the historical PRISMA flow. The private full texts remain outside Git.
