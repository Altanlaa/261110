---
title: "Self-Consistency (自我一致性)"
category: "techniques"
tags: [decoding, ensemble, sampling, reasoning]
---

# Self-Consistency (自我一致性)

## 概述
自我一致性（Self-Consistency）是由 Google Research 於 2022 年提出的一種用於提升大語言模型多步驟推理可靠性的集成解碼策略。

## 機制解析
傳統解碼多採用貪婪搜尋（Greedy Search），一旦其中一個推導步驟出現隨機噪聲或幻覺，該錯誤便不可逆。
自我一致性利用了人類思維中的直觀特性：**「複雜問題的解法可能百百種，但正確的答案往往是一致的」**。

### 演算法流程
1. **多路徑採樣**：設定適度隨機性（如 Temperature = 0.7），讓模型對同一個輸入問題生成 $k$ 條獨立的推導思維鏈。
2. **答案提取與邊際化**：從各條思維鏈結尾提取出最終數值或結論 $y_1, y_2, \dots, y_k$。
3. **多數表決 (Majority Vote)**：統計出現頻率最高的答案作為最終輸出。

$$y^* = \arg\max_y \sum_{i=1}^k \mathbb{I}(y_i = y)$$

此方法無需重新微調模型權重，純粹透過推論階段的並行計算，大幅消弭單一思維鏈的偶然錯誤。

## 關聯文獻與概念
- [[Wang2022-SelfConsistency: Self-Consistency Improves Chain of Thought Reasoning in Language Models]]
- [[Chain of Thought (CoT)]]
- [[Test-Time Compute]]
