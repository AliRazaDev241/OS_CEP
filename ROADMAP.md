# OS CEP shared roadmap — two independent groups

## State and authority

`guidelines.md` and `topics.md` remain unchanged assignment authorities. The future canonical repository is https://github.com/AliRazaDev241/OS_CEP; the Windows folder is staging until an initial import PR is merged. See `GROUP_WORKFLOW.md` for layout, group mapping and PR rules. Root `protocol.md`, `evidence/`, and `report/` are shared pre-search drafts/history, not either group's completed review.

For every item below, track **group-a** and **group-b** separately in their own `ROADMAP.md`. “Planned” means not started; “scoping” is terminology/feasibility discovery; “frozen” requires dated group approval; “verified” requires a dated artifact. Do not transfer completed status between teams. Each group has three members and independently targets 15–20 included peer-reviewed primary studies (15 minimum), PRISMA 2020, and its own IEEE-cited 12-point, approximately 20–30-page LaTeX/PDF report.

## Shared setup and migration

- [x] Read assignment and topic documents for the shared Topic 23.
- [ ] Map `group-a` and `group-b` to the user's and friend's real groups; record three members and roles for each.
- [ ] Ask the instructor to confirm both groups may review the same topic and clarify any expected distinction without omitting time-slicing, MPS, MIG or API remoting.
- [ ] Confirm the week-13 date, report template, institutional access and permitted export handling for both teams.
- [ ] Have the repository owner create a minimal initial `main` commit in the presently empty repo, then place staged files on `docs/initial-os-cep-import` and open a PR targeting `main`.
- [ ] Review the import PR, check that `guidelines.md` and `topics.md` match the originals, and identify root protocol/evidence/report as draft material. A human owner merges after review.

No project research files have been pushed to GitHub by this roadmap edit. Thereafter every change uses a scoped branch and PR; agents do not directly push `main` or merge.

## Per-group gates — apply each step twice

### 0. Assign ownership and calibrate

- [ ] **group-a:** Confirm three member IDs, two screeners, adjudicator, access and schedule.
- [ ] **group-b:** Confirm its own three member IDs, two screeners, adjudicator, access and schedule.
- [ ] **Both independently:** Pilot a small screening sample, record disagreements, and resolve the decision rules.

**Gate 0:** Neither group starts formal screening before its own protocol freeze and database-interface pilot.

### 1. Scope and validate searches

- [ ] **Each group:** Examine recent reviews for overlap; record discovery as candidates only.
- [ ] **Each group:** Check the proposed IEEE Xplore, ACM DL, ScienceDirect and Springer Nature Link interfaces, entitlement, exact syntax, filters, count, export route and seed recall; justify any database substitution.
- [ ] **Each group:** Test all four mechanism families and assess feasibility of the 15-study minimum. Seek instructor guidance before any scope change that removes a required family.

**Gate 1:** Scoping records do not enter PRISMA or become included studies automatically.

### 2. Finalize a group protocol before selection

- [ ] **Each group:** Adapt the root candidate into its own `protocol.md` with objective, RQs, databases, keywords, exact executable strings, period, inclusion/exclusion, screening, QA, extraction and synthesis.
- [ ] **Each group:** Specify report/record/study linkage, exclusion codes, reviewer adjudication, RQ-to-evidence map and amendment procedure.
- [ ] **Each group:** Date and approve its validated freeze; keep its own amendment register. The root v1.1 is not a substitute.

**Gate 2:** Formal search and selection begin only under that group's frozen rules. Later semantic changes require a dated justified amendment with count impacts.

### 3. Search and screen separately

- [ ] **Each group:** Execute and log its own exact database queries, dates, filters, hits, exports and reviewer; log citation chasing separately.
- [ ] **Each group:** Retain source records, deduplicate without losing provenance, link reports to unique studies, record two independent screening decisions and adjudication.
- [ ] **Each group:** Retrieve full texts lawfully; distinguish retrieval failure from an assessed full-text exclusion; reconcile its own PRISMA flow.
- [ ] **Each group:** Stop and ask the instructor before revising criteria if the final eligible count cannot meet 15.

### 4. Appraise, extract and synthesize separately

- [ ] **Each group:** Apply its frozen quality rubric and source-anchored extraction to every included study.
- [ ] **Each group:** Compare mechanisms only under compatible hardware, workload, baseline and metric definitions; document counterevidence and missing data.
- [ ] **Each group:** Answer its RQs via a taxonomy, evidence/comparability tables, sensitivity analysis and conditional decision matrix.

### 5. Produce and review two submissions

- [ ] **group-a:** Compile its own `report/main.tex`, references and final PDF; inspect page count, 12-point type, citations, PRISMA reconciliation and print layout.
- [ ] **group-b:** Compile and inspect its own corresponding TeX, references and PDF against the same requirements.
- [ ] **Each group:** Submit work on its scoped feature branch through a PR with provenance, checks and changes identified; ask a human teammate to review. A designated human maintainer handles merge.

**Immediate next task:** Map the two groups and institutional access; then each team independently pilots database queries and signs off its own protocol. The shared v1.1 draft records no formal searches, screened studies or PRISMA counts.
