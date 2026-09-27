# OS CEP systematic literature review — project brief

## Authority and project goal

guidelines.md and topics.md are the assignment authorities. They must never be changed by project work. If this brief conflicts with either, follow the authority and record the correction in the protocol amendment register.

The canonical destination is https://github.com/AliRazaDev241/OS_CEP. The Windows folder is a staging copy until its initial import PR is merged; subsequently work from a current GitHub branch. Two independent groups of three students share the assigned topic. **Each group** must produce its own evidence-based systematic literature review (SLR), reported under PRISMA 2020, with a compilable IEEE-cited LaTeX report and print-ready PDF. Each deliverable is a reproducible, conditional engineering decision framework. See `GROUP_WORKFLOW.md` for ownership and PR rules.

**Assigned topic:** GPU sharing mechanisms for multi-tenant inference serving: time-slicing versus MPS versus MIG versus API remoting/virtualization, examining GPU utilization and tenant density against predictable per-tenant inference latency and fault isolation.

**Report title:** *GPU Sharing Mechanisms for Multi-Tenant Inference Serving: A Systematic Literature Review of Utilization and Latency Isolation Trade-offs.*

## Defined engineering problem, objective, and contribution

**Problem.** An engineer must share a single GPU among concurrent inference tenants while balancing utilization and tenant density against tail-latency predictability, performance interference, memory/resource boundaries, and fault isolation. No named mechanism is universally best because the outcome depends on workload, GPU generation, configuration, and SLO.

**Objective.** Systematically evaluate primary research evidence to determine which mechanism or combination is appropriate under stated operating conditions and what trade-offs it requires.

**Contribution.** A mechanism taxonomy, comparability-aware evidence matrix, and conditional decision matrix whose recommendations state supporting evidence strength and uncertainty.

## Protocol scope requirements (apply separately to each group)

The protocol must operationalize these rules before formal study selection:

- Include peer-reviewed primary journal/conference studies with enough technical detail to evaluate a relevant single-node GPU-sharing mechanism for inference serving or a directly justified transferable inference workload.
- Exclude training-only studies, cluster-orchestration-only studies, vendor/blog claims, surveys as primary evidence, editorials/posters, abstract-only reports, and studies without relevant engineering evidence.
- Treat vendor documentation only as contextual mechanism explanation; it never counts toward the primary-study set.
- Track conference, journal, preprint, and duplicate reports separately from the underlying unique study. Prefer the most complete peer-reviewed version and link related reports.
- Record inaccessible full texts and never extract unsupported results from abstracts.
- Use 2020–2026 as the normal period; include older work only when it is seminal or an essential directly relevant baseline, with a recorded justification.

## Required outcomes and evidence controls

- Freeze and version `groups/<group>/protocol.md` before that group's formal screening. A short documented scoping/pilot search may precede it solely to refine vocabulary, test query syntax, discover overlapping reviews, and assess feasibility.
- Select and justify preferably at least four databases actually listed by the NED E.A. Khan Library E-Databases page. Google Scholar is supplementary only and its citation chasing is logged separately.
- Use database-specific executable queries. The supplied IEEE string is a candidate only; the final query matrix must cover time-slicing/context scheduling, MPS, MIG, partitioning, CUDA/API remoting or proxying, and virtualization synonyms.
- Target **15–20 final included peer-reviewed primary studies; 15 is the minimum floor**. If pilot screening makes this implausible, pause and seek instructor approval before changing scope or eligibility.
- Keep a database-wise search log, imported-record list, duplicate/report-link record, title/abstract and full-text decisions, reason codes, quality scores, extraction sheet, claims matrix, and PRISMA 2020 counts that reconcile exactly.
- Use two independent screeners for title/abstract and full text where team capacity permits; the third member adjudicates disagreements. Record reviewer IDs, decisions, conflict resolution, and a pilot calibration exercise.
- Maintain `groups/<group>/evidence/protocol_amendments.md` for each group's post-freeze changes, including date, rationale, affected artifacts, and impact on counts.

## Shared candidate research questions (each group adapts and freezes its own)

1. Which single-node time-slicing, MPS, MIG, and API remoting/virtualization mechanisms have been evaluated for multi-tenant inference, and what isolation boundaries do they provide?
2. How do studies measure utilization, throughput, tenant density, latency distribution/tail latency, interference, and fault isolation, and how comparable are their experiments?
3. Under what workloads, GPU generations, model sizes, batching/concurrency levels, tenant mixes, and configurations do mechanisms change utilization and latency predictability?
4. What trade-offs, implementation costs, limitations, and apparently conflicting findings emerge, and which experimental differences plausibly explain them?
5. Which mechanism or combination should an engineer choose for specified inference-serving conditions, given evidence quality and limits?

## Required RQ-to-evidence design

Before screening, map every RQ to its extraction fields, analysis method, output artifact, and decision use. Capture a comparability profile for every included study: GPU/SKU and partition profile, CUDA/driver/runtime and OS/kernel, model/workload, batching and arrival pattern, tenant count/co-tenant mix, baseline, metric definitions and units, latency percentile, warm-up/measurement window, and reported caveats.

## Evidence and synthesis rules

Record DOI or stable publisher URL, source database, retrieval date, publication/report status, full-text access state, exact page/figure/table anchors, conditions, units, limitations, and whether a statement is a paper finding or team interpretation.

For isolation, distinguish performance interference, resource/memory partitioning, security isolation, and fault containment. Record each as measured, claimed, not reported, or not applicable—never infer it from a mechanism name.

Do not compare raw performance numbers across non-comparable hardware, models, batching, tenant counts, or latency definitions as if they were head-to-head results. Label evidence strength in the decision matrix as direct comparison, indirect primary evidence, contextual vendor evidence, or insufficient evidence. Run a sensitivity synthesis excluding low-quality or incomplete studies.

## Planned workspace outputs

The following deliverables are required separately for `groups/group-a/` and `groups/group-b/`. Root-level `protocol.md`, `evidence/`, and `report/` are shared pre-search draft/history and do not count as either group's final review.

| File or directory (relative to each group) | Purpose |
| --- | --- |
| protocol.md | Versioned protocol, RQ-to-evidence map, and screening rules |
| evidence/protocol_amendments.md | Dated protocol changes and justification |
| evidence/search_runs.csv | Exact database searches, filters, dates, counts, exports |
| evidence/studies.csv | Records, reports, study IDs, decisions, and exclusion reasons |
| evidence/duplicates.csv | DOI/title-normalized duplicate and version links |
| evidence/quality.csv | Predefined quality rubric, scores, and reviewer notes |
| evidence/extraction.csv | Source-anchored findings and comparability profiles |
| evidence/claims.md | Claim-to-study links, counterevidence, and synthesis notes |
| report/main.tex, report/references.bib | IEEE-cited manuscript |
| report/report.pdf | Checked final print-ready report |

These are planned artifacts only. Their presence must never be presented as evidence that searches, screening, or synthesis have happened.

All repository changes must be submitted from a feature branch as a PR to `main` for human review. Agents do not push directly to `main` or merge PRs. The empty repository requires a one-time minimal bootstrap commit, then an initial import branch and PR; the user will handle migration after the PC edits. See `GROUP_WORKFLOW.md`.

## Completion and decisions

For **each group independently**, completion requires all mandatory guideline deliverables, a reconciled PRISMA 2020 flow, 15–20 included primary studies (minimum 15), transparent quality assessment, answers to every RQ, conditional recommendations, research gaps, threats to validity, complete IEEE references, and a visually checked 12-point PDF suitable for hard copy.

The final report should target 20–30 pages of main report content unless the instructor clarifies otherwise; appendices hold supporting records.

Before either group's protocol freeze, confirm: week-13 calendar date; its three members and reviewer roles; NED database access; permitted export-sharing procedure; preferred IEEE/LaTeX template; and its accepted RQs. Map `group-a` and `group-b` to the real teams. Record unanswered items as open decisions rather than assumptions. If both groups use the same source, each must independently retrieve, screen, assess and extract it.