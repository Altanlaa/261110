---
title: "Math Reasoning Benchmarks"
type: "evaluation"
created: "2025-01-22"
last_updated: "2025-01-22"
aliases: ["數學推理評測", "MATH-500", "AIME", "GSM8K"]
related: ["[[DeepSeek-R1]]", "[[Test-Time Compute]]"]
sources: ["2025-01-22_2025-deepseek-r1"]
---

# Math Reasoning Benchmarks

## 演進脈絡與核心定位
數學推理評測是檢驗大語言模型多步驟邏輯演繹、符號推導與深度反思能力的最核心試金石。相較於易受資料污染（Data Contamination）或模糊語義影響的問答任務，數學評測具備客觀唯一答案，能透過正則或確定性腳本精確判定對錯。

## 主流基準測試梯隊
1. **GSM8K (Grade School Math 8K)**：小學等級的多步驟應用題。在 2023-2024 年間曾為主流基準，但現代前沿模型（如 GPT-4o, Claude 3.5, [[Llama 3]] 70B）得分普遍超越 95%，出現嚴重飽和。
2. **MATH / MATH-500**：涵蓋高中代數、幾何、微積分與數論的競賽題庫。MATH-500 為社群廣泛採用的 500 題無偏測試子集，目前 [[DeepSeek-R1]] 與 OpenAI-o1 正式版皆已突破 96%–97%。
3. **AIME (American Invitational Mathematics Examination)**：美國數學邀請賽題目，代表當前非專業數學家的最高競賽水平。每一題皆需要複雜的多步推導、構造性幾何或精密組合計數。在 AIME 2024 上，純粹前饋生成的傳統大模型得分通常低於 30%，而結合 [[Test-Time Compute]] 的推理模型（如 R1、o1）已取得 79%–85% 以上的高分。

## 評測指標計算方式
- **Pass@1**：單次取樣生成的解答中，答案正確的比例。代表模型的基準確定性能力。
- **Consensus@K / Majority Voting**：針對同一題目獨立取樣 $K$ 次解法（如 $K=64$），由最高票數的答案作為最終答案。
- **Pass@K**：在 $K$ 次取樣中，只要有任意一次命中正確答案即算通過，通常用於估計模型可能探索到的能力上限。
