#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingest.py
掃描 data/ 目錄下的文獻與原始檔案，標準化轉換並輸出至 raw/entries/。
支援格式：
- Markdown (*.md, *.markdown)
- 純文字 (*.txt)
- JSON (*.json)
輸出格式：raw/entries/{date}_{id}.md，附帶標準 YAML frontmatter。
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = ROOT_DIR / "raw" / "entries"

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def process_file(file_path):
    rel_path = file_path.relative_to(DATA_DIR)
    ext = file_path.suffix.lower()
    
    # 判斷 source_type
    parent_folder = file_path.parent.name
    if parent_folder in ["papers", "blogs", "reports"]:
        source_type = parent_folder[:-1] # paper, blog, report
    else:
        source_type = "document"

    # 取得或猜測日期
    mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
    date_str = mod_time.strftime("%Y-%m-%d")
    
    # 嘗試從檔名匹配 YYYY-MM-DD
    date_match = re.search(r'(\d{4}[-_]\d{2}[-_]\d{2})', file_path.name)
    if date_match:
        date_str = date_match.group(1).replace('_', '-')

    file_stem = file_path.stem
    # 移除檔名中可能自帶的日期
    clean_stem = re.sub(r'^\d{4}[-_]\d{2}[-_]\d{2}[-_]?', '', file_stem)
    entry_id = slugify(clean_stem) or "entry"

    title = clean_stem.replace('-', ' ').replace('_', ' ').title()
    content = ""
    tags = []

    if ext in ['.md', '.markdown', '.txt']:
        try:
            raw_text = file_path.read_text(encoding='utf-8')
        except Exception:
            raw_text = file_path.read_text(encoding='latin-1', errors='ignore')

        # 檢查是否自帶 frontmatter
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', raw_text, re.DOTALL)
        if fm_match:
            # 原文已有 frontmatter
            content = fm_match.group(2).strip()
            # 嘗試抓取自帶標題
            for line in fm_match.group(1).splitlines():
                if line.startswith('title:'):
                    title = line.split(':', 1)[1].strip().strip('"\'')
                elif line.startswith('date:'):
                    extracted_date = line.split(':', 1)[1].strip().strip('"\'')
                    if re.match(r'^\d{4}-\d{2}-\d{2}$', extracted_date):
                        date_str = extracted_date
        else:
            content = raw_text.strip()
            # 若第一行為 # Title 則提取
            for line in content.splitlines():
                if line.startswith('# '):
                    title = line[2:].strip()
                    break

    elif ext == '.json':
        try:
            with open(file_path, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
                title = data.get('title', title)
                date_str = data.get('date', date_str)
                tags = data.get('tags', [])
                content = data.get('content', '') or data.get('abstract', '') or json.dumps(data, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[Warn] 無法解析 JSON {file_path}: {e}")
            return None
    else:
        # 不支援或二進位檔案跳過
        return None

    # 目標檔案路徑
    target_filename = f"{date_str}_{entry_id}.md"
    target_path = RAW_DIR / target_filename

    frontmatter_block = f"""---
id: {entry_id}
title: "{title}"
date: {date_str}
source_type: {source_type}
original_file: "{rel_path.as_posix()}"
tags: {json.dumps(tags, ensure_ascii=False)}
---

# {title}

{content}
"""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target_path.write_text(frontmatter_block, encoding='utf-8')
    print(f"[Ingest] 已編譯原始文獻: {rel_path} -> {target_path.name}")
    return target_path

def main():
    if not DATA_DIR.exists():
        print(f"找不到 data/ 目錄: {DATA_DIR}")
        return

    count = 0
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            file_path = Path(root) / f
            if file_path.suffix.lower() in ['.md', '.markdown', '.txt', '.json']:
                res = process_file(file_path)
                if res:
                    count += 1
    print(f"\n[完成] Ingest 完成，共轉換 {count} 個文獻至 raw/entries/")

if __name__ == "__main__":
    main()
