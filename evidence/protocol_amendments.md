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

## Amendment entry template

| Date | Version | Change | Rationale | Affected artifacts/records | Effect on search/screening counts | Approved by |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | vX.Y |  |  |  |  |  |
