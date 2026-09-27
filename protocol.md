# GPU Sharing Mechanisms for Multi-Tenant Inference Serving — SLR Review Protocol

**Version:** v1.2, proposed pre-search revision, 27 September 2026 (PKT)  
**Status:** Not frozen. The four database interfaces, exact executable queries, access, seed recall, group ownership and reviewer sign-off remain unverified. No formal search, screened study or PRISMA count is claimed.  
**Ownership:** Shared candidate for two independent three-student groups. Each group must adapt, pilot, date and freeze its own protocol before formal selection. Neither may inherit the other's decisions or counts. The root v1.0/v1.1 history remains in `evidence/protocol_amendments.md`.

The twelve sections below follow the instructor's requested order. PRISMA-P informs protocol transparency [1], PRISMA 2020 informs final review reporting [2], PRISMA-S informs reproducible search documentation [3], and software-engineering SLR guidance informs the review process [4]. These reporting guidelines are **method references**, not included primary studies.

## 1. Research objective

Identify, critically appraise and synthesize peer-reviewed primary studies evaluating how **one physical GPU on a single node** is shared by multiple inference tenants. Compare temporal time-slicing, CUDA Multi-Process Service (MPS), Multi-Instance GPU (MIG), CUDA/GPU API remoting or virtualization, and hybrids. The intended output is a conditional engineering choice: which mechanism fits a specified model and arrival pattern, GPU generation/configuration, latency service-level objective (SLO), utilization or tenant-density goal, and isolation requirement. Treat performance interference, resource/memory separation, security isolation and fault containment as distinct observations; no mechanism name proves a measured outcome [10], [11].

## 2. Research questions

1. **RQ1 (alternatives):** Which of the four assigned mechanism families and hybrids have been evaluated for concurrent inference tenants on a single GPU, and what control/resource boundaries were evaluated?
2. **RQ2 (measurement):** How are utilization, throughput/goodput, tenant density, p50/p95/p99 latency, SLO violations, interference and isolation measured? Which studies can actually be compared?
3. **RQ3 (conditions):** How do workload/model, request arrival and batching, tenant mix, GPU generation, MPS settings, MIG profile and remoting path affect the reported outcomes?
4. **RQ4 (trade-offs):** What performance, isolation, implementation and operational trade-offs, conflicting findings and evidence gaps are reported?
5. **RQ5 (decision):** Under stated SLO, utilization/density, isolation and hardware conditions, what mechanism or combination is supported, and how strong is that support?

The group must map each final RQ to the extraction fields in §11 and synthesis outputs in §12 before freezing.

## 3. Selected academic databases

The **proposed formal sources** are IEEE Xplore (engineering/systems), ACM Digital Library (computing/systems), ScienceDirect (Elsevier engineering/computing journals), and Springer Nature Link (computing journals/proceedings). NED's E-Resources page lists these platforms in its E-Databases area [5]. Verify each group's actual entitlement, indexed collection and export route before freeze; a publisher collection is not an exhaustive cross-publisher index. If unavailable, document a justified replacement and revised coverage.

Scopus and Web of Science, if accessible, supplement cross-publisher coverage/citation checking; any systematic run must be logged and screened like a formal source. Google Scholar and backward/forward references are supplementary discovery, logged separately. Check whether USENIX and other systems proceedings are missed by the proposed publisher platforms. Do not mistake publisher access for database coverage.

## 4. Search keywords

| Concept | Candidate keywords and spelling variants |
|---|---|
| Hardware | GPU; graphics processing unit; accelerator |
| Inference | inference; model serving; deep learning; DNN; neural network; LLM; online serving |
| Temporal sharing | time slicing; time-slicing; time sharing; context switching; preemptive scheduling |
| MPS | MPS; multi-process service; CUDA MPS; process concurrency |
| MIG/partitioning | MIG; multi-instance GPU; GPU partitioning; spatial sharing |
| API remoting | API remoting; CUDA remoting; GPU proxy; API interception; virtual GPU; GPU virtualization |
| Outcomes/setting (optional refinements) | multi-tenant; co-location; utilization; latency; tail latency; QoS; SLO; interference; isolation |

The mandatory query logic is hardware AND inference AND an OR of **all four** mechanism families. Do not require `multi-tenant` or an outcome word in every record: relevant seed papers may lack that literal term [12]. Pilot spelling, tokenization, wildcard and subject-field choices for each interface before freeze. MPS and MIG alone can have unrelated meanings, so pair with GPU/inference and inspect precision.

## 5. Search strings

**Candidate Boolean logic (not yet an executed search):**

```text
(GPU OR "graphics processing unit")
AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM)
AND ("time slicing" OR "time sharing" OR "context switching"
     OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU"
     OR "GPU partitioning" OR "API remoting" OR "CUDA remoting"
     OR "GPU proxy" OR "GPU virtualization")
```

| Interface to pilot | Proposed entry and mandatory validation |
|---|---|
| IEEE Xplore Command Search | Enter the candidate logic; verify uppercase Boolean, phrase grouping, metadata field, date/type facets and displayed executed query. |
| ACM DL Advanced Search | Enter concepts in the builder in the **ACM full-text collection**; capture its generated syntax, field scope and collection (not automatically the broader ACM Guide). |
| ScienceDirect Advanced Search | Test the broad logic in the Advanced Search terms field; record accepted syntax, whether full text or title/abstract/keywords was searched, and applied article/date filters. |
| Springer Nature Link Advanced Search | Test grouping, phrases, uppercase Boolean, field scope and year/content-type facets; record the executed representation. |

If clause limits or seed misses require it, run **four separately logged queries per platform** with the common GPU AND inference blocks and one mechanism-family OR block from §4 each; deduplicate their exported records. A family split or field change affecting recall must be chosen and recorded **before** formal freeze. `evidence/query_validation.md` contains the existing unexecuted platform inputs; each group must replace proposals with its actual accepted query, field, URL, filters, pilot hit count and seed-retrieval result. Suggested seed *candidates* span PipeSwitch [12], ParvaGPU [13] and Torpor [14]; none is pre-included. A seed absent from its publisher collection tests coverage, not necessarily query syntax.

For every later **formal** run log group ID, database/collection, exact executed query, fields, filters, date/time, URL, total hits, export filename and reviewer. Keep pilot and formal runs separate. PRISMA-S [3] motivates this audit trail. Backward/forward citation chasing begins after an eligible full text is found; log seed, direction, date, source and candidate IDs, and apply the same eligibility and screening rules.

## 6. Publication period

Search for English-language works dated **1 January 2020 through 27 September 2026 inclusive** (date of draft). The final group protocol must state its actual search cutoff and search date. If an interface filters by year only, inspect 2026 records and exclude post-cutoff publications manually. An older seminal mechanism or indispensable baseline may enter only with a per-study written reason and a demonstrated direct connection to the RQs; older contextual work is otherwise background, not part of the included set. The assignment targets 15–20 **unique included primary studies**, minimum 15, per group; do not relax eligibility just to reach that count.

## 7. Inclusion criteria

All conditions must hold after full-text assessment:

1. English, peer-reviewed journal or full conference paper reporting an original empirical or technical evaluation; ordinarily within §6.
2. A clearly identifiable local GPU sharing, partition, process-concurrency or API-interception/remoting mechanism involving at least two inference tenants, services, models or processes on a physical GPU. A transferable mixed workload qualifies only if inference-specific evidence and transfer rationale are explicit.
3. Sufficient full-text detail to identify workload, sharing configuration and at least one RQ-relevant engineering outcome or directly assessable isolation property.
4. A unique study, with multiple conference/journal/preprint reports linked and the most complete peer-reviewed report selected for extraction.

Eligibility is independent of whether a mechanism performs well. Report negative and null findings. Record any justified older exception and the group's adjudication.

## 8. Exclusion criteria

At full text record one primary reason, with secondary notes if useful: **E1** no inference-serving evidence; **E2** no relevant single-node multi-tenant sharing; **E3** mechanism outside assigned scope; **E4** training-only; **E5** cluster orchestration without local sharing evaluation; **E6** no peer-reviewed original primary study (survey, vendor page, blog, preprint-only, poster, editorial, patent); **E7** insufficient technical/outcome evidence; **E8** duplicate/less complete report of the same study; **E9** outside date/language rule without exception; **E10** other, with written justification. Vendor guides [10], [11] describe mechanism context but cannot count as primary evidence or demonstrate workload performance. Track full text **not retrieved** as an access outcome, with attempts, rather than an exclusion among assessed reports [2].

## 9. Screening procedure

1. **Identification:** Execute and export each frozen query. Assign a unique record ID to every hit, preserving database/run provenance. Log citation-chased candidates separately.
2. **Deduplication and versions:** Normalize DOI, title, year and authors; retain raw records and link record IDs → report IDs → underlying unique study IDs. Prefer the complete peer-reviewed version without treating its preprint as a second study.
3. **Calibration:** Both screeners independently apply the draft rule set to a small common pilot set; record disagreements and clarify ambiguous terms before freeze. The group's third member adjudicates.
4. **Title/abstract:** Two independent screeners mark include, exclude or uncertain with reason and IDs. Retrieve uncertain records; adjudicate disagreement without inventing a consensus.
5. **Full text:** Record retrieval attempts and access status. Two screeners independently apply §§7–8 to retrieved reports; the third adjudicates discrepancies and records the final reason and study/report links. No inference from an unavailable full text.
6. **Flow:** Derive PRISMA 2020 record, report and study counts from those logs, including pre-screen removals, reports sought, reports not retrieved, assessed reports, exclusions with reasons and included unique studies [2]. Reconcile counts by group and by formal/supplementary discovery route.

If the pilot suggests fewer than 15 eligible studies, consult the instructor before changing the assigned scope or criteria. Do not retrospectively turn scoping candidates into screened inclusions.

## 10. Quality-assessment criteria

Two reviewers independently score each **included** study on Q1–Q10: **1** adequate, **0.5** partial/unclear, **0** absent/not reported. Reconcile with a recorded rationale; the third member resolves persistent disagreement. This group-designed rubric is an appraisal plan, not a validated universal instrument [4].

| ID | Question |
|---|---|
| Q1 | Is the engineering question and tenant setting explicit? |
| Q2 | Are the mechanism and isolation/configuration described sufficiently? |
| Q3 | Are GPU SKU/count, partition, OS, driver and runtime stated? |
| Q4 | Are model, workload, batching/arrivals and co-tenant mix stated? |
| Q5 | Is the baseline appropriate and configured fairly? |
| Q6 | Are utilization, latency percentiles and other metric definitions/units clear? |
| Q7 | Are warm-up, duration, repetitions/variance and load generation adequate? |
| Q8 | Do figures/tables/data support the reported findings? |
| Q9 | Are limitations, confounders and validity threats discussed? |
| Q10 | Is there enough information to reproduce or critically interpret the comparison? |

Total 0–10: **high 8–10**, **moderate 6–7.5**, **low <6**. Score does not replace eligibility. Retain eligible low-quality evidence with labels and rerun conclusions without it. Log reviewer-specific scores, evidence anchors, reconciliation and missing facts.

## 11. Data-extraction fields

Use one study-level identity row plus report/result rows where needed, each with PDF page/section/table/figure anchors. Pilot the form on multiple mechanism families before freeze.

| Field group | Required fields |
|---|---|
| Provenance | Group, record/report/study IDs, query/run and database, DOI/publisher URL, authors, title, year, venue, peer-review/version status, access/retrieval date, source anchor |
| Mechanism | Time-slice policy or context switch; MPS version/limits; MIG profile; API remoting/proxy path; hybrid; scheduler/control layer, admission/QoS policy |
| Environment | GPU vendor/SKU/count/memory/partition, host CPU/RAM, OS/kernel, driver, CUDA/runtime, container or VM |
| Workload | Inference task/model/size/input, tenant identity and mix, batch size, arrival pattern, concurrency, load, warm-up/window/repetitions |
| Comparator | Baseline, direct vs indirect comparison, configuration equivalence |
| Outcomes | Utilization/occupancy, throughput/goodput, tenant density, p50/p95/p99 and units, SLO threshold/miss rate, interference, overhead, energy if given, uncertainty/variance |
| Isolation | **Separately** measured or claimed performance interference, resource/memory partitioning, security boundary and fault containment; mark not reported where absent |
| Interpretation | Verbatim-sized finding summary in own words, exact anchor, author caveat, reviewer inference separately, QA scores, confounders and comparability notes |

Do not fill absent values by assuming a GPU mechanism's default behavior. Capture both favorable and unfavorable findings.

## 12. Evidence-synthesis strategy

Build a mechanism taxonomy (temporal, MPS, MIG, API remoting/virtualization, hybrids), an RQ-to-study matrix and a condition/comparability table. For RQ1 summarize evaluated control and isolation dimensions; for RQ2 compare metric and experiment definitions; for RQ3 stratify by GPU generation/profile, model and batch/arrival/tenant conditions; for RQ4 trace reported trade-offs and counterexamples to differing baselines and conditions; for RQ5 create a conditional decision matrix with evidence strength and uncertainty.

Use structured narrative synthesis because different GPUs, workloads, tenancy and latency percentiles make raw pooling misleading. Compare numerical effects only inside genuinely compatible experimental strata; otherwise report direction, conditions and limitations without an invented aggregate. Report each recommendation as **direct within-study comparison**, **indirect primary evidence**, **vendor context only**, or **insufficient evidence**. Apply the SWiM transparency principles for any synthesis without meta-analysis [9]. Repeat the conclusion after excluding low-QA/incomplete studies. Report coverage gaps, publication/access bias, heterogeneity and reviewer disagreement. No mechanism is declared universally optimal.

## Protocol changes and freeze record

**A001 (historical):** v1.0 was prematurely called frozen; v1.1 corrected the proposed databases, recall risk and full-text accounting before any formal screening. Details remain in `evidence/protocol_amendments.md`; no count impact was claimed.

**A002 (this proposal, 27 September 2026 PKT):** Reorganize the shared protocol into the instructor's exact twelve headings, expand methodological and mechanism references, specify executable-query validation and group-specific ownership, and align report source and Markdown. This is a **pre-search reporting/clarification revision**, not a claim of completed search or changed eligibility. Once the two groups are named, each must evaluate these choices independently and record its own dated freeze; A002 affects zero formal records based on the current documented status.

**After a group starts formal searching:** Before using a major change, append a dated entry to *that group's* `evidence/protocol_amendments.md` with old/new rule, trigger, justification, approving reviewers, affected queries/dates/records, whether earlier databases must be rerun, screening/PRISMA count effects, and how old and new results will be reconciled. Version the protocol and label deviations in the report. Log purely syntactic platform translations in search logs; a recall-changing translation is a major amendment. PRISMA-P calls for recording important protocol amendments [1].

## References (IEEE style; context and method only, no included studies claimed)

[1] L. Shamseer *et al*., “Preferred reporting items for systematic review and meta-analysis protocols (PRISMA-P) 2015: elaboration and explanation,” *BMJ*, vol. 349, g7647, 2015. doi: [10.1136/bmj.g7647](https://doi.org/10.1136/bmj.g7647).

[2] M. J. Page *et al*., “The PRISMA 2020 statement: an updated guideline for reporting systematic reviews,” *BMJ*, vol. 372, n71, 2021. doi: [10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71).

[3] M. L. Rethlefsen *et al*., “PRISMA-S: an extension to the PRISMA statement for reporting literature searches in systematic reviews,” *Systematic Reviews*, vol. 10, art. 39, 2021. doi: [10.1186/s13643-020-01542-z](https://doi.org/10.1186/s13643-020-01542-z).

[4] B. Kitchenham and S. Charters, “Guidelines for performing systematic literature reviews in software engineering,” EBSE Technical Report EBSE-2007-01, 2007. [Online]. Available: [EBSE record](https://ebse.webspace.durham.ac.uk/ebse-bibliography/guidelines-for-performing-systematic-literature-reviews-in-software-engineering/).

[5] Engr. Abul Kalam Library, NED University, “E-Resources,” accessed Sept. 27, 2026. [Online]. Available: [NED E-Resources](https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html).

[6] IEEE, “IEEE Xplore: Searching and Saving Searches,” user guide. [Online]. Available: [IEEE guide](https://ieeexplore.ieee.org/Xplorehelp/downloads/user-guides/IEEE_Xplore_Searching_and_Saving_Searches.pdf).

[7] ACM, “Search tools,” ACM Digital Library. [Online]. Available: [ACM search tools](https://libraries.acm.org/training-resources/search-tools).

[8] Springer Nature, “Springer Nature Link advanced search option.” [Online]. Available: [Search help](https://support.springernature.com/en/support/solutions/articles/6000080445-springer-nature-link-advanced-search-option).

[9] M. Campbell *et al*., “Synthesis without meta-analysis (SWiM) in systematic reviews: reporting guideline,” *BMJ*, vol. 368, l6890, 2020. doi: [10.1136/bmj.l6890](https://doi.org/10.1136/bmj.l6890).

[10] NVIDIA, “Introduction,” *Multi-Instance GPU User Guide*. [Online]. Available: [MIG introduction](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/introduction.html).

[11] NVIDIA, “Architecture,” *Multi-Process Service*. [Online]. Available: [MPS architecture](https://docs.nvidia.com/deploy/mps/architecture.html).

[12] Z. Bai *et al*., “PipeSwitch: Fast pipelined context switching for deep learning applications,” in *Proc. 14th USENIX OSDI*, 2020. [Online]. Available: [USENIX venue page](https://www.usenix.org/conference/osdi20/presentation/bai). **Search seed only; not screened.**

[13] M. Lee *et al*., “ParvaGPU: Efficient spatial GPU sharing for large-scale DNN inference in cloud environments,” in *Proc. SC '24*, 2024. doi: [10.1109/SC41406.2024.00048](https://doi.org/10.1109/SC41406.2024.00048). **Search seed only; not screened.**

[14] M. Yu *et al*., “Torpor: GPU-enabled serverless computing for low-latency, resource-efficient inference,” in *Proc. USENIX ATC '25*, 2025. [Online]. Available: [USENIX venue page](https://www.usenix.org/conference/atc25/presentation/yu). **Search seed only; not screened.**
