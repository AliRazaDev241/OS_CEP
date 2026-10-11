"""Build the intermediate manuscript and evidence documentation from the registers."""
import csv,json,re
from pathlib import Path
from urllib.parse import urlencode
P=Path(__file__).resolve().parents[1]; E=P/'evidence'; R=P.parents[1]/'report'
C=json.loads((E/'prisma_counts.json').read_text()); S=json.loads((E/'included_studies.json').read_text())
rows=list(csv.DictReader((E/'studies.csv').open()))
def csvout(name,data):
    keys=list(dict.fromkeys(k for r in data for k in r))
    with (E/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(data)
common='(GPU OR "graphics processing unit") AND (inference OR "model serving" OR "deep learning" OR DNN OR LLM) AND '
families={'MPS':'(MPS OR "multi-process service")','MIG':'(MIG OR "multi-instance GPU" OR "GPU partitioning")','TEMPORAL':'("time slicing" OR "time sharing" OR "context switching")','API':'("API remoting" OR "CUDA remoting" OR "GPU proxy" OR "GPU virtualization")'}
master=common+'("time slicing" OR "time sharing" OR "context switching" OR MPS OR "multi-process service" OR MIG OR "multi-instance GPU" OR "GPU partitioning" OR "API remoting" OR "CUDA remoting" OR "GPU proxy" OR "GPU virtualization")'
runs=[]
for family,count in [('MPS',25),('MIG',23),('TEMPORAL',45),('API',9)]:
    runs.append(dict(run_id='IEEE-'+family,database='IEEE Xplore',date='2026-10-11',time_utc='not_recorded',status='executed',collection='Xplore all metadata',query=common+families[family],fields='All metadata (Search by All); not field-qualified Command Search',filters='Publication years2020-2026; date/language/type checked during screening',hits=count,imported_occurrences=count,export='imported_records.json: matching run_id',export_method='Public rendered-result metadata; all pages captured; publisher CSV requires personal sign-in; BibTeX export timed out',url='https://ieeexplore.ieee.org/search/searchresult.jsp',reviewer='AI-CODEX'))
runs.append(dict(run_id='SPR-MASTER',database='Springer Nature Link',date='2026-10-11',time_utc='not_recorded',status='executed',collection='Springer Nature Link',query=master,fields='General search/full-text indexed collection',filters='English; Research article OR Conference paper;2020-2026; manual cutoff',hits=587,imported_occurrences=587,export='imported_records.json: matching run_id',export_method='Rendered metadata from all30 pages; publisher CSV routes to sign-in',url='https://link.springer.com/search?'+urlencode({'query':master,'content-type':['Research','Conference Paper'],'language':'En','date':'custom','dateFrom':'2020','dateTo':'2026','sortBy':'relevance','page':1},doseq=True),reviewer='AI-CODEX'))
for db,url,why in [('ACM Digital Library','https://dl.acm.org/','Cloudflare challenge loop; no result list obtained; no bypass attempted'),('ScienceDirect','https://www.sciencedirect.com/','Search page unavailable; no result list obtained')]:
    runs.append(dict(run_id=('ACM' if db.startswith('ACM') else 'SD')+'-PILOT',database=db,date='2026-10-11',time_utc='not_recorded',status='blocked_pilot',collection='not_validated',query='GPU AND inference AND MPS',fields='not_validated',filters='not_applied',hits='UNKNOWN',imported_occurrences=0,export='',export_method=why,url=url,reviewer='AI-CODEX'))
runs.append(dict(run_id='SUP-SELECTED',database='Supplementary public web/venue/author lookup',date='2026-10-11',time_utc='not_recorded',status='selected_candidates',collection='Selected named papers; not an exhaustive search-engine export',query='Named-paper lookups and official venue/author retrieval; see supplementary_discovery.csv',fields='Public metadata/full texts',filters='Same protocol eligibility',hits='UNKNOWN',imported_occurrences=C['supplementary_selected'],export='supplementary_discovery.csv',export_method='Selected sources reused from scoping and checked after protocol adoption; no total web hit count claimed',url='',reviewer='AI-CODEX'))
csvout('search_runs.csv',runs)
csvout('supplementary_discovery.csv',[dict(record_id=r['record_id'],method='Named-paper public lookup',query='"'+r['title']+'" GPU inference',seed='Submitted protocol seeds / related-system references / targeted public discovery',direction='not_systematic_citation_chasing',date='2026-10-11',source_url=r['url'],selected_for_register='yes',note='Selected record only; query wording here is a reproducible follow-up, not a verbatim historical web query') for r in rows if r['record_route']=='supplementary'])
priority=['GA-X005','GA-R0011','GA-R0004','GA-R0292','GA-R0006','GA-R0014','GA-X006','GA-X007','GA-R0009','GA-R0037']
assert len(priority)<=10, 'User download ceiling exceeded'
pending=[r for r in rows if r['decision']=='pending'];pending.sort(key=lambda r: (priority.index(r['record_id']) if r['record_id'] in priority else 1000,int(re.sub(r'\D','',r['record_id']))))
requests=[]
for i,r in enumerate(pending,1):
    platform='IEEE Xplore' if 'ieee' in r['url'] or '10.1109/' in r['url'] else 'ACM DL' if '10.1145/' in r['url'] else 'ScienceDirect' if 'sciencedirect' in r['url'] else 'Springer Nature Link'
    requests.append(dict(priority='unavailable_not_requested_again' if r['record_id'] in priority else 'deferred_not_requested',record_id=r['record_id'],title=r['title'],platform=platform,url=r['url'],reason='Access backlog only; user supplied six of original ten and no further download is requested. '+r['reason'],ned_platform_listing='https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html',listing_checked='2026-10-11',individual_entitlement='UNVERIFIED; platform listing is not a subscription guarantee'))
csvout('download_requests.csv',requests)
md='''# Group A — received papers and remaining access backlog

The original request was capped at ten papers. The user could obtain six and supplied their Markdown conversions: VastPipe, ArkGPU, Dyna-P, iGniter, InferFair and the REEF journal extension. All six have now been assessed. Five add unique studies; REEF replaces the less complete conference report within GA-S001. See uploaded_paper_receipts.csv and six_paper_review.md.

The remaining original requests (GhostWriter GA-R0011, HAS-GPU GA-R0004, CNN prediction GA-R0292, vGPU GA-R0009) remain inaccessible. They are not exclusions and are not requested again. No replacement batch or additional paper download is requested. download_requests.csv is now an access backlog with zero active requests; all other unresolved records are deferred.

ACM/ScienceDirect formal query totals remain UNKNOWN. Six full texts resolve six access cases, not missing database search coverage. Recover exports only if accessible, preserving exact query, collection, filters, date and counts; otherwise retain the coverage limitation. NED platform listing does not prove article-level entitlement. Licensed source files remain private; git contains metadata, hashes and reviewer paraphrases only.
'''
(E/'download_requests.md').write_text(md)
claims='''# Group A — provisional claim and RQ matrix

All recommendations are reviewer interpretations of heterogeneous published experiments, not deployments validated by this group. The full-text set is current, not a final systematic selection. No pooled numerical effect is calculated.

| ID / RQ | Provisional interpretation | Primary support | Counterevidence / condition | Strength |
|---|---|---|---|---|
| C1 / RQ1,3 | Temporal scheduling is a candidate for priority inference when co-tenant work can be controlled. | GA-S001,003,004,008,014,015; extraction anchors | Memory handover, context and runtime differ; no universal bound | Direct within each study; indirect across studies |
| C2 / RQ1,3 | MPS provisioning can support density goals, with workload-specific tuning. | GA-S002,012 | Loading/reconfiguration and interference matter; density is not security | Direct within study; conditional interpretation |
| C3 / RQ1,3 | MIG and MPS can be combined; slice memory pressure must be checked. | GA-S010,016 | Parva author manuscript; Fermilab local-slice evidence only | Direct within each study; indirect comparison |
| C4 / RQ2 | Goodput, throughput, busy time, GUE and occupancy require distinct columns. | GA-S004,005,010,012 | Different denominators and percentiles prevent raw pooling | Measurement interpretation |
| C5 / RQ4 | Protecting priority latency can reduce lower-priority throughput. | GA-S009 section5.3 Fig6 | Tally does not dominate TGS on BE throughput in that stratum | Direct counterexample |
| C6 / RQ4,5 | API remoting is a candidate when transfer costs fit the SLO budget. | GA-S005,006,007,009,011 | PCIe/NVLink path, runtime compatibility, process boundary and scheduler overhead | Conditional, indirect across systems |
| C7 / RQ1,4,5 | Performance protection does not establish security or fault containment. | GA-S007 section2.2; all isolation columns | Most extracted results do not test adversarial isolation; GhostWriter awaits retrieval | Insufficient comparative security evidence |

RQ-to-final-output: RQ1 → mechanism/control boundary taxonomy; RQ2 → definitions and comparability table; RQ3 → hardware/workload/configuration strata; RQ4 → trade-offs/counterexamples/operating cost; RQ5 → conditional decision matrix. Required field groups are preserved in extraction.csv; untranscribed parameters are explicitly NOT EXTRACTED rather than marked absent in the paper.

Sensitivity: all current QA totals are at least8, so dropping QA<6 removes none and provides no discriminating test. Removing author-manuscript ParvaGPU and Tally weakens the hybrid MIG and negative-throughput evidence. Removing AMD-only KRISP and the main AMD REEF stratum leaves NVIDIA temporal/API/MPS evidence but does not validate AMD-to-NVIDIA transfer. Dropping incomplete environment profiles would remove much of the set; current recommendations are therefore provisional. Do not convert a high rubric total into high causal confidence or complete search coverage.

Next extraction pass: finish driver/runtime versions, MIG profile names, MPS quotas, batching, exact arrival rates, warm-up/windows/variance and measured-vs-claimed isolation fields before final recommendations. Check all newer/related reports and repeat synthesis after resolving the access queue. No experiments or code artifacts have been rerun.
'''
claims=claims.replace('all current QA totals are at least8','all current QA totals are at least6.5')
claims=claims.replace('GA-S002,012','GA-S002,012,017,020').replace('GA-S010,016','GA-S010,016,019')
claims=claims.replace('GhostWriter awaits retrieval','GhostWriter remains inaccessible, with no further user download requested')
claims+='''

Six-paper update: GA-S017 VastPipe supplies local A100 MPS and separate MI100 CU-mask throughput strata; its 1000-NPU cluster results are outside the local GPU comparison. GA-S018 ArkGPU supplies mixed inference/training p99/QPS evidence; its four-GPU goodput gains are separate. GA-S019 Dyna-P supplies local MIG inference-job results and a concurrency/JCT trade-off; cluster simulations and makespan are not online p99 measurements. GA-S020 iGniter supplies local MPS interference and transient p99 failure/recovery evidence; fleet cost savings are not local utilization. GA-S021 InferFair supplies local fairness/SLO goodput with distinct unfairness definition. Updated GA-S001 journal REEF supplies NVIDIA comparisons and a throughput cost of latency protection; the OSDI report is a linked E8 companion, never an additional study.

Reporting sensitivity: the four newly included moderate-QA studies (VastPipe6.5, ArkGPU7, Dyna-P7, InferFair7.5) are removed by a stricter QA>=8 sensitivity stratum; iGniter and journal REEF score8.5. Removing these moderate rows weakens dynamic-MIG placement, API-throttled inference/training and relative-goodput fairness evidence. QA<6 removes none. Scores do not resolve missing full-text plot data. No universal or pooled percentage improvement is defensible.
'''
(E/'claims.md').write_text(claims)
(E/'README.md').write_text('''# Group A evidence — 11 October 2026

Start with search_runs.csv, prisma_counts.json and studies.csv. imported_records.json preserves all689 formal query occurrences; duplicates.csv links10 repeated records without deleting provenance. studies.csv is the decision authority; accepted.csv, rejected.csv and pending.csv are derived views. Twenty-one study IDs link accepted reports to extraction.csv, quality.csv and the included-only ../../report/query_references.bib. Supplementary selected records are20, not an exhaustive web export. Six uploaded conversions resolved six pending access cases; the preferred REEF journal report replaces its conference extraction without double-counting. See six_paper_review.md, uploaded_paper_receipts.csv and uploaded_review_assessments.json; source Markdown files are not committed.

Screening is one AI reviewer authorized by the user, not independent student review. Title exclusions are explicitly title-stage judgments; no unavailable paper has an invented full-text result. Access failures remain pending. A report ID identifies a bibliographic report candidate; a study ID is assigned only when identity is assessed. REEF version links select GA-X007 for GA-S001 and mark GA-SUP001 E8, retaining companion extraction/QA history.

Public result-page capture substitutes for unavailable publisher exports; it does not preserve abstracts that were never displayed. metadata contains only the matched result item, never signed-in account or network details. retrieval_lookups.json is a sanitized public-access ledger, not an archive of copyrighted full texts. Download requests are linked to NED-listed platforms; individual entitlements are unverified.

Counts reconcile the captured subset only. ACM/ScienceDirect totals are UNKNOWN. No final PRISMA diagram or completed four-database SLR is claimed. Use the report's checkpoint flow and the machine-readable counts together.

Calibration/reconsiderations: PipeSwitch retained because inference switching outcomes are explicit; KRISP retained under protocol7.2 local partition/API control but its AMD emulation is isolated from NVIDIA MPS evidence; TGS excluded as training-only; Fermilab Triton reconsidered and retained only after Fig10 showed concurrent distinct models inside a slice. DIPPM rejected at full text because profile suggestion alone is not concurrent tenant evaluation. No reviewer disagreement or consensus is invented.

Rebuild derived data: python groups/group-a/scripts/build_evidence.py, then python groups/group-a/scripts/build_report.py. Validate with validate_evidence.py. The scripts preserve recorded assessments; they cannot recreate searches or replace reviewer decisions. The Excel workbook is a review view of the CSV registers, with count formulas; CSV/JSON remain authoritative.
''')
def tx(s):
    return ''.join({'&':r'\&','%':r'\%','_':r'\_','#':r'\#','$':r'\$','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}.get(c,c) for c in str(s)).replace('—','---').replace('–','--').replace('’',"'")
tex=r'''\documentclass[12pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{iftex}
\ifPDFTeX\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{mathptmx}\else\usepackage{fontspec}\setmainfont{Times New Roman}\fi
\usepackage{longtable,booktabs,array,enumitem,microtype,xcolor,needspace}
\usepackage[hidelinks]{hyperref}
\usepackage{parskip}
\setlength{\emergencystretch}{3em}
\setlist{nosep}
\newcolumntype{P}[1]{>{\raggedright\arraybackslash}p{#1}}
\title{GPU Sharing Mechanisms for Multi-Tenant Inference Serving\\\large Group A: Search Execution and Evidence Report}
\author{MUHAMMAD BURHAN UN NADEEM (SE-24071)\\MUHAMMAD FAAIZ ALAM (SE-24094)\\ALI RAZA (SE-24302)}
\date{11 October 2026\\Operating Systems Complex Engineering Problem\\NED University of Engineering and Technology}
\begin{document}
\maketitle
\begin{abstract}
This intermediate deliverable records execution of the submitted SLR protocol and prepares traceable evidence for the final CEP report. Two databases yielded 689 captured query occurrences; supplementary public venue and author searches supplied additional named candidates. Sixteen distinct peer-reviewed studies currently meet full-text eligibility. Unavailable full texts, incomplete publisher coverage and extraction gaps remain explicit. The paper set and conditional synthesis are provisional; the completed four-database SLR and final CEP submission are not claimed.
\end{abstract}
\textbf{Status: evidence checkpoint, not final SLR.} The publication window is 1 January 2020--11 October 2026 inclusive. One AI reviewer conducted screening and appraisal at the user's direction; the listed students are the project authors, not claimed independent reviewers.
\newpage\tableofcontents\newpage
\section{Purpose and requirements}
The engineering problem is to share a physical GPU among inference tenants while balancing useful work and density against predictable latency and isolation. The assigned alternatives are time-slicing, MPS, MIG and API remoting/virtualization, including hybrids. The unit of technical comparison is local sharing on one GPU. A study containing cluster experiments qualifies only when local inference-sharing evidence is identifiable; cluster-wide GPU counts are never substituted for local occupancy.

The submitted \texttt{report/SLR\_protocol.tex} and \texttt{report/SLR\_protocol.pdf} are the protocol baseline identified by the user. The protocol contents are preserved. Query deliverables reside in the root \texttt{report/} folder; Group A evidence remains under \texttt{groups/group-a/evidence/}. The final assignment still requires 15--20 unique peer-reviewed primary studies, at least15, a 12-point IEEE-cited LaTeX report, and approximately20--30 pages of main content. Meeting a provisional paper count does not complete searching or the final deliverable. No additional intermediate-page requirement was supplied.

The five questions ask which mechanisms are evaluated (RQ1), how outcomes are measured and compared (RQ2), which operating conditions change results (RQ3), what trade-offs and gaps remain (RQ4), and what conditional choice is supported (RQ5). All five map to extraction and the claim register, rather than to an unconditional ranking of mechanisms.

\section{Protocol adoption and deviations}
The Group A execution copy adopts the submitted protocol. Amendment GA-A001 extends the cutoff from27 September to11 October2026. GA-A002 records the user's instruction that Codex conduct screening and quality appraisal as a single AI reviewer. There is no independent second reviewer, inter-rater agreement statistic or adjudicated human consensus. GA-A003 permits supplementary full-text work while unavailable database coverage remains open. GA-A004 records the actual public-interface execution and metadata capture in place of signed-in publisher exports. None changes the inclusion criteria to meet a target count.

Eligibility requires an English peer-reviewed original journal or full conference report, a local sharing/partition/process/API mechanism, explicit concurrent inference or justified mixed inference evidence, and sufficient configuration/outcome detail. Training-only, cluster-only, surveys and vendor claims are excluded from the primary set. Unretrieved reports are pending access outcomes, not assessed full-text rejections. Related conference, journal and preprint reports are one underlying study until an independent contribution is established.

\section{Search execution and provenance}
NED's E-Resources page lists the four planned publisher platforms. The listing was checked on11 October2026: \url{https://eaklibrary.neduet.edu.pk/eakl/E-Resources.html}. It confirms platform availability in the list, not entitlement to each requested article. No university credentials or licensed full-text PDFs enter this public repository.

\begin{longtable}{P{0.27\linewidth}P{0.38\linewidth}P{0.25\linewidth}}
\toprule Source/run & Actual implementation & Observed hits\\\midrule\endhead
IEEE MPS & All metadata; years2020--2026 &25\\
IEEE MIG & All metadata; years2020--2026 &23\\
IEEE temporal & All metadata; years2020--2026 &45\\
IEEE API & All metadata; years2020--2026 &9\\
Springer master & General search; English; research articles/conference papers;2020--2026 &587\\
ACM pilot & Search blocked by challenge loop &Unknown; no import\\
ScienceDirect pilot & Search page unavailable &Unknown; no import\\
\bottomrule
\end{longtable}
The common block is GPU or graphics-processing-unit AND inference, model serving, deep learning, DNN or LLM. IEEE uses one family block per run. Springer uses all family blocks in one OR group. Exact strings, filters, source URLs, dates and export limitations are in \texttt{search\_runs.csv}. The IEEE field implementation differs from the planned field-qualified Command Search and is disclosed, not described as an equivalent validated command. Research type/language and precise2026 cutoff checks are manual where facets are unavailable. No accepted study is dated after2025.

All30 Springer result pages (20 hits/page,7 on the final page) and all IEEE pages were captured, yielding587+25+23+45+9=689 occurrences. These are rendered-result metadata imports, not publisher-generated RIS/CSV exports. Springer export redirects to sign-in; IEEE results export requires personal sign-in and public citation export timed out. The imports retain IDs, database/run, page, title, DOI/URL and displayed date/item metadata. Clock time was not retained and is marked unrecorded.

Springer's broad index includes reference/full-text matches and unrelated acronym expansions such as welding MIG. Search hits therefore do not imply eligible GPU studies. Seed checks recovered ParvaGPU and KRISP in IEEE; papers in other publisher proceedings require supplementary discovery and completion of ACM coverage. Supplementary records are selected named-paper lookups checked after adoption, including submitted seeds and related systems. They are not an exhaustive search-engine result export or completed backward/forward citation search. Their follow-up query strings are reproducible suggestions, not invented historical exact queries.

\section{Screening checkpoint and reconciliation}
Every formal occurrence receives a record ID. Exact DOI/URL and normalized-title checks link duplicate occurrences without deleting provenance. Bibliographic report IDs identify candidate reports; study IDs identify accepted underlying studies. The pending REEF journal extension is linked to its conference study and cannot add another included study automatically.
'''
tex+=r'\begin{longtable}{P{0.7\linewidth}r}\toprule Checkpoint quantity & Count\\\midrule\endhead'+'\n'
for label,key in [('Formal query occurrences','formal_occurrences'),('Duplicate occurrences','formal_duplicates'),('Unique formal records','formal_unique'),('Selected supplementary records','supplementary_selected'),('Excluded before full text','excluded_before_fulltext'),('Full texts assessed','fulltext_assessed'),('Full-text exclusions','fulltext_excluded'),('Accepted unique studies','accepted_unique_studies'),('Pending / not retrieved','pending')]:tex+=tx(label)+' & '+str(C[key])+r'\\'+'\n'
tex+=r'''\bottomrule\end{longtable}
The reconciled captured subset is: 689-10+20=699 records; 699 equals pre-full-text exclusions plus assessed reports plus pending records. Assessed reports equal included reports plus full-text exclusions. Missing ACM/ScienceDirect populations are unknown and outside these arithmetic identities. This checkpoint is intentionally not a completed PRISMA2020 flow. Reports sought include pending retrieval attempts, but complete formal-database retrieval and final study-version resolution remain open.

Title decisions are first-pass relevance judgments, explicitly labelled as title stage. Abstract decisions cite publisher scope; full-text decisions identify a section or experiment. Training and inference are not interchangeable: PipeSwitch and SIRIUS are retained for explicit inference outcomes, whereas TGS is rejected for training-only evidence. The Fermilab paper was retained after its multi-model slice experiment was inspected, rather than merely because it mentioned MIG. DIPPM was rejected because profile prediction alone does not test concurrent tenant sharing.

Full-text rejection examples include DIPPM (no concurrent tenant comparison), the accelerator-pool vRAN simulation and the low-latency FEC offloading paper (no inference evidence), DRMaestro's Rodinia workload evaluation (no serving inference), CalcGraph (assigned GPU partitioning left to future work), and the mediated-device passthrough benchmark (HPC applications without inference). The complete reasons and stages are in \texttt{rejected.csv}. Pending files have no fabricated technical results or QA scores.

\section{Current accepted primary studies}
The following studies are accepted for this intermediate evidence set. Selection remains subject to access completion and checking more complete peer-reviewed versions. KRISP is a scope-boundary inclusion under protocol7.2 because it evaluates local spatial resource control and inference workers; its emulated AMD feature and non-NVIDIA baseline are explicitly isolated in synthesis. No vendor document or preprint-only unpublished work counts toward this table.
\begin{longtable}{P{0.15\linewidth}P{0.25\linewidth}P{0.4\linewidth}r}
\toprule Study & Report/year & Mechanism / scope & QA\\\midrule\endhead
'''
for s in S:tex+=tx(s['study_id'])+' & '+tx(s['key'].upper()+' '+str(s['year']))+r' \cite{'+s['key']+'} & '+tx(s['mechanism'])+' & '+str(sum(float(q['Q'+str(n)]) for q in csv.DictReader((E/'quality.csv').open()) if q['study_id']==s['study_id'] for n in range(1,11)))+r'\\'+'\n'
tex+=r'''\bottomrule\end{longtable}
USENIX proceedings PDFs are official published copies. ACM/IEEE author or camera-ready copies are linked to verified proceedings metadata and do not become separate preprint studies. ParvaGPU's author manuscript is provisional for publisher-version comparison; its reported runtime-version anomaly remains flagged. The REEF journal extension requires a completeness check. Accessible copies of Orion, GSLICE, KRISP, Tally and Paella avoid unnecessary institutional download requests.

\section{Quality appraisal and extraction controls}
Q1--Q10 cover tenant question, mechanism/configuration, environment, workload/arrivals, comparator fairness, metric clarity, measurement controls, result support, validity limits and reproducibility/interpretability. Scores are1 adequate,0.5 partial and0 absent; totals8--10 are high,6--7.5 moderate and below6 low. The single-reviewer scores, concise rationales and source anchors are in \texttt{quality.csv}. Scores assess reporting and interpretability; they do not prove unbiased results, system security, reproducible artifacts or complete searching.

The current totals are all at least8. Environment and measurement-control fields are frequently partial. No authors' experiments or code artifacts were rerun. Artifact availability alone is not experimental replication. The extraction register captures source/version, mechanism, hardware/runtime, tenant workload, comparator, a bounded finding, caveat and precise source location. Fields not yet fully transcribed are labelled NOT EXTRACTED, distinct from a source's not-reported value. A further detailed extraction pass is needed before final numerical comparisons.

Isolation observations remain four different columns: performance interference, resource/memory separation, adversarial security and fault containment. Most current findings establish workload performance rather than comparative security or fault containment. The KRYPTON fault experiment is specifically identified; it does not validate all mechanisms or all GPU generations.

\section{Provisional answers to the research questions}
\subsection{RQ1: mechanism and control boundaries}
The set contains temporal scheduling, MPS resource provisioning, MIG plus MPS, and API/runtime interception or remoting. Hybrids are counted as studies once, not once per mechanism. Software scheduling may control task admission, kernel dispatch, preemption or memory handover; these are different operating boundaries. A process-sharing prototype, a kernel-intercepted container and a hardware slice cannot be assigned the same security meaning. The detailed mapping is in \texttt{extraction.csv} and \texttt{claims.md}.

\subsection{RQ2: outcome definitions and comparability}
Keep requests/second, SLO-compliant goodput, allocated GPU count, GPU busy time, SM occupancy, memory utilization and paper-specific efficiency ratios separate. Likewise p95, p98, p99, average latency, time-to-first-token and time-between-tokens are not substitute measurements. A reduction in context-switch latency does not by itself establish p99 end-to-end latency isolation. Normalize only within an explicitly comparable experiment and retain the original denominator and statistic.

\begin{longtable}{P{0.27\linewidth}P{0.63\linewidth}}
\toprule Comparison check & Required condition before numerical comparison\\\midrule\endhead
Hardware & Same GPU/vendor/memory/profile or explicit indirect label; separate AMD emulation from NVIDIA mechanisms.\\
Workload & Same models/input sizes, batching, tenants and co-tenant mix; mixed training comparisons retain inference outcomes.\\
Load & Same open/closed-loop arrival process, rate, burstiness, warm-up and measurement window.\\
Comparator & Same resource budget; disclose reimplementations, wrappers and baseline adaptations.\\
Outcome & Same latency percentile/SLO and throughput denominator; occupancy and device-count reduction remain separate.\\
\bottomrule\end{longtable}

\subsection{RQ3: operating conditions}
Current evidence suggests that model memory demand, launch granularity, arrival burstiness, batching, priority mix and transfer path alter the sharing result. GPU generation constrains which resource boundaries are available. Local slice experiments are informative for memory pressure, while cluster scaling results require their own placement/network interpretation. Recommendation confidence falls when driver/runtime, quota/profile and experiment windows have not yet been completely transcribed.

\subsection{RQ4: trade-offs and counterevidence}
Stricter priority protection may trade lower-priority throughput for predictability. Remoting or swapping adds path-dependent transfer cost. Resource partitioning may reduce packing flexibility. Fine-grained control can require compiler changes, API interception, driver hooks or baseline adaptations. These implementation costs must accompany reported gains. The source-anchored counterexample and parameter-specific results reside in the extraction register, avoiding an invented common percentage improvement across studies.

\subsection{RQ5: conditional engineering choices}
The following are provisional reviewer interpretations, not validated deployment instructions.
\begin{longtable}{P{0.28\linewidth}P{0.35\linewidth}P{0.27\linewidth}}
\toprule Operating objective & Candidate to investigate & Evidence / unresolved condition\\\midrule\endhead
Priority-sensitive inference & Temporal/API scheduling with admission and memory controls &GA-S001,003,004,008,009,011,014; direct per-paper tests, indirect transfer.\\
Density with controlled workload mix & Tuned MPS provisioning &GA-S002,012; check memory/compute contention and reconfiguration cost.\\
Slice boundary with concurrent models & MIG, optionally MPS inside a slice &GA-S010,016; profile, packing and memory pressure; no universal isolation result.\\
Serverless remoting and elasticity & API remoting/runtime virtualization &GA-S005,006,007; runtime compatibility and transport budget.\\
Strong adversarial/fault guarantee & No universal selection supported &Comparative evidence insufficient; retrieve security candidates and distinguish failure types.\\
\bottomrule\end{longtable}

\section{Sensitivity, limitations and continuation}
Removing QA<6 removes no current study, so that sensitivity test is uninformative. Removing provisional author-manuscript evidence weakens hybrid MIG and the recorded negative throughput comparison. Excluding AMD-only feature evidence limits cross-vendor conclusions. Removing all incompletely transcribed environment profiles would sharply reduce evidence; final recommendations require completing those fields. No pooled effect or universal winner is asserted.

The main limitations are incomplete ACM/ScienceDirect searches, single-AI-reviewer bias, inaccessible full texts, supplementary-selection bias, baseline and hardware heterogeneity, incomplete parameter extraction and unresolved report versions. The accessible set is concentrated in systems proceedings and older DNN workloads; LLM and adversarial isolation evidence requires further checking. A minimum paper count cannot offset these limitations.

Next, obtain the prioritized publisher PDFs and blocked database exports, log their receipt and version, apply the same full-text criteria, complete extraction and rerun counts/claims/sensitivity. Link any new report to its underlying study before adding a citation. Exact2026 dates must be verified. Scope changes still require a documented amendment and instructor guidance; this report does not relax eligibility.

\section{Evidence package and institutional requests}
The evidence directory supplies search runs, imported records, duplicates, all decisions and reasons, accepted/rejected/pending views, retrieval lookups, QA, extraction, claims and checkpoint counts. \texttt{references.bib} contains only the16 currently chosen primary reports, each cited here. The spreadsheet is a review view; CSV/JSON records remain the authority. Scripts validate linkage and reconciliation and regenerate derived views.

The full unresolved link queue is in \texttt{download\_requests.csv}; \texttt{download\_requests.md} lists at most 10 requested papers; other unresolved entries are deferred and are not requests. All requested publisher platforms appear on NED's list, but article-level access must be checked using university access. PDFs should be supplied privately through the conversation, not committed to the public repository. Query exports must preserve exact syntax, collection, facets and counts; sending papers alone does not repair incomplete systematic search coverage.

\bibliographystyle{IEEEtran}\bibliography{query_references}
\end{document}
'''
findings=r'\Needspace{16\baselineskip}\subsection{Source-anchored finding register}\begin{longtable}{P{0.18\linewidth}P{0.48\linewidth}P{0.24\linewidth}}\toprule Study & Bounded finding & Source location\\\midrule\endhead'+'\n'
for s in S:
    findings+=tx(s['study_id'])+r' \cite{'+s['key']+'} & '+tx(s['finding'])+' & '+tx(s['anchor'])+r'\\'+'\n'
findings+=r'\bottomrule\end{longtable}'+'\n'
tex=tex.replace(r'\section{Quality appraisal and extraction controls}',findings+r'\section{Quality appraisal and extraction controls}')
tex=tex.replace('Sixteen distinct peer-reviewed studies','Twenty-one distinct peer-reviewed studies')
tex=tex.replace('The pending REEF journal extension is linked to its conference study and cannot add another included study automatically.', 'The REEF journal extension is selected for GA-S001; its less complete conference report is a linked E8 companion and adds no study.')
tex=tex.replace('The REEF journal extension requires a completeness check.', 'The supplied REEF journal conversion establishes a more complete implementation/evaluation; it is now the preferred report for GA-S001. The conference report is retained as a linked companion.')
tex=tex.replace('The current totals are all at least8.', 'Current totals range from6.5 to9.0. Four newly included studies score below8; their configuration or measurement controls and missing plot data require caution.')
tex=tex.replace('only the16 currently chosen primary reports','only the21 currently chosen primary reports')
tex=tex.replace('Next, obtain the prioritized publisher PDFs and blocked database exports, log their receipt and version, apply the same full-text criteria, complete extraction and rerun counts/claims/sensitivity.', 'Next, continue public-access recovery and available database exports, complete parameter extraction and rerun claims/sensitivity. The user supplied six of the ten requested papers; all six are assessed. The remaining four are unavailable and no further paper download is requested.')
tex=tex.replace(r'The full unresolved link queue is in \texttt{download\_requests.csv}; \texttt{download\_requests.md} lists at most 10 requested papers; other unresolved entries are deferred and are not requests.', r'The unresolved access backlog is in \texttt{download\_requests.csv}; there are zero active requests. \texttt{download\_requests.md} records the six received conversions and four unavailable original requests. No additional paper download is requested.')
update=r'''\section{Review of six supplied full texts}
Five reports add unique studies: VastPipe, ArkGPU, Dyna-P, iGniter and InferFair. REEF's journal report explicitly extends OSDI2022 with a complete NVIDIA implementation, additional kernel handling and newer comparisons; the journal is preferred within GA-S001. Six previously pending reports are now assessed; the earlier conference report becomes a full-text E8 companion. There are21 accepted studies,28 assessed reports including7 full-text exclusions, and96 pending access cases. Search occurrence and discovery counts are unchanged.

The source files are Markdown conversions. Two-column interleaving, missing plot pixels and damaged mathematical symbols prevent exact extraction of some equations, CDFs, error bars and configurations. Only readable labelled tables, captions and explicitly stated numeric results enter the register. Missing values are not interpolated. The receipt ledger records filenames and SHA-256 hashes; licensed source contents are not published.

Local GPU strata determine inclusion. VastPipe's NPU-cluster outcomes, ArkGPU's four-GPU goodput, Dyna-P's multi-GPU aggregates and cluster simulation, iGniter's fleet cost, and InferFair's four-GPU trace are distinguished from local results. ArkGPU qualifies through the explicit mixed inference/training exception; transfer is limited to priority inference protection. Dyna-P's job completion and makespan do not establish online p99. InferFair's unfairness is a relative slowdown ratio and does not establish adversarial isolation.

Journal REEF's same-engine GV100 PyTorch comparison reports DISB-C p99 below1.05 times solo versus1.17 for Orion, alongside separately normalized total throughput. Its TensorRT comparison also reports lower mean normalized throughput than Triton; preserving this counterexample prevents a universal superiority claim. iGniter's initial p99 violation followed by shadow-process correction likewise qualifies any steady-state SLO statement. Source locations and QA rationales are recorded per report.

At the stricter QA threshold8, VastPipe, ArkGPU, Dyna-P and InferFair are omitted; their mechanism-specific conclusions weaken. At the protocol low-quality threshold6, none is omitted. This is a reporting-quality sensitivity, not a pooled causal result. The set now exceeds the protocol's15--20-study target range; retain all eligible studies at this checkpoint and document any final narrowing transparently rather than removing evidence to fit a count.

'''
tex=tex.replace(r'\section{Quality appraisal and extraction controls}',update+r'\section{Quality appraisal and extraction controls}')
# Improve ordinary prose spacing and allow breaks in study-ID lists.
tex=re.sub(r'(?<=[a-z])(?=\d)', ' ', tex)
tex=tex.replace('S001,003,004,008,009,011,014','S001, S003, S004, S008, S009, S011, S014')
tex=re.sub(r'(S\d{3}),',r'\1, ',tex)
(R/'query_report.tex').write_text(tex)
# Compact workbook source; separate fields remain in CSV for reproducible processing.
book={
'Summary':[['Group A evidence checkpoint','2026-10-11'],['Status','Intermediate; incomplete search coverage'],['Formal occurrences',C['formal_occurrences']],['Formal duplicates',C['formal_duplicates']],['Selected supplementary',C['supplementary_selected']],['Pre-full-text exclusions',C['excluded_before_fulltext']],['Assessed reports',C['fulltext_assessed']],['Pending retrieval',C['pending']],['Accepted studies',C['accepted_unique_studies']],['Full-text exclusions',C['fulltext_excluded']],['Record reconciliation',None],['Assessment reconciliation',None]],
'Decisions':[['Record','Report','Study','Title','Decision','Stage','Code','Reason','Source','Run','Access','URL']]+[[r[k] for k in ['record_id','report_id','study_id','title','decision','stage','reason_code','reason','database','run_id','access','url']] for r in rows],
'Included':[['Study','Paper','Mechanism','Source','Anchor','Finding','Caveat']]+[[s[k] for k in ['study_id','key','mechanism','fulltext_url','anchor','finding','limitation']] for s in S],
'Quality':[['Study']+[f'Q{n}' for n in range(1,11)]+['Total','Band','Anchor']]+[[q['study_id']]+[float(q[f'Q{n}']) for n in range(1,11)]+[float(q['total']),q['band'],q['anchor']] for q in csv.DictReader((E/'quality.csv').open())],
'Downloads':[['Priority','Record','Title','Platform','URL','Entitlement']]+[[r[k] for k in ['priority','record_id','title','platform','url','individual_entitlement']] for r in requests],
'Searches':[['Run','Source','Date','Status','Hits','Imported','Query','Filters']]+[[r[k] for k in ['run_id','database','date','status','hits','imported_occurrences','query','filters']] for r in runs]}
receipt=list(csv.DictReader((E/'uploaded_paper_receipts.csv').open()))
book['Received']=[['Record','Study','Filename','Decision','QA','Source SHA256']]+[[r[k] for k in ['record_id','study_id','filename','decision','qa_total','sha256']] for r in receipt]
(E/'workbook_source.json').write_text(json.dumps(book,ensure_ascii=False))
print('Report and supporting documentation generated; counts',C)
