---
id: note-deepseek-r1-reasoning
title: "DeepSeek-R1 與大語言模型推理能力激發機制研究"
date: "2026-11-16"
type: "research-note"
wiki_grounded_articles: 
  - "[[DeepSeek-R1]]"
  - "[[Group Relative Policy Optimization (GRPO)]]"
  - "[[Multi-Head Latent Attention (MLA)]]"
  - "[[Test-Time Compute]]"
  - "[[Math Reasoning Benchmarks]]"
  - "[[Scaling Laws]]"
status: "completed"
---

# DeepSeek-R1 與大語言模型推理能力激發機制研究

> **【知識庫約束聲明】**
> 本筆記之技術正文**完全嚴格基於本專案 Wiki 知識庫**已有之收錄詞條撰寫，涵蓋 [[DeepSeek-R1]]、[[Group Relative Policy Optimization (GRPO)]]、[[Multi-Head Latent Attention (MLA)]]、[[Test-Time Compute]]、[[Math Reasoning Benchmarks]] 與 [[Scaling Laws]]。
> 任何超出既有 Wiki 範圍的外部文獻，均隔離列於文末「建議參考文獻」清單，提供直接下載與後續 Wiki 化連結。

---

## 一、研究背景：從預訓練擴展到測試期計算量擴展

長期以來，大語言模型的性能演進主要遵循 [[Scaling Laws]]。Kaplan 與 Chinchilla 等定律確立了模型參數規模 $N$ 與預訓練資料量 $D$ 的擴展關係。然而，隨著網路公開高質量文字資源逼近極限，單純增加預訓練算力的邊際效益開始遞減。

[[Test-Time Compute]] 代表了全新的範式轉移：**透過允許模型在生成最終答案前投入計算資源進行思維推導、自我驗證與錯誤回溯，可以在固定參數量的前提下實現複雜推理能力的突破**。DeepSeek-R1 的問世，驗證了不依賴龐大人類 SFT 資料、純粹藉由強化學習自發激發長思維鏈（Long CoT）的可行性。

---

## 二、DeepSeek-R1-Zero 的純 RL 湧現機制

根據 [[DeepSeek-R1]] 的收錄記載，研究團隊首先在預訓練底座 `DeepSeek-V3-Base` 上進行了極端實驗——**完全不引入任何人類標註 SFT 冷啟動資料，直接實施純強化學習**，誕生了 `DeepSeek-R1-Zero`。

### 1. 規則導向的獎勵函數
R1-Zero 捨棄了容易遭受博弈（Reward Hacking）的神經網絡獎勵模型，轉而採用客觀的規則校驗：
- **正確性獎勵（Accuracy Reward）**：針對數學題與代碼題，直接比對確定性數值答案或通過編譯器單元測試，給予 $0$ 或 $1$ 的二元反饋。
- **格式獎勵（Format Reward）**：強制要求模型將內部思維過程封裝於 `<think>...</think>` 標籤中。

### 2. 自主認知行為湧現
在連續的 RL 步數推進下，模型自發性展現出高階人類思維特徵：
- **長思維鏈自發擴展**：推理 Token 數隨訓練步數呈指數級拉長。
- **自我驗證與回溯（Backtracking）**：模型在思考過程中自發出現「Wait, let me rethink this...」等轉折，推翻前述錯誤邏輯並重新構建解法。

---

## 三、演算法突破：Group Relative Policy Optimization (GRPO)

根據 [[Group Relative Policy Optimization (GRPO)]]，該演算法是支撐 R1 大規模訓練的核心數學基石。其最大貢獻在於**徹底拔除 PPO 框架中龐大的 Critic（Value）模型，大幅削減顯存負載**。

### 1. 數學推導機制
針對特定輸入 Prompt $q$，GRPO 自當前策略 $\pi_\theta$ 取樣一組 $G$ 個候選回應 $\{o_1, o_2, \dots, o_G\}$，並透過客觀規則計算純量得分 $\{r_1, r_2, \dots, r_G\}$。

組內優勢函數（Advantage）直接透過群組均值 $\mu$ 與標準差 $\sigma$ 進行相對正規化：

$$A_i = \frac{r_i - \mu}{\sigma}, \quad \text{其中 } \mu = \frac{1}{G}\sum_{j=1}^G r_j, \quad \sigma = \sqrt{\frac{1}{G}\sum_{j=1}^G (r_j - \mu)^2}$$

GRPO 的策略優化目標函數為：

$$\mathcal{J}_{GRPO}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)} A_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta \parallel \pi_{ref}) \right) \right]$$

### 2. 主流演算法對比
| 演算法 | 需要 Critic 模型 | 顯存負載 | 優勢估計機制 | 核心定位 |
| :--- | :--- | :--- | :--- | :--- |
| **PPO** | 是（通常與 Actor 等大） | 極高 | GAE (依賴狀態價值網絡) | 通用人類偏好對齊 |
| **DPO** | 否（離線靜態微調） | 低 | 隱含獎勵推導 (成對偏好) | 靜態成對資料微調 |
| **GRPO** | **否（群組動態取樣）** | **極低** | **群組相對分數正規化** | **可客觀驗證之長推理探索** |

---

## 四、底層架構協同：Multi-Head Latent Attention (MLA)

根據 [[Multi-Head Latent Attention (MLA)]]，在長上下文多輪思考中，傳統 MHA 導致的 KV Cache 顯存頻寬成為極大瓶頸。即便 [[Grouped-Query Attention (GQA)]] 縮減了頭數，依然損害了鍵值空間維度。

MLA 透過低秩聯合壓縮（Low-rank Joint Compression），在推論時僅快取低維潛在向量 $c^{KV}$，配合解耦式 RoPE 策略，使得 DeepSeek-R1 能在長達數萬 Token 的長思維鏈推理下，維持極高的吞吐量與極低顯存佔用。

---

## 五、評測指標與知識蒸餾能力躍遷

根據 [[Math Reasoning Benchmarks]] 與 [[DeepSeek-R1]] 詞條：
- **AIME 2024**：Pass@1 達到 **79.8%**（Consensus@64 達 **92.3%**），媲美 OpenAI-o1 正式版。
- **MATH-500**：Pass@1 達到 **97.3%**。
- **蒸餾實驗**：藉由 R1 輸出的 80 萬條優質推理資料微調 Qwen-2.5-32B，其 AIME 達到 72.6%，驗證了「**大模型探索出的推理邏輯可高效蒸餾給小模型**」。

---

## 六、知識庫目前邊界與局限說明
目前我們的 Wiki 知識庫已完整覆蓋上述 R1、GRPO、MLA 與數學評測的核心機理，但對於以下維度**尚未收錄**：
1. 過程獎勵模型（Process Reward Models, PRM）與結果獎勵模型（ORM）的細緻對比。
2. 測試期計算量在不同難度題目下的動態自適應分配演算法（Compute-optimal Scaling）。
3. 非數學程式類（如創意寫作、多輪自由對話）中推理標籤帶來的負面影響（Reasoning Tax）。

---

## 七、建議參考文獻（Pending Ingestion Backlog）

以下為針對上述知識缺口自學術網絡檢索到的關鍵文獻，提供直接下載連結與預計維基化目標：

| 論文名稱 | 來源與下載連結 | 核心貢獻摘要 | 建議 Wiki 化分類 |
| :--- | :--- | :--- | :--- |
| **DeepSeek-R1 Official Technical Report** | [📥 下載 PDF (arXiv:2501.12948)](https://arxiv.org/pdf/2501.12948) | 官方完整技術報告，詳解 Cold-start 格式微調與多階段 RL | `models/deepseek-r1.md` |
| **DeepSeek-V3 Technical Report** | [📥 下載 PDF (arXiv:2412.19437)](https://arxiv.org/pdf/2412.19437) | MLA 與 DeepSeekMoE 架構的完整數學推導與預訓練細節 | `architectures/mla.md` |
| **Scaling LLM Test-Time Compute Optimally** | [📥 下載 PDF (arXiv:2408.03314)](https://arxiv.org/pdf/2408.03314) | 證明測試期計算在特定難題下比擴大參數量有效 4 倍以上 | `concepts/test-time-compute.md` |
| **Kimi k1.5 Technical Report** | [📥 下載 PDF (arXiv:2501.12599)](https://arxiv.org/pdf/2501.12599) | 長上下文多模態長思考模型的強化學習與視覺推理實踐 | `models/kimi-k1-5.md` |
