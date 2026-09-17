# Raw Markdown Completeness Audit

Date: 2026-09-17  
Branch: `codex/domain-map-d02-w1e`

## Conclusion

The repository already contains MinerU-style local Markdown for the existing paper corpus. A bulk re-download and re-conversion is not warranted.

Before this supplement:

```text
paper directories: 64
full *.raw.md files: 63
paper without full raw Markdown: P0066 Safe-Sim
```

After this supplement:

```text
paper directories: 64
full *.raw.md files: 64
paper directories with raw Markdown: 64/64
```

## Existing corpus check

The six raw-Markdown result/QC manifests were inspected:

```text
manifests/batch_0a_rawmd_results.json
manifests/batch_census1_rawmd_results.json
manifests/batch_census2_rawmd_results.json
manifests/batch_round2_rawmd_results.json
manifests/batch_phase_c5_rawmd_results.json
manifests/batch_phase_c5_qc.json
```

Across those manifests there are 106 result records and 63 unique paper IDs. The latest record for every one of the 63 existing papers reports:

```text
qc = RAW_MD_READY
problems = []
```

The records also document title/abstract/body-section/reference checks and image-copy checks. The Phase C.5 records explicitly document `mineru_returncode = 0` for the newly added P0061–P0065 conversion batch. The earlier batches provide the equivalent QC for the earlier corpus.

This is a structural extraction/QC conclusion. `RAW_MD_READY` does not mean that every OCR glyph, equation, table, or line break is semantically perfect. The raw layer is intentionally the MinerU output and should not be manually rewritten into a polished reading copy.

## Safe-Sim supplement

P0066 had a verified paper and official-code audit, but only a source note; it was the sole paper directory without a full raw Markdown extraction.

The official ECCV paper PDF was downloaded locally and converted with the repository's existing MinerU runner. The PDF is deliberately not tracked in Git.

```text
paper: Safe-Sim: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
paper ID: P0066
source: ECVA ECCV 2024 paper PDF
pages: 17
MinerU return code: 0
raw Markdown: papers/raw_md/P0066_SafeSim/P0066_SafeSim.raw.md
images: papers/raw_md/P0066_SafeSim/images/ (18 files)
PDF SHA256: 7a092e02de9f03031ff51660966d0a94c66635682cda2e6970375f6c21f92b2e
```

Local QC of the generated raw Markdown:

```text
characters: 51,145
Markdown headings: 22
referenced images: 4
referenced images missing: 0
abstract paragraph: present
method/approach content: present
experiments/results content: present
conclusion content: present
references: present
```

The extracted text retains normal MinerU/OCR imperfections, including occasional malformed punctuation and spelling artifacts. Those are recorded as extraction-quality caveats, not silently corrected in the raw evidence layer.

## Scope and non-actions

- No ontology, route map, or D02 classification was changed.
- No existing `*.raw.md` was overwritten.
- No paper PDF was added to Git; PDFs remain local under the ignored `papers/pdf/` directory.
- The existing source note for P0066 was updated to point to the completed extraction.
- This supplement closes raw-Markdown presence for the current 64-directory corpus; it does not claim that every paper in the wider literature has been collected.

