---
title: "A2C 與 PPO 在滲透測試之對比 (A2C vs PPO in Pentesting)"
type: "technique"
created: "2024-08-09"
last_updated: "2024-08-09"
aliases: ["A2C vs PPO", "滲透測試強化學習演算法"]
related: ["[[Raiju 後滲透自動化框架 (Raiju Framework)]]"]
sources: ["2024-08-09_raiju-rl-post-exploitation"]
---

# A2C 與 PPO 在滲透測試之對比 (A2C vs PPO in Pentesting)

## 核心定義與演算法背景
在網路安全滲透測試（Penetration Testing）中，智慧體（Agent）需要在離散且龐大的動作空間（如數十至上百種 Exploit 模組）中探索。傳統 DQN（Deep Q-Networks）在大型動態動作空間中更新 Q 值的計算開銷過大，容易發生策略退化。因此，基於策略梯度的 Actor-Critic 演算法成為主流選擇。

[[Raiju 後滲透自動化框架 (Raiju Framework)]] 深度評估了兩大經典策略優化演算法：**Advantage Actor-Critic (A2C)** 與 **Proximal Policy Optimization (PPO)**。

---

## 1. Advantage Actor-Critic (A2C)
A2C 結合策略網絡（Actor）與價值評估網絡（Critic）。Actor 生成動作機率分佈 $\pi_\theta(a|s)$，Critic 估計狀態價值 $V_\phi(s)$。

其核心優勢在於引入**優勢函數（Advantage Function）** $A^{\pi_\theta}(s_t, a_t) = R_t - V_\phi(s_t)$，衡量特定動作相較於平均狀態價值的超額回報：

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim p(\tau|\theta)} \left[ \sum_{t=0}^{T-1} \nabla_\theta \log \pi_\theta(a_t|s_t) A^{\pi_\theta}(s_t, a_t) \right]$$

A2C 的總體損失函數包含 Actor 損失、Critic 均方誤差（MSE）與鼓勵探索的熵正則化項（Entropy）：

$$\mathcal{L}_{A2C} = \mathcal{L}_{actor} + \mathcal{L}_{critic} - \beta \times \mathcal{H}(\pi_\theta(\cdot|s))$$

其中 $\mathcal{L}_{actor} = -\log \pi_\theta(a|s) \times A$，$\mathcal{L}_{critic} = \text{MSE}(V(s), R_t)$。

---

## 2. Proximal Policy Optimization (PPO)
PPO 透過截斷機制（Clipped Surrogate Objective）限制策略更新幅度，防止新舊策略偏離過大：

$$\mathcal{L}_{CLIP}(\theta) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right], \quad \text{其中 } r_t(\theta) = \frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}$$

---

## 3. 滲透測試實戰橫向評測 (A2C vs. PPO)

在 Raiju 的四個實體測試環境中，實驗揭示了顯著的性能差距：

| 評測維度 | Advantage Actor-Critic (A2C) | Proximal Policy Optimization (PPO) |
| :--- | :--- | :--- |
| **訓練時間開銷** | **快** (2000 回合耗時 40 分鐘) | **慢** (2000 回合耗時 55 分鐘，需儲存歷史比對) |
| **多環境平行取樣** | **高度優異** (顯著降低環境間的梯度方差) | 容易受多環境動態重置影響而陷入局部最優 |
| **權限提升 (PE) 成功率** | 100% | 100% (但平均需多花 3–5 倍探索步數) |
| **橫向移動 (LM) 成功率** | **>80%** | 40%–50% (在多主機跨平台拓撲中穩定性差) |
| **所需平均攻擊步數** | **<55 步** (決策路徑短且果斷) | ~70–80 步 (策略探索波動大) |

### 核心結論
在後滲透情境下，由於狀態空間具有離散、稀疏且跨主機跳躍的特性，**A2C 藉由多環境非同步平行探索與精確的優勢縮放，顯著優於 PPO**，成為自動化紅隊工具的最佳演算法基底。
