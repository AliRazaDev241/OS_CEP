# Group A — provisional claim and RQ matrix

All recommendations are reviewer interpretations of heterogeneous published experiments, not deployments validated by this group. The full-text set is current, not a final systematic selection. No pooled numerical effect is calculated.

| ID / RQ | Provisional interpretation | Primary support | Counterevidence / condition | Strength |
|---|---|---|---|---|
| C1 / RQ1,3 | Temporal scheduling is a candidate for priority inference when co-tenant work can be controlled. | GA-S001,003,004,008,014,015; extraction anchors | Memory handover, context and runtime differ; no universal bound | Direct within each study; indirect across studies |
| C2 / RQ1,3 | MPS provisioning can support density goals, with workload-specific tuning. | GA-S002,012,017,020 | Loading/reconfiguration and interference matter; density is not security | Direct within study; conditional interpretation |
| C3 / RQ1,3 | MIG and MPS can be combined; slice memory pressure must be checked. | GA-S010,016,019 | Parva author manuscript; Fermilab local-slice evidence only | Direct within each study; indirect comparison |
| C4 / RQ2 | Goodput, throughput, busy time, GUE and occupancy require distinct columns. | GA-S004,005,010,012 | Different denominators and percentiles prevent raw pooling | Measurement interpretation |
| C5 / RQ4 | Protecting priority latency can reduce lower-priority throughput. | GA-S009 section5.3 Fig6 | Tally does not dominate TGS on BE throughput in that stratum | Direct counterexample |
| C6 / RQ4,5 | API remoting is a candidate when transfer costs fit the SLO budget. | GA-S005,006,007,009,011 | PCIe/NVLink path, runtime compatibility, process boundary and scheduler overhead | Conditional, indirect across systems |
| C7 / RQ1,4,5 | Performance protection does not establish security or fault containment. | GA-S007 section2.2; all isolation columns | Most extracted results do not test adversarial isolation; GhostWriter remains inaccessible, with no further user download requested | Insufficient comparative security evidence |

RQ-to-final-output: RQ1 → mechanism/control boundary taxonomy; RQ2 → definitions and comparability table; RQ3 → hardware/workload/configuration strata; RQ4 → trade-offs/counterexamples/operating cost; RQ5 → conditional decision matrix. Required field groups are preserved in extraction.csv; untranscribed parameters are explicitly NOT EXTRACTED rather than marked absent in the paper.

Sensitivity: all current QA totals are at least6.5, so dropping QA<6 removes none and provides no discriminating test. Removing author-manuscript ParvaGPU and Tally weakens the hybrid MIG and negative-throughput evidence. Removing AMD-only KRISP and the main AMD REEF stratum leaves NVIDIA temporal/API/MPS evidence but does not validate AMD-to-NVIDIA transfer. Dropping incomplete environment profiles would remove much of the set; current recommendations are therefore provisional. Do not convert a high rubric total into high causal confidence or complete search coverage.

Next extraction pass: finish driver/runtime versions, MIG profile names, MPS quotas, batching, exact arrival rates, warm-up/windows/variance and measured-vs-claimed isolation fields before final recommendations. Check all newer/related reports and repeat synthesis after resolving the access queue. No experiments or code artifacts have been rerun.


Six-paper update: GA-S017 VastPipe supplies local A100 MPS and separate MI100 CU-mask throughput strata; its 1000-NPU cluster results are outside the local GPU comparison. GA-S018 ArkGPU supplies mixed inference/training p99/QPS evidence; its four-GPU goodput gains are separate. GA-S019 Dyna-P supplies local MIG inference-job results and a concurrency/JCT trade-off; cluster simulations and makespan are not online p99 measurements. GA-S020 iGniter supplies local MPS interference and transient p99 failure/recovery evidence; fleet cost savings are not local utilization. GA-S021 InferFair supplies local fairness/SLO goodput with distinct unfairness definition. Updated GA-S001 journal REEF supplies NVIDIA comparisons and a throughput cost of latency protection; the OSDI report is a linked E8 companion, never an additional study.

Reporting sensitivity: the four newly included moderate-QA studies (VastPipe6.5, ArkGPU7, Dyna-P7, InferFair7.5) are removed by a stricter QA>=8 sensitivity stratum; iGniter and journal REEF score8.5. Removing these moderate rows weakens dynamic-MIG placement, API-throttled inference/training and relative-goodput fairness evidence. QA<6 removes none. Scores do not resolve missing full-text plot data. No universal or pooled percentage improvement is defensible.


## Batch 1 — current 31-study evidence (17 October 2026)

Source anchors and separate isolation fields are in `batch1_extraction.csv` / `current_extraction.csv`; quality rationales are in their matching QA registers. New single-reviewer accepted studies: GA-S022 MIGER, S023 Deft, S024 FaST-GShare, S025 SPLIT, S026 MIGServe, S027 MMK, S028 BOER, S029 AdMix, S030 SGDRC, S031 EnerTune. Distinct experiments are not pooled.

- RQ1/3: Hybrid MIG/MPS design is not a guarantee of low interference. MIGER's mixed training/inference, MMK's extra kernel control and BOER's inference-only grouping have different workloads and objectives. BOER section 2.4 gives a local adverse case for identical-model hybrid packing.
- RQ2/3: Deft's JCT inflation, SPLIT's block-time jitter, FaST-GShare's unspecified tail percentile, MIGServe's 90%-attainment request rate and AdMix's mean TTFT/TPOT are different outcomes. Do not rank their raw values together. AdMix TP1 local evidence is separate from TP2; MIGServe rates are four-GPU server outcomes.
- RQ4/5: SGDRC section 10 explicitly does not isolate shared-context GPU runtime errors. Software resource interference control and MIG boundary descriptions do not establish adversarial security.
- RQ4/5: EnerTune's local pair-energy example can favor a different colocation than utilization-only placement; fleet energy/power savings are a separate experiment. AdMix can improve BE throughput while increasing protected LLM mean latency relative to solo execution.
- Sensitivity: Removing all moderate QA reports drops Deft/FaST-GShare plus the previous four, leaving 25 high-scored studies. This weakens synchronization and serverless conclusions. Low-QA exclusion removes none and is non-discriminating. New QA does not resolve incomplete measurements, missing figures or unintegrated searches.

Ten assessed additions do not complete the combined PRISMA flow. Pantheon/Jormungandr remain preliminary and the other 66 download-queue reports remain candidates.

## Batch 2 — current 34-study evidence (17 October 2026)

Eleven more received reports yielded GA-S032 FluidFaaS, GA-S033 Bless and GA-S034 Understanding GPU Resource Interference One Level Deeper; eight were excluded with full-text reasons. QA/extraction and citations are in the batch-2 and current registers; the older batch-1 paragraph above is a dated checkpoint.

- RQ1/3: FluidFaaS evaluates MIG-based function pipelines, while Bless uses MPS/SM-affinity and temporal kernel squads on one A100. Their system-level SLO rates and single-GPU inference latency are different strata.
- RQ2/4: The SoCC interference study measures LLM P90 time between tokens with synthetic co-tenants. Green Context SM separation leaves L2 and memory bandwidth shared; its isolated whole-GPU and partitioned comparisons have different resource budgets.
- RQ4/5: Guardian's co-located training experiments plus standalone inference overhead do not provide a concurrent inference-serving evaluation under protocol 7.2. Its memory-safety design remains context, outside the included set.
- Sensitivity: All three additions score 8/10. Removing the six moderate studies leaves 28 high-scored studies; it does not remove these three or settle the 55 unassessed queue reports and two earlier eligible-pending-integration cases.
