# Dated scoping log — candidate discovery only

**Shared background:** This root discovery log predates the split into `group-a` and `group-b`. It supplies candidate vocabulary and links to both groups, but neither group inherits an inclusion decision, formal search run, PRISMA count or extraction from it. Maintain separate group evidence under `groups/<group>/evidence/`.

**Purpose:** terminology, database feasibility, methodology checks, and overlap-risk assessment before formal searches. This file is not an import log; no item below is an included primary study and none contributes to PRISMA counts. **Correction A001:** early rows proposing Scopus and Web of Science among the four formal E-Databases are historical and superseded by the added 2026-09-27 observations and protocol v1.1; these are NED Analytics resources.

| Date (PKT) | Source type | Source / stable link | Discovery observation | Protocol action |
|---|---|---|---|---|
| 2026-09-27 | NED Library resource page | https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html | NED lists E-Databases and describes IEEE, Scopus and Web of Science resources. | Select IEEE Xplore, Scopus and Web of Science subject to team access check. |
| 2026-09-27 | NED Library FAQ | https://eaklibrary.neduet.edu.pk/eakl/FAQ.html | NED identifies IEEE, Springer, ScienceDirect, ACM, Wiley and Taylor & Francis; it recommends Scopus for broad discovery, ACM DL for computing and Web of Science for citation tracking. | Select ACM DL as the specialist fourth database; use Google Scholar only for supplementary citation discovery. |
| 2026-09-27 | NED Research Guide | https://eaklibrary.neduet.edu.pk/eakl/ResearchGuide.html | Library recommends Scopus + Web of Science then specialist databases; confirms computing/IT use of ACM DL. | Use complementary index-plus-specialist database design. |
| 2026-09-27 | Reporting-method standard | https://www.prisma-statement.org/prisma-2020-statement | PRISMA 2020 supplies a 27-item checklist and flow-diagram templates. | Specify record/report/study logs and derive PRISMA counts from them. |
| 2026-09-27 | Software-engineering SLR guidance | https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf | Kitchenham and Charters describe protocol-led, auditable SLR practice. | Freeze protocol before formal selection; define criteria, QA and extraction fields in advance. |
| 2026-09-27 | Survey (context only) | https://arxiv.org/abs/2203.09040 | Existing survey: *A Survey of Multi-Tenant Deep Learning Inference on GPU* (2022) signals that the topic is active and terminology is broad. | Narrow the contribution to single-node, mechanism-level utilization vs. latency/isolation trade-offs; survey remains excluded as primary evidence. |
| 2026-09-27 | Candidate primary study | https://dl.acm.org/doi/10.1145/3673038.3673089 | MIGER (2024) explicitly combines MIG and MPS; validates hybrid mechanism terms. | Include hybrid MIG+MPS vocabulary in frozen query block. It is not yet screened/included. |
| 2026-09-27 | Candidate primary study | https://arxiv.org/abs/2409.14447 | ParvaGPU (2024) describes spatial GPU sharing for DNN inference and integrates MIG/MPS. | Retain inference, MIG, MPS, partition and SLO terms. It is not yet screened/included. |

## Scoping conclusion

A non-duplicate SLR contribution remains plausible because the proposed review does not attempt a generic survey of multi-tenant inference. It will transparently synthesize peer-reviewed, single-node evidence across four specified sharing categories and explain conditional utilization, latency predictability, and isolation trade-offs. The feasibility of reaching the 15-study minimum is still unverified and must be assessed after database searches, deduplication, and screening.

## Additional scoping observations — 2026-09-27 PKT

All observations below are from publisher/venue pages or official search guidance. They identify candidate vocabulary/coverage risks, **not screened study findings**. No result count can be inferred from these spot checks.

| Source type | Link | Scoping observation and action |
|---|---|---|
| IEEE search guide | https://ieeexplore.ieee.org/Xplorehelp/downloads/user-guides/IEEE_Xplore_Searching_and_Saving_Searches.pdf | Boolean operators must be uppercase; Command Search supports nested concepts. Pilot actual metadata field syntax and capture the platform-generated query. |
| ACM Search Tools | https://libraries.acm.org/training-resources/search-tools | ACM distinguishes its DL full-text collection from broader discovery. Validate Advanced Search query syntax in the live interface; the old `Abstract:` literal was never established. |
| Springer Nature Link support | https://support.springernature.com/en/support/solutions/articles/6000079741-boolean-operators-search-function-results-and-wildcard-searches | Phrase matching and case-sensitive Boolean OR affect planned strings. Use uppercase Boolean and inspect applied field/date filters. |
| NED E-Resources | https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html | Scopus and Web of Science appear under Analytics, separately from the E-Databases section; revise the four primary source platforms to IEEE, ACM, ScienceDirect, and Springer Nature Link, subject to access. |
| PipeSwitch, OSDI 2020 venue abstract | https://www.usenix.org/conference/osdi20/technical-sessions | Candidate temporal/context-sharing seed spanning inference and other workloads; four-block multi-tenant requirement may miss it. Need full-text eligibility and same-node inference assessment later. |
| Torpor, USENIX ATC 2025 publisher PDF | https://www.usenix.org/system/files/atc25-yu.pdf | Candidate for inference-oriented asynchronous GPU API redirection/remoting vocabulary. Peer-reviewed venue does not automatically establish our full eligibility. |
| ParvaGPU, SC 2024 publisher DOI | https://dl.acm.org/doi/10.1109/SC41406.2024.00048 | Candidate MIG/MPS hybrid for DNN inference; use to test seed recall without pre-inclusion. |
| MIGER, ACM DOI | https://dl.acm.org/doi/10.1145/3673038.3673089 | Candidate hybrid MIG/MPS; online/offline jobs require checking whether inference-serving evidence actually satisfies scope. |
| Existing 2022 survey | https://arxiv.org/abs/2203.09040 | Broad multi-tenant inference survey; map overlap and citation leads only, not primary-study inclusion. |
| PRISMA official flow | https://www.prisma-statement.org/prisma-2020-flow-diagram | Distinguish reports not retrieved from reports assessed and reports excluded with reasons. |

**Caution:** Some USENIX papers may be absent from individual publisher-platform collections. The pilot should test index coverage, and any supplementation/citation chasing must be logged and screened under the same criteria. Do not claim that the topic's estimated 50–85 candidates is an observed search result.

## Mechanism documentation (context only) — 2026-09-27 PKT

| Vendor source | Contextual point to verify against primary evidence |
|---|---|
| https://docs.nvidia.com/datacenter/tesla/mig-user-guide/introduction.html | NVIDIA describes dedicated MIG compute/memory paths and hardware-profile limits. This is a product mechanism claim, not a measured cross-study latency conclusion. |
| https://docs.nvidia.com/datacenter/tesla/mig-user-guide/deployment-considerations.html | CUDA MPS can operate on a MIG instance; hybrid MIG+MPS is not a contradiction. Record GPU generation, driver, and instance profile. |
| https://docs.nvidia.com/deploy/mps/architecture.html | MPS has distinct architecture and limited QoS/resource-provisioning behavior; driver/MPS version matters, particularly when interpreting older papers. |
| https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/22.9.2/gpu-sharing.html | The vendor describes time-slicing versus MIG memory/fault-isolation trade-off; not evidence that every workload has predictable latency. |

None of these vendor pages is a peer-reviewed primary study or can fill the 15-study minimum. Separate vendor-stated design properties from independently measured latency/interference, security isolation, and fault containment.
