# Group A export intake — chunk 1 (16 October 2026)

This is an intake checkpoint for the ACM Digital Library and ScienceDirect files supplied in the OS CEP conversation. It extends the 11 October intermediate report; it does **not** revise that report's PRISMA flow, screen records, or assert completed ACM/ScienceDirect searches. The received bytes are held outside the public repository. `export_intake.csv` records the selected source filenames, complete SHA-256 hashes, sizes, and parsed entry counts.

## What is available

| Source | Batches | Parsed entries, before cross-file deduplication | Integrity observation |
|---|---:|---:|---|
| ScienceDirect, temporal | 11 RIS | 1,053 | Each file's `TY` and `ER` counts match |
| ScienceDirect, MPS | 6 RIS | 563 | Each file's `TY` and `ER` counts match; one filename begins `SSD_` |
| ScienceDirect, MIG | 3 RIS | 241 | Each file's `TY` and `ER` counts match |
| ScienceDirect, API | 1 RIS | 41 | `TY` and `ER` counts match |
| ACM, master 01 | 1 BibTeX | 829 | 829 entry starts; 829 distinct entry keys |
| ACM, master 02 | 1 BibTeX | 1,000 | 1,000 entry starts; 1,000 distinct entry keys |

There are **23 selected files and 3,727 parsed entry occurrences** (1,898 RIS plus 1,829 BibTeX). The ACM files share 442 exact BibTeX keys, leaving 1,387 distinct keys across those two files. This is a parser/key check, not a DOI/title-level deduplication or PRISMA count. A record may appear in several ScienceDirect family exports and in the preexisting IEEE/Springer register. The export occurrence count is **not** a database hit count: query result totals, exact queries, facets, dates and page/export coverage must be corroborated by the search-run evidence.

The Library also contains filename variants marked `(1)`, `(2)`, `(3)` and a different-size `ACM_MASTER_01.bib.bib`. Selection in the CSV used the larger available variant for each normalized ScienceDirect batch and the matching-size `(1)` copies of the two ACM master files. The alternate ACM file has **not** been assumed equivalent or counted. The user described 24 uploads; only 23 distinct canonical batch labels were identifiable from the 21 ScienceDirect family files and two ACM master files. Reconcile the twenty-fourth intended batch against a user's export list or search log before declaring the inventory complete. The duplicate-name variants and differing small first-page exports are not additional search runs by themselves.

## Provenance and next checkpoints

1. Link each batch to an actual database run: executed query, searched fields/collection, filters, local date, result URL, displayed total, range or pages exported, and operator. The metadata exports alone do not establish these fields. Do not replace `UNKNOWN` by guesses from filenames or parsed entries.
2. Parse all entries with stable new **record IDs** scoped to the source batch. Preserve raw fields and byte hash; link them to the existing Group A report/study IDs without overwriting earlier decisions. Validate RIS boundaries and BibTeX multiline/braced values before screening.
3. Deduplicate within and across ACM, ScienceDirect, IEEE, Springer and supplementary discovery using normalized DOI plus title/author/year checks. Preserve every occurrence and manually adjudicate ambiguous matches and related publication versions.
4. Screen new unique reports using the frozen Group A protocol. Record one authorized AI reviewer, title/abstract decision and reason, retrieval status, full-text decision/reason, and study links. Bibliographic metadata is not full-text evidence; do not infer quality or findings from these exports.
5. Reconcile new search-run and PRISMA counts from the record ledger; then update `report/query_report.tex`, the checked PDF and `report/query_review_workbook.xlsx`. Complete quality assessment and source-anchored extraction for newly eligible full texts under protocol §§10–11. Preserve the previous checkpoint in version history.

The first chunk resolves access to the export bytes and creates a reproducible file-level receipt. The open query and filter fields, ambiguous alternate, deduplication, screening, quality assessment, and extraction remain pending; the existing report's ACM/ScienceDirect `UNKNOWN` status remains accurate for its 11 October checkpoint.
