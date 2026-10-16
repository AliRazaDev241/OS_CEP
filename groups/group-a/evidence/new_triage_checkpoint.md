# New export title/abstract triage — checkpoint 3 (16 October 2026)

`new_screening_triage.csv` covers all 3,727 received occurrences in stable source order. The reproducible script `scripts/triage_new_exports.py` checks the 23 private source hashes against `export_intake.csv` and reads the supplied RIS/BibTeX abstracts without committing their bodies. Of 3,727 entries, 3,263 have an abstract and 464 do not. The script also compares normalized DOI against all 709 preexisting `studies.csv` rows, including the 20 supplementary records.

| First-pass class | Occurrences | Basis |
|---|---:|---|
| Exact DOI repeat | 427 | Same normalized DOI to a prior old or new occurrence; preserve source provenance |
| Exact ACM BibTeX key repeat | 88 | Same nonempty key in the overlapping master exports; retain source occurrence |
| Title/abstract exclusion | 2,615 | Six previously documented exclusions plus 2,609 rule-assisted decisions with explicit E1/E2/E4 rationale |
| Retrieve for eligibility | 12 | Previously recorded priority candidates, not full-text inclusions |
| Needs individual title/abstract review | 585 | Topical or ambiguous metadata, including version/date checks and missing abstracts |
| Total | 3,727 | Occurrences, not deduplicated reports or included studies |

The code protects papers discussing concurrent inference even when `GPU` is absent from their title/abstract, and it does not equate a title-only match or a different DOI with a duplicate. The exclusion rule uses supplied title/abstract evidence: no identifiable accelerator sharing mechanism, or GPU material without inference-serving evidence. A random sample of 30 rule exclusions was inspected for obvious topical false negatives; this sampling is not a claim of independent dual review. The rule cannot find a relevant local-GPU experiment hidden only in the full text. Its decisions must be reviewed for sensitivity before a final systematic flow; do not promote the 585 open decisions, 12 retrieval leads or 515 exact DOI/key links directly into a final included-study count.

This is a durable screening chunk, not the final query deliverable. The earlier 21-study extraction and the interim 11 October PRISMA diagram are unchanged. Next: inspect the 585 ambiguous records, adjudicate the remaining 31 different-DOI title matches and cross-source report versions, recover and assess eligible full texts, then revise the flow and Section 14 extraction. The ACM/ScienceDirect operator-count conflicts remain independent of this screening pass.
