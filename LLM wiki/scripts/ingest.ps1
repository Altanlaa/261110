# scripts/ingest.ps1
# Windows PowerShell 原生版本：掃描 data/ 目錄下的文獻，標準化輸出至 raw/entries/
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $rootDir "data"
$rawDir = Join-Path (Join-Path $rootDir "raw") "entries"

if (-not (Test-Path $rawDir)) {
    New-Item -ItemType Directory -Path $rawDir -Force | Out-Null
}

$files = Get-ChildItem -Path $dataDir -Recurse -File -Include *.md, *.markdown, *.txt, *.json
$count = 0

foreach ($file in $files) {
    $parentName = $file.Directory.Name
    $sourceType = "document"
    if ($parentName -in @("papers", "blogs", "reports")) {
        $sourceType = $parentName.TrimEnd("s")
    }

    $modDate = $file.LastWriteTime.ToString("yyyy-MM-dd")
    $name = $file.BaseName
    if ($name -match '^(\d{4}[-_]\d{2}[-_]\d{2})[-_]?(.*)') {
        $modDate = $matches[1] -replace '_', '-'
        $cleanId = $matches[2]
    } else {
        $cleanId = $name
    }

    $entrySlug = ($cleanId.ToLower() -replace '[^\w\s-]', '') -replace '[-\s]+', '-'
    if (-not $entrySlug) { $entrySlug = "entry" }

    $rawContent = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $title = $cleanId -replace '[-_]', ' '

    # 檢查是否已有 frontmatter
    if ($rawContent -match '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)') {
        $fm = $matches[1]
        $body = $matches[2].Trim()
        foreach ($line in ($fm -split '\r?\n')) {
            if ($line -match '^title:\s*["'']?(.*?)["'']?$') { $title = $matches[1] }
            if ($line -match '^date:\s*["'']?(\d{4}-\d{2}-\d{2})["'']?$') { $modDate = $matches[1] }
        }
    } else {
        $body = $rawContent.Trim()
        foreach ($line in ($body -split '\r?\n')) {
            if ($line.StartsWith("# ")) {
                $title = $line.Substring(2).Trim()
                break
            }
        }
    }

    $targetFile = Join-Path $rawDir "${modDate}_${entrySlug}.md"

    $relOriginal = (Resolve-Path -Path $file.FullName -Relative) -replace '\\', '/'

    $outputContent = @"
---
id: $entrySlug
title: "$title"
date: $modDate
source_type: $sourceType
original_file: "$relOriginal"
tags: []
---

# $title

$body
"@

    [System.IO.File]::WriteAllText($targetFile, $outputContent, [System.Text.Encoding]::UTF8)
    Write-Host "[Ingest] $($file.Name) -> $(Split-Path -Leaf $targetFile)"
    $count++
}

Write-Host "`n[完成] Ingest 完成，共轉換 $count 個文獻至 raw/entries/"
