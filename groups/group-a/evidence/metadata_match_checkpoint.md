# Group A metadata matching — chunk 2 (16 October 2026)

The deterministic import in `scripts/import_new_exports.py` checks each of the 23 PC-directory files against the SHA-256 receipt, parses 3,727 occurrences, and compares normalized DOI or title with the **689 preexisting formal records** in `imported_records.json`. It emits stable `GA-N00001`–`GA-N03727` occurrence IDs and leaves every new screening status `not_screened`.

| Automated match class | Occurrences | Meaning |
|---|---:|---|
| DOI match to existing record | 2 | Candidate link to the old ledger |
| Normalized title match to existing record | 7 | Review manually; a title match does not prove same report |
| DOI match to earlier new occurrence | 418 | Candidate internal duplicate |
| Normalized title match to earlier new occurrence | 119 | Review manually; DOI/version differences can matter |
| No match on either key | 3,181 | Candidate for screening, not an eligible study |

There are 596 new occurrences without a DOI and two RIS occurrences without a title. Their missing fields stay blank and require metadata recovery before confident screening. Matching is directional and does not delete any source occurrence. A DOI/title match may link related conference, journal or preprint reports rather than exact duplicates; the report/study distinction in the protocol still requires human or reviewer assessment. The 20 supplementary records and Group A report/study IDs in other registers have **not yet** been cross-linked. No revised PRISMA count follows from this automated pass, particularly while the ACM and ScienceDirect run totals remain inconsistent.

To reproduce, use the exact 23 private files named in `export_intake.csv` under one directory, and run:

```text
python groups/group-a/scripts/import_new_exports.py --exports <private-export-directory> --intake groups/group-a/evidence/export_intake.csv --baseline groups/group-a/evidence/imported_records.json --output <local-occurrence-ledger.csv>
```

The full generated occurrence ledger is a working metadata file; the next chunk will merge adjudicated report/record links and screening decisions into the authoritative Group A registers, then regenerate the workbook. Until then, keep the 11 October PRISMA checkpoint and its accepted-study set intact.
