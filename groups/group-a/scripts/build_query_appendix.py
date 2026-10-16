"""Render the current Group A QA and extraction registers as TeX evidence cards."""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "groups/group-a/evidence"
OUTPUT = ROOT / "report/query_evidence_appendix.tex"


def rows(name):
    with (EVIDENCE / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def latex(value):
    value = str(value or "not recorded")
    # The registers preserve terse source transcription. Improve display
    # spacing without changing the stored values or splitting 1,000-style nums.
    value = re.sub(r"(?<=,)(?!\d{3}\b)(?=\S)", " ", value)
    value = re.sub(r"(?<=;)(?=\S)", " ", value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


qa = {row["study_id"]: row for row in rows("current_quality.csv")}
extraction = {row["study_id"]: row for row in rows("current_extraction.csv")}
if qa.keys() != extraction.keys():
    raise ValueError("The included QA and extraction study IDs differ")

parts = [
    r"\section{Study-level evidence cards}\label{app:cards}",
    r"\pending{These cards reflect the current 43-study accepted set after batch 3; the complete four-database selection flow remains open.}",
    r"The item rationales below reproduce the Group A quality register. Bounded outcomes and caveats reproduce the extraction register. They are not a new independent appraisal or a substitute for the cited full texts.",
]
for study_id in sorted(qa):
    q, e = qa[study_id], extraction[study_id]
    parts.extend(
        [
            r"\Needspace{12\baselineskip}",
            rf"\subsection{{{latex(study_id)}: {latex(e['title'])}}}",
            rf"\textbf{{Preferred report:}} {latex(e['venue'])}, {latex(e['year'])}; report {latex(q['report_id'])}. "
            rf"\textbf{{Current QA:}} {latex(q['total'])}/10 ({latex(q['band'])}).",
            r"\begin{longtable}{P{0.15\linewidth}P{0.75\linewidth}}",
            r"\toprule Extraction field & Recorded observation\\\midrule\endhead",
        ]
    )
    for label, key in [
        ("Mechanism", "mechanism"),
        ("Environment", "environment"),
        ("Workload", "workload"),
        ("Comparator", "comparator"),
        ("Bounded finding", "finding"),
        ("Transfer limit", "limitation"),
        ("Source anchor", "anchor"),
    ]:
        parts.append(rf"{label} & {latex(e[key])}\\")
    parts.extend([r"\bottomrule\end{longtable}", r"\begin{longtable}{P{0.09\linewidth}P{0.10\linewidth}P{0.67\linewidth}}", r"\toprule QA & Score & Source-based rationale\\\midrule\endhead"])
    for number in range(1, 11):
        parts.append(
            rf"Q{number} & {latex(q[f'Q{number}'])} & "
            rf"{latex(q[f'Q{number}_rationale'])}\\"
        )
    parts.extend([r"\bottomrule\end{longtable}", ""])

OUTPUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
print(f"Wrote {OUTPUT} for {len(qa)} studies")
