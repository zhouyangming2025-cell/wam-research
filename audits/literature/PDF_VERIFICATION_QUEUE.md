# PDF_VERIFICATION_QUEUE

Last updated: 2026-09-14

Status: **HISTORICAL CONDITIONAL EVIDENCE QUEUE — execute only when a listed numeric/detail claim is reused; not a current research direction.**

Principle:

```text
Do not upload/archive every PDF into GitHub.
Verify only evidence points that carry field-level conclusions or remain OCR/source-path ambiguous.
Use public official/venue PDFs first; request user/local extraction only when public access is unavailable.
```

## Priority A — verify before reusing a listed claim

| priority | paper | exact evidence point | why it matters | preferred source |
|---:|---|---|---|---|
| A1 | **Epona** | joint visual+trajectory training vs trajectory-only planning ablation; exact cells/protocol | key evidence that visual-future task improves planner representation | ICCV 2025 camera-ready PDF |
| A2 | **OccWorld** | tokenizer reconstruction/forecast/planning ablation; spatial/temporal attention ablation; Table-2 `†` metric footnote | carries `world fidelity != decision utility` counterexample | canonical paper PDF |
| A3 | **WoTE** | trajectory-only vs evaluator-only vs evaluator+future-state table | cleanest Wave-2 evidence that online predicted future adds value beyond scorer | canonical ICCV/arXiv PDF |
| A4 | **LAW** | no-WM / latent / action-aware ablation; future-horizon table | carries action-aware representation and non-monotonic-horizon conclusions | ICLR 2025 / canonical PDF |
| A5 | **DriveLaW** | video-pretraining scale table; representation comparison; denoising-step table; Stage-3 freeze wording | strongest evidence that exact WM hidden state matters to planning | CVPR 2026 / canonical PDF + code if needed |
| A6 | **Auto-JEPA** | component ablation; K sensitivity; semantic occlusion statistics | carries planning-oriented compression evidence | canonical public paper/PDF |
| A7 | **DA-WAM** | future-configuration ablation; expert-matched predictive-loss wording | carries candidate-specific-future attribution and supervision-boundary conclusion | canonical public paper/PDF |
| A8 | **DrivingGPT** | exact deployment planning decode path, especially whether intervening visual-token generation is bypassed | affects inference-coupling taxonomy | public source code if available; PDF cannot alone resolve if unspecified |

## Priority B — verify before reusing a listed numerical claim

```text
M2I conditional GT-vs-predicted influencer table
GameFormer raw vs cost-refined planning table
What Truly Matters dynamics-gap percentages
UniAD planner collision/L2 ablation
DiffusionDrive matched TransFuser roadmap
DriveSuprim oracle candidate-ranking table
ViDAR downstream transfer + ray-casting control
Drive-WM reward/planning table
```

These claims are already sufficiently stable for continuing the field reconstruction, but final numeric citations should be canonical-PDF checked.

## Already hardened

```text
LAW inference-path semantics            = CODE VERIFIED
WoTE target-generation reactivity      = CODE VERIFIED
Think2Drive RSSM/imagination mechanism = PDF VERIFIED (ECCV 2024 official)
Think2Drive CARLA-v2 Table 3           = PDF VERIFIED (ECCV 2024 official)
NAVSIM non-reactive protocol           = PRIMARY-TEXT VERIFIED / benchmark-level stable
```

## User action rule

Do **not** ask the user to upload PDFs by default.

User/local help is needed only if:

```text
public official PDF is unavailable/paywalled
or
canonical local version differs from public version in a decision-critical way
or
an image/supplement/source artifact exists only locally
```

If local help is needed, request the smallest evidence unit possible:

```text
one PDF
or one table/figure image
or one exact section extraction
```

rather than the entire corpus.
