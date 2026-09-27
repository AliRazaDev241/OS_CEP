# SLR Protocol v1.1 — pre-search corrective draft

## GPU Sharing Mechanisms for Multi-Tenant Inference Serving

**Protocol status:** v1.1 corrective amendment drafted 2026-09-27 (Asia/Karachi); **formal-search freeze pending database-interface pilot and group sign-off**. v1.0 was prematurely marked frozen before the roadmap's pilot gate; see `evidence/protocol_amendments.md`.  
**Ownership:** Shared pre-search candidate only. Neither group's protocol is frozen or approved. Each three-person group must create and validate its own `groups/group-a/protocol.md` or `groups/group-b/protocol.md`, with its own dated search strings, reviewers, eligibility, extraction and amendment register before formal screening. The group-specific protocol controls that group's decisions; this root draft is background and cannot supply final PRISMA counts.  
**Scope status:** Formal study selection has not started. Web checks in `evidence/scoping_log.md` are candidate discovery only and must not be counted in PRISMA. No database hit counts, validated query executions, or eligible studies are claimed.

**Repository transition:** The planned canonical source is https://github.com/AliRazaDev241/OS_CEP after the staged files are imported through a reviewed PR. Each group's subsequent changes go through its own feature branch and PR; agents do not merge. See `GROUP_WORKFLOW.md`.

## 1. Research objective

To systematically identify, appraise, and synthesize peer-reviewed primary evidence on single-node GPU-sharing mechanisms for multi-tenant inference serving—temporal sharing/time-slicing, NVIDIA Multi-Process Service (MPS), Multi-Instance GPU (MIG), and CUDA/API remoting, proxying, or virtualization. The review will determine when each mechanism, or a combination, is appropriate under stated workloads, GPU hardware, configurations, and service-level objectives (SLOs), balancing GPU utilization and tenant density against tail-latency predictability, interference, resource/memory isolation, and fault containment.

## 2. Engineering problem and scope

An engineer must run concurrent inference tenants on one physical GPU. Greater multiplexing can improve occupancy and reduce idle capacity, but it may worsen request interference or p95/p99 latency. Stronger partitioning can improve predictability and resource boundaries, but may create fragmentation, reduce elastic sharing, or require supported hardware and operational reconfiguration. The review is bounded to the **single-node OS/runtime layer**. Cluster-wide scheduling is considered only when a study exposes and evaluates a relevant local GPU-sharing mechanism.

### Operational definitions

- **Inference serving:** execution of trained ML/DNN/LLM models to answer online or batch-service requests; training-only workloads are excluded.
- **Multi-tenant:** two or more separately scheduled workloads, users, models, services, or processes sharing one physical GPU.
- **Single-node sharing:** sharing controlled on one host/GPU by driver, runtime, process, partition, or API layer.
- **Time-slicing:** temporal multiplexing/context scheduling of a physical GPU without a dedicated hardware partition.
- **MPS:** NVIDIA CUDA Multi-Process Service or a clearly equivalent process-concurrency implementation.
- **MIG:** NVIDIA Multi-Instance GPU or a hardware partitioning mechanism with separately assigned GPU resources.
- **API remoting/virtualization:** interception, proxying, forwarding, or virtual presentation of CUDA/GPU APIs that enables multiple clients to access a GPU; virtual machines/containers qualify only when this mechanism is evaluated.
- **Isolation:** recorded separately as measured performance interference, resource/memory partitioning, security boundary, and fault containment. A mechanism name alone does not prove any of them.

## 3. Research questions

| ID | Research question |
|---|---|
| RQ1 | Which single-node time-slicing, MPS, MIG, and API-remoting/virtualization mechanisms have been evaluated for multi-tenant inference, and what isolation boundaries do they provide? |
| RQ2 | How do studies measure utilization, throughput, tenant density, latency distribution/tail latency, interference, and fault isolation, and how comparable are their experiments? |
| RQ3 | Under what model/workload, GPU generation, partition/configuration, batching/concurrency, and tenant-mix conditions do mechanisms change utilization and latency predictability? |
| RQ4 | What engineering trade-offs, implementation costs, limitations, and apparently conflicting findings are reported, and which experimental differences plausibly explain them? |
| RQ5 | Which mechanism or combination should an engineer choose for specified inference-serving conditions, given evidence quality and uncertainty? |

## 4. Databases and justification

NED Engr. Abul Kalam Library separates **E-Databases** from **Analytics** on its E-Resources page. The four planned formal source platforms are from the E-Databases section, pending actual NED entitlement and interface checks:

| Formal source | Role and rationale |
|---|---|
| IEEE Xplore | Electrical/computer engineering and systems journals/conferences; the assigned topic supplies an IEEE example query. |
| ACM Digital Library | Specialist computing and OS/systems conference/journal coverage; distinguish ACM full-text collection from the wider ACM Guide at execution. |
| ScienceDirect | Complementary Elsevier engineering/computing journal coverage, including systems venues. |
| Springer Nature Link (SpringerLink) | Complementary computing/engineering journals and proceedings; filter research papers from books/chapters and duplicates. |

**Scopus and Web of Science** are NED-listed analytics/citation indexes and are useful as *additional* cross-publisher validation/citation-tracking sources if the team has access. They do not replace four E-Databases sources, and if searched formally their runs and exports receive the same complete logging/screening. **Google Scholar** is supplementary citation discovery only. USENIX and other publisher sites may supply full-text copies and seed records but are not automatically formal database runs. This coverage limitation, especially USENIX proceedings not necessarily indexed in these platforms, must be assessed in the pilot and reported as a review threat.

## 5. Search concepts and keywords

The query design combines four concepts:

1. **GPU and sharing:** GPU, graphics processing unit, accelerator, sharing, multiplexing, multi-tenant, multi-tenancy, co-location, colocated.
2. **Mechanisms:** time slicing, timeslicing, context scheduling, MPS, multi-process service, MIG, multi-instance GPU, GPU partitioning, virtualization, virtual GPU, vGPU, CUDA remoting, API remoting, CUDA proxy, GPU proxy, GPU virtualization.
3. **Inference context:** inference, serving, online inference, model serving, DNN, deep learning, neural network, machine learning, LLM, transformer.
4. **Evaluation outcomes:** utilization, occupancy, throughput, latency, tail latency, p95, p99, QoS, SLO, interference, isolation, tenant density.

Use the mechanism and inference blocks in every formal search. Do **not** require a separate sharing/multi-tenant block: relevant papers such as PipeSwitch can describe time-sharing and inference without the exact phrase `multi-tenant` in their title/abstract. Sharing and outcome terms remain optional refinements. Run a documented pilot with known candidate seeds from `evidence/scoping_log.md`, checking retrieval for all four mechanism categories; revise through the amendment register before the formal freeze if a category is systematically missed.

## 6. Database-specific search strings

### Candidate query logic for v1.1 (not yet interface-validated)

```text
(GPU OR "graphics processing unit")
AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM)
AND ("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR partition* OR virtuali* OR "API remoting" OR "CUDA remoting" OR "GPU proxy")
```

The mechanism block should be split into four separately logged mechanism-family queries where a platform restricts length or a pilot shows recall loss. Do not add an outcome or multi-tenancy AND block until a documented seed-recall check establishes that it does not suppress relevant records. See `evidence/query_validation.md` for per-platform proposed inputs, syntax caveats, seed tests, and execution gate.

### v1.0 strings retired

The unexecuted v1.0 strings assumed four mandatory blocks and misclassified two analytics indexes as the four E-Databases. They were removed from the operative protocol to prevent accidental use. See the amendment register; no historical query is operative in v1.1.

### Citation chasing

Backward and forward citation chasing begins only after at least one eligible full-text report is confirmed. Each seed report, direction, platform, date, candidate count, and decision will be logged separately. Citation-chased candidates receive the same duplicate check, independent screening, quality assessment, and full-text rule as database records.

## 7. Publication period and language

The normal period is **1 January 2020 to 27 September 2026**, inclusive, and English language. Older material may be included only if it is a seminal mechanism paper or an essential directly relevant baseline. The report must record the reason, mechanism, and why no newer equivalent evidence suffices. The final included set must contain 15–20 peer-reviewed primary studies; 15 is the minimum.

## 8. Eligibility criteria

| Type | Criterion |
|---|---|
| Include | Peer-reviewed journal or conference primary study in English, normally published 2020–2026. |
| Include | Evaluates, compares, implements, or technically analyses at least one in-scope single-node GPU-sharing mechanism for multi-tenant inference serving. |
| Include | Reports enough full-text technical detail to assess mechanism/configuration and at least one engineering outcome relevant to an RQ (e.g., utilization, tenant density, throughput, latency, interference, isolation, overhead). |
| Include | Directly transferable inference evidence may be included only when the mechanism, workload assumptions, and transfer rationale are explicitly recorded. |
| Exclude | Duplicate report of an already represented study: retain provenance, link reports, and extract from the most complete peer-reviewed version. |
| Exclude | Training-only, cluster-orchestration-only, or allocation-only work that does not evaluate a local sharing mechanism. |
| Exclude | Surveys/reviews, vendor documentation, blogs, editorials, posters, patents, slides, opinion pieces, and abstract-only reports as primary evidence. |
| Exclude | Studies without sufficient technical or engineering evidence, inaccessible full text, or no discernible relation to the RQs. |

## 9. Screening and PRISMA procedure

1. **Identification:** run each frozen database query, record exact syntax, URL, date, filters, hit count, export file, and reviewer in `evidence/search_runs.csv`; import every hit with source provenance.
2. **Duplicate and version handling:** normalize DOI, title, year, and authors; preserve all records. Link record → report → underlying study in `evidence/duplicates.csv`; do not delete provenance.
3. **Pilot calibration:** two reviewers independently label the same small pilot set. Record disagreements, decisions, refinements, and calibration date. Do not change the frozen criteria without a formal amendment.
4. **Title/abstract screening:** two reviewers independently apply eligibility criteria. Record both decisions and a controlled reason for exclusion.
5. **Full-text assessment:** retrieve legally accessible reports; two reviewers independently assess complete text. Record access state separately from exclusion reason. The third member adjudicates disagreements.
6. **Inclusion:** assign a unique Study ID only after final eligibility; link all reports and identify the extraction report.
7. **PRISMA 2020:** derive every count from the logs: records identified, records removed before screening, records screened, reports sought/retrieved, reports assessed, reports excluded with reasons, and unique studies included.

Controlled full-text exclusion codes (for **assessed** reports): `E1 Not inference serving`; `E2 Not multi-tenant/single-node sharing`; `E3 Mechanism out of scope`; `E4 Training-only`; `E5 Cluster-only`; `E6 Not peer-reviewed primary study`; `E7 Insufficient technical/evaluation evidence`; `E8 Duplicate/less-complete report`; `E10 Other (narrative required)`. **Full text not retrieved** is tracked as a report-retrieval outcome (e.g., `R1 Full text unavailable after documented attempts`), not falsely counted among full-text reports assessed. Preserve retrieval attempts and source links.

## 10. Quality assessment

Each included study is scored independently by two reviewers: **1 = yes/adequate, 0.5 = partial/unclear, 0 = no/not reported**. The total (0–10) is used to label evidence, not automatically discard a study: High 8.0–10; Moderate 6.0–7.5; Low <6.0. Low-quality evidence is retained only when eligible, labelled clearly, and excluded in a sensitivity synthesis.

| ID | Quality question |
|---|---|
| QA1 | Is the engineering objective/problem clearly defined? |
| QA2 | Is the sharing mechanism and configuration described sufficiently? |
| QA3 | Are GPU/SKU, partition profile, OS/kernel, driver/CUDA/runtime described? |
| QA4 | Are model/workload, batching/arrival pattern, tenant/co-tenant mix described? |
| QA5 | Are baselines and comparison conditions fair and explicit? |
| QA6 | Are relevant metrics precisely defined with units and latency percentile where relevant? |
| QA7 | Is the evaluation methodology adequate (warm-up/window/repetitions or equivalent)? |
| QA8 | Are results supported by data/figures/tables and source anchors? |
| QA9 | Are limitations or threats to validity acknowledged? |
| QA10 | Is enough information available to reproduce or critically interpret the experiment? |

## 11. Data-extraction fields

The extraction sheet has one row per report-result where necessary, linked to a Study ID. Every numerical or substantive finding used in synthesis must include a PDF page, figure, table, or section anchor.

| Group | Required fields |
|---|---|
| Identity/provenance | Record ID, Report ID, Study ID, database, source URL/DOI, retrieval date, title, authors, year, venue, peer-review status, full-text access status, report-version relation. |
| Mechanism | taxonomy class; product/framework; time-slice/MPS/MIG/remoting/virtualization configuration; scheduler/control layer; partition profile; admission/QoS policy. |
| Environment | GPU vendor/SKU/count; memory; CPU/RAM; OS/kernel; driver; CUDA/runtime; container/VM details. |
| Workload | model and version; task; model size; dataset/input; batch size; arrival/request pattern; warm-up and measurement window; tenant count and co-tenant mix. |
| Comparator | baseline mechanism/configuration and whether comparison is direct or indirect. |
| Outcomes | utilization/occupancy; throughput/goodput; mean/median/p50/p95/p99 latency and units; SLO misses; interference; tenant density; overhead; energy when reported. |
| Isolation | performance interference; resource/memory partitioning; security boundary; fault containment: each marked measured, claimed, not reported, or not applicable. |
| Interpretation controls | exact finding with source anchor; paper-stated limitation; team interpretation (separate); evidence strength; QA score; comparability notes. |

## 12. Taxonomy and evidence-synthesis strategy

### Taxonomy

Synthesis will classify evidence first by mechanism: (A) temporal/time-slice sharing, (B) process-level concurrency/MPS, (C) hardware partitioning/MIG, (D) API interception/remoting/virtualization, and (E) hybrid mechanisms (e.g., MIG+MPS). Within each class, studies are further grouped by isolation boundary, control/scheduling layer, partitioning granularity, workload class, GPU generation, and QoS/admission policy.

### Synthesis method

- Build an RQ-to-evidence matrix and a comparability profile before numerical comparison.
- Use structured narrative synthesis and mechanism-level evidence tables; no statistical meta-analysis is planned because hardware, models, batching, tenant mixes, latency definitions, and baselines are expected to be heterogeneous.
- Compare quantitative results only within compatible experimental strata. Otherwise describe direction, conditions, and evidence strength rather than pooling raw values.
- Label every conclusion: **direct comparison**, **indirect primary evidence**, **contextual vendor information**, or **insufficient evidence**.
- Analyze conflicting results against GPU/SKU, partition size, driver/runtime, workload/model size, batching, concurrency/arrival pattern, tenant mix, baseline, and metric/measurement differences.
- Run a sensitivity synthesis excluding low-QA and incomplete-report evidence; report whether conditional recommendations change.
- Produce a conditional decision matrix covering latency SLO, utilization/tenant-density priority, isolation/fault-containment need, MIG-capable hardware availability, workload/model heterogeneity, and operational complexity.

## 13. RQ-to-evidence map

| RQ | Core extraction fields | Analysis output | Decision use |
|---|---|---|---|
| RQ1 | mechanism, configuration, isolation dimensions, scheduler/control layer | taxonomy and isolation matrix | establishes alternatives and boundaries |
| RQ2 | metric definitions, units, percentile, hardware, workload, baseline, measurement protocol | comparability matrix | prevents invalid cross-study comparison |
| RQ3 | GPU/SKU, partition, model, batching, tenant mix, latency/utilization/throughput results | condition-by-mechanism evidence table | identifies workload/hardware-dependent behavior |
| RQ4 | overhead, limitations, QoS misses, interference, QA, experimental differences | trade-off and conflict matrix | explains why findings differ |
| RQ5 | all above plus evidence-strength label and sensitivity result | conditional decision matrix | supports recommendation rather than a universal winner |

## 14. Protocol deviations and amendments

This protocol is **v1.1, pre-search corrective draft**. Its predecessor v1.0 was marked frozen before the required database-interface pilot and team ownership confirmation; the corrective changes are documented in `evidence/protocol_amendments.md`. Formal selection is still prohibited. Once four source interfaces have been piloted, exact executable strings and filters have been captured, and the group signs off, issue a dated freeze (v1.2 if search semantics change). Thereafter any material change to scope, RQs, databases, queries, dates, criteria, screening, QA, extraction, or synthesis must be entered in the register before use, with rationale and effects on records/counts. Syntax-only interface transformations are logged in search runs; semantic changes require an amendment.

## 15. Open decisions before formal screening

1. Confirm the calendar date for week 13.
2. Enter the three members’ reviewer IDs and assign two screeners plus one adjudicator.
3. Confirm NED VPN/database access, index availability, and permitted export-sharing procedure.
4. Confirm the IEEE LaTeX template expected by the instructor.
5. Confirm the five RQs or record instructor-approved revisions as an amendment.

## Methodological basis for this protocol

- Page *et al.*, PRISMA 2020, specifies transparent reporting through a 27-item checklist and flow-diagram templates.
- Kitchenham and Charters provide software-engineering SLR guidance for a protocol-led, auditable process.
- NED’s library pages identify IEEE, ACM, Scopus, Web of Science, ScienceDirect, Springer and related sources, supporting the selected database set.
- The scoping review discovery found an existing multi-tenant inference survey and recent hybrid MIG/MPS primary studies. Therefore this review remains focused on single-node mechanism-level utilization–latency isolation trade-offs and treats surveys as vocabulary/context only, not primary evidence.
