# Two-group OS CEP workflow

## Repository and authority

The planned canonical repository is [AliRazaDev241/OS_CEP](https://github.com/AliRazaDev241/OS_CEP). It is currently empty; `C:\Projects\OS_CEP` is the staging copy until the initial import is reviewed and merged. After import, work from a checked-out branch of that repository. Do not assume that a local edit has reached GitHub.

`guidelines.md` and `topics.md` remain the unchanged assignment authorities. Both groups have the same assigned Topic 23 and each consists of three students. Group identifiers `group-a` and `group-b` are neutral placeholders; record which is yours and which is your friend's, member names, and reviewer roles before formal screening. Do not infer membership from the GitHub owner name.

## Repository layout after initial import

```text
guidelines.md                 # authoritative, unchanged
topics.md                     # authoritative, unchanged
AGENTS.md                    # shared operating rules
PRD.md                       # shared scope and deliverables
ROADMAP.md                   # shared gates; each group has its own progress
GROUP_WORKFLOW.md            # ownership, layout, and PR process
protocol.md                  # historical v1.1 candidate; shared scoping reference only
evidence/                    # historical shared scoping and query-pilot drafts
groups/group-a/              # independent three-person SLR and report
groups/group-b/              # independent three-person SLR and report
```

Each group path will contain its own `README.md`, `ROADMAP.md`, `protocol.md`, `evidence/` (amendments, search runs, imported records, duplicates, screening, quality, extraction, claims, PRISMA), and `report/` (LaTeX, references, checked PDF). These are planned paths, not claims that two studies/reviews already exist. The existing root `report/main.tex` and `report/main.pdf` are a shared **protocol draft**, not either group's final SLR report.

## Two independent versions of every research stage

| Stage or artifact | `groups/group-a/` | `groups/group-b/` |
|---|---|---|
| Ownership and schedule | Its own three members, two screeners, one adjudicator, dates and decisions | Its own three members, two screeners, one adjudicator, dates and decisions |
| Scoping and protocol | Its own scope rationale, RQs, validated database queries, eligibility, quality and synthesis rules | Independently justified scope rationale, RQs, queries, eligibility, quality and synthesis rules |
| Search and PRISMA | Its own dated runs, exports, record/report/study IDs, duplicate links, two-reviewer decisions and reconciled flow | Separate dated runs, exports, IDs, decisions and reconciled flow |
| Extraction and analysis | Its own source-anchored extraction, quality scores, taxonomy, comparison and conflict synthesis | Separate source-anchored extraction, quality scores, taxonomy, comparison and conflict synthesis |
| Submission | Its own 20–30-page, 12-point IEEE-cited LaTeX report, PDF, appendices and supporting evidence | Its own 20–30-page, 12-point IEEE-cited LaTeX report, PDF, appendices and supporting evidence |

The instructor's requirements apply **to each group independently**. Each final included set must meet the 15–20 primary-study target (minimum 15); counts and screeners from one group cannot be borrowed by the other. The same paper may appear in both reviews if each group independently retrieves, screens, appraises and extracts it. Shared bibliography discovery, reusable blank templates and mechanism terminology may live at root when their provenance is clear, but they are never pre-included evidence or a substitute for either group's decisions. Do not submit two paraphrases of one review; each group must own its questions, analysis, claims and writing while covering the assigned four mechanisms. If a planned distinction would narrow away a required topic element, obtain instructor guidance first.

Every task request must name `group-a`, `group-b`, or `shared`. If the request says “both groups,” produce and review two separately labelled deliverables. If the group is unspecified, advance shared non-decision work and mark group-specific work pending identification. Never silently copy conclusions, PRISMA counts, quality scores or prose across groups.

## Pull-request workflow and initial bootstrap

1. Since the GitHub repository has no commits yet, its owner first creates a minimal initial `main` commit (for example, a README) through GitHub. This is the one-time branch bootstrap; do not treat it as approval to push the research files directly to `main`.
2. Import the staged PC files on a new branch such as `docs/initial-os-cep-import`, push that branch, and open a PR into `main`. Show the changed-file list; confirm `guidelines.md` and `topics.md` are unmodified and identify the v1.1 root protocol as shared draft.
3. For subsequent work, update `main` locally, create a short-lived branch named `group-a/<task>`, `group-b/<task>`, or `shared/<task>`, commit only the scoped files, push, and open a PR into `main`. Use separate PRs for each group's evidence and report whenever possible.
4. A PR description must state group, guideline requirement, files changed, research status (scoping/proposed/verified), evidence provenance, amendment if protocol rules changed, and checks performed. Ask at least one appropriate human teammate to review. Resolve feedback on the branch and keep the PR open for the group owner to merge.
5. Agents must **never merge, enable auto-merge, push to `main`, force-push, bypass branch protection, or mark a review as approved**. A user or designated human maintainer handles merges after review. A request to prepare/push a PR authorizes a branch and PR, not a merge.

The repository is currently public. Do not commit credentials, NED VPN details, private links, licensed publisher PDFs, or personal identifiers without authorization. Store links/DOIs and permitted extraction notes rather than copying full papers. Set branch protection or rulesets when the repository supports them; the written PR rule applies regardless of enforcement. Nothing has been pushed from the PC folder in this step.

## Decisions to fill before either group's formal search

- Map `group-a` / `group-b` to the two real teams and list three members each.
- Confirm each group's owner, two independent screeners and adjudicator.
- Confirm whether the instructor accepts two reviews of the same assigned topic and any group-specific RQ emphases; do not assume that duplicating one submission is acceptable.
- Confirm institutional database access and publication-export permissions for both groups.
- Confirm the week-13 date and any specific LaTeX/report template; record each group's protocol freeze separately.
