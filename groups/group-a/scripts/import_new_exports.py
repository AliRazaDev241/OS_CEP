"""Build an occurrence ledger for supplied ACM/ScienceDirect exports.

Metadata and duplicate candidates only. No screening or PRISMA decisions.
Run from the repository root with explicit private-export and baseline paths.
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def norm_doi(value):
    value = (value or "").strip().lower()
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:)", "", value).rstrip("/ .")


def norm_title(value):
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def ris_records(path):
    current = {}
    last = None
    for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])  - ?(.*)$", line)
        if m:
            tag, value = m.groups()
            if tag == "TY":
                current = {}
            elif tag == "ER":
                yield current
                current = {}
            else:
                current.setdefault(tag, []).append(value.strip())
            last = tag
        elif last and current.get(last):
            current[last][-1] += " " + line.strip()


def bib_records(path):
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    starts = list(re.finditer(r"^@\w+\s*\{([^,]+),", text, re.M))
    for i, match in enumerate(starts):
        block = text[match.end(): starts[i + 1].start() if i + 1 < len(starts) else len(text)]
        def field(name):
            hit = re.search(r"^" + name + r"\s*=\s*\{([^\n]*?)\}\s*,?\s*$", block, re.M | re.I)
            return hit.group(1).strip() if hit else ""
        yield {"key": match.group(1).strip(), "title": field("title"), "doi": field("doi"),
               "year": field("year"), "url": field("url")}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--exports", type=Path, required=True)
    p.add_argument("--intake", type=Path, required=True)
    p.add_argument("--baseline", type=Path, required=True)
    p.add_argument("--included", type=Path, help="Existing accepted-study metadata for version linking")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    intake = list(csv.DictReader(args.intake.open(newline="", encoding="utf-8")))
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    included = json.loads(args.included.read_text(encoding="utf-8")) if args.included else []
    known_doi = {}
    known_title = {}
    for b in baseline:
        if norm_doi(b.get("doi")):
            known_doi.setdefault(norm_doi(b["doi"]), b["record_id"])
        if norm_title(b.get("title")):
            known_title.setdefault(norm_title(b["title"]), b["record_id"])
    seen_doi = {}
    seen_title = {}
    included_doi = {norm_doi(s.get("doi")): s.get("key", "") for s in included if norm_doi(s.get("doi"))}
    included_title = {norm_title(s.get("title")): s.get("key", "") for s in included if norm_title(s.get("title"))}
    count = Counter()
    columns = ["record_id", "run_id", "source_file", "source_ordinal", "bibtex_key", "title", "year", "publication_date",
               "doi", "url", "match_existing_record", "match_prior_new_record", "match_basis", "match_included_key", "included_match_basis",
               "metadata_status", "screening_status"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, columns)
        writer.writeheader()
        serial = 0
        for batch in intake:
            path = args.exports / batch["received_filename"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != batch["sha256"]:
                raise ValueError(f"{path.name}: SHA-256 differs from receipt")
            records = ris_records(path) if path.suffix.lower() == ".ris" else bib_records(path)
            batch_count = 0
            for ordinal, raw in enumerate(records, 1):
                serial += 1
                batch_count += 1
                recid = f"GA-N{serial:05d}"
                if path.suffix.lower() == ".ris":
                    title = " ".join(raw.get("T1") or raw.get("TI") or [])
                    doi = " ".join(raw.get("DO") or [])
                    year = " ".join(raw.get("PY") or [])
                    date = " ".join(raw.get("DA") or [])
                    url = " ".join(raw.get("UR") or [])
                    key = ""
                else:
                    title, doi, year, url, key = (raw[k] for k in ("title", "doi", "year", "url", "key"))
                    date = ""
                d, t = norm_doi(doi), norm_title(title)
                existing = known_doi.get(d, "") if d else ""
                prior = seen_doi.get(d, "") if d else ""
                basis = "doi" if existing or prior else ""
                if not existing and not prior and t:
                    existing, prior = known_title.get(t, ""), seen_title.get(t, "")
                    if existing or prior:
                        basis = "normalized_title_needs_review"
                included_key = included_doi.get(d, "") if d else ""
                included_basis = "doi" if included_key else ""
                if not included_key and t:
                    included_key = included_title.get(t, "")
                    included_basis = "normalized_title_needs_review" if included_key else ""
                row = dict(zip(columns, [recid, batch["search_run_id"], path.name, ordinal, key, title,
                    year, date, d, url, existing, prior, basis, included_key, included_basis, "metadata_only", "not_screened"]))
                writer.writerow(row)
                count["existing_match" if existing else "prior_new_match" if prior else "new_candidate"] += 1
                if included_key:
                    count["included_study_report_candidate"] += 1
                if d:
                    seen_doi.setdefault(d, recid)
                if t:
                    seen_title.setdefault(t, recid)
            if batch_count != int(batch["parsed_entries"]):
                raise ValueError(f"{path.name}: parsed {batch_count}; receipt says {batch['parsed_entries']}")
    if serial != 3727 or len(baseline) != 689:
        raise ValueError(f"Unexpected input sizes: new={serial}, baseline={len(baseline)}")
    print(json.dumps({"occurrences": serial, "baseline_records": len(baseline), **count}, sort_keys=True))


if __name__ == "__main__":
    main()
