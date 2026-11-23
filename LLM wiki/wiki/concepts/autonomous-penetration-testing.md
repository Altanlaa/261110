---
title: "Autonomous Penetration Testing (自動化滲透測試)"
category: "concepts"
tags: [cybersecurity, pentesting, red-team, automation, agents]
---

# Autonomous Penetration Testing (自動化滲透測試)

## 概述
自動化滲透測試（Autonomous Penetration Testing）是指利用人工智慧（強化學習、規劃演算法或大語言模型智能體），在無需或僅需最少人類干預的情況下，自主對目標電腦網絡進行弱點探勘、漏洞利用、權限提升與橫向移動的安全性評估技術。

## 演進歷程
1. **第一代：腳本噴射 (Script Spraying, ~2015)**：暴力嘗試所有已知漏洞，容易引發目標崩潰與強烈警報。
2. **第二代：深度強化學習 (DRL, 2018~2024)**：
   - 代表作：[[Takaesu2018-DeepExploit]], [[Microsoft2021-CyberBattleSim]], [[Pham2024-Raiju.md]]。
   - 將攻防轉化為馬可夫決策過程，透過獎勵訊號學會高成功率的利用路徑。
3. **第三代：LLM 智慧代理人 (LLM Agents, 2023~)**：
   - 代表作：[[Deng2023-PentestGPT]]。
   - 結合大語言模型的語義推理、任務樹規劃與終端日誌解析，具備靈活因應複雜未見場景的通用能力。

## 關聯文獻
- [[Pham2024-Raiju.md]]
- [[Deng2023-PentestGPT.md]]
- [[Takaesu2018-DeepExploit.md]]
- [[Microsoft2021-CyberBattleSim.md]]
- [[Schwartz2019-POMDPPenTest.md]]
