#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rebuild_index.py
掃描 wiki/ 目錄下的所有 Markdown 詞條，自動生成：
1. wiki/_index.md (包含分類統計、別名 aliases、所有文章清單)
2. wiki/_backlinks.json (反向連結拓撲圖，記錄誰引用了誰)
3. wiki/_absorb_log.json (初始化文獻吸收日誌)
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"
ROOT_DIR = Path(__file__).resolve().parent.parent

WIKILINK_PATTERN = re.compile(r'\[\[(.*?)\]\]')
FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def parse_yaml_simple(yaml_str):
    """簡易 YAML 前言解析器，處理基本鍵值與字串陣列"""
    data = {}
    lines = yaml_str.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            val = parts[1].strip()
            # 處理 list: ["a", "b"] 或 [a, b]
            if val.startswith('[') and val.endswith(']'):
                items = [item.strip().strip('"\'') for item in val[1:-1].split(',') if item.strip()]
                data[key] = items
            else:
                data[key] = val.strip('"\'')
    return data

def extract_article_info(file_path):
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    frontmatter = {}
    body = content

    match = FRONTMATTER_PATTERN.match(content)
    if match:
        frontmatter = parse_yaml_simple(match.group(1))
        body = content[match.end():]

    title = frontmatter.get('title')
    if not title:
        # 從第一個 H1 抓取標題
        for line in body.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
    if not title:
        title = file_path.stem

    article_type = frontmatter.get('type')
    if not article_type:
        # 依父資料夾命名
        article_type = file_path.parent.name

    aliases = frontmatter.get('aliases', [])
    if isinstance(aliases, str):
        aliases = [aliases]
    
    # 抽取雙括號 wikilinks
    links = []
    for link in WIKILINK_PATTERN.findall(body):
        clean_link = link.split('|')[0].strip()
        if clean_link:
            links.append(clean_link)

    rel_path = file_path.relative_to(WIKI_DIR).as_posix()

    return {
        "title": title,
        "type": article_type,
        "file_name": file_path.name,
        "rel_path": rel_path,
        "aliases": aliases,
        "links": links,
        "sources": frontmatter.get('sources', []),
        "created": frontmatter.get('created', ''),
        "last_updated": frontmatter.get('last_updated', ''),
    }

def main():
    if not WIKI_DIR.exists():
        print(f"Wiki directory not found: {WIKI_DIR}")
        return

    articles = []
    # 遍歷 wiki 下所有非底線開頭的 .md
    for root, dirs, files in os.walk(WIKI_DIR):
        # 排除以 . 開頭的目錄
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.md') and not f.startswith('_'):
                full_path = Path(root) / f
                info = extract_article_info(full_path)
                if info:
                    articles.append(info)

    # 建立別名到正名映射
    title_lookup = {}
    for art in articles:
        title_lookup[art['title'].lower()] = art['title']
        for alias in art['aliases']:
            title_lookup[alias.lower()] = art['title']

    # 建立反向連結 (Backlinks)
    backlinks = {art['title']: [] for art in articles}
    for art in articles:
        source_title = art['title']
        for target in art['links']:
            canonical_target = title_lookup.get(target.lower(), target)
            if canonical_target in backlinks:
                if source_title not in backlinks[canonical_target]:
                    backlinks[canonical_target].append(source_title)
            else:
                backlinks.setdefault(canonical_target, [])
                if source_title not in backlinks[canonical_target]:
                    backlinks[canonical_target].append(source_title)

    # 寫入 _backlinks.json
    backlinks_path = WIKI_DIR / "_backlinks.json"
    with open(backlinks_path, 'w', encoding='utf-8') as f:
        json.dump(backlinks, f, ensure_ascii=False, indent=2)
    print(f"[OK] 已更新反向連結圖譜: {backlinks_path}")

    # 確保 _absorb_log.json 存在
    log_path = WIKI_DIR / "_absorb_log.json"
    if not log_path.exists():
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump({"absorbed_entries": [], "last_sync": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
        print(f"[OK] 已初始化文獻吸收日誌: {log_path}")

    # 產出 _index.md
    articles_by_type = {}
    for art in articles:
        articles_by_type.setdefault(art['type'], []).append(art)

    index_lines = [
        "# LLM 研究知識維基 - 主索引 (Master Index)",
        "",
        f"> 最後自動同步時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> 詞條總數：**{len(articles)}** 篇",
        "",
        "## 分類導覽",
        ""
    ]

    for type_name, items in sorted(articles_by_type.items()):
        index_lines.append(f"- **{type_name}** ({len(items)} 篇)")

    index_lines.append("")
    index_lines.append("---")
    index_lines.append("")

    for type_name, items in sorted(articles_by_type.items()):
        index_lines.append(f"## {type_name.capitalize()}")
        index_lines.append("")
        for item in sorted(items, key=lambda x: x['title'].lower()):
            alias_str = ""
            if item['aliases']:
                alias_str = f" `also: {', '.join(item['aliases'])}`"
            ref_count = len(backlinks.get(item['title'], []))
            index_lines.append(f"- [[{item['title']}]] ({item['rel_path']}){alias_str} — *被引用 {ref_count} 次*")
        index_lines.append("")

    index_lines.append("## 核心技術拓撲 (高引用詞條 Top 10)")
    index_lines.append("")
    sorted_by_refs = sorted(articles, key=lambda x: len(backlinks.get(x['title'], [])), reverse=True)[:10]
    for item in sorted_by_refs:
        ref_count = len(backlinks.get(item['title'], []))
        index_lines.append(f"- **[[{item['title']}]]** ({item['type']}): 被引用 {ref_count} 次")
    index_lines.append("")

    index_path = WIKI_DIR / "_index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(index_lines))
    print(f"[OK] 已更新全局主索引: {index_path}")

if __name__ == "__main__":
    main()
