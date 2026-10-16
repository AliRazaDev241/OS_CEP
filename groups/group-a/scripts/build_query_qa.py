"""Build the Group A QA detail from the authoritative quality register."""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
source = ROOT / "groups/group-a/evidence/current_quality.csv"
target = ROOT / "report/query_qa_detail.tex"
rows = list(csv.DictReader(source.open(newline="", encoding="utf-8")))
assert len(rows) == 43 and len({r["study_id"] for r in rows}) == 43
score = lambda r, q: float(r[f"Q{q}"])
for row in rows:
    assert abs(sum(score(row, q) for q in range(1, 11)) - float(row["total"])) < 1e-9

def fmt(x):
    return f"{float(x):.1f}".removesuffix(".0")

out = [
    r"\subsection{Section 13: item-level quality assessment}",
    r"The adopted ten-item rubric scores reporting and interpretability from 0 (absent), 0.5 (partial) or 1 (adequate), for a maximum of 10. Eligibility was assessed separately. The preferred peer-reviewed report of each accepted study is scored once; the earlier Reef conference version remains in the assessment history but does not add a study. The same single AI reviewer prepared all scores. No independent agreement statistic or experimental replication is claimed.",
    r"\begingroup\scriptsize\setlength{\tabcolsep}{3pt}",
    r"\begin{longtable}{P{0.14\linewidth}*{10}{>{\centering\arraybackslash}p{0.045\linewidth}}P{0.08\linewidth}P{0.10\linewidth}}",
    r"\toprule Study & Q1 & Q2 & Q3 & Q4 & Q5 & Q6 & Q7 & Q8 & Q9 & Q10 & /10 & Band\\\midrule\endhead",
]
for row in rows:
    scores = " & ".join(fmt(score(row, q)) for q in range(1, 11))
    out.append(r"\texttt{" + row["study_id"] + "} & " + scores + " & " + fmt(row["total"]) + " & " + row["band"] + r"\\")
out += [r"\bottomrule\end{longtable}\endgroup"]

bands = Counter(r["band"] for r in rows)
total = sum(float(r["total"]) for r in rows)
out.append(
    f"The {len(rows)} preferred reports total {fmt(total)} points (mean {total/len(rows):.2f}, range "
    f"{fmt(min(float(r['total']) for r in rows))}--{fmt(max(float(r['total']) for r in rows))}). "
    f"There are {bands['high']} high (8--10), {bands['moderate']} moderate (6--7.5) and "
    f"{bands['low']} low (below 6) scores. Their individual Q-item rationales, "
    r"preferred-report IDs and source anchors are recorded in \path{current_quality.csv}; "
    r"Appendix~\ref{app:cards} presents study-level evidence cards."
)

out += [
    r"\begin{longtable}{P{0.11\linewidth}P{0.50\linewidth}rrr}",
    r"\toprule Item & Interpretation & Adequate & Partial & Absent\\\midrule\endhead",
]
labels = [
    "Question and tenant setting", "Mechanism and configuration", "Hardware/software profile",
    "Model, load and co-tenant mix", "Comparator and resource budget", "Metric definition and units",
    "Measurement controls", "Support in figure/table/text", "Threats and adverse cases",
    "Reproduction or critical interpretation",
]
for q, label in enumerate(labels, 1):
    counts = Counter(score(row, q) for row in rows)
    out.append(f"Q{q} & {label} & {counts[1.0]} & {counts[0.5]} & {counts[0.0]}" + r"\\")
out += [r"\bottomrule\end{longtable}"]
out += [
    f"Hardware/software completeness, baseline fidelity and measurement controls remain qualified across the current set. The item-count table above is regenerated from all {len(rows)} rows. Numeric prose can support a bounded finding even when the supplied conversion lacks readable plot pixels; no missing curve or confidence interval is reconstructed.",
    f"\\paragraph{{Sensitivity and version control.}} Removing the {bands['moderate']+bands['low']} moderate/low scored reports leaves {bands['high']} high-scored studies. This weakens particular mechanism comparisons and does not prove complete causal controls in the retained set. The preferred Reef journal extension remains one study, with its conference assessment retained as history.",
    r"\paragraph{Limits of the appraisal.} Some supplied conversions lacked readable chart images; Q8 is based on accessible captions, tables and stated numbers, not reverse-engineered pixels. The experiments and code were not rerun, so Q10 assesses whether a reader can critically interpret the configuration. Performance isolation, resource separation, adversarial security and fault containment need different experiments; a high total cannot establish all four. \pending{Pantheon and Jormungandr remain unscored pending report-version and eligibility sign-off; if admitted, their own source-anchored Q1--Q10 rows and all summary counts must be regenerated.}",
]
target.write_text("\n\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {target} from {len(rows)} Group A rows")
