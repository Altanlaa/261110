---
title: "Pham2024-Raiju: RL-Guided Post-Exploitation for Automating Security Assessment"
type: "paper"
created: "2024-08-09"
last_updated: "2026-11-23"
aliases: ["Pham2024-Raiju", "Raiju", "Raiju Framework"]
related: ["[[A2C 與 PPO 在滲透測試之對比 (A2C vs PPO in Pentesting)]]", "[[Reinforcement Learning in Cybersecurity]]"]
sources: ["raw/papers/Raiju.pdf"]
tags: ["Reinforcement Learning", "Post-Exploitation", "Penetration Testing", "Metasploit", "A2C", "PPO"]
---

# Raiju: Reinforcement Learning-Guided Post-Exploitation for Automating Security Assessment of Network Systems

## 論文資訊 (Paper Metadata)
- **論文標題**：Raiju: Reinforcement learning-guided post-exploitation for automating security assessment of network systems
- **作者團隊**：Van-Hau Pham, Hien Do Hoang, Phan Thanh Trung, Van Dinh Quoc, Trong-Nghia To, Phan The Duy
- **發表期刊**：*Computer Networks* 253 (2024) 110706, Elsevier
- **DOI**：[10.1016/j.comnet.2024.110706](https://doi.org/10.1016/j.comnet.2024.110706)
- **原始來源**：`raw/papers/Raiju.pdf`

---

## 核心動機與問題定義 (Problem Formulation)
在滲透測試（Penetration Testing, PT）與紅隊演練（Red Teaming）中，攻擊者成功取得目標主機初始存取權限後的**後滲透階段（Post-Exploitation）**，是評估內部網路實質風險的最關鍵時期。其主要任務涵蓋三大目標：
1. **Privilege Escalation (PE, 權限提升)**：突破受限使用者權限，取得本機管理員（Windows Administrator / NT SYSTEM）或 Linux Root 權限。
2. **Gathering Hashdump (GH, 憑證雜湊提取)**：傾印並竊取帳號密碼雜湊，供進一步離線破解或權限傳遞（Pass-the-Hash）。
3. **Lateral Movement (LM, 橫向移動)**：以已攻陷節點作為跳板，橫向穿越內部子網，入侵相鄰主機或網域控制站（Domain Controller）。

**技術瓶頸**：
- 後滲透環境具備高度即時性、連續性與不確定性，傳統監督式學習（Supervised Learning）由於缺乏靜態標註資料集而無法適用。
- 現行滲透工具（如 Metasploit、Empire）需高度仰賴具備多年實戰經驗的資安專家手動決策，難以擴展。

---

## Raiju 系統架構與狀態-動作空間設計

Raiju 框架將強化學習智慧體（RL Agent）與開源滲透測試工具 Metasploit Framework (MSF) 及 Nmap 深度整合：

### 1. 10 維跨平台狀態特徵向量 (State Space)
為克服過往研究僅限單一作業系統（如僅支援 Windows 本地資訊）的局限，Raiju 定義了 10 項標準化環境特徵：
- `Platform`：目標作業系統類型（`0: Windows`, `1: Linux`, `-1: Unknown`）。
- `Windows 安全特徵`：`Windows UAC` 狀態、`Windows Admin Group`、`Windows Admin User`、`Windows System User`。
- `Linux 權限與核心特徵`：`Linux Root User`、`Linux Kernel Vuln`（核心是否存在已知漏洞）。
- `憑證狀態`：`Hashdump`（是否已成功提取帳密雜湊，`0: No`, `1: Yes`）。
- `網路拓撲特徵`：`Number of peers`（探勘到的相鄰主機數量）、`Peers index`、`Peer platform`。

### 2. 動作空間封裝 (Action Space)
Raiju 挑選並封裝了 Metasploit 中 99 個成熟的 Exploit 利用模組：
- **Privilege Escalation (PE)**：95 個模組（23 個 Windows 模組、72 個 Linux 模組）。
- **Gathering Hashdump (GH)**：2 個專屬密碼雜湊提取模組。
- **Lateral Movement (LM)**：2 個基於 SMB (Port 445) 服務的橫向滲透模組。

---

## 關鍵數學推導與演算法虛擬碼 (Mathematical Formulations)

### 1. 折扣累積獎勵函數 (Discounted Sum of Rewards)
智慧體在時間步 $t$ 的累積回報目標為：

$$R_t = \sum_{i=t}^T \gamma^{i-t} \cdot r_i$$

其中 $\gamma \in [0, 1]$ 為折現因子（實驗設為 $0.99$），$r_i$ 為單步獎勵。研究比較了兩種獎勵機制：
- **RW1**：成功得 $r_s = +1$，失敗扣 $r_f = -1$。
- **RW20（最優）**：成功得 $r_s = +20$，失敗扣 $r_f = -1$。由於滲透成功的動作極其稀疏，RW20 能有效放大正確決策的梯度訊號。

### 2. Advantage Actor-Critic (A2C) 損失函數與推導
A2C 藉由優勢函數 $A(s_t, a_t) = R_t - V_\phi(s_t)$ 縮放策略梯度：

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim p(\tau|\theta)} \left[ \sum_{t=0}^{T-1} \nabla_\theta \log \pi_\theta(a_t|s_t) A^{\pi_\theta}(s_t, a_t) \right]$$

A2C 綜合損失函數包含 Actor 損失、Critic 均方誤差（MSE）與鼓勵探索的熵正則化項（Entropy）：

$$\mathcal{L}_{A2C} = \mathcal{L}_{actor} + \mathcal{L}_{critic} - \beta \times \mathcal{H}(\pi_\theta(\cdot|s))$$

$$\mathcal{L}_{actor} = -\log \pi_\theta(a|s) \times A(s, a), \quad \mathcal{L}_{critic} = \text{MSE}(V(s), R_t)$$

$$\mathcal{H}(\pi_\theta(\cdot|s)) = -\sum_a \pi_\theta(a|s) \log \pi_\theta(a|s)$$

### 3. A2C 訓練演算法虛擬碼 (Algorithm Workflow)

```python
# A2C 訓練虛擬碼 (Algorithm 1 in Paper)
Require: envs, gamma, beta, N_episodes, T_steps
Ensure: Trained Actor network pi_theta, Critic network V_phi

def TrainA2C(envs, gamma, beta, N, T):
    init_actor_network(pi_theta)
    init_critic_network(V_phi)
    
    for episode in range(1, N + 1):
        for env in envs:
            s_0 = env.reset()
            trajectory = []
            
            # 1. 採樣軌跡 (Rollout)
            for t in range(1, T + 1):
                a_t = sample_from_policy(pi_theta(a | s_t))
                s_next, r_t = env.step(a_t)
                trajectory.append((s_t, a_t, r_t, s_next))
            
            # 2. 回溯計算累積回報與優勢 (Backtrack Return & Advantage)
            R_t = 0
            for t in reversed(range(1, T + 1)):
                R_t = r_t + gamma * R_t
                A_t = R_t - V_phi(s_t)
                
                # 3. 梯度更新 (Update Networks)
                update_critic(loss = (R_t - V_phi(s_t)) ** 2)
                update_actor(loss = -log_prob(pi_theta(a_t | s_t)) * A_t - beta * entropy)
                
    return pi_theta, V_phi
```

---

## 實驗評測與消融成果 (Experimental Results)

在 4 套涵蓋 Windows 7 與 Metasploitable 2 的真實混合拓撲環境（ENV1 至 ENV4）中進行 100 次完整測試：

| 評測指標 | Advantage Actor-Critic (A2C) | Proximal Policy Optimization (PPO) | Random Agent (RA) |
| :--- | :--- | :--- | :--- |
| **訓練時間 (2000 回合)** | **40 分鐘** (高效穩定) | 55 分鐘 (+37.5% 顯著耗時) | 無需訓練 |
| **Privilege Escalation (PE)** | **100% 成功率** | 100% (但探索步數較多) | 90%–100% |
| **Gathering Hashdump (GH)** | **>84% 成功率** | 30%–50% | 40%–50% |
| **Lateral Movement (LM)** | **>80% 成功率** (全網攻破) | 40%–50% (跨網段探索易發散) | <20% (高失敗率) |
| **平均完成攻擊步數** | **<55 步** (決策精準高效) | 70–80 步 (策略頻繁震盪) | 100+ 步 (接近超時上限) |

---

## 結論與對後續研究之啟發
1. **多環境平行採樣對對抗網路的高方差至關重要**：A2C 在跨主機滲透測試中顯著勝過 PPO，主因在於 A2C 能夠利用多環境非同步採樣有效平滑不同主機配置帶來的回報震盪。
2. **與真實滲透框架（Metasploit）整合之可行性**：Raiju 驗證了透過狀態抽象化，RL Agent 能夠直接驅動真實滲透工具庫完成端到端的紅隊攻防演練。
