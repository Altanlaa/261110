# scripts/rebuild_index.ps1
# Windows PowerShell 原生版本：自動掃描 wiki/ 生成 _index.md 與 _backlinks.json
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$rootDir = Split-Path -Parent $PSScriptRoot
$wikiDir = Join-Path $rootDir "wiki"

if (-not (Test-Path $wikiDir)) {
    Write-Error "找不到 wiki 目錄: $wikiDir"
    exit 1
}

$files = Get-ChildItem -Path $wikiDir -Recurse -File -Filter "*.md" | Where-Object { -not $_.Name.StartsWith("_") }

$articles = @()
$titleLookup = @{}

foreach ($f in $files) {
    $raw = Get-Content -Path $f.FullName -Raw -Encoding UTF8
    $relPath = ($f.FullName.Substring($wikiDir.Length).TrimStart('\', '/')) -replace '\\', '/'
    
    $title = $f.BaseName
    $articleType = $f.Directory.Name
    $aliases = @()
    $sources = @()
    $links = @()

    if ($raw -match '(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)') {
        $fm = $matches[1]
        $body = $matches[2]
        foreach ($line in ($fm -split '\r?\n')) {
            if ($line -match '^title:\s*["'']?(.*?)["'']?$') { $title = $matches[1] }
            if ($line -match '^type:\s*["'']?(.*?)["'']?$') { $articleType = $matches[1] }
            if ($line -match '^aliases:\s*\[(.*?)\]') {
                $rawAliases = $matches[1] -split ','
                foreach ($a in $rawAliases) {
                    $cleanA = $a.Trim().Trim('"').Trim("'")
                    if ($cleanA) { $aliases += $cleanA }
                }
            }
        }
    } else {
        $body = $raw
        foreach ($line in ($body -split '\r?\n')) {
            if ($line.StartsWith("# ")) {
                $title = $line.Substring(2).Trim()
                break
            }
        }
    }

    # 提取 [[wikilinks]]
    $linkMatches = [regex]::Matches($body, '\[\[(.*?)\]\]')
    foreach ($m in $linkMatches) {
        $target = ($m.Groups[1].Value -split '\|')[0].Trim()
        if ($target) { $links += $target }
    }

    $artObj = [PSCustomObject]@{
        Title = $title
        Type = $articleType
        RelPath = $relPath
        Aliases = $aliases
        Links = $links
    }
    $articles += $artObj
    $titleLookup[$title.ToLower()] = $title
    foreach ($al in $aliases) {
        $titleLookup[$al.ToLower()] = $title
    }
}

# 建立反向連結 (Backlinks)
$backlinks = [ordered]@{}
foreach ($art in $articles) {
    $backlinks[$art.Title] = @()
}

foreach ($art in $articles) {
    $srcTitle = $art.Title
    foreach ($tgt in $art.Links) {
        $canon = if ($titleLookup.ContainsKey($tgt.ToLower())) { $titleLookup[$tgt.ToLower()] } else { $tgt }
        if (-not $backlinks.Contains($canon)) {
            $backlinks[$canon] = @()
        }
        if ($backlinks[$canon] -notcontains $srcTitle) {
            $backlinks[$canon] += $srcTitle
        }
    }
}

# 寫入 _backlinks.json
$backlinksPath = Join-Path $wikiDir "_backlinks.json"
$backlinksJson = $backlinks | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($backlinksPath, $backlinksJson, [System.Text.Encoding]::UTF8)
Write-Host "[OK] 反向連結圖譜已產出: $backlinksPath"

# 初始化 _absorb_log.json
$logPath = Join-Path $wikiDir "_absorb_log.json"
if (-not (Test-Path $logPath)) {
    $initLog = [PSCustomObject]@{
        absorbed_entries = @()
        last_sync = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
    } | ConvertTo-Json
    [System.IO.File]::WriteAllText($logPath, $initLog, [System.Text.Encoding]::UTF8)
    Write-Host "[OK] 文獻吸收日誌已初始化: $logPath"
}

# 產出 _index.md
$grouped = $articles | Group-Object Type
$nowStr = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

$indexContent = @"
# LLM 研究知識維基 - 主索引 (Master Index)

> 最後自動同步時間：$nowStr
> 詞條總數：**$($articles.Count)** 篇

## 分類導覽

"@

foreach ($g in ($grouped | Sort-Object Name)) {
    $indexContent += "- **$($g.Name)** ($($g.Count) 篇)`n"
}

$indexContent += "`n---`n`n"

foreach ($g in ($grouped | Sort-Object Name)) {
    $indexContent += "## $($g.Name.ToUpper())`n`n"
    foreach ($item in ($g.Group | Sort-Object Title)) {
        $aliasStr = ""
        if ($item.Aliases.Count -gt 0) {
            $joined = $item.Aliases -join ', '
            $aliasStr = ' `also: ' + $joined + '`'
        }
        $refCount = 0
        if ($backlinks.Contains($item.Title)) { $refCount = $backlinks[$item.Title].Count }
        $indexContent += ('- [[' + $item.Title + ']] (' + $item.RelPath + ')' + $aliasStr + ' — *被引用 ' + $refCount + " 次*`n")
    }
    $indexContent += "`n"
}

$indexContent += "## 核心技術拓撲 (高引用詞條 Top 10)`n`n"
$sortedByRefs = $articles | Sort-Object { if ($backlinks.Contains($_.Title)) { $backlinks[$_.Title].Count } else { 0 } } -Descending | Select-Object -First 10
foreach ($item in $sortedByRefs) {
    $refCount = 0
    if ($backlinks.Contains($item.Title)) { $refCount = $backlinks[$item.Title].Count }
    $indexContent += ('- **[[' + $item.Title + ']]** (' + $item.Type + '): 被引用 ' + $refCount + " 次`n")
}

$indexPath = Join-Path $wikiDir "_index.md"
[System.IO.File]::WriteAllText($indexPath, $indexContent, [System.Text.Encoding]::UTF8)
Write-Host "[OK] 全局主索引已產出: $indexPath"
