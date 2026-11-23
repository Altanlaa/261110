---
title: "RLHF and PPO (人類回饋強化學習)"
category: "techniques"
tags: [rlhf, ppo, alignment, policy-optimization]
---

# RLHF and PPO (人類回饋強化學習)

## 概述
人類回饋強化學習（Reinforcement Learning from Human Feedback, RLHF）是將大語言模型從純粹的「網路文本模仿者」轉變為「人類可信賴助手」的核心技術範式。其採用近端策略最佳化（Proximal Policy Optimization, PPO）演算法，以獎勵函數作為引導訊號更新神經網絡權重。

## 核心方程式
在 PPO 階段，策略更新目標最大化人類獎勵訊號，並以 KL 散度作為正則化約束，防止模型遺忘原本的語言能力：

$$\mathcal{L}_{\text{PPO}}(\phi) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\phi) \hat{A}_t, \, \text{clip}(r_t(\phi), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right] - \beta D_{\text{KL}}(\pi_\phi \parallel \pi_{\text{ref}})$$

其中 $r_t(\phi) = \frac{\pi_\phi(a_t \mid s_t)}{\pi_{\text{old}}(a_t \mid s_t)}$ 代表機率比率，$\hat{A}_t$ 為優勢函數。

## 現代延伸與演化
- **純強化學習 (Pure RL)**：DeepSeek-R1 拔除人類獎勵模型與 Critic 網絡，改用規則型客觀獎勵（符號驗證與格式約束）與 GRPO，使得模型在沒有人類示範資料下自主湧現出反思能力。
- **智能體決策 (Agentic Decision)**：在 Raiju 中，PPO 被用於安全漏洞利用與滲透測試策略學習。

## 關聯詞條
- [[Ouyang2022-InstructGPT: Training language models to follow instructions with human feedback]]
- [[DeepSeek-R1]]
- [[Actor-Critic and PPO]]
- [[Group Relative Policy Optimization (GRPO)]]
