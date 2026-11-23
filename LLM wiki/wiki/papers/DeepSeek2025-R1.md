---
title: "DeepSeek2025-R1: Incentivizing Reasoning Capability in LLMs via RL"
type: "paper"
created: "2025-01-22"
last_updated: "2026-11-23"
aliases: ["DeepSeek2025-R1", "DeepSeek-R1", "R1", "R1-Zero"]
related: ["[[Group Relative Policy Optimization (GRPO)]]", "[[Test-Time Compute]]", "[[Multi-Head Latent Attention (MLA)]]"]
sources: ["https://arxiv.org/pdf/2501.12948"]
tags: ["Reasoning", "Reinforcement Learning", "GRPO", "Distillation", "Cold-Start"]
---

# DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

## 論文資訊 (Paper Metadata)
- **論文標題**：DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning
- **作者團隊**：DeepSeek-AI
- **發表日期**：2025-01-22
- **arXiv 編號**：[arXiv:2501.12948](https://arxiv.org/abs/2501.12948)
- **PDF 下載**：[https://arxiv.org/pdf/2501.12948](https://arxiv.org/pdf/2501.12948)

---

## 核心動機與研究突破 (Problem & Motivation)
長期以來，大語言模型（LLM）的複雜邏輯推理由於依賴昂貴且稀缺的人類長思維鏈（Long Chain-of-Thought, CoT）標註資料，面臨 Scaling 瓶頸。

DeepSeek-R1 的核心突破在於證實：**在不經過任何監督式微調（Supervised Fine-Tuning, SFT）示範的前提下，直接於預訓練底座上執行純強化學習（Pure RL），即可自發激發出強大的多步驟邏輯推理、自我驗證與錯誤回溯（Backtracking）能力**。

---

## 核心演算法：Group Relative Policy Optimization (GRPO)

傳統 PPO 需維護與 Actor 等大的 Critic（Value）模型，在百億/千億參數模型訓練中帶來巨大的 GPU 顯存負擔。GRPO 徹底捨棄 Critic 模型，改為從同一 Prompt $q$ 中取樣一組 $G$ 個候選輸出 $\{o_1, \dots, o_G\}$，並以群組相對得分計算 Advantage：

### 1. Advantage 歸一化推導

$$A_i = \frac{r_i - \mu}{\sigma}, \quad \text{其中 } \mu = \frac{1}{G}\sum_{j=1}^G r_j, \quad \sigma = \sqrt{\frac{1}{G}\sum_{j=1}^G (r_j - \mu)^2}$$

### 2. 策略優化目標函數 (Objective Function)

$$\mathcal{J}_{GRPO}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\}_{i=1}^G \sim \pi_{\theta_{old}}(O|q)} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} A_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta \parallel \pi_{ref}) \right) \right]$$

其中 KL 散度懲罰項採用無偏估計量以防止策略大幅偏離預訓練底座：

$$\mathbb{D}_{KL}(\pi_\theta \parallel \pi_{ref}) = \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - \log \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - 1$$

---

## 訓練管線與湧現現象 (Training Pipeline)

1. **DeepSeek-R1-Zero（純 RL）**：
   - 僅依賴確定性規則獎勵：Accuracy Reward（數學/程式碼對錯判別 $0/1$）與 Format Reward（強制將思考內容封裝於 `<think>...</think>`）。
   - 自主湧現長思維鏈反思現象（如自發寫出「Wait, let me double check my derivation...」）。
2. **DeepSeek-R1 正式版（四階段混合管線）**：
   - 階段 1：數千條優質長思考資料進行 Cold-Start SFT，改善可讀性。
   - 階段 2：針對推理任務執行大規模 GRPO 訓練。
   - 階段 3：針對模型生成的推導結果進行 Rejection Sampling，混合通用資料進行次輪 SFT。
   - 階段 4：全場景偏好對齊強化學習。

---

## 評測指標與知識蒸餾 (Evaluation & Distillation)

| 評測基準 (Benchmark) | DeepSeek-R1-Zero | DeepSeek-R1 | OpenAI-o1 (正式版) |
| :--- | :--- | :--- | :--- |
| **AIME 2024 (Pass@1)** | 71.0% | **79.8%** (Cons@64: 92.3%) | 79.2% |
| **MATH-500 (Pass@1)** | 95.9% | **97.3%** | 96.4% |
| **Codeforces (Percentile)** | 88.0% | **96.3%** | 96.6% |

**知識蒸餾突破**：
以 DeepSeek-R1 產生的 80 萬條優質推理資料直接微調開源模型（Qwen-2.5-32B），其 AIME 2024 得分達到 **72.6%**，顯著超越直接在 32B 模型上運行純 RL 的效果，證明**大模型的思維鏈模式具備極高的可遷移性**。
