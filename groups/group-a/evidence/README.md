# Group A evidence — 11 October 2026

Start with search_runs.csv, prisma_counts.json and studies.csv. imported_records.json preserves all689 formal query occurrences; duplicates.csv links10 repeated records without deleting provenance. studies.csv is the decision authority; accepted.csv, rejected.csv and pending.csv are derived views. Sixteen study IDs link accepted reports to extraction.csv, quality.csv and the included-only report/references.bib. Supplementary selected records are20, not an exhaustive web export.

Screening is one AI reviewer authorized by the user, not independent student review. Title exclusions are explicitly title-stage judgments; no unavailable paper has an invented full-text result. Access failures remain pending. A report ID identifies a bibliographic report candidate; a study ID is assigned only when identity is assessed (the pending REEF journal extension links to its conference study).

Public result-page capture substitutes for unavailable publisher exports; it does not preserve abstracts that were never displayed. metadata contains only the matched result item, never signed-in account or network details. retrieval_lookups.json is a sanitized public-access ledger, not an archive of copyrighted full texts. Download requests are linked to NED-listed platforms; individual entitlements are unverified.

Counts reconcile the captured subset only. ACM/ScienceDirect totals are UNKNOWN. No final PRISMA diagram or completed four-database SLR is claimed. Use the report's checkpoint flow and the machine-readable counts together.

Calibration/reconsiderations: PipeSwitch retained because inference switching outcomes are explicit; KRISP retained under protocol7.2 local partition/API control but its AMD emulation is isolated from NVIDIA MPS evidence; TGS excluded as training-only; Fermilab Triton reconsidered and retained only after Fig10 showed concurrent distinct models inside a slice. DIPPM rejected at full text because profile suggestion alone is not concurrent tenant evaluation. No reviewer disagreement or consensus is invented.

Rebuild derived data: python groups/group-a/scripts/build_evidence.py, then python groups/group-a/scripts/build_report.py. Validate with validate_evidence.py. The scripts preserve recorded assessments; they cannot recreate searches or replace reviewer decisions. The Excel workbook is a review view of the CSV registers, with count formulas; CSV/JSON remain authoritative.
