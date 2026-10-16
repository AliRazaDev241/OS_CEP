# Batch 1 full-text review — 17 October 2026

Single reviewer: AI-CODEX. Ten supplied Markdown conversions were read for eligibility, original Q1–Q10 appraisal, and source-anchored extraction. Source bodies remain private; only metadata, SHA-256 receipts, scores and paraphrases are committed.

Current accepted set: 31 unique studies (21 historical + 10 new). The extension full-text register contains 12 assessed reports: 10 accepted here and 2 earlier eligible-pending-integration reports. The supplied 76-entry download queue has 10 received and 66 unassessed. These are not a completed PRISMA flow.

The historical Flow A registers remain reproducible. Current combined accepted/quality/extraction registers use the `current_` prefix; extension decisions remain in `new_fulltext_assessments.csv`. Do not add 10 to the historical Flow A PRISMA boxes.

## GA-S022 — miger

Include under protocol 7.2 mixed-workload transfer: local assigned MPS/MIG comparisons and explicit online inference latency/QoS; cluster title does not displace the local evidence.

DOI: 10.1145/3673038.3673089. Publication basis: 2024-08-12/2024-08-15 (conference). QA: 8/10.

Section 3.1/Fig. 2 directly compares local MPS 57/29/14 percent and MIG 4g/2g/1g allocations. Section 5.2/Fig. 8 reports testbed mean JCT 46.6% below MuxFlow and 36% below MISO; these are job/cluster outcomes, not inference p99 gains. Fig. 9 notes slower small jobs under MIGER.

Includes mixed training/inference and multi-GPU optimization; retain only explicitly local sharing and inference-QoS evidence for assigned comparison. Abstract and introduction swap comparator order for the two JCT percentages; use section 5.2 mapping. No chart coordinates reconstructed or universal p99 claim.

Anchor: Printed pp. 505-506, 510-511; sections 3.1-3.3, 5.1-5.4; Tables 1-3; Figs. 2, 4, 8-11; N00001.md lines 119-229, 478-662

## GA-S023 — deft

Include: full original workshop proceedings paper with implemented local two-inference-job preemption and workload-dependent JCT/SLO evidence, not a poster or abstract.

DOI: 10.1145/3631311.3632401. Publication basis: 2023-12-11/2023-12-15 conference; export publication year 2024; printed reference says 2023. QA: 7/10.

Sections 3.2 and 5 show optimal synchronization depends on batch and image size; the fixed strategy can impose much larger preempting-job JCT inflation after a workload change. Section 5.2 reports Deft switches to synchronizing every kernel for batch 30; earlier batch-1 case uses every 500 kernels. Table 2 cells are interleaved, so no exact violation-rate row is imported.

Preliminary six-page workshop evaluation with two principal models and one A40. Exhaustive pair profiling does not scale; no cluster/generative-model implementation claimed (section 6). Keep export year 2024 and printed conference/reference year 2023 separately; both inside window.

Anchor: Printed pp. 15-17; sections 3.2, 4.2, 5.1-5.3 and 6; Table 2 and Fig. 4 discussed in prose; N00005.md lines 250-468

## GA-S024 — fastgshare

Include: implemented per-GPU MPS/time-quota mechanism with multiple concurrent inference pods and explicit throughput, tail-latency and occupancy outcomes.

DOI: 10.1145/3605573.3605638. Publication basis: 2023-08-07/2023-08-10 (conference). QA: 7.5/10.

Local section 5.3 states eight RNNT pods at 12% SM shares reach about 40 req/s with tail latency below 500 ms, versus one racing pod about 12 req/s and above 1250 ms. The local ResNet/RNNT comparison in Fig. 9 reports removing their observed interference with 24% shares. No unlabelled tail value is relabelled p99.

Model-specific/proportional share effects, IPC memory trust and batching limit transfer. Prose fractional-gain notation is ambiguous (3.15x with raw 296.8/71.37), so no such multiplier imported. Supplied plot coordinates/percentile identity and repetitions not reconstructed.

Anchor: Printed pp. 641-643; sections 4, 5.1-5.4; Figs. 8-10; N00015.md lines 523-735

## GA-S025 — split

Include: multi-model inference on one physical GPU, directly evaluated temporal preemption and per-request QoS evidence.

DOI: 10.1145/3605573.3605627. Publication basis: 2023-08-07/2023-08-10 (conference). QA: 8.5/10.

Section 5.5 reports violation rate below 10% beyond alpha=4 versus 26% under RT-A in the discussed comparison. For short requests, jitter reductions versus Clockwork/PREMA/RT-A are 55.3/46.8/68.9% at low load and 56.0/50.3/69.3% at high load. Jitter is block-execution standard deviation, not p99 latency. Section 6 reports split overhead and static-graph limits.

One edge GPU and synthetic Poisson load; not a server-class GPU generalization. Temporal predictability sacrifices spatial parallelism; long-request stability can worsen. Table 3 split overhead and RNN limits qualify short-request improvements.

Anchor: Printed pp. 611-613; sections 5.1-5.5, 6; Tables 1-3; Figs. 6-7; N00040.md lines 451-629

## GA-S026 — migserve

Include: single-node physical-GPU MIG control with local partition/layout evidence and concurrent model serving; multi-GPU request-rate results retained as separate system stratum.

DOI: 10.1145/3832810.3832898. Publication basis: 2026-09-28/2026-10-01 (conference). QA: 8/10.

Section 5.2 Azure: sustainable rate at 90% SLO attainment is 9.84 RPS versus LA-Dyn 4.13 and Static 1.85. Arena approximately 10.99 versus 2.37 and 2.48 RPS. These are four-GPU server outcomes; local mechanism is MIG layout control, not a single-GPU throughput multiplier.

Four-GPU evaluation and constructed layout-agnostic comparator; 90% attainment is weaker than 99% SLO targets used elsewhere. MIG hardware isolation is described, without adversarial/fault experiment. Source pixels and unreported repeats/versions are not reconstructed.

Anchor: Printed pp. 850-853; sections 4, 5.1-5.4; Fig. 9 and Figs. 11-13; N00831.md lines 519-780

## GA-S027 — mmk

Include under mixed-workload transfer rule: per-GPU MIG/MPS/kernel control and explicitly inference-labelled QoS workloads, distinct from cluster-only scheduling.

DOI: 10.1145/3820163. Publication basis: July 2026 (printed issue publication date). QA: 8/10.

Section 4.3/Fig. 9 reports mean JCT 28% lower, makespan 32% lower and normalized progress-rate STP 35% higher than MIGER. These are mixed-job/testbed metrics, not per-request p99 latency. Section 4.5 reports 1.5% MIG and 3.2% MPS reconfiguration lifecycle overhead.

Mixed inference/training and two-GPU optimization; local priority scheduling is the transferable mechanism. Many figure labels contain NUL/glyph corruption, so numerical prose only. STP/JCT does not establish online tail-latency or fault containment.

Anchor: Article pp. 84:15-84:19; sections 4.1-4.5; Table 3; Figs. 9-12; N00839.md lines 789-1040

## GA-S028 — boer

Include: explicit local MPS/MIG concurrent inference comparison and hybrid configuration mechanism; evaluate system-level gains in their own eight-GPU stratum.

DOI: 10.1145/3712285.3759857. Publication basis: 2025-11-16/2025-11-21 (conference). QA: 8.5/10.

Local section 2.4/Fig. 3 observes ParvaGPU can underperform MIG-only serving for larger BERT/ResNet50 while helping lightweight MobileNet. Section 5.2/Fig. 8 gives eight-GPU QoS-preserved throughput mean 34.61% above ParvaGPU; 56.8/62.49/34.63/44.83% above MIG-serving/gpulet/USHER/PARIS. Keep local qualitative counterexample separate from fleet improvements.

Bayesian exploration cost and instance interference qualify hybrid gains. Baseline reductions (MIG-serving fast/USHER IR only) and multi-GPU request fan-out constrain comparison. Same senior author as MIGER, but different inference-only system and experiments; not a same-study report extension identified in supplied text.

Anchor: Printed pp. 521, 526-528; sections 2.4, 4.6, 5.1-5.4; Tables 2-3; Figs. 3, 8, 10; N00844.md lines 200-265, 700-890

## GA-S029 — admix

Include: original full workshop proceedings evaluation with two inference workloads sharing a local GPU in TP1; TP2 results retained separately. Not a poster or abstract.

DOI: 10.1145/3816891.3834895. Publication basis: 2026-09-28/2026-10-01 conference; ACM indexed publication 2026-09-27. QA: 8.5/10.

Section 4.2 reports average best-effort throughput 1.58x Static MPS with local LLaMA-7B (TP1) and 3.9x with Qwen-14B (TP2), keeping strata distinct. AdMix still increases mean TTFT/TPOT versus LLM-only; on Qwen its mean latency increases exceed Static MPS. More throughput is not zero interference.

Full six-page original workshop report; one/two-GPU workload strata and tuned-on-test-trace static reference limit transfer. Estimates of average latency do not establish p99. No testbed code rerun or security/fault experiment inferred.

Anchor: Printed pp. 3-5; sections 3 and 4.1-4.2; Table 1; Figs. 5-6; N00872.md lines 270-453

## GA-S030 — sgdrc

Include: concurrent latency-sensitive and best-effort inference on each physical GPU, software allocation/virtualization and MPS/temporal comparators provide assigned-scope evidence.

DOI: 10.1145/3710848.3710863. Publication basis: 2025-03-01/2025-03-05 (conference). QA: 8.5/10.

Section 9.3: versus Orion, P40 overall throughput up to 1.47x and BE up to 2.36x; A2000 up to 1.32x and 1.79x, respectively. Mean SLO attainment 99.0% across evaluated settings. Section 10 explicitly states shared-context GPU runtime errors are not isolated.

Software coloring is not a proven security boundary. MIG integration is future work; not benchmarked on A100/H100. Reverse-engineering/calibration and TVM compatibility matter; do not treat throughput maxima as averages or infer a P40 MPS result.

Anchor: Printed pp. 276-277; sections 9.2-9.3, 10; Table 3 and Fig. 18; N00904.md lines 863-965

## GA-S031 — enertune

Include: local GPU multiplexing and explicit model-pair energy/latency experiments support assigned utilization/latency trade-offs; fleet optimization retained as separate context.

DOI: 10.1145/3830418.3843913. Publication basis: 2026-09-29/2026-10-02 conference; ACM indexed publication 2026-09-28. QA: 9/10.

Section 2.1/Fig. 2: co-location choice can increase energy; SDXL plus MobileNetV3 example uses 13% less energy versus no sharing despite 1.14x latency. Section 7.1/Fig. 9: 16-GPU testbed energy reduced by factors 1.4-2.3 and power by 1.3-2.6 versus baselines while meeting SLOs; fleet results are not local per-GPU savings.

Joint power/energy objectives select different allocations. Local model-pair evidence must stay distinct from fleet savings and from frequency-only effects. Source chart pixels not available; experiments/code not rerun; missing warm-up and independent-run uncertainty not assumed.

Anchor: Printed pp. 66-67, 73-75; sections 2.1-2.2, 6, 7.1-7.2; Figs. 2, 9; N00946.md lines 140-249, 798-995
