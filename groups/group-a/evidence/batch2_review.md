# Batch 2 full-text review — 17 October 2026

Single reviewer AI-CODEX; 11 full reports assessed, three accepted and eight excluded. No full-paper bodies committed. The historical Flow A is a separate dated checkpoint.

## GA-N00920 — N00920.md

Include: original HPDC full paper evaluates concurrent inference functions with local MIG partitioning and request SLO outcomes; separate server-level from local mechanism claims.

Anchor: N00920.md abstract, sections 3, 6, 7.1; Tables 2, 5–6; Figs. 9 and 12

SHA-256: 200bfa689fceed161581e292ea63991073594a21027303d772bb2748ca7db16f

## GA-N01085 — N01085.md

Include: original EuroSys full paper explicitly evaluates co-located inference instances with an implemented single-A100 temporal/MPS hybrid.

Anchor: N01085.md intro, sections 4, 6.1–6; Fig. 1 and BERT co-location result prose

SHA-256: 0e62afeeff01ba125900294c709e5b6f77bddbbaf2f560149579a724ba16e9df

## GA-N01096 — N01096.md

Include as direct interference/isolation evidence: real single-GPU LLM inference is concurrently run with a distinct synthetic process/kernel under streams and Green Context SM partition; a mixed co-tenant experiment is explicitly bounded, with no claim of two production inference services.

Anchor: N01096.md sections 3–5, especially 4.1–4.4; Fig. 2 and Table 1

SHA-256: 76fca8fc31f23603170a57e7f536e90ebe4811351931ece9945ee4d015b8f3cb

## GA-N00002 — N00002.md

E2: Cricket/unikernel CUDA remoting is evaluated with microbenchmarks and proxy applications across two nodes, without a concurrent inference-tenant GPU comparison. The JetsonInference library appears in related work, not the evaluated setting.

Anchor: Section 4 evaluation setup and benchmarks; section 2 related work

SHA-256: 73c74ea3eac76bdae0799ff8882142432be7693924420d07b4bc3e795fedebe7

## GA-N00004 — N00004.md

E1: AWS Lambda/rCUDA case study compares CPU, native GPU and remote GPU for a single GPU-BLAST processing path; AI inference is motivation, without measured inference-serving outcomes for concurrent tenants.

Anchor: Case study scenarios 1–3 and Figs. 5–6; introduction

SHA-256: 216df7d8e6fb5b3e76e4b37d4637787efb6a00949d7598bdf3c8028ba4e88505

## GA-N00055 — N00055.md

E4: nvshare's measured co-located TensorFlow ResNet152v2 applications train models; the authors explicitly select training-only evaluation although inference is mentioned as background.

Anchor: Section 4 evaluation methodology and Table 1

SHA-256: 7598275b755aa109cca6f373d50f2a0b7c39270446fb18bfe183047640d6d777

## GA-N00088 — N00088.md

E1: GPUPool evaluates throughput-oriented long jobs and simulated kernel pairs; inference appears as a motivating workload class/reference, without an inference-specific measured serving outcome.

Anchor: Sections 2 and 4–5, especially workload/QoS scope and GPGPU-Sim methodology

SHA-256: 623d8a0da89be3d6c2898e6fe2e1b18ceea3d1c5b9ba2d95328d02351cb59e3c

## GA-N00102 — N00102.md

E2: Guardian's multi-application spatial-sharing comparison uses epoch-based training/co-run workloads (Table 2, Fig. 6); inference phases are tested standalone for overhead (Fig. 7b). There is no evaluated concurrent inference-serving arrangement under the adopted criterion.

Anchor: Section 7.1–7.2, Table 2 and Figs. 6–8

SHA-256: 816b711bb21de3bef29ffb7b14fc32cd6554d7632a3f10d615c1c38fe6606242

## GA-N01195 — N01195.md

E2: ReFINE evaluates synthetic priority kernel pairs in Accel-Sim architectural simulation rather than a measured concurrent inference arrangement on one physical GPU; inference serving is an illustrative motivation.

Anchor: Abstract, evaluation methodology/Accel-Sim and section 5

SHA-256: 4bfa4724442c738a940170e91903cafa4d5df8fb7034d496de5ad84bbe790e00

## GA-N01866 — N01866.md

E1: Edge-device rCUDA evaluation runs the Fuzzy Minimals clustering algorithm across remote node/GPU settings; no inference-serving workload or outcome is evaluated.

Anchor: Introduction contributions, experimental environment and Fuzzy Minimals evaluation

SHA-256: 6e7c34027d40ae4893b47cb48131faa8373f0668f948c8ca755c9d4ab7bacbe2

## GA-N01945 — N01945.md

E1: MIG scheduling and reconfiguration evaluates Rodinia/Altis benchmarks and synthetic task queues for makespan; inference latency is that of the DRL scheduler itself, not a model-serving tenant outcome.

Anchor: Abstract, section 5 workload setup and section 6.1 scheduler-inference timing

SHA-256: df47b1f2ca455847e530313586a57a9be21ba78d6c50c55047fa3830ddef99e4
