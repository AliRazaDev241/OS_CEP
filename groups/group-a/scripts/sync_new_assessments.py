"""Refresh workbook views of the new export triage and assessed full reports.

Run after triage_new_exports.py and after the base workbook_source.json exists.
The old, reconciled 11 October tabs are left as their own checkpoint.
"""
import csv
import json
from pathlib import Path

E = Path(__file__).resolve().parents[1] / "evidence"
source = E / "workbook_source.json"
book = json.loads(source.read_text(encoding="utf-8"))

def read(name):
    return list(csv.DictReader((E / name).open(newline="", encoding="utf-8")))

triage = read("new_screening_triage.csv")
occurrences = {r["record_id"]: r for r in read("new_export_occurrences.csv")}
assessments = {r["record_id"]: r for r in read("new_fulltext_assessments.csv")}
book["Triage"] = [["Record", "Run", "Title", "Year", "Decision", "Reason code", "Rationale", "Canonical record", "Evidence basis"]]
for r in triage:
    o = occurrences[r["record_id"]]
    book["Triage"].append([r["record_id"], o["run_id"], o["title"], int(o["year"]) if o["year"].isdigit() else o["year"], r["decision"], r["reason_code"], r["rationale"], r["canonical_record"], r["evidence_basis"]])
for row in book["NewQueue"][1:]:
    if row[0] in assessments:
        row[4] = assessments[row[0]]["decision"]
        row[6] = "assessed published full report"
        row[7] = "eligible; QA/version and integration pending"

fields = ["record_id", "doi", "publication_status", "decision", "source_url", "source_anchor", "mechanism", "environment", "workload", "comparator", "outcome", "limitations"]
book["AssessedNew"] = [["Record", "DOI", "Publication", "Decision", "Full text", "Anchor", "Mechanism", "Environment", "Workload", "Comparator", "Outcome", "Limitations"]]
book["AssessedNew"] += [[a[f] for f in fields] for a in assessments.values()]
source.write_text(json.dumps(book, ensure_ascii=False), encoding="utf-8")
print(f"Workbook views: {len(triage)} new occurrences, {len(assessments)} assessed full reports")
