---
title: "Chain of Thought (CoT)"
category: "concepts"
tags: [reasoning, cognitive, zero-shot, few-shot]
---

# Chain of Thought (思維鏈)

## 概述
思維鏈（Chain of Thought, 簡稱 CoT）是一種引導大語言模型進行多步驟複雜推理的提示技術與認知機制。其核心在於打破直接預測最終答案的捷徑，強制模型將複雜問題拆解為由連續自然語言句子組成的中間推導步驟。

## 核心機制與「草稿紙」比喻
人類在進行多位數乘法或邏輯題目時，無法僅憑大腦直覺「一眼看穿」答案，必須藉由一張「草稿紙」逐步記錄中間運算狀態。
自回歸 Transformer 本身缺乏內在循環反覆運算結構，每個 Token 生成時的計算時間是固定的。因此：
- **傳統 Prompt**：模型只有單次前向傳播（Forward Pass）來決定最終解答，容易因算力不足而猜測錯誤。
- **思維鏈 CoT**：生成的中間步驟 Token（如「首先計算 15 * 3 = 45」）重新輸入 Transformer 的自注意力層，使得後續結論能夠以先前計算成果為條件機率基礎，等效擴增了「測試期計算量（Test-Time Compute）」。

## 關聯論文與概念
- [[Wei2022-ChainOfThought: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
- [[Self-Consistency]]
- [[Test-Time Compute]]
- [[DeepSeek-R1]]
