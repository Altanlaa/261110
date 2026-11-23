---
title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
authors: "Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Denny Zhou"
year: 2022
venue: "ICLR 2023"
arxiv: "2203.11171"
tags: [reasoning, self-consistency, sampling, ensembling]
---

# Self-Consistency Improves Chain of Thought Reasoning in Language Models

## 1. 核心動機與研究背景
Chain-of-Thought (CoT) 雖然大幅提升了多步驟推理能力，但傳統推論通常採用**貪婪解碼（Greedy Decoding）**。若模型在推導的某一個微小步驟中犯錯，貪婪解碼無法回溯，錯誤將持續累積至最終結論。

## 2. 核心機制：自我一致性 (Self-Consistency)
人類面對複雜難題時，往往會從不同角度思考解題途徑，若多種獨立推導方法皆指向同一個結論，該結論正確的信心程度顯著提高。

Self-Consistency 的演算法流程：
1. **多路隨機採樣 (Temperature Sampling)**：設定溫度 $T > 0$，針對同一個 Prompt $X$ 自主回歸生成 $N$ 條不同的思維鏈路徑 $\{ (c^{(i)}, y^{(i)}) \}_{i=1}^N$。
2. **邊際化與多數表決 (Majority Voting)**：將中間思維鏈 $C$ 作為潛在變量（Latent Variable）進行邊際化，以邊際機率最大化選取最終答案 $\hat{y}$：
   $$\hat{y} = \arg\max_{y \in \mathcal{Y}} \sum_{i=1}^N \mathbf{1}(y^{(i)} = y)$$
   或者考慮每條鏈路的條件機率加權：
   $$\hat{y} = \arg\max_{y} \sum_{i=1}^N P(c^{(i)}, y \mid X)$$

## 3. 實驗成果
- 在 GSM8K 數據集上，Self-Consistency 在 PaLM 540B 基礎上進一步將準確率推升至 $74.4\%$（比常規 CoT 提升近 $18\%$）。
- 證明「推理時增加採樣預算」可以顯著轉化為任務精準度，奠定了後續 Test-Time Compute 的理論基石。

## 4. 關聯詞條
- [[Self-Consistency]]
- [[Chain of Thought (CoT)]]
- [[Test-Time Compute]]
- [[Math Reasoning Benchmarks]]
