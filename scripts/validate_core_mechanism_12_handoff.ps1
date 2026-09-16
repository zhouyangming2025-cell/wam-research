$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$manifestPath = Join-Path $repoRoot 'handoff/core_mechanism_12/PAPER_SET_12.tsv'
$requiredPackageFiles = @(
    'handoff/core_mechanism_12/README.md',
    'handoff/core_mechanism_12/GPT6_TASK_PROMPT.md',
    'handoff/core_mechanism_12/RESEARCH_PROTOCOL.md',
    'handoff/core_mechanism_12/PAPER_EVIDENCE_INDEX.md',
    'handoff/core_mechanism_12/DRAFTS_TO_ATTACK.md',
    'handoff/core_mechanism_12/HUMAN_VALIDATION_TEMPLATE.md',
    'papers/WAM_SIX_PAPER_UNIFIED_MODULE_AUDIT.md',
    'papers/WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md',
    'papers/WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md',
    'papers/WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md'
)

$errors = [System.Collections.Generic.List[string]]::new()

foreach ($relativePath in $requiredPackageFiles) {
    $absolutePath = Join-Path $repoRoot $relativePath
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
        $errors.Add("Missing package file: $relativePath")
    }
}

if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) {
    $errors.Add('Missing PAPER_SET_12.tsv')
} else {
    $rows = Import-Csv -LiteralPath $manifestPath -Delimiter "`t" -Encoding UTF8

    if ($rows.Count -ne 12) {
        $errors.Add("Expected 12 manifest rows, found $($rows.Count)")
    }

    $uniqueIds = @($rows.paper_id | Sort-Object -Unique)
    if ($uniqueIds.Count -ne 12) {
        $errors.Add("Expected 12 unique paper IDs, found $($uniqueIds.Count)")
    }

    $validationCount = @($rows | Where-Object group -eq 'human_validation').Count
    $stressCount = @($rows | Where-Object group -eq 'stress_test').Count
    if ($validationCount -ne 6 -or $stressCount -ne 6) {
        $errors.Add("Expected 6 human-validation + 6 stress-test rows, found $validationCount + $stressCount")
    }

    foreach ($row in $rows) {
        foreach ($column in @('raw_paper', 'code_or_version_audit', 'deep_analysis')) {
            $relativePath = $row.$column
            $absolutePath = Join-Path $repoRoot $relativePath
            if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
                $errors.Add("$($row.paper_id) missing $column file: $relativePath")
            }
        }
    }
}

if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output 'CORE_MECHANISM_12_HANDOFF_OK'
Write-Output 'papers=12 human_validation=6 stress_test=6'
