"""Conservative title/abstract triage of the supplied ACM/ScienceDirect occurrences.

Read private exports through the validated receipt. This is a first-pass decision ledger,
not full-text eligibility, quality appraisal or a final PRISMA count. Abstract bodies
are not copied into the public output.
"""
import argparse
import csv
import hashlib
import re
from collections import Counter
from pathlib import Path

from import_new_exports import bib_records, norm_doi, ris_records

ACCELERATOR = re.compile(r"\bgpus?\b|graphics processing unit|\bcuda\b|\baccelerator\b|\bmig\b|\bmps\b|\bnvidia\b|\btensor.?rt\b|\btriton\b", re.I)
INFERENCE = re.compile(r"inferen|serving|\bdnn\b|deep learning|\bllm\b|neural network|model deployment", re.I)
SHARING = re.compile(r"multi.?tenant|co.?locat|co.?execut|shar|partition|virtualiz|\bmig\b|\bmps\b|time.?slic|context.?switch|preempt|remot|interfer|isolat|schedul|concurren|resource allocat|resource manag", re.I)
PROTECT = re.compile(r"multi.?tenant|co.?locat|co.?execut|shar|partition|virtualiz|time.?slic|preempt|interfer|isolat|concurren", re.I)


def read_csv(path):
    return list(csv.DictReader(path.open(newline="", encoding="utf-8")))


def abstracts(exports, receipt, occurrences):
    by_file = {}
    for row in occurrences:
        by_file.setdefault(row["source_file"], []).append(row)
    result = {}
    for batch in receipt:
        path = exports / batch["received_filename"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != batch["sha256"]:
            raise ValueError(f"Receipt mismatch: {path.name}")
        if path.suffix.lower() == ".ris":
            vals = [" ".join(r.get("AB", [])) for r in ris_records(path)]
        else:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            starts = list(re.finditer(r"^@\w+\s*\{([^,]+),", text, re.M))
            vals = []
            for i, match in enumerate(starts):
                block = text[match.end():starts[i + 1].start() if i + 1 < len(starts) else len(text)]
                hit = re.search(r"^abstract\s*=\s*\{(.*)\},?\s*$", block, re.M | re.I)
                vals.append(hit.group(1) if hit else "")
        rows = by_file.get(path.name, [])
        if len(vals) != int(batch["parsed_entries"]) or len(vals) != len(rows):
            raise ValueError(f"Record/abstract cardinality mismatch: {path.name}")
        for row in rows:
            result[row["record_id"]] = vals[int(row["source_ordinal"]) - 1]
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--exports", type=Path, required=True)
    p.add_argument("--evidence", type=Path, default=Path("groups/group-a/evidence"))
    args = p.parse_args()
    e = args.evidence
    rows = read_csv(e / "new_export_occurrences.csv")
    abs_by_id = abstracts(args.exports, read_csv(e / "export_intake.csv"), rows)
    known = read_csv(e / "studies.csv")
    known_doi = {norm_doi(x["doi"]): x["record_id"] for x in known if norm_doi(x["doi"])}
    prior_doi = {}
    prior_bibkey = {}
    exclusions = {x["record_id"]:x for x in read_csv(e / "priority_title_abstract_decisions.csv")}
    queue = {x["record_id"]:x for x in read_csv(e / "priority_fulltext_queue.csv")}
    fields = ["record_id", "canonical_record", "stage", "decision", "reason_code", "rationale", "abstract_available", "evidence_basis", "reviewer", "review_date", "full_text_status"]
    out = []
    for row in rows:
        rid, title, doi = row["record_id"], row["title"], norm_doi(row["doi"])
        bibkey = row["bibtex_key"]
        abstract = abs_by_id[rid]
        text = title + " " + abstract
        prior = known_doi.get(doi) or prior_doi.get(doi) if doi else None
        key_prior = prior_bibkey.get(bibkey) if bibkey else None
        if rid in exclusions:
            q = exclusions[rid]
            vals = ("title_abstract", "exclude", q["primary_reason_code"], q["rationale"], "reviewed title/abstract", q["reviewer"], q["date"], "not assessed")
        elif prior:
            vals = ("pre_screen", "remove_exact_doi_duplicate", "D-DOI", f"Identical normalized DOI to {prior}; occurrence retained for provenance.", "exact normalized DOI", "deterministic", "2026-10-16", "not applicable")
        elif key_prior:
            prior = key_prior
            vals = ("pre_screen", "remove_exact_bibkey_duplicate", "D-BIBKEY", f"Identical ACM BibTeX entry key to {prior}; occurrence retained for provenance.", "exact same-source BibTeX key", "deterministic", "2026-10-16", "not applicable")
        elif rid in queue:
            vals = ("title_abstract", "retrieve_for_eligibility", "", queue[rid]["reason"], "reviewed title/abstract", "AI-CODEX", "2026-10-16", "not assessed")
        elif not ACCELERATOR.search(text) and not (INFERENCE.search(text) and PROTECT.search(text)) and title:
            vals = ("title_abstract", "exclude", "E2", "Title and supplied abstract do not indicate a GPU/accelerator sharing mechanism for the assigned local inference question; broad full-text query match only.", "title and available abstract" if abstract else "title only; abstract absent", "AI-CODEX rule-assisted", "2026-10-16", "not assessed")
        elif abstract and ACCELERATOR.search(text) and not INFERENCE.search(text):
            code = "E4" if re.search(r"train", title, re.I) else "E1"
            rationale = ("Title and supplied abstract concern GPU training without an identifiable inference-serving outcome."
                         if code == "E4" else "Title and supplied abstract concern GPU/accelerator work but give no inference-serving evidence for the assigned question.")
            vals = ("title_abstract", "exclude", code, rationale, "title and available abstract", "AI-CODEX rule-assisted", "2026-10-16", "not assessed")
        else:
            vals = ("title_abstract", "needs_individual_review", "", "Topical or ambiguous metadata; review title/abstract and version before a decision.", "title and available abstract" if abstract else "title only; abstract absent", "", "", "not assessed")
        out.append(dict(zip(fields, [rid, prior or "", *vals[:4], "yes" if abstract else "no", *vals[4:]])))
        if doi:prior_doi.setdefault(doi, rid)
        if bibkey:prior_bibkey.setdefault(bibkey, rid)
    if len(out) != 3727:
        raise ValueError(len(out))
    with (e / "new_screening_triage.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields, lineterminator="\n"); w.writeheader(); w.writerows(out)
    print(dict(Counter(x["decision"] for x in out)))
    print("missing abstract",sum(x["abstract_available"] == "no" for x in out))

if __name__ == "__main__":
    main()
