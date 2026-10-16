# Group A export intake — chunk 1 (16 October 2026)

This is an intake checkpoint for the ACM Digital Library and ScienceDirect files in `C:\Projects\OS_CEP\OS_CEP_query_export`. It extends the 11 October intermediate report; it does **not** revise that report's PRISMA flow or screen records. The 23 export files on that PC match the uploaded copies byte for byte by SHA-256. Their bytes are held outside the public repository. `export_intake.csv` records source filenames, complete hashes, sizes, parsed entry counts and the associated run-log fields. `search_log_received.txt` preserves the supplied operator log; `search_runs_received.csv` transcribes its five runs and flags conflicts.

## What is available

| Source | Batches | Parsed entries, before cross-file deduplication | Integrity observation |
|---|---:|---:|---|
| ScienceDirect, temporal | 11 RIS | 1,053 | Each file's `TY` and `ER` counts match |
| ScienceDirect, MPS | 6 RIS | 563 | Each file's `TY` and `ER` counts match; one filename begins `SSD_` |
| ScienceDirect, MIG | 3 RIS | 241 | Each file's `TY` and `ER` counts match |
| ScienceDirect, API | 1 RIS | 41 | `TY` and `ER` counts match |
| ACM, master 01 | 1 BibTeX | 829 | 829 entry starts; 829 distinct entry keys |
| ACM, master 02 | 1 BibTeX | 1,000 | 1,000 entry starts; 1,000 distinct entry keys |

There are **23 export files and 3,727 parsed entry occurrences** (1,898 RIS plus 1,829 BibTeX). The ACM files share 442 exact BibTeX keys, leaving 1,387 distinct keys across those two files. This is a parser/key check, not a DOI/title-level deduplication or PRISMA count. A record may appear in several ScienceDirect family exports and in the preexisting IEEE/Springer register. The log records 1,600 displayed ACM hits, 1,053 temporal, 517 MPS, 241 MIG and 41 API ScienceDirect hits. Displayed hits and exported occurrences are distinct measures; neither is substituted for the other.

The directory's 24th item is `search_log.txt.txt`, resolving the initial file-count question. Conversation upload variants marked `(1)`, `(2)`, `(3)` and a different-size `ACM_MASTER_01.bib.bib` are not additional PC-directory exports or search runs. The selected matching uploaded copies provided the parsed entry counts and hashes. `SSD_MPS_06.ris` retains its exact source filename.

## Reconciliation before PRISMA update

- **ACM:** the operator recorded 1,600 displayed hits and 1,603 exported records, whereas the two matching BibTeX files parse to 829 + 1,000 = 1,829 entries. The files overlap by 442 exact entry keys. Obtain page ranges/export selections or a corrected operator log to explain the difference; do not assign 1,600, 1,603 or 1,829 as an unquestioned identification count.
- **ScienceDirect MPS:** 517 displayed hits versus 563 exported and parsed entries. Confirm whether the page selections changed across refreshes, repeated records were exported, or the displayed count was transcribed incorrectly.
- **ScienceDirect temporal:** 1,053 displayed hits and 1,053 parsed entries, but the logged result URL contains an `openaccess` facet that the written filters list omits. Check whether that facet was applied at export time. The other three ScienceDirect family counts match their parsed entry totals.
- **Publication cutoff:** the recorded 2020–2026 interface facets may admit dates after the protocol's 11 October 2026 cutoff. Enforce the cutoff during screening. ACM's transformed query uses all fields and the ACM Full-Text Collection; record this scope rather than treating it as metadata-only.

## Provenance and next checkpoints

1. Confirm page ranges/export selections and the three conflicts above with the operator. The received log supplies exact entered/transformed ACM query, ScienceDirect family strings, fields, dates, URLs and displayed totals, but the contradictory totals and temporal facet prevent final flow reconciliation.
2. Parse all entries with stable new **record IDs** scoped to the source batch. Preserve raw fields and byte hash; link them to the existing Group A report/study IDs without overwriting earlier decisions. Validate RIS boundaries and BibTeX multiline/braced values before screening.
3. Deduplicate within and across ACM, ScienceDirect, IEEE, Springer and supplementary discovery using normalized DOI plus title/author/year checks. Preserve every occurrence and manually adjudicate ambiguous matches and related publication versions.
4. Screen new unique reports using the frozen Group A protocol. Record one authorized AI reviewer, title/abstract decision and reason, retrieval status, full-text decision/reason, and study links. Bibliographic metadata is not full-text evidence; do not infer quality or findings from these exports.
5. Reconcile new search-run and PRISMA counts from the record ledger; then update `report/query_report.tex`, the checked PDF and `report/query_review_workbook.xlsx`. Complete quality assessment and source-anchored extraction for newly eligible full texts under protocol §§10–11. Preserve the previous checkpoint in version history.

The first chunk resolves access to the export bytes and log and creates a reproducible file/run receipt. Deduplication, screening, quality assessment, extraction and updated PRISMA counts remain pending; the existing report's ACM/ScienceDirect `UNKNOWN` status accurately describes its **11 October** checkpoint, before these 14 October runs were supplied.
