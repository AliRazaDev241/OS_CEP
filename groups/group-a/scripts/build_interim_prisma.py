"""Reconcile the logged four-source checkpoint without claiming final report identity."""
import csv
import json
from collections import Counter
from pathlib import Path

E = Path(__file__).resolve().parents[1] / "evidence"


def rows(name):
    with (E / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


old = json.loads((E / "prisma_counts.json").read_text())
occurrences = rows("new_export_occurrences.csv")
triage = rows("new_screening_triage.csv")
step5 = rows("received_step5_decisions.csv")
assessments = rows("new_fulltext_assessments.csv")
queue = rows("deduplicated_download_queue.csv")
current = rows("current_accepted.csv")
assert len(occurrences) == len(triage) == 3727
assert len({r["record_id"] for r in occurrences}) == 3727
assert len({r["record_id"] for r in step5}) == len(step5) == 596
assert {r["record_id"] for r in step5} <= {r["record_id"] for r in occurrences}
assert Counter(r["run_id"] for r in occurrences) == {
    "ACM-MASTER": 1829, "SD-TEMPORAL": 1053, "SD-MPS": 563,
    "SD-MIG": 241, "SD-API": 41,
}
assert Counter(r["decision"] for r in triage)["remove_exact_doi_duplicate"] == 427
assert Counter(r["decision"] for r in triage)["remove_exact_bibkey_duplicate"] == 88
assert Counter(r["decision"] for r in step5) == {"X": 526, "R": 66, "L": 4}
assert Counter(r["decision"] for r in assessments) == {
    "accepted": 22, "excluded": 9, "eligible_pending_integration": 2,
}
assert len(queue) == 76 and sum(r["download_status"].startswith("received_assessed") for r in queue) == 31
assert len(current) == len({r["study_id"] for r in current}) == 43
assert old["formal_occurrences"] == 689 and old["formal_duplicates"] == 10
assert old["supplementary_selected"] == 20 and old["excluded_before_fulltext"] == 575
assert old["fulltext_assessed"] == 28 and old["not_retrieved"] == 96

# The 11 reinstatements and 4 additional links are documented in the received
# Step 5 review, but are not yet applied as canonical row decisions in triage.
new_exact_links = 427 + 88
additional_links_pending = 4
new_early_excluded = 526 + (2609 - 11) + 6
new_advanced = 66 + 10 + 2
assert new_exact_links + additional_links_pending + new_early_excluded + new_advanced == len(occurrences)
assert len(assessments) + 45 == new_advanced

counts = {
    "status": "INTERIM_FOUR_SOURCE_STAGE_MAP_NOT_FINAL_PRISMA",
    "date": "2026-10-17",
    "formal_by_source": {"IEEE Xplore": 102, "Springer Nature Link": 587,
                         "ACM DL": 1829, "ScienceDirect": 1898},
    "formal_occurrences": old["formal_occurrences"] + len(occurrences),
    "supplementary_selected": old["supplementary_selected"],
    "exact_duplicate_occurrences": old["formal_duplicates"] + new_exact_links,
    "additional_links_pending_adjudication": additional_links_pending,
    "provisional_records_screened": old["formal_occurrences"] + len(occurrences)
        + old["supplementary_selected"] - old["formal_duplicates"]
        - new_exact_links - additional_links_pending,
    "earlier_stage_exclusions": old["excluded_before_fulltext"] + new_early_excluded,
    "advanced_to_retrieval_or_assessed": old["fulltext_assessed"] + old["not_retrieved"] + new_advanced,
    "awaiting_retrieval_request": 45,
    "reports_sought_or_attempted": old["fulltext_assessed"] + old["not_retrieved"] + len(assessments),
    "not_retrieved": old["not_retrieved"],
    "reports_assessed": old["fulltext_assessed"] + len(assessments),
    "assessed_excluded": old["fulltext_excluded"] + 9,
    "eligible_pending_integration": 2,
    "accepted_preferred_reports": len(current),
    "accepted_unique_studies": len(current),
    "limitations": ["Four additional Step 5 links await canonical report/version adjudication.",
                    "45 extension reports are unsought; 96 older reports have unresolved retrieval.",
                    "Publisher displayed hits and parsed export occurrences disagree; coverage is unverified."],
}
assert sum(counts["formal_by_source"].values()) == counts["formal_occurrences"]
assert counts["provisional_records_screened"] == counts["earlier_stage_exclusions"] + counts["advanced_to_retrieval_or_assessed"] == 3907
assert counts["advanced_to_retrieval_or_assessed"] == counts["awaiting_retrieval_request"] + counts["reports_sought_or_attempted"] == 202
assert counts["reports_sought_or_attempted"] == counts["not_retrieved"] + counts["reports_assessed"] == 157
assert counts["reports_assessed"] == counts["assessed_excluded"] + counts["eligible_pending_integration"] + counts["accepted_preferred_reports"] == 61
(E / "interim_four_source_prisma.json").write_text(json.dumps(counts, indent=2) + "\n")
print("PASS: interim four-source flow 4436 identified -> 3907 provisionally screened -> 202 advanced -> 61 assessed -> 43 accepted; open 45+96+2")
