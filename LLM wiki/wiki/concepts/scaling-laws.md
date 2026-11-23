---
title: "Scaling Laws"
type: "concept"
created: "2024-07-23"
last_updated: "2024-07-23"
aliases: ["比例定律", "Chinchilla Scaling Laws", "Neural Scaling Laws"]
related: ["[[Llama 3]]", "[[Test-Time Compute]]"]
sources: ["2024-07-23_2024-llama-3-herd"]
---

# Scaling Laws

## 核心定義
Scaling Laws（神經網絡比例定律）描述了大語言模型在模型參數規模（$N$）、訓練資料 Token 數（$D$）與總計算量（$C \approx 6ND$）擴展時，交叉熵損失（Cross-Entropy Loss）與下游能力的冪律（Power-law）關係。

## 歷史演進：Kaplan 到 Chinchilla
1. **Kaplan 比例定律 (OpenAI, 2020)**：最初認為模型參數量 $N$ 的擴展權重高於資料量 $D$，建議每增加 $1\times$ 計算量時，優先增加參數量而非訓練資料。這導致了早期模型（如 GPT-3 175B 僅訓練 300B Tokens）普遍處於「嚴重欠擬合（Under-trained）」狀態。
2. **Chinchilla 比例定律 (DeepMind, 2022)**：Hoffmann 等人提出，在固定訓練算力最優預算下，參數量與資料量應當以大致等比例擴展（約 $D \approx 20N$）。

## 現代實踐：過度訓練 (Over-training) 的性價比突破
以 [[Llama 3]] 為代表的現代實踐打破了 Chinchilla 僅追求「訓練算力最優」的狹隘定義：
- Meta 在 8B 參數的模型上注入了高達 15T 的 Tokens（資料模型比達 $1875:1$）。
- 理由在於**推理成本的攤銷**：雖然訓練階段消耗了超出理論最優的計算算力，但模型參數量小（8B）使得全球部署與長期推論的顯存與延遲成本大幅降低。
- 此外，隨著預訓練規模逼近網路公開文字的上限，資料品質過濾與合成資料成為維持 Scaling 曲線斜率的關鍵支柱。
