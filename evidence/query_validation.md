# Query validation and database pilot — v1.1

**Shared candidate template:** This root file is terminology and interface-planning context for both three-person groups. Each group must run and record its own pilots, validate strings, freeze its own protocol, and log formal searches under `groups/<group>/evidence/`. Do not count another group's pilots or hit counts as its own.

**Status: PROPOSED, NOT EXECUTED.** No platform hit counts, export files, or seed-retrieval outcomes have been observed. The four formal platforms are those named in NED's E-Databases section: IEEE Xplore, ACM Digital Library, ScienceDirect, and Springer Nature Link. Scopus/Web of Science appear under Analytics and can supplement coverage/citation tracking; they do not substitute for these four formal sources.

## Core query inputs to test on each platform

These are proposed copy/paste strings, not representations of a completed search. Use title/abstract/keywords or metadata scope where the platform supports it. Interface transformations, limits, exact applied facets and result URLs must be transcribed from the live platform before freeze. Split by mechanism family if the long query fails or suppresses known seeds; preserve all runs separately and deduplicate exports downstream.

| Platform | Proposed input (single broad pilot) | Interface/validation requirement |
|---|---|---|
| IEEE Xplore Command Search | `(GPU OR "graphics processing unit") AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM) AND ("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR partitioning OR virtualization OR "API remoting" OR "CUDA remoting" OR "GPU proxy")` | Verify Command Search interprets uppercase Boolean and phrases; capture displayed exact fielded query. Apply years, publication types, language and metadata scope in facets or command as recorded. |
| ACM DL Advanced Search | `(GPU OR "graphics processing unit") AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM) AND ("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR partitioning OR virtualization OR "API remoting" OR "CUDA remoting" OR "GPU proxy")` | Use Advanced Search builder in ACM full-text collection, not the broader Guide by default. Capture its **View Query Syntax** / generated query verbatim; do not assume `Abstract:` is a valid free-form field operator. Check abstract-only field against known seeds, otherwise use metadata/all-fields and document scope. |
| ScienceDirect Advanced Search | `(GPU OR "graphics processing unit") AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM) AND ("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR partitioning OR virtualization OR "API remoting" OR "CUDA remoting" OR "GPU proxy")` | Enter in the advanced terms field if accepted; note whether it searches all full text versus title/abstract/keywords, and record the applied research-article/year/language filters. Elsevier API syntax is not presumed identical to the website. |
| Springer Nature Link Advanced Search | `(GPU OR "graphics processing unit") AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM) AND ("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR partitioning OR virtualization OR "API remoting" OR "CUDA remoting" OR "GPU proxy")` | Confirm grouping, phrase matching, and whether the search applies to all text; filter to articles and conference papers in 2020–2026, excluding books/chapters as primary studies at screening. Capture exact interface wording and URL. |

**Planned filters:** publication dates 2020-01-01 through 2026-09-27, English, peer-reviewed journal articles or conference papers where an interface supports these filters. Do not rely solely on platform's document-type facet for peer review; verify venue at screening. A 2026 year facet can include future-dated records, so record actual publication date and enforce cutoff during screening.

## Mechanism-family fallback strings

If a platform caps Boolean clauses or the broad input loses seeds, use these separate searches with `GPU AND (inference OR "model serving" OR "deep learning")` as common prefix; OR the family terms below, log each run, and deduplicate records. The fallback is a **planned pre-freeze design choice**; decide from the pilot, then document the exact executed variant for each platform.

| Family | Add as AND block |
|---|---|
| Temporal | `("time slicing" OR timeslicing OR "time sharing" OR "context switching" OR "preemptive scheduling")` |
| MPS/process concurrency | `(MPS OR "multi-process service" OR "multiple processes" OR "process-level concurrency")` |
| MIG/partitioning | `(MIG OR "multi-instance GPU" OR "GPU partitioning" OR "spatial sharing")` |
| API remoting/virtualization | `("API remoting" OR "CUDA remoting" OR "API interception" OR "GPU proxy" OR "virtual GPU" OR "GPU virtualization")` |

## Seed recall check (scoping candidates, never automatic inclusions)

| Candidate | Source | Why it probes query coverage | Pilot retrieval result |
|---|---|---|---|
| PipeSwitch (OSDI 2020) | https://www.usenix.org/conference/osdi20/presentation/bai | temporal/context-switch sharing of inference and other applications; may be missed by required `multi-tenant` phrase | Not tested |
| ParvaGPU (SC 2024) | https://dl.acm.org/doi/10.1109/SC41406.2024.00048 | combined MIG/MPS and DNN inference | Not tested |
| MIGER (2024) | https://dl.acm.org/doi/10.1145/3673038.3673089 | hybrid MIG/MPS terminology; check actual inference relevance at screening | Not tested |
| Torpor (USENIX ATC 2025) | https://www.usenix.org/system/files/atc25-yu.pdf | inference-driven asynchronous CUDA API redirection/remoting | Not tested |
| KRYPTON / *Efficient Performance-Aware GPU Sharing with Compatibility and Isolation through Kernel Space Interception* (USENIX ATC 2025) | https://www.usenix.org/system/files/atc25-zhang-shulai.pdf | kernel-space interception/virtualization vocabulary; boundary test, because inference-specific eligibility remains uncertain | Not tested |

A seed missing from a given publisher's own collection is a *coverage* issue, not necessarily a query failure. Validate discovery against Scopus/WoS if accessible and record the difference. Avoid robots, bulk scraping, or systematic PDF downloads on publisher sites; use authorized manual search/export interfaces and institutional access terms.

## Pilot record form (one row per interface test)

`date_PKT | reviewer | platform | collection/index | exact_executed_query | fields | filters | URL | hit_count | export_route | seed_tested | seed_found | issue | resolution`.

## Freeze gate

Before the formal search: (1) confirm four database entitlements, (2) run and log pilot syntax and seed coverage without screening, (3) settle any family-split variant and publication date filter, (4) record v1.2 if semantics change, (5) designate owner and reviewer IDs, and only then mark the protocol frozen. Formal search runs must be new, dated, separately logged runs; pilot counts cannot be silently substituted.

## Interface-method references

- NED E-Resources: https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html
- NED FAQ: https://eaklibrary.neduet.edu.pk/eakl/FAQ.html
- IEEE Xplore Searching and Saving Searches guide: https://ieeexplore.ieee.org/Xplorehelp/downloads/user-guides/IEEE_Xplore_Searching_and_Saving_Searches.pdf
- ACM Search Tools: https://libraries.acm.org/training-resources/search-tools
- Elsevier ScienceDirect: https://www.elsevier.com/products/sciencedirect
- Springer Nature Link advanced search: https://support.springernature.com/en/support/solutions/articles/6000080445-springer-nature-link-advanced-search-option
- Springer Boolean operators: https://support.springernature.com/en/support/solutions/articles/6000079741-boolean-operators-search-function-results-and-wildcard-searches
