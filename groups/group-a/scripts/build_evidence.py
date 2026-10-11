"""Rebuild derived registers from captured metadata and recorded reviewer assessments.

This script does not perform searches, assess eligibility, or infer missing evidence.
The title triage allow-list and explicit overrides below record the single reviewer's
assessment of the captured title list. Uncertain titles stay pending.
"""
import csv, json, re, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
E = ROOT / 'evidence'
DATE = '2026-10-11'
def write(name, rows):
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with (E/name).open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
def study(key,title,authors,year,venue,pages,doi,url,pdf,family,hardware,workload,baseline,outcome,caveat,anchor,scores,formal=0):
    return dict(key=key,title=title,authors=authors,year=year,venue=venue,pages=pages,doi=doi,publisher_url=url,fulltext_url=pdf,mechanism=family,environment=hardware,workload=workload,comparator=baseline,finding=outcome,limitation=caveat,anchor=anchor,scores=scores,formal=formal)
S=[
study('reef','Microsecond-scale Preemption for Concurrent GPU-accelerated DNN Inferences','Mingcong Han and Hanze Zhang and Rong Chen and Haibo Chen',2022,'USENIX OSDI','539--558','','https://www.usenix.org/conference/osdi22/presentation/han','https://www.usenix.org/system/files/osdi22-han.pdf','Temporal preemption','MI50 16GB; Ubuntu18.04; ROCm4.3; TVM0.8; limited V100/CUDA10.2 check','Five DNNs; RT Poisson/uniform 20req/s; saturated BE','Sequential; streams; prior schedulers','DISB-A: RT overhead 0.5% vs RT-only; throughput 1.60x sequential.','Main platform AMD; TOCS extension awaits version assessment.','PDF pp11-12; sections7.1-7.2; Fig11',[1,1,.5,1,.5,1,.5,1,.5,1]),
study('gpulet','Serving Heterogeneous Machine Learning Models on Multi-GPU Servers with Spatio-Temporal Sharing','Seungbeom Choi and Sunho Lee and Yeonjae Kim and Jongse Park and Youngjin Kwon and Jaehyuk Huh',2022,'USENIX ATC','199--216','','https://www.usenix.org/conference/atc22/presentation/choi-seungbeom','https://www.usenix.org/system/files/atc22-choi-seungbeom.pdf','MPS + temporal','RTX2080Ti 11GB; two/server; Ubuntu18.04; CUDA10.2; driver440.64; PyTorch1.10','Nine models; Poisson arrivals; per-model SLO','Adapted SBP/Nexus; best-fit with/without interference','Local gpulets support interference-aware provisioning; cluster throughput is a different outcome.','Server-level gains cannot be treated as one-GPU utilization.','PDF p10 Table2/3; section5; local profiling section3',[1,1,1,1,.5,1,.5,1,.5,1]),
study('pipeswitch','PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications','Zhihao Bai and Zhen Zhang and Yibo Zhu and Xin Jin',2020,'USENIX OSDI','499--514','','https://www.usenix.org/conference/osdi20/presentation/bai','https://www.usenix.org/system/files/osdi20-bai.pdf','Temporal context switching','V10016GB or T416GB EC2; PyTorch1.3; CUDA10.1','Training batch32; inference8; RN152/InceptionV3/BERT; 100 runs','Unoptimized/grouped/per-layer transfer','Fig7: inference preemption latency reduced by up to 38.2ms.','Average switch/inference latency is not p99; multi-VM throughput separate.','PDF pp11-13; sections6-6.2; Fig7',[1,1,.5,1,1,1,1,1,.5,1]),
study('clockwork','Serving DNNs like Clockwork: Performance Predictability from the Bottom Up','Arpan Gujarati and Reza Karimi and Safya Alzayat and Wei Hao and Antoine Kaufmann and Ymir Vigfusson and Jonathan Mace',2020,'USENIX OSDI','443--462','','https://www.usenix.org/conference/osdi20/presentation/gujarati','https://www.usenix.org/system/files/osdi20-gujarati.pdf','Temporal exclusive scheduling','V10032GB; DellR740; worker32cores/768GB; two GPUs/host','Local experiment: one GPU; 15 RN50 copies; 16 clients/model; SLO10-500ms','Clockwork variants; INFaaS on different hardware','Fig5 measures goodput satisfying SLO, rather than raw request throughput.','Cross-hardware INFaaS comparison is indirect; controller/worker distinction.','PDF p10; section6.1; Fig5',[1,1,.5,1,.5,1,.5,1,1,1]),
study('torpor','Torpor: GPU-Enabled Serverless Computing for Low-Latency, Resource-Efficient Inference','Minchen Yu and Ao Wang and Dong Chen and Haoxuan Yu and Xiaonan Luo and Zhuohao Li and Wei Wang and Ruichuan Chen and Dapeng Nie and Haoran Yang and Yu Ding',2025,'USENIX ATC','597--612','','https://www.usenix.org/conference/atc25/presentation/yu','https://www.usenix.org/system/files/atc25-yu.pdf','API remoting + temporal swapping','Worker48vCPU/384GB; four V10032GB','Eight inference models; warm-up; CV80ms/BERT200ms SLO','Native; remote GPU; PCIe/NVLink swap','BERT Table4: native42ms, remote43ms, PCIe swap144ms, NVLink swap45ms.','p98 tail; busy time is not SM occupancy; node scaling separate.','PDF pp10-11; Table4; sections7.2-7.3',[1,1,.5,1,1,1,.5,1,.5,1]),
study('streambox','StreamBox: A Lightweight GPU SandBox for Serverless Inference Workflow','Hao Wu and Yue Yu and Junxiao Deng and Shadi Ibrahim and Song Wu and Hao Fan and Ziyue Cheng and Hai Jin',2024,'USENIX ATC','59--73','','https://www.usenix.org/conference/atc24/presentation/wu-hao','https://www.usenix.org/system/files/atc24-wu-hao.pdf','API/runtime sandbox virtualization','Four V10016GB; 28cores/128GB; CUDA10.1; PyTorch1.3; TensorFlow2.12','Three concurrent inference workflows/GPU','MPS; INFless; Astraea; Stream-only','Table2 evaluates runtime sandbox workflows on shared GPUs.','Sandbox memory separation is not proof of adversarial security.','PDF p10 onward; section9; Table2',[1,1,.5,1,.5,1,.5,1,.5,1]),
study('krypton','KRYPTON: Efficient Performance-Aware GPU Sharing with Compatibility and Isolation through Kernel Space Interception','Shulai Zhang and Ao Xu and Quan Chen and Han Zhao and Weihao Cui and Zhen Wang and Yan Li and Limin Xiao and Minyi Guo',2025,'USENIX ATC','1003--1019','','https://www.usenix.org/conference/atc25/presentation/zhang-shulai','https://www.usenix.org/system/files/atc25-zhang-shulai.pdf','Kernel API virtualization + hybrid','A10040GB/RTX4090; Ubuntu20.04; kernel5.15.0-91; driver550.90.07; CUDA12.1; PyTorch2.2.1','Inference/training/rendering in separate containers; solo-throughput targets','Temporal; MIG; adapted gpulet','Inference-specific sharing comparisons; section2.2 tests fault propagation.','Baseline adaptations and workload mix constrain attribution.','PDF p10 Tables1-2; section5; section2.2 Fig3',[1,1,1,1,.5,1,.5,1,1,1]),
study('sirius','SIRIUS: Colocating ML Inference and Training with Fast GPU Memory Handover','Jiali Wang and Yankui Wang and Mingcong Han and Rong Chen',2025,'USENIX ATC','1657--1675','','https://www.usenix.org/conference/atc25/presentation/wang-jiali','https://www.usenix.org/system/files/atc25-wang-jiali.pdf','Temporal + MPS memory handover','V10016GB; Ubuntu20.04; CUDA11.6; PyTorch2.1.2; TVM0.14; LLM case A10080GB','One GPU; six DNNs/up to56 instances + SWIN training; 300s; Poisson MAF; SLO4x solo','Reimplemented TaskSwitch; SP50/SP75; UM+MPS','Inference p99/SLO outcomes accompany training progress; separate TTFT/TBT LLM case.','TaskSwitch is a reimplementation, not vanilla PipeSwitch.','Section6.1 Fig10; section6.6',[1,1,.5,1,.5,1,1,1,.5,1]),
study('tally','Tally: Non-Intrusive Performance Isolation for Concurrent Deep Learning Workloads','Wei Zhao and Anand Jayarajan and Gennady Pekhimenko',2025,'ACM ASPLOS Volume 1','1052--1068','10.1145/3669940.3707282','https://doi.org/10.1145/3669940.3707282','https://arxiv.org/pdf/2410.07381','CUDA API interception + priority','A10040GB; Ubuntu20.04; CUDA12.2; PyTorch2.2; ONNX1.17','Same-GPU pairs; MAF inference traces; high-priority p99','Time slicing; MPS; priority MPS; TGS','At 10% idle time: normalized throughput Tally1.19 vs TGS1.65.','Latency protection sacrifices some BE throughput; author manuscript.','PDF pp9-11; sections5-5.3; Fig6',[1,1,.5,1,1,1,.5,1,1,1]),
study('parva','ParvaGPU: Efficient Spatial GPU Sharing for Large-Scale DNN Inference in Cloud Environments','Munkyu Lee and Sihoon Seong and Minki Kang and Jihyuk Lee and Gap-Joo Na and In-Geol Chun and Dimitrios S. Nikolopoulos and Cheol-Ho Hong',2024,'IEEE/ACM SC','','10.1109/SC41406.2024.00048','https://ieeexplore.ieee.org/document/10793202','https://arxiv.org/pdf/2409.14447','MIG + MPS','A10080GB; Ubuntu20.04; CUDA12.0.1; reported PyTorch1.14.0 needs checking','Eleven models; six scenario mixes; same-model MPS inside MIG','MIG-serving; gpulet and system variants','Fig7 separates internal/external fragmentation; Fig5 counts GPUs.','Author manuscript; unusual runtime version; GPU count is not occupancy.','PDF p8 onward; sectionIV; TableIV; Figs5/7',[1,1,.5,1,.5,1,.5,1,.5,1],589),
study('orion','Orion: Interference-aware Fine-grained GPU Sharing for ML Applications','Foteini Strati and Xianzhe Ma and Ana Klimovic',2024,'ACM EuroSys','1075--1092','10.1145/3627703.3629578','https://doi.org/10.1145/3627703.3629578','https://fotstrt.github.io/files/2024-orion.pdf','CUDA API interception + temporal','V10016GB/CUDA10.2; A10040GB/CUDA11.3; PyTorch1.12; Python3.9','Inference-inference and inference-training; uniform/Poisson; three repeats','MPS; streams; temporal; REEF-N reimplementation','Interference-aware scheduling compares inference latency and BE throughput.','Prototype clients share a process; REEF-N differs from AMD REEF.','PDF pp8-9; sections5.3-6.1; Tables1/3',[1,1,.5,1,.5,1,1,1,1,1]),
study('gslice','GSLICE: Controlled Spatial Sharing of GPUs for a Scalable Inference Platform','Aditya Dhakal and Sameer G. Kulkarni and K. K. Ramakrishnan',2020,'ACM SoCC','492--506','10.1145/3419111.3421284','https://doi.org/10.1145/3419111.3421284','https://www.cse.iitb.ac.in/~puru/courses/spring2024-25/downloads/gslice.pdf','MPS adaptive provisioning','One V10016GB; XeonGold6148; kernel4.4.0-150; DPDK19.02; CNTK/PyTorch/TensorRT','Two-four inference functions; VGG case SLO50ms; traffic replay','Standalone functions; MPS provisioning variants','GUE measures efficiency; shadow instance loading takes about12s in Fig15.','GUE is not GPU busy percentage; median latency not p99; academic mirror.','PDF pp8-12; section4; Table3; Fig15',[1,1,.5,1,1,1,1,1,.5,1]),
study('krisp','KRISP: Enabling Kernel-wise RIght-sizing for Spatial Partitioned GPU Inference Servers','Marcus Chow and Ali Jahanshahi and Daniel Wong',2023,'IEEE HPCA','624--637','10.1109/HPCA56546.2023.10071121','https://doi.org/10.1109/HPCA56546.2023.10071121','https://danielwong.org/files/KRISP-HPCA2023.pdf','Spatial partition/API control (AMD)','One MI50/60CUs; dualEPYC7302/512GB; Ubuntu18.04; kernel5.4; ROCm4.5','One/two/four workers and heterogeneous pairs; batch32; aggregate8/16; eight models','AMD unrestricted concurrency labelled MPSDefault','Kernel-wise right-sizing evaluates throughput and p95 inference latency.','Feature emulated; overhead subtracted; baseline is not NVIDIA MPS.','PDF pp9-10; sectionsV-VI; TableIII',[1,1,1,1,.5,1,.5,1,.5,.5],594),
study('xsched','XSched: Preemptive Scheduling for Diverse XPUs','Weihang Shen and Mingcong Han and Jialong Liu and Rong Chen and Haibo Chen',2025,'USENIX OSDI','671--692','','https://www.usenix.org/conference/osdi25/presentation/shen-weihang','https://www.usenix.org/system/files/osdi25-shen-weihang.pdf','Temporal API interposition','One GV100 inference case; broader XPU experiments separate','Two BERT-large clients; HP10req/s; saturated BE','Triton; Triton+priority; Triton+XSched','Fig15: relative p99 1.53/1.51/1.07 respectively versus solo.','Data assumed to fit memory; CUDA graphs and undocumented driver limits.','PDF pp14-15; section8 Case3 Fig15; section9',[1,1,.5,1,1,1,.5,1,1,1]),
study('paella','Paella: Low-latency Model Serving with Software-defined GPU Scheduling','Kelvin K. W. Ng and Henri Maxime Demoulin and Vincent Liu',2023,'ACM SOSP','595--610','10.1145/3600006.3613163','https://doi.org/10.1145/3600006.3613163','https://vincen.tl/files/ng23paella.pdf','Temporal software scheduling + MPS comparison','TeslaT4; XeonSilver4114/64GB; Linux4.15.0; CUDA11.7; modified TVM0.10','Eight models; lognormal sigma1.5/2; stabilized measurements','CUDA single/multiple streams; MPS; Triton23.03; ablations','p99 latency and throughput under bursty model mixes; Fig12 includes MPS.','Custom Triton TVM wrapper; MPS omitted from Fig11; dynamic batching unsupported.','PDF pp9-12; section7 Table3/Figs11-12; section8',[1,1,.5,1,.5,1,.5,1,1,1])
]
S.append(study('gnntriton','Optimizing High-Throughput Inference on Graph Neural Networks at Shared Computing Facilities with the NVIDIA Triton Inference Server','Claire Savard and Nicholas Manganelli and Burt Holzman and Lindsey Gray and Alexx Perloff and Kevin Pedro and Kevin Stenson and Keith Ulmer',2024,'Computing and Software for Big Science','14','10.1007/s41781-024-00123-2','https://link.springer.com/article/10.1007/s41781-024-00123-2','https://link.springer.com/article/10.1007/s41781-024-00123-2','MIG + concurrent model serving','A10080GB; 20/40GB slices; two hosts/four GPUs each; AMD Epyc7543; 100Gbps','Distinct ParticleNet copies within one MIG slice; four requesting workers/model; 120s samples','20GB vs40GB slices; scaling settings','Fig10: thrashing after two models/20GB or five/40GB.','Local slice evidence only; multi-server scaling separate; isolation properties described, not attack-tested.','HTML Multi-model Scaling/Fig10; Triton implementation; limitations',[1,1,.5,1,.5,1,.5,1,1,1],41))
raw=json.loads((E/'imported_records.json').read_text())
# Titles retained for abstract/full-text investigation by the reviewer.
keep=set([1,2,3,4,5,6,7,8,9,11,12,13,14,16,18,19,22,25,26,27,30,33,35,37,38,39,41,44,45,48,49,51,59,60,61,67,69,70,79,81,85,87,89,92,96,97,113,117,131,137,139,150,154,157,171,173,187,195,197,211,217,232,239,242,249,255,277,292,293,328,370,391,424,445,446,471,479,497,525,533,551,589,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,607,608,613,614,617,618,620,621,622,624,628,630,631,636,637,638,639,640,641,642,644,646,647,648,650,654,655,656,657,659,662,663,666,668,672,674,678,681,682,684,685,686,687,688])
overrides={19:('excluded','E4','abstract','Publisher abstract explicitly evaluates deep-learning training jobs only.'),51:('excluded','E5','abstract','Publisher abstract evaluates virtual-cluster resource-demand prediction and queuing, without a local sharing comparison.')}
for ids,code,reason in [([12],'E3','NVLink interconnect covert-channel study; assigned local sharing comparison not identified in abstract.'),([18],'E2','Video compression pipeline, rather than concurrent inference tenant sharing.'),([22,25,26,27,35,157,173,195,197,239,391,551],'E5','Abstract emphasizes distributed placement, adaptation, forecasting, infrastructure or workflows rather than local assigned GPU-sharing evaluation.'),([33,44,96,97,113,137,445],'E2','Abstract concerns a different application, runtime or systems problem; required concurrent inference-sharing comparison not identified.'),([59,187],'E4','Abstract identifies training/collective communication evidence rather than serving inference.'),([60],'E3','Abstract parallelizes operators inside one recommendation model with CUDA streams, rather than multi-tenant sharing.'),([61,79,131,232],'E6','Work-in-progress, conceptual framework, overview or perspective; not eligible primary evidence.'),([85,211],'E1','Abstract evaluates covert communication or SAXPY/matrix multiplication, not inference-serving workloads.'),([525],'E3','OP-TEE SoC-FPGA accelerator is outside GPU mechanism scope.')]:
    for n in ids:overrides[n]=('excluded',code,'abstract',reason)
overrides[171]=('excluded','E1','full_text','HTML section6.9 simulates vRAN pooling; AI inference is prospective context, not evaluated inference tenancy.')
overrides[497]=('excluded','E1','full_text','HTML Testing environment/The benchmark evaluates Rodinia applications including training; no inference-serving comparison.')
overrides[217]=('excluded','E3','full_text','HTML sections4.6/5 evaluate differentiable programming; GPU core partitioning is future work, not the assigned sharing evaluation.')
overrides[154]=('excluded','E5','abstract','Abstract/conclusion concern heterogeneous data-center prediction/allocation; local assigned mechanism comparison unresolved and not identified.')
overrides[45]=('excluded','E2','full_text','Open HTML sections3-4 evaluate single-model latency/energy/memory prediction and MIG-profile suggestion, without concurrent tenant sharing comparison.')
overrides[293]=('excluded','E1','full_text','Open HTML section5 evaluates vRAN FEC/turbo-code offloading, not DNN inference; inference is suggested future applicability.')
attempted=set([1,2,3,4,6,8,9,11,14,16,30,37,38,49,69,292,328,471])
def norm(t):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',t).lower())
seen={}; records=[]; dup=[]
for x in raw:
    n=int(x['record_id'][-4:]); key=x.get('doi') or x['url'] or norm(x['title'])
    # Exact URL/DOI is the principal rule; identical normalized title is an auxiliary check.
    t=norm(x['title']); previous=seen.get(key) # Distinct identifiers are separate reports even if titles match.
    r={k:x.get(k,'') for k in ['record_id','database','run_id','page','title','url','doi','publication_date']}
    r.update(record_route='formal',report_id=f'GA-P{n:04}',study_id='',decision='pending',stage='title',reason_code='',reason='',access='not_attempted',reviewer='AI-CODEX',decision_date=DATE,duplicate_of='')
    if previous:
        r.update(decision='duplicate',stage='deduplication',reason_code='E8',reason='Same DOI/URL; provenance retained.',duplicate_of=previous,report_id=next(a['report_id'] for a in records if a['record_id']==previous))
        dup.append(dict(record_id=r['record_id'],canonical_record_id=previous,relation='same report',rule='exact DOI/URL'))
    else:
        seen[key]=seen[t]=r['record_id']
        if n in keep:r['reason']='Title may fit scope; abstract/full-text eligibility remains unresolved.'
        else:
            code='E4' if re.search(r'training|fine.tuning',r['title'],re.I) else 'E6' if re.search(r'review|survey|work.in.progress|conceptual',r['title'],re.I) else 'E3' if re.search(r'FPGA|Ascend NPU|On.Device NPU',r['title'],re.I) else 'E2'
            r.update(decision='excluded',reason_code=code,reason='Title screen: '+r['title']+'; no assigned single-GPU multi-tenant inference comparison identified. This is not a full-text finding.')
        if n in overrides:
            decision,code,stage,reason=overrides[n];r.update(decision=decision,reason_code=code,stage=stage,reason=reason,access='abstract_only')
        if n in attempted:r.update(stage='abstract',access='not_retrieved',reason='Public publisher metadata/abstract examined; full text unavailable. Local inference sharing/assigned mechanism must be checked before acceptance.')
        if r['decision']=='pending' and any(z['record_id']==r['record_id'] for z in json.loads((E/'retrieval_lookups.json').read_text())):
            r.update(access='not_retrieved',reason='Public retrieval attempted; full-text assessment unavailable from returned metadata, fetch failure or robot verification. Title eligibility remains uncertain; no results inferred.')
    records.append(r)
for i,s in enumerate(S,1):
    sid=f'GA-S{i:03}';s['study_id']=sid;s['report_id']=f'GA-PS{i:03}'
    if s['formal']:
        r=next(x for x in records if x['record_id']==f"GA-R{s['formal']:04}"); s['report_id']=r['report_id']
    else:
        r=dict(record_id=f'GA-SUP{i:03}',database='Supplementary web / venue / author',run_id='SUP-SELECTED',page='',title=s['title'],url=s['publisher_url'],doi=s['doi'],publication_date=str(s['year']),record_route='supplementary',report_id=s['report_id'],duplicate_of='')
        records.append(r)
    s['record_id']=r['record_id']
    r.update(study_id=sid,decision='accepted',stage='full_text',reason_code='',reason='Peer-reviewed primary report; local concurrent inference or explicit transferable inference co-location; source-anchored outcomes. '+s['limitation'],access='retrieved',reviewer='AI-CODEX',decision_date=DATE)
    for d in records:
        if d.get('duplicate_of')==r['record_id']:d['study_id']=sid
extra=[
('TGS: Transparent GPU Sharing in Container Clouds for Deep Learning Workloads','https://www.usenix.org/conference/nsdi23/presentation/wu','excluded','abstract','E4','Official abstract concerns training workloads.','abstract_only'),
('HiveD: Sharing a GPU Cluster for Deep Learning with Guarantees','https://www.usenix.org/conference/osdi20/presentation/zhao-hanyu','excluded','abstract','E5','Official abstract describes cluster-level resource guarantees, not the required local inference comparison.','abstract_only'),
('Enhancing the performance of GPU acceleration in virtual environments: Thoroughly benchmarking the rigidity of mediated device passthrough','https://www.sciencedirect.com/science/article/pii/S0167739X25002390','excluded','full_text','E1','Earlier retrieved HTML section4.2 evaluates CloverSW++, MtCarlo, BLAST and MEME/HPC applications, without inference-serving evidence. Public repeat fetch now returns403.','retrieved'),
('On the Efficiency, Fairness, and Security of AI Accelerator Sharing','https://doi.org/10.1145/3721427','excluded','abstract','E6','Survey; context only, not an original primary evaluation.','abstract_only'),
('iGniter: Interference-Aware GPU Resource Provisioning for Predictable DNN Inference in the Cloud','https://doi.org/10.1109/TPDS.2022.3232715','pending','abstract','','Verified published TPDS study; publisher unavailable; arXiv PDF retrieval failed.','not_retrieved'),
('InferFair','https://www.sciencedirect.com/science/article/pii/S0167739X23003187','pending','abstract','','ScienceDirect 403; full-text eligibility and metadata require verification.','not_retrieved'),
('Real-time Work-conserving GPU Scheduling for DNN Inference','https://doi.org/10.1145/3768622','pending','abstract','','Related REEF journal report; assess completeness before replacing conference extraction; never count twice.','not_retrieved')]
for j,(title,url,decision,stage,code,reason,access) in enumerate(extra,1):
    records.append(dict(record_id=f'GA-X{j:03}',database='Supplementary web / publisher',run_id='SUP-SELECTED',page='',title=title,url=url,doi=url.split('doi.org/')[-1] if 'doi.org/' in url else '',publication_date='',record_route='supplementary',report_id=f'GA-PX{j:03}',study_id='GA-S001' if j==7 else '',decision=decision,stage=stage,reason_code=code,reason=reason,access=access,reviewer='AI-CODEX',decision_date=DATE,duplicate_of=''))
# Apply recorded full-text reviews to existing records, preserving discovery counts
# and stable study IDs. Uploaded licensed conversions are never copied into git.
reviews=json.loads((E/'uploaded_review_assessments.json').read_text())
for review in reviews:
    r=next(x for x in records if x['record_id']==review['record_id'])
    if review['study_id']=='GA-S001':
        old=next(x for x in records if x['record_id']=='GA-SUP001')
        old.update(decision='excluded',stage='full_text',reason_code='E8',
            reason='Less complete OSDI2022 report of GA-S001; journal GA-X007 explicitly extends it with NVIDIA implementation/evaluation. Retained as linked companion, not a second study.',access='retrieved')
        s=S[0]
    else:
        s=dict(formal=0)
        S.append(s)
    s.update(review)
    s.update(report_id=r['report_id'],fulltext_url=review['publisher_url'],
        source_type='User-supplied Markdown conversion of published journal report',
        journal=True)
    r.update(title=s['title'],doi=s['doi'],publication_date=s['publication_date'],
        study_id=s['study_id'],decision='accepted',stage='full_text',reason_code='',
        reason=s['eligibility']+' '+s['limitation'],access='retrieved',
        reviewer='AI-CODEX',decision_date=DATE)
    for d in records:
        if d.get('duplicate_of')==r['record_id']:d['study_id']=s['study_id']
write('studies.csv',records);write('duplicates.csv',dup)
write('accepted.csv',[r for r in records if r['decision']=='accepted'])
write('rejected.csv',[r for r in records if r['decision']=='excluded'])
write('pending.csv',[r for r in records if r['decision']=='pending'])
extract=[];quality=[]
rubric=['Explicit tenant question','Mechanism specified','Environment completeness','Workload specified','Comparator suitability/configuration','Units/latency statistic clear','Measurement controls','Result figure/table','Validity limits','Interpretability; experiments not rerun']
for s in S:
    scores=s.pop('scores'); total=sum(scores)
    q=dict(study_id=s['study_id'],report_id=s['report_id'],reviewer='AI-CODEX',date=DATE,total=total,band='high' if total>=8 else 'moderate' if total>=6 else 'low',anchor=s['anchor'],source_url=s['fulltext_url'])
    for n,score in enumerate(scores,1):
        q[f'Q{n}']=score
        q[f'Q{n}_rationale']=s['qa_rationales'][n-1] if s.get('qa_rationales') else rubric[n-1] if score==1 else 'Partial: '+rubric[n-1].lower()
    quality.append(q)
    r={k:v for k,v in s.items() if k not in ['formal','pages','qa_rationales']}
    r.update(retrieved_date=DATE,peer_review='Published journal article' if s['key']=='gnntriton' else 'Published full conference paper',version='Open publisher HTML' if s['key']=='gnntriton' else 'Author/camera-ready copy' if s['doi'] else 'Official USENIX proceedings PDF',eligibility='Protocol7.2: local partition/process/scheduling control; inference outcome explicit',performance_isolation='Measured workload interference/latency',resource_memory='Mechanism described; independent enforcement outcome not fully extracted',security='Not established by extracted results',fault_containment='Measured Fig3 section2.2' if s['key']=='krypton' else 'Not established by extracted results',untranscribed_fields='Exact driver/MIG profiles/batch/warm-up/variance missing from this row remain NOT EXTRACTED, not assumed absent',qa=total,evidence_strength='Within-study comparison; cross-study inference indirect')
    if s.get('journal'):
        r.update(peer_review='Published journal article',version=s['source_type'],
            eligibility=s['eligibility'],performance_isolation=s['performance_isolation'],
            resource_memory=s['resource_memory'],security=s['security'],fault_containment=s['fault_containment'],
            untranscribed_fields='See environment/workload/limitation; absent chart data and corrupted equations are not reconstructed. NOT EXTRACTED does not imply missing from original PDF.')
    extract.append(r)
write('extraction.csv',extract);write('quality.csv',quality)
(E/'included_studies.json').write_text(json.dumps(S,indent=2,ensure_ascii=False))
counts=dict(date=DATE,status='INTERMEDIATE_NOT_FINAL',formal_occurrences=len(raw),formal_duplicates=len(dup),formal_unique=len(raw)-len(dup),supplementary_selected=sum(r['record_route']=='supplementary' for r in records),accepted_unique_studies=len(S),fulltext_assessed=sum(r['stage']=='full_text' and r['decision'] in ['accepted','excluded'] for r in records),fulltext_excluded=sum(r['stage']=='full_text' and r['decision']=='excluded' for r in records),excluded_before_fulltext=sum(r['decision']=='excluded' and r['stage']!='full_text' for r in records),pending=sum(r['decision']=='pending' for r in records),not_retrieved=sum(r['decision']=='pending' and r['access']=='not_retrieved' for r in records),pending_not_yet_sought=sum(r['decision']=='pending' and r['access']!='not_retrieved' for r in records),acm_hits=None,sciencedirect_hits=None)
(E/'prisma_counts.json').write_text(json.dumps(counts,indent=2))
bib=[]
for s in S:
    fields=dict(title='{'+s['title']+'}',author=s['authors'],year=s['year'],booktitle=s['venue'],url=s['publisher_url'])
    if s['doi']:fields['doi']=s['doi']
    if s['pages']:fields['pages']=s['pages']
    if s.get('journal'):
        fields['journal']=fields.pop('booktitle')
        for k in ['volume','number']:
            if s.get(k):fields[k]=s[k]
        if s.get('article_number'):fields['note']='Art. no. '+s['article_number']
        if s['key']=='reef':fields['note']='Art. no. 1; publication date November 2025 as printed in supplied report'
    if s['key']=='gnntriton':fields['journal']=fields.pop('booktitle');fields['volume']=8;fields.pop('pages',None);fields['note']='Art. no. 14'
    bib.append(('@article{' if s['key']=='gnntriton' or s.get('journal') else '@inproceedings{')+s['key']+',\n'+',\n'.join('  '+k+' = {'+str(v)+'}' for k,v in fields.items())+'\n}')
(ROOT.parents[1]/'report/query_references.bib').write_text('\n\n'.join(bib)+'\n')
print(json.dumps(counts,indent=2))
