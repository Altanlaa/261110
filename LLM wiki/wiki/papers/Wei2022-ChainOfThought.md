---
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
authors: "Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Florencia Fei, Ed Chi, Quoc Le, Denny Zhou"
year: 2022
venue: "NeurIPS 2022"
arxiv: "2201.11903"
tags: [reasoning, chain-of-thought, prompting, few-shot]
---

# Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

## 1. 核心動機與研究背景
大型語言模型（LLM）在許多自然語言任務上表現出色，但在多步驟符號邏輯與數學推理題（如 GSM8K、SVAMP）上經常遭遇瓶頸。傳統 Few-shot Prompting 直接要求模型輸出最終答案，導致模型在複雜推導中缺乏「工作記憶（Working Memory）」緩衝區。

## 2. 核心機制：思維鏈 (Chain of Thought, CoT)
CoT 的核心思想極度直觀：在提供給模型的 Few-shot 範例中，不只是「問題 $\rightarrow$ 答案」，而是在問題與答案之間人為插入「逐步推理的中間步驟（Chain of Thought）」。

形式化而言，傳統生成目標為：
$$P(Y \mid X) = \prod_{t=1}^{|Y|} P(y_t \mid X, y_{<t})$$

而引入思維鏈 $C = (c_1, c_2, \dots, c_k)$ 後，生成過程轉化為兩階段條件機率：
$$P(C, Y \mid X) = P(C \mid X) \cdot P(Y \mid X, C)$$

其中 $C$ 充當自回歸生成時的「大腦草稿紙」，讓後續 Token 的生成建立在先前推導的中間結論之上。

## 3. 核心發現與實驗指標
- **湧現能力 (Emergent Ability)**：CoT 的優勢在模型規模小於 $\sim 100\text{B}$ 參數時並不明顯，只有在超大規模模型（如 PaLM 540B、GPT-3 175B）中才會展現出非線性的巨大突破。
- **GSM8K 突破**：在 PaLM 540B 上，標準 Prompting 的準確率僅為 $17.9\%$，加入 CoT 後暴增至 $56.9\%$，大幅超越當時最佳微調模型。

## 4. 關聯詞條
- [[Chain of Thought (CoT)]]
- [[Test-Time Compute]]
- [[Self-Consistency]]
- [[Math Reasoning Benchmarks]]
