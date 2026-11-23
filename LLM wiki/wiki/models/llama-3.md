---
title: "Llama 3"
type: "model"
created: "2024-07-23"
last_updated: "2024-07-23"
aliases: ["Llama-3", "Llama 3.1", "Llama-3-405B"]
related: ["[[Grouped-Query Attention (GQA)]]", "[[Scaling Laws]]", "[[Test-Time Compute]]"]
sources: ["2024-07-23_2024-llama-3-herd"]
---

# Llama 3

## 核心定義與架構概述
Llama 3 是由 Meta AI 於 2024 年 7 月完整發布的開源旗艦大語言模型系列，包含 8B、70B 以及最高達 405B 的密集（Dense）自回歸 Transformer 模型。

該系列最具開創性的意義在於推動了極限數據規模下的 [[Scaling Laws]] 實踐：Meta 使用超過 15 兆（15T）高質量 Token 對模型進行預訓練，大幅超越傳統 Chinchilla 最優比例，驗證了小參數量模型（如 8B）在過度訓練（Over-training）條件下能展現極強的推論性價比。

## 架構特點
Llama 3 在模型架構上維持極度保守且標準的 Dense Transformer 設計，以確保各推理引擎的最大硬體相容性：
1. **注意力機制**：全系列（包括 8B 模型）統一採用 [[Grouped-Query Attention (GQA)]]，鍵值頭（KV Heads）設定為 8，大幅降低長序列推論時的顯存消耗。
2. **上下文長度與位置編碼**：在 Llama 3.1 階段將原生上下文長度擴展至 128K Tokens，採用調整後的 RoPE（Rotary Position Embedding）頻率基數。
3. **分詞器（Tokenizer）**：升級為 128K 詞表的 tiktoken 分詞器，顯著改善程式碼與多語言的壓縮率與編碼效率。

## 訓練與後訓練流程
Meta 團隊採用了高度自動化的迭代式後訓練（Post-training）循環：
- **合成資料生成（Synthetic Data Generation）**：405B 模型作為資料引擎，生成數百萬條用於程式碼、數學和推理的合成問答對。
- **混合對齊策略**：結合拒絕取樣（Rejection Sampling）、PPO 以及 DPO（Direct Preference Optimization），進行連續 6 輪（Rounds）以上的微調迭代。

## 產業影響與技術定位
Llama 3 405B 是人類首個在開源領域達到與同期頂級閉源模型（如 GPT-4, Claude 3.5 Sonnet）旗鼓相當的稠密模型，並成為後續研究（包含資料過濾、合成資料生成、以及蒸餾小模型）的重要學術基礎底座。
