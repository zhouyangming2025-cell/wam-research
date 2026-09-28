# WAM+VLA Source Ingest Audit — 2026-09-28

## Scope

This audit covers source-asset ingestion only: identity verification, official PDF acquisition, MinerU conversion, raw Markdown QA, and corpus registration. It does not perform paper analysis, route classification, dataset synthesis, model reproduction, or canonical-12 edits.

- Branch: `codex/wam-vla-source-ingest`
- Baseline commit: `eb0fcc377eaf2870383e5386714dc24fffeff42c` (`origin/main`, fetched 2026-09-28)
- Existing worktree modifications were preserved and are unrelated to this batch.
- Existing raw corpus allocation was checked through `P0067`; this batch uses `P0068`–`P0077`.
- PDFs are local-only under `papers/pdf/` and are excluded by `.gitignore`.

## Identity verification

All 10 seed names were mapped to a formal paper page before PDF ingest. No `IDENTITY-UNRESOLVED` item remains.

| P-ID | Seed | Verified title | arXiv / year | Authors | Scope check | Official code / project |
|---|---|---|---|---|---|---|
| P0068 | DriveWorld-VLA | DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving | [2602.06521](https://arxiv.org/abs/2602.06521), 2026 | Feiyang Jia; Lin Liu; Ziying Song; Caiyan Jia; Hangjun Ye; Xiaoshuai Hao; Long Chen | Direct WAM+VLA | [liulin815/DriveWorld-VLA](https://github.com/liulin815/DriveWorld-VLA) |
| P0069 | Uni-World VLA | Uni-World VLA: Interleaved World Modeling and Planning for Autonomous Driving | [2603.27287](https://arxiv.org/abs/2603.27287), 2026 | Qiqi Liu; Huan Xu; Jingyu Li; Bin Sun; Zhihui Hao; Dangen She; Xiatian Zhu; Li Zhang | Direct WAM+VLA | [LogosRoboticsGroup/UniWorldVLA](https://github.com/LogosRoboticsGroup/UniWorldVLA) |
| P0070 | SGDrive | SGDrive: Scene-to-Goal Hierarchical World Cognition for Autonomous Driving | [2601.05640](https://arxiv.org/abs/2601.05640), 2026 | Jingyu Li; Junjie Wu; Dongnan Hu; Xiangkai Huang; Bin Sun; Zhihui Hao; Xianpeng Lang; Xiatian Zhu; Li Zhang | Autonomous-driving VLA / world-cognition adjacent | [LogosRoboticsGroup/SGDrive](https://github.com/LogosRoboticsGroup/SGDrive) |
| P0071 | FSDrive | FutureSightDrive: Thinking Visually with Spatio-Temporal CoT for Autonomous Driving | [2505.17685](https://arxiv.org/abs/2505.17685), 2025 | Shuang Zeng; Xinyuan Chang; Mengwei Xie; Xinran Liu; Yifan Bai; Zheng Pan; Mu Xu; Xing Wei; Ning Guo | Direct world-model-enhanced VLA | [MIV-XJTU/FSDrive](https://github.com/MIV-XJTU/FSDrive) |
| P0072 | DriveVLA-W0 | DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving | [2510.12796](https://arxiv.org/abs/2510.12796), 2025 / ICLR 2026 | Yingyan Li; Shuyao Shang; Weisong Liu; Bing Zhan; Haochen Wang; Yuqi Wang; Yuntao Chen; Xiaoman Wang; Yasong An; Chufeng Tang; Lu Hou; Lue Fan; Zhaoxiang Zhang | Direct world-model-enhanced VLA | [BraveGroup/DriveVLA-W0](https://github.com/BraveGroup/DriveVLA-W0) |
| P0073 | CoT4AD | CoT4AD: A Vision-Language-Action Model with Explicit Chain-of-Thought Reasoning for Autonomous Driving | [2511.22532](https://arxiv.org/abs/2511.22532), 2025 | Zhaohui Wang; Tengbo Yu; Hao Tang | Autonomous-driving VLA adjacent; no explicit WM claim confirmed for this ingest | No official repository verified; paper says code will be released upon acceptance |
| P0074 | WAM-Flow | WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving | [2512.06112](https://arxiv.org/abs/2512.06112), 2025 / CVPR 2026 | Yifang Xu; Jiahao Cui; Feipeng Cai; Zhihao Zhu; Hanlin Shang; Shan Luan; Mingwang Xu; Neng Zhang; Yaoyi Li; Jia Cai; Siyu Zhu | Autonomous-driving VLA / WAM-adjacent | [fudan-generative-vision/WAM-Flow](https://github.com/fudan-generative-vision/WAM-Flow) |
| P0075 | ExploreVLA | ExploreVLA: Dense World Modeling and Exploration for End-to-End Autonomous Driving | [2604.02714](https://arxiv.org/abs/2604.02714), 2026 / ECCV 2026 | Zihao Sheng; Xin Ye; Jingru Luo; Sikai Chen; Liu Ren | Direct world-model-enhanced VLA | [Project page](https://zihaosheng.github.io/ExploreVLA/) |
| P0076 | UniDriveVLA | UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving | [2604.02190](https://arxiv.org/abs/2604.02190), 2026 | Yongkang Li; Lijun Zhou; Sixu Yan; Bencheng Liao; Tianyi Yan; Kaixin Xiong; Long Chen; Hongwei Xie; Bing Wang; Guang Chen; Hangjun Ye; Wenyu Liu; Haiyang Sun; Xinggang Wang | Autonomous-driving VLA adjacent | [xiaomi-research/unidrivevla](https://github.com/xiaomi-research/unidrivevla) |
| P0077 | UniDrive-WM | UniDrive-WM: Unified Understanding, Planning and Generation World Model for Autonomous Driving | [2601.04453](https://arxiv.org/abs/2601.04453), 2026 / ECCV 2026 | Zhexiao Xiong; Xin Ye; Burhan Yaman; Sheng Cheng; Yiren Lu; Jingru Luo; Nathan Jacobs; Liu Ren | Direct world-model-enhanced VLA | [Project page](https://unidrive-wm.github.io/UniDrive-WM/); no official repository verified |

## Ingest ledger

| P-ID | Seed name | Source PDF | PDF check | PDF SHA256 | MinerU | raw.md | QA | Code | Status |
|---|---|---|---|---|---|---|---|---|---|
| P0068 | DriveWorld-VLA | [arXiv PDF](https://arxiv.org/pdf/2602.06521) | 20 pages; 8,392,521 B | `047ebabbce3437a5722302de5ac813c3e3fb664c276099f92d444f581ab579c8` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0068_DriveWorld-VLA/P0068_DriveWorld-VLA.raw.md` | 60,613 chars; 15/15 images; no mojibake | Available | PASS |
| P0069 | Uni-World VLA | [arXiv PDF](https://arxiv.org/pdf/2603.27287) | 22 pages; 2,960,577 B | `09aa65ced8445e87e0d93dd8d9d88fdcfbe335ec30579e47579e5ddfe801d41e` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0069_UniWorldVLA/P0069_UniWorldVLA.raw.md` | 56,492 chars; 8/8 images; no mojibake | Available | PASS |
| P0070 | SGDrive | [arXiv PDF](https://arxiv.org/pdf/2601.05640) | 16 pages; 3,734,272 B | `ecab1f1e8efd4f921e9d861c4c4fb416b83ea663e5cad75b776d86fa6ba8ea2c` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0070_SGDrive/P0070_SGDrive.raw.md` | 64,456 chars; 10/10 images; no mojibake | Available | PASS |
| P0071 | FSDrive | [arXiv PDF](https://arxiv.org/pdf/2505.17685) | 14 pages; 6,904,609 B | `f8afdb8f41bff28c665830bfc7d6621334fbf192330daa87a984d8c8a32d17d1` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0071_FSDrive/P0071_FSDrive.raw.md` | 60,964 chars; 3/3 images; no mojibake | Available | PASS |
| P0072 | DriveVLA-W0 | [arXiv PDF](https://arxiv.org/pdf/2510.12796) | 22 pages; 3,330,317 B | `f5c200f838546b9c62ff35d38c21f788ef2db2adab919d6db58ec180c55e4823` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md` | 73,518 chars; 18/18 images; no mojibake | Available | PASS |
| P0073 | CoT4AD | [arXiv PDF](https://arxiv.org/pdf/2511.22532) | 11 pages; 1,941,170 B | `a6a5dd574630d5b98c8edad7b7e2bb96ea2f1f4c1597b1c1537aaf1691eeb385` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0073_CoT4AD/P0073_CoT4AD.raw.md` | 55,085 chars; 4/4 images; no mojibake | Not verified | PASS |
| P0074 | WAM-Flow | [arXiv PDF](https://arxiv.org/pdf/2512.06112) | 18 pages; 19,856,924 B | `33988ff4f224e625d05da7777731dfddfbd74908c23e34440947e811b96f184e` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md` | 73,284 chars; 18/18 images; no mojibake | Available | PASS |
| P0075 | ExploreVLA | [arXiv PDF](https://arxiv.org/pdf/2604.02714) | 24 pages; 3,129,686 B | `72dcaec0470540eb187025982941d04ba2b3f2d570c05d99eb8b43c29db7ae63` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0075_ExploreVLA/P0075_ExploreVLA.raw.md` | 69,030 chars; 6/6 images; no mojibake | Project page | PASS |
| P0076 | UniDriveVLA | [arXiv PDF](https://arxiv.org/pdf/2604.02190) | 18 pages; 1,895,948 B | `8f66f7ce0c13bfc01898edcabb7d7c30e9c2b0f5c1fd43e6ba97823e33019249` | 3.4.5 `pipeline/auto` | `papers/raw_md/P0076_UniDriveVLA/P0076_UniDriveVLA.raw.md` | 82,499 chars; 6/6 images; Abstract body present without heading | Available | PASS-WITH-MINOR-PARSE-ISSUES |
| P0077 | UniDrive-WM | [arXiv PDF](https://arxiv.org/pdf/2601.04453) | 27 pages; 20,047,536 B | `9557a3a40bf9e405ab76b290848ca4a8996cfdae894da854b51d1ff7bacc0fce` | 3.4.5 `pipeline/auto`; retry `pipeline/txt` | `papers/raw_md/P0077_UniDrive-WM/P0077_UniDrive-WM.raw.md` | 79,635 chars; 11/11 images; numbered bibliography present without heading | Project page; no repository verified | PASS-WITH-MINOR-PARSE-ISSUES |

The repository's generated automated result ledger is `manifests/batch_wamvla_rawmd_results.json`; it reports `RAW_MD_READY=8/10` before the manual content-level review of P0076 and P0077.

## Commands and evidence

Primary parse command used for P0068–P0077:

```text
D:\Program Files\Mineru\venv\Scripts\python.exe scripts/run_mineru.py -p papers/pdf/Pxxxx_ShortName.pdf -o papers/quarantine/mineru_artifacts/Pxxxx_ShortName -b pipeline -m auto
```

P0077 retry command:

```text
D:\Program Files\Mineru\venv\Scripts\python.exe scripts/run_mineru.py -p papers/pdf/P0077_UniDrive-WM.pdf -o papers/quarantine/mineru_artifacts/P0077_UniDrive-WM_retry_txt -b pipeline -m txt
```

Per-paper logs are in `experiment_logs/mineru_P0068.log` through `experiment_logs/mineru_P0077.log`; the retry log is `experiment_logs/mineru_P0077_retry_txt.log`. All MinerU intermediate artifacts remain under `papers/quarantine/mineru_artifacts/` and were not manually rewritten.

## Artifact hashes

| P-ID | raw.md SHA256 |
|---|---|
| P0068 | `290f900961c38da0f2b51693ccce6af4c9e35b09fe0bb9e2134fe438bcba9e99` |
| P0069 | `91dc05bc305b994228a6d7a61eac6f2ae21b8da466d7eed6c97b8e343e741ca4` |
| P0070 | `687fc2a31fb3ac3d2fe0308be01fe77359288b967bbf37c4a14524089c1b237c` |
| P0071 | `69a433efdab84f637cfd7fb50ec9fff05c6f250def4f906ce009072cce77c8dd` |
| P0072 | `693d8d4bd744529592d6e61388c0a1f937afbcbae038d6378abe2f47d96bd6fa` |
| P0073 | `e4cc47e67edb08b53f51d5419fe6e3731111928a55939b260c9b19d75bf71231` |
| P0074 | `555ef0d794433414226791a588e89459649da7396a0d247916d7c87100e6271d` |
| P0075 | `ffcf3156cedf588cbcbaea0e14c2d691c7e4484b093fd2edd67c01abe1f5a5f5` |
| P0076 | `e7fe612ee95c762a0b7324d4cd19604749f71abb276aba4be43950e6f35f2092` |
| P0077 | `dc18209f0f9ba1783b7042e077c398a7f581ed06943a67bf23dc6d0565277c18` |
