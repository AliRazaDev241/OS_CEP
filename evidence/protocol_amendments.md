# Protocol amendment register

## Protocol v1.0 baseline

- **Date:** 2026-09-27 (Asia/Karachi)
- **Change type:** Initial protocol freeze; not an amendment.
- **Scope:** Single-node GPU sharing for multi-tenant inference serving: time-slicing, MPS, MIG, and API remoting/virtualization.
- **Formal-search status:** Not started.
- **PRISMA status:** No counts may be entered until frozen searches are executed and logged.

## Amendment A001 — v1.0 to v1.1 (pre-search correction)

- **Date:** 2026-09-27 (Asia/Karachi)
- **Reason:** v1.0 was prematurely labelled frozen before the roadmap-required database-interface pilot, access check, seed-recall test, and group ownership confirmation. It also selected Scopus and Web of Science as two of the four E-Databases although NED presents them under Analytics; its four mandatory Boolean blocks risked recall loss; ACM's literal `Abstract:` syntax was not validated. Finally, full-text unavailability was incorrectly coded among assessed-report exclusions.
- **Changes:** Choose four NED E-Databases platforms (IEEE Xplore, ACM Digital Library, ScienceDirect, Springer Nature Link) pending entitlement check; treat Scopus/WoS as supplementary indexes; replace operative four-block strings with a three-concept candidate and mechanism-family pilot in `evidence/query_validation.md`; separate reports not retrieved from assessed-report exclusions; change status to v1.1 pre-search corrective draft.
- **Affected artifacts:** `protocol.md`, `report/main.tex`, `evidence/query_validation.md`, `evidence/scoping_log.md`, `ROADMAP.md`.
- **Impact on counts:** None: no formal search, import, screening, inclusion, or PRISMA counts had occurred. No claim of database hit count or retrieval is made.
- **Next gate:** Verify interfaces/access and exact executed syntax, capture pilot results, assign owner/reviewers, then freeze revised protocol before formal selection. Future semantic changes require another numbered amendment.


## Amendment A002 — v1.1 to proposed v1.2 (pre-search presentation and sourcing)

- **Date:** 2026-09-27 (Asia/Karachi)
- **Reason:** The existing LaTeX protocol conflated search keywords with strings, inclusion with exclusion, and extraction with synthesis. The assignment explicitly requires twelve separate protocol elements. It also needed more verifiable methodology and topic references.
- **Changes:** Reorganize the shared candidate protocol and its Markdown/LaTeX/PDF report into the instructor's twelve numbered elements; add verified references to PRISMA-P, PRISMA 2020, PRISMA-S, EBSE, SWiM, publisher search guidance, NVIDIA documentation and three candidate search seeds. Clarify that seeds are not included studies and that group-specific protocol freezes and post-search amendments are independent.
- **Affected artifacts:** `protocol.md`, `report/main.tex`, `report/main.pdf`, `evidence/protocol_amendments.md`.
- **Status and impact:** Proposed shared pre-search revision; no change to eligibility or executed formal search. No formal searches, included studies, or PRISMA counts are claimed; zero recorded count impact. Each group must validate its own executable strings, entitlement, seed recall, roles and dated freeze.
- **After-search rule:** A major change requires date, previous/new rule, justification, approvals, affected databases/records, any rerun and screening/PRISMA count effects, entered in that group's amendment register before use.

## Amendment A003 — Professor-facing presentation polish (pre-search)

- **Date:** 2026-09-27 (Asia/Karachi)
- **Reason:** Internal version, ownership, two-group and drafting notes are inappropriate on the professor's protocol submission; author identification and the required Times New Roman font were absent.
- **Changes:** Remove internal project-management notes from the submitted Markdown, TeX and PDF while retaining the twelve required methods and a concise rule for documenting major post-search changes; add the three group members in ascending roll-number order; configure all LaTeX font families as Times New Roman and build/verify the PDF with that installed font.
- **Affected artifacts:** `protocol.md`, `report/main.tex`, `report/main.pdf`, build workflow and this register.
- **Impact:** Presentation only. No change to search logic, eligibility or documented formal counts; no formal searches or study selection are claimed.

## Amendment entry template

| Date | Version | Change | Rationale | Affected artifacts/records | Effect on search/screening counts | Approved by |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | vX.Y |  |  |  |  |  |
