---
title: "LLM Security Agent (大語言模型安全智能體)"
category: "techniques"
tags: [llm-agent, pentestgpt, cybersecurity, reasoning-tree]
---

# LLM Security Agent (大語言模型安全智能體)

## 概述
大語言模型安全智能體（LLM Security Agent）是指利用具備推理與工具調用能力的大語言模型（如 GPT-4、Claude 3.5 Sonnet），結合外部資安工具鏈（Nmap, Metasploit, Sqlmap, BurpSuite），自主執行威脅分析與滲透測試的智慧系統。

## 核心架構突破
以 [[Deng2023-PentestGPT.md]] 為代表，為解決大模型「容易遺忘長文本上下文」與「缺乏全域任務規劃」的瓶頸，現代安全智能體多採用分工解耦架構：
1. **推理模組 (Reasoning)**：維持全域「滲透任務樹（PTT）」，不做終端日誌讀取，專注大局策略。
2. **生成模組 (Generation)**：將抽象子任務翻譯為精確命令行語法（避免參數幻覺）。
3. **解析模組 (Parsing)**：以 Regex 與小模型濃縮終端機數千行輸出，將觀測精簡後回傳。

## 關聯詞條
- [[Deng2023-PentestGPT.md]]
- [[Autonomous Penetration Testing]]
- [[Pham2024-Raiju.md]]
