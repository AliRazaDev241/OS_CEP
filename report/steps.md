# Group A query report and workbook: remaining steps

**Updated:** 17 October 2026 (PKT)
**Scope:** Complete guideline sections 7–14 in `report/query_report.tex`, `report/query_report.pdf`, and `report/query_review_workbook.xlsx`. PR #5 has merged; the expanded report and this guide belong on the follow-up branch `group-a/expanded-query-report-followup` in `AliRazaDev241/OS_CEP`. Keep the submitted `SLR_protocol.*`, `guidelines.md`, and `topics.md` unchanged. Keep the 11 October checkpoint and its interim PRISMA flow identifiable until a reconciled four-database flow replaces it.

PR #5 merged at `2a03a3f`, containing the earlier provenance edit `67b57f8`. The expanded 41-page report was added to the old head branch after that merge, so it was absent from `main`; this follow-up branch carries it forward. The report describes 23 matching export hashes, the log's final CRLF, dated run-count discrepancies, and the remaining four-database work. Step 1 and Step 2 notes supplied on 17 October were checked against an older uploaded checkout ending at `fa1b17a`; their statement that `67b57f8` is missing applies only to that zip. The workbook still needs regeneration after the final ledgers are settled. Neither 3,727 parsed occurrences nor 21 accepted checkpoint studies is a final four-database PRISMA total.

**Group B reuse check (16 October):** Group B's report describes 1,582 ACM occurrences from 79 numbered BibTeX files whose exact query/run mapping is unknown. It also has 15 source-assessed QA/extraction forms and two full-text exclusions. The 15 named reports overlap Group A's current 21 accepted studies; Group B's counts, votes, QA scores, and decisions are independent and cannot be copied into Group A's flow. Use the report as a checklist of source anchors and possible ACM records only. The numbered exports become Group A identification evidence only if their exact run, filters, date, original files, and duplicate relationship to Group A's exports are established. The supplied Group B TeX alone does not establish those facts.

## Working rules for every step

1. Edit authoritative CSV/JSON decision records first, then generate workbook/report views. Keep every original occurrence ID and source file link.
2. Record **observed**, **inferred**, and **unknown** values separately. Do not alter a site count to match an export count. Keep the original files and log intact; put corrections in a dated note or new field.
3. Count records, reports, and studies separately. One paper can appear in several export files; one study can have several reports.
4. Do not count a retrieval lead or a provisionally assessed report as a newly included study until identity, eligibility, QA, and extraction are settled.
5. A missing full text is a retrieval outcome, not a full-text rejection. Use source page/section/table/figure anchors for technical findings.

## Step 1 — Protect the source and finish the short provenance checks

**Files:** private `C:\Projects\OS_CEP\OS_CEP_query_export`, private `source_papers/`, `groups/group-a/evidence/export_intake.csv`, supplied `step1_provenance_checks.md`.

**Already checked in the uploaded zip (17 October):** 23/23 export hashes and byte sizes match the ledger; six Markdown conversion hashes match their receipt; no screenshots or page-range files appear in that zip; the 6,302-byte original log differs from the 6,304-byte received copy only by a final CRLF. The zip's file times are copy-time clues, not proof of the original export times. These checks do not establish the current PC directory or backup state.

1. Confirm a private backup of the 23 exports, the original `search_log.txt.txt`, and six supplied paper copies outside the public checkout. Do not commit licensed full texts.
2. In PowerShell, run the commands below and save the output privately as `step1_pc_output.txt` with the date. Compare case-insensitive hashes and byte sizes to `export_intake.csv`. Treat any 16 October copy times as copy-time evidence, not proof of a 14 October export time.

   ```powershell
   cd C:\Projects\OS_CEP\OS_CEP_query_export
   Get-ChildItem | Select-Object Name, CreationTime, LastWriteTime | Format-Table -AutoSize
   Get-FileHash -Algorithm SHA256 *.bib, *.ris | Select-Object Hash, @{n='File';e={Split-Path $_.Path -Leaf}}
   ```
3. Inspect the helper's export folder for an ACM screenshot, export-limit notice, or page-range record. Record what was found or `not found`.
4. Keep the original log hash difference closed: its lines are the same; the received copy has one extra final CRLF. Do not edit either copy.
5. If Group B can share the numbered ACM export manifest and raw files under the team's permitted access, compare their hashes and DOI/key/title sets with Group A's two master files. Do not count the 1,582 as additional Group A records at this stage.

**Done when:** the backup is confirmed, the current files still match all 23 ledger hashes, and the two optional provenance searches have dated outcomes. A screenshot or historical creation time is not required if unavailable.

## Step 2 — Close database and query provenance (guidelines 7–8)

**Files:** `search_runs.csv`, `search_runs_received.csv`, `search_log_received.txt`, `export_intake.csv`, `groups/group-a/protocol.md`, `report/query_report.tex`, supplied `step2_search_provenance.md`.

**Already recorded in the supplied Step 2 note:** five successful 14 October runs map to 23 files and 3,727 parsed occurrences; 11 October ACM/ScienceDirect pilots produced no countable hits. The note refers to `search_run_provenance.csv` and `export_file_run_map.csv`, but those companion files were not supplied with these two Markdown files. Do not mark those CSV deliverables present until they are provided or generated and checked.

1. Keep the five successful 14 October runs separate from the blocked 11 October ACM/ScienceDirect pilots. Use `export_intake.csv` to map **all** files to each run; the log names only the first file.
2. The protocol allows a split into family searches using the common inference block. ScienceDirect's four executed family queries omit `DNN OR LLM`, so the omission is a deviation with an unmeasured possible recall loss. Draft a dated amendment, identify affected runs and 1,898 parsed occurrences, and have the team decide whether to rerun and approve the entry. Until that decision, describe the deviation in the report and leave the amendment register unchanged.
3. Record that ACM used the site's Export button for two page ranges in one session; 442 exact keys overlap. Decide with the team whether to re-export in stable, recorded chunks or submit with a clearly stated coverage limitation. Save the decision, date, and basis. A numerical count of *missing* ACM results is not established.
   - Group B's numbered files might locate records absent from the two master files, but its report explicitly labels their run mapping unknown. If the original query, date, filters, and file provenance can be demonstrated, compare unique identifiers before importing any occurrence; otherwise keep them as supplementary discovery leads, not an added formal run.
4. Keep ACM's 1,600 saved displayed value, the operator's 1,603 site count, 1,829 parsed rows, and 1,387 distinct keys as different measurements. Keep MPS's 517 earlier displayed value and 563 export/current-page value as different dated observations. The origin of 517 can remain `not recorded`.
5. Record the ScienceDirect temporal URL's Open Access facet: the operator observed 298 with it and 1,053 without it on **16 October**. The 1,053 exported rows are consistent with the unfiltered set, but this does not prove the filter state on 14 October. Record any content-type or language filters as `not recorded` unless there is source evidence.
6. Confirm whether ACM access used NED VPN, campus IP, or another route if the operator knows. The ACM log says NED library access but does not state how. ScienceDirect VPN use is operator-confirmed. Platform listing and VPN use do not establish article-level entitlement.

**Done when:** every executed run has the exact query, interface/collection, entered or transformed query where recorded, filters or unknowns, date/time or `not recorded`, result URL, displayed hit observation, file mapping, parsed count, and reconciliation note. The original log remains preserved. The remaining ACM coverage decision, amendment, access route, and temporal facet uncertainty are recorded with dated outcomes or explicit limitations.

## Step 3 — Apply the 11 October 2026 publication cutoff (guideline 9)

**Files:** new occurrence/triage ledger, `studies.csv`, date-check notes.

1. Filter the 2026 candidates. The Task 3 total of **1,089 is parsed occurrences** (291 ACM and 798 ScienceDirect), not unique papers.
2. Deduplicate and prioritize candidates that could pass topic screening. For each potentially eligible 2026 report, verify its exact publication date from publisher metadata or the report. Record source URL, accessed date, date type (online/issue/conference), and decision against **11 October 2026 inclusive**.
3. If only a publication year is available, label the exact-date decision unresolved. Do not automatically treat a 2020–2026 site facet as enforcing the October cutoff.

**Done when:** every 2026 candidate that could advance has a supported cutoff decision or a visible unresolved date status.

## Step 4 — Adjudicate duplicates, non-paper records, and report versions

**Files:** `new_export_occurrences.csv`, `new_screening_triage.csv`, `duplicates.csv`, `studies.csv`, report/version register.

1. Preserve all **3,727** occurrence IDs. Review the 427 DOI and 88 ACM-key links from the first pass; verify their canonical targets and any cross-links to the old ledger. Do not add the 442 ACM cross-file repeated keys to 515 as a separate count without checking overlap.
2. Classify the 549 ACM `proceedings` rows (472 distinct keys) as whole-volume records, with a documented record-type exclusion or non-study treatment. Check the book/inbook/techreport types too; a volume is not a primary study merely because it matched the search.
3. Review the 31 different-DOI same-title leads, approximately 20 same-title/different-DOI pairs in SD-MPS, and conference/journal/preprint relationships. A shared title is a lead, not an automatic duplicate.
4. Normalize DOI forms where possible, including bare ACM numeric keys, but retain the original key and raw occurrence. Assign canonical record, report ID, study ID where warranted, relationship, and rationale.

**Done when:** each duplicate removal used in the new PRISMA flow points to an occurrence and canonical record, and each assessed report version maps to one underlying study or a reasoned distinct contribution.

## Step 5 — Finish title and abstract screening (guidelines 10, 12)

**Files:** `new_screening_triage.csv`, title/abstract decision register, `studies.csv`.

1. Individually decide the **585 open occurrences** under the frozen criteria. Read an abstract when available; record `title only` when it is not. Use an inclusion/exclusion code and a short, specific rationale.
2. Sensitivity-review the **2,609 rule-assisted exclusions** for false negatives using a documented method; correct any errors with a dated reason. Keep the six separately documented exclusions distinct. Do not silently turn an assisted rule into an independent human decision.
3. After duplicates and non-paper records are settled, integrate decisions into the canonical ledger without erasing the first-pass class or original source information.

**Done when:** every screened canonical record has a title/abstract outcome, stage, reason where excluded, and reviewer process. The number advanced to retrieval is derived from these rows.

## Step 6 — Retrieve and assess full texts (guidelines 10–12)

**Files:** retrieval register, `new_fulltext_assessments.csv`, `studies.csv`, `rejected.csv`.

1. Follow the ten current retrieval leads and any new leads from Step 5 through lawful public or available institutional routes. Record sought date, source, retrieved/not retrieved outcome, and reason for nonretrieval when known.
2. Read each retrieved full report against the adopted criteria. Record inclusion or exclusion code, a specific reason, and page/section/experiment anchor. Keep the four previously unavailable requested papers as unavailable unless access actually changes.
3. Integrate the two preliminary Pantheon and Jormungandr assessments only after confirming publication/version identity and final eligibility. Link related versions before changing the included-study count.

**Done when:** every sought report has a retrieval state, every assessed report has an anchored eligibility decision, and excluded full texts have reason counts that can be summed.

## Step 7 — Build the complete PRISMA 2020 flow (guideline 11)

**Files:** canonical ledgers, `prisma_counts.json`, `report/query_report.tex`, workbook `Summary`/flow view.

1. Derive by database: identified **occurrences**, duplicates and other removals before screening, records screened, records excluded, reports sought, reports not retrieved, reports assessed, full-text exclusions by reason, included reports, and unique included studies.
2. Keep supplementary identification separate and include its path into screening. Ensure the same record is not counted as both a duplicate removal and a screened exclusion. Keep reports distinct from studies.
3. Assert every transition arithmetically from ledger row IDs. For example, `records screened = identified records - removed before screening`, and `reports assessed = reports sought - reports not retrieved`, after applying the documented mapping between records and reports.
4. Replace the interim TikZ diagram and checkpoint table in `query_report.tex` with the complete four-database flow once settled. Preserve the 11 October flow in historical evidence rather than presenting it as the final flow.

**Done when:** every diagram value and exclusion-reason total can be reproduced from named rows in the authoritative ledgers, and the TeX and workbook show the same values. No unsupported count is inserted to make a box balance.

## Step 8 — Complete quality assessment (guideline 13)

**Files:** `quality.csv`, report QA section, workbook `Quality`.

1. Apply the existing Q1–Q10 rubric (0, 0.5, or 1 per item) to every newly included unique study or preferred full report. Record each score's rationale and full-text anchor.
   - Group B's 15 forms cover reports already named in Group A's 21-study set. Compare their source anchors and caveats as a second reading aid, then verify in Group A's own full texts before changing a Group A score. Do not import Group B scores or imply independent Group A review.
2. Keep the 21 earlier scores unless source verification warrants a documented correction. When a new report replaces an earlier version of the same study, retain the older assessment history and identify the preferred report.
3. Recompute total scores and sensitivity groups from the final included set. Do not score a metadata-only record.

**Done when:** every included study has one current QA result with rationales and anchors, and the workbook mirrors `quality.csv`.

## Step 9 — Complete data extraction (guideline 14)

**Files:** `extraction.csv`, `claims.md`, `included_studies.json`, `query_references.bib`, report study/finding tables, workbook `Included` and `AssessedNew`.

1. For each included study, record mechanism/control boundary, GPU and runtime, model/workload and tenant mix, batching/load, baseline, metric definition and units, result, caveat, and page/figure/table anchor.
   - Use Group B's 15 paper tables and 45 outcome rows to identify potentially missing configuration details or within-paper contrasts for overlapping studies. Verify every useful row against Group A's preferred report version and record the exact source anchor; Group B's REEF conference and ParvaGPU arXiv version should not silently replace Group A's preferred versions.
2. Keep performance interference, resource/memory separation, adversarial security, and fault containment in separate fields. Use `not reported` only after checking the source; use `not yet extracted` while work remains.
3. Keep local-GPU outcomes separate from cluster placement, GPU-count, cost, and fleet outcomes. Add only genuinely new unique studies to the included list and bibliography.
4. Refresh the report's study list, findings, provisional RQ answers, limitations, and references from the finished extraction. Do not infer a common percentage effect across incomparable experiments.

**Done when:** each included study has anchored extraction, QA, an eligibility trail, and a matching report citation; each numerical claim can be traced to its specific experiment and denominator.

## Step 10 — Make the report build reproducible

**Files:** `groups/group-a/scripts/build_report.py`, `report/query_report.tex`, `report/BUILD.md`.

1. The PR branch builder now detects the maintained TeX marker and preserves the expanded report. Keep that guard when adding new generated views.
2. Once the canonical evidence is final, update the maintained sections or generate them from authoritative inputs. Compare the resulting TeX to intended report content before committing.
3. Keep `report/BUILD.md` aligned with the actual build order.

**Done when:** rerunning the builder preserves the verified provenance and produces the same intended TeX from the current ledgers.

## Step 11 — Regenerate and check the workbook

**Files:** `groups/group-a/scripts/build_workbook.mjs`, its input JSON/CSV, `report/query_review_workbook.xlsx`.

1. Review the builder's input sheet structure and extend it as needed. The workbook currently contains the old `Summary`, `Decisions`, `Included`, and `Quality` views plus later intake views such as `Triage`, run reconciliation, priority review, and `AssessedNew`. The CSV/JSON ledgers remain authoritative.
2. Feed the adjudicated run, duplicate, screening, retrieval, eligibility, QA, and extraction rows into those views. Keep raw and canonical IDs available for filters. Add final PRISMA calculations or a clear flow sheet linked to ledger totals.
3. Regenerate with the documented Node runtime, open the workbook, test filters, check formulas and row counts, and compare every summary count against the ledger and TeX.

**Done when:** the workbook has no stale pending status for settled records and its study set, reasons, QA, and flow agree with the report.

## Step 12 — Validate, compile, and inspect the deliverables

1. Once Step 10 is safe and decisions are settled, run from the repository root, in order:

   ```bash
   python groups/group-a/scripts/build_evidence.py
   python groups/group-a/scripts/build_uploaded_review.py
   python groups/group-a/scripts/build_report.py
   python groups/group-a/scripts/validate_evidence.py
   ```

2. Run the workbook builder as described in `report/BUILD.md` using the available Node runtime. From `report/`, compile:

   ```bash
   latexmk -pdf -interaction=nonstopmode -halt-on-error query_report.tex
   ```

3. Inspect the PDF's diagram labels, tables, citations, page breaks, and 12-point text. Check the PRISMA arithmetic, all workbook formulas and filters, and the TeX/PDF/workbook/CSV agreement. Record the check and any remaining limitations in draft PR #5; leave the PR for human review and merge.

**Done when:** the compiled PDF matches the committed TeX, the workbook matches the authoritative ledgers, the validator passes, and guideline sections 7–14 are supported by traceable evidence.

## What can remain unknown without inventing a value

- The exact historical cause of ACM's overlapping page ranges and any unobserved missing results. Disclose export coverage limits and the team's re-export decision.
- The origin of the earlier ScienceDirect MPS 517 display observation; retain the dated 563 export/current-page observations.
- The temporal Open Access facet state at the original export time if no contemporaneous evidence exists.
- ACM's precise NED access route and unrecorded extra publisher filters if the operator cannot substantiate them.

These unknowns belong in the search limitations. They must not be converted into fabricated PRISMA records or silently corrected counts.
