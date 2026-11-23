---
title: "Group Relative Policy Optimization (GRPO)"
type: "technique"
created: "2025-01-22"
last_updated: "2025-01-22"
aliases: ["GRPO", "群組相對策略優化"]
related: ["[[DeepSeek-R1]]", "[[Test-Time Compute]]", "[[Math Reasoning Benchmarks]]"]
sources: ["2025-01-22_2025-deepseek-r1"]
---

# Group Relative Policy Optimization (GRPO)

## 核心定義與動機
Group Relative Policy Optimization (GRPO) 是一種專門為大語言模型強化學習設計的無 Critic 模型（Critic-free）策略梯度演算法。由 DeepSeek 團隊於 DeepSeek-Math 與 [[DeepSeek-R1]] 中提出並廣泛應用。

在傳統的 PPO（Proximal Policy Optimization）框架中，通常需要維護一個與演員模型（Actor / Policy）參數量相當的評論家模型（Critic / Value Model），用於估計每個 Token 的狀態價值 $V(s)$。對於數百億甚至數千億參數的大模型，這意味著：
1. 訓練期間顯存負載倍增（需常駐 Actor、Critic、Reference、Reward 四個大模型）。
2. Value 網絡訓練不穩定，經常成為整個 RL 管線的收斂瓶頸。

GRPO 徹底捨棄了獨立的 Critic 模型，改為**直接從同一 Prompt 取樣的一組候選輸出（Group of Outputs）的相對得分中計算優勢函數（Advantage）**。

## 數學機制與演算法流程
針對每一個輸入 Prompt $q$，GRPO 的執行機制如下：

1. **群組取樣**：從當前策略 $\pi_\theta$ 取樣生成一組 $G$ 個不同的候選回應 $\{o_1, o_2, \dots, o_G\}$。
2. **計算獎勵**：利用規則檢驗器或獎勵模型計算各回應的純量獎勵 $\{r_1, r_2, \dots, r_G\}$。
3. **組內標準化優勢估計**：對群組內的獎勵計算均值 $\mu$ 與標準差 $\sigma$，每個候選回應的優勢函數正規化為：
   $$A_i = \frac{r_i - \mu}{\sigma}$$
4. **策略更新目標**：目標函數最大化截斷策略比率，同時加入 KL 散度懲罰（或約束）以防止策略崩潰：
   $$\mathcal{J}_{GRPO}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)} A_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) \right) \right]$$

## 與主流 RL 演算法之比較
| 演算法 | 需要 Critic 模型 | 記憶體開銷 | 優勢估計方式 | 主要適用情境 |
| :--- | :--- | :--- | :--- | :--- |
| **PPO** | 是（通常與 Actor 等大） | 極高 | Generalized Advantage Estimation (GAE) | 通用對齊、人類偏好微調 |
| **DPO** | 否（離線無損微調） | 低 | 隱含獎勵推導（Implicit Reward） | 成對資料微調，缺乏長思考探索 |
| **GRPO** | **否（群組平均基準）** | **極低** | **群組相對得分正規化** | **數學/代碼等可客觀驗證之長推理探索** |

## 優勢與局限
- **優勢**：顯存節省高達 40%–50%，訓練吞吐量大幅提高；群組取樣天然契合思維鏈的多樣性探索。
- **局限**：組大小 $G$ 的選擇至關重要（通常 $G \ge 16$），若組內候選輸出的品質完全相同（例如全部答錯導致均值與標準差為 0），則無有效梯度產生。
