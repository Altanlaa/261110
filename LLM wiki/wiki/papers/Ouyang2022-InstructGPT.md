---
title: "Training language models to follow instructions with human feedback"
authors: "Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, Ryan Lowe"
year: 2022
venue: "NeurIPS 2022"
arxiv: "2203.02155"
tags: [rlhf, ppo, alignment, instructgpt]
---

# Training language models to follow instructions with human feedback (InstructGPT)

## 1. 核心動機與問題定義
傳統大語言模型使用「次字預測（Next-Token Prediction）」在無標註網際網路語料上訓練，這導致模型目標為「模仿人類寫作文本的分佈」，而非「有幫助且真實地遵循人類指令（Helpful, Honest, Harmless）」。這產生了經典的目標錯位（Alignment Problem）。

## 2. 核心機制：人類回饋強化學習 (RLHF 三階段)
InstructGPT 建立了現代大模型對齊的三階段範式：
1. **監督式微調 (SFT)**：使用人類撰寫的高品質示範資料微調預訓練模型，得到 $\pi^{\text{SFT}}$。
2. **獎勵模型訓練 (Reward Modeling)**：輸入同一個提示的多個模型回應，由人類評審標註偏好排序，訓練純量獎勵模型 $r_\theta(x, y)$，損失函數為 Pairwise Ranking Loss：
   $$\mathcal{L}_{\text{RM}}(\theta) = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( r_\theta(x, y_w) - r_\theta(x, y_l) \right) \right]$$
3. **PPO 強化學習微調 (RL Fine-tuning)**：以 PPO 演算法更新策略 $\pi_\phi$，最大化人類獎勵，同時引入 KL 散度懲罰防止策略過度偏離 SFT 模型：
   $$\text{obj}(\phi) = \mathbb{E}_{(x, y) \sim \mathcal{D}_{\pi_\phi}} \left[ r_\theta(x, y) - \beta D_{\text{KL}}(\pi_\phi(y \mid x) \parallel \pi^{\text{SFT}}(y \mid x)) \right] + \gamma \mathbb{E}_{x \sim \mathcal{D}_{\text{pretrain}}} \left[ \log \pi_\phi(x) \right]$$

## 3. 重要意義
RLHF 成功證明了強化學習可以作為雕琢語言模型行為的強大控制器，後續的 DeepSeek-R1 與 Raiju 均在此基礎上衍生為純 RL (GRPO) 與自主 Agent 決策。

## 4. 關聯詞條
- [[RLHF and PPO]]
- [[DeepSeek-R1]]
- [[Actor-Critic and PPO]]
- [[Scaling Laws]]
