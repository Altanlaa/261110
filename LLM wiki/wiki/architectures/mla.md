---
title: "Multi-Head Latent Attention (MLA)"
type: "architecture"
created: "2025-01-20"
last_updated: "2025-01-22"
aliases: ["MLA", "多頭潛在注意力機制"]
related: ["[[Grouped-Query Attention (GQA)]]", "[[DeepSeek-R1]]"]
sources: ["2025-01-22_2025-deepseek-r1"]
---

# Multi-Head Latent Attention (MLA)

## 核心定義與動機
Multi-Head Latent Attention (MLA) 是由 DeepSeek 團隊於 DeepSeek-V2 首次提出，並在 DeepSeek-V3 與 [[DeepSeek-R1]] 中發揚光大的創新型注意力機制。

其核心動機在於突破 [[Grouped-Query Attention (GQA)]] 在「顯存壓縮」與「模型表達力」之間的權衡邊界。GQA 雖然降低了 KV Cache 體積，但在本質上縮減了鍵值空間的有效維度。MLA 採用**低秩聯合壓縮（Low-rank Joint Compression）**，將 Key 與 Value 壓縮至一個低維潛在向量（Latent Vector），使得在推理階段僅需快取這個微小的潛在向量，從而實現比 GQA 激進數倍的 KV Cache 壓縮率，同時保持完全媲美 MHA 的強大表徵能力。

## 核心機制與解耦式 RoPE
MLA 的設計面臨一個巨大的數學挑戰：旋轉位置編碼（RoPE）依賴特定維度的幾何旋轉，無法直接與低秩矩陣結合並在推論前預先吸收合併。

為了解決此衝突，MLA 採用了巧妙的**解耦式 RoPE（Decoupled RoPE）**策略：
1. **內容向量（Content Part）**：Query 與 Key/Value 分別經過低秩壓縮投影，此部分不攜帶位置編碼，推論時可直接將解壓縮矩陣與後續投影矩陣在線性層合併。
2. **位置向量（Positional Part）**：額外分流出較低維度（如 64 維）的獨立向量，專門施加 RoPE。

推論時，每個 Token 的 KV Cache 僅需儲存低維潛在向量與單一共享的位置向量，在長序列推理中極大幅度解放了 GPU 記憶體頻寬。
