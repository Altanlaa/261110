---
title: "Grouped-Query Attention (GQA)"
type: "architecture"
created: "2024-07-23"
last_updated: "2024-07-23"
aliases: ["GQA", "分組查詢注意力"]
related: ["[[Llama 3]]", "[[Multi-Head Latent Attention (MLA)]]"]
sources: ["2024-07-23_2024-llama-3-herd"]
---

# Grouped-Query Attention (GQA)

## 核心定義與動機
Grouped-Query Attention (GQA) 是一種介於多頭注意力（Multi-Head Attention, MHA）與多查詢注意力（Multi-Query Attention, MQA）之間的注意力架構。其主要目標是**解決大語言模型在自回歸解碼時，Key-Value (KV) Cache 所帶來的 GPU 顯存容量與記憶體頻寬（Memory Bandwidth）瓶頸**。

在傳統 MHA 中，每個 Query 頭皆擁有專屬的 Key 頭與 Value 頭。在長上下文或大批次（Batch Size）推理情境下，KV Cache 隨長度線性成長，導致記憶體存取成為整個推理速度的最大限制。
- **MQA**：所有 Query 頭強制共享單一組 Key 和 Value 頭。KV Cache 壓縮最大，但顯著損害模型容量與複雜任務性能。
- **GQA**：將 Query 頭均勻分組，每組共享一組 Key 和 Value 頭。

## 架構原理對比
若模型具有 $H$ 個 Query 頭，GQA 將其劃分為 $G$ 個組，每組包含 $H / G$ 個 Query 頭，對應 1 個 Key 頭與 1 個 Value 頭。

| 架構 | KV 頭數量 | KV Cache 記憶體佔用 | 表達能力 / 任務準確率 |
| :--- | :--- | :--- | :--- |
| **MHA** | $H$ | 基準 ($1\times$) | 最高 |
| **GQA** | $G$ (通常為 8) | 約 $G / H$ (通常降至 $1/4 \sim 1/8$) | 接近 MHA，幾乎無顯著退化 |
| **MQA** | $1$ | 最低 ($1/H$) | 易在長文理解與細粒度檢索中退化 |

## 業界應用
GQA 已經成為當代主流開源密集模型的標準配置，包括：
- [[Llama 3]] 系列（8B、70B、405B 全面採用 8 個 KV Heads）
- Mistral 7B / Mixtral 8x7B
- Qwen 2 / 2.5 系列
- Gemma 2 系列
