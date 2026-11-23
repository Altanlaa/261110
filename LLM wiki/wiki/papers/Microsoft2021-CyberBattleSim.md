---
title: "Microsoft2021-CyberBattleSim: Investigating Network Security via Reinforcement Learning"
type: "paper"
authors: "Christian Seifert, Michael Betser, William Blum, James Bono, Kate Farris, Emily Goren, Jesse Gomez, Justin Grana"
year: 2021
venue: "Microsoft Defender Research (arXiv:2104.09363)"
aliases: ["CyberBattleSim", "Microsoft2021-CyberBattleSim"]
related: ["[[Pham2024-Raiju.md]]", "[[Autonomous Penetration Testing]]", "[[POMDP in Cyber Operations]]"]
tags: ["Reinforcement Learning", "Gym Environment", "Network Security", "Lateral Movement", "Cyber Defense"]
---

# CyberBattleSim: Investigating Network Security via Reinforcement Learning

## 1. 論文資訊 (Paper Metadata)
- **論文標題**：CyberBattleSim: An experimental platform for investigating the run-time security of networks through the lens of reinforcement learning
- **研究機構**：Microsoft Defender Research (微軟資安防護研究團隊)
- **發表時間**：2021 年 (arXiv:2104.09363)
- **開源專案**：[github.com/microsoft/CyberBattleSim](https://github.com/microsoft/CyberBattleSim)

---

## 2. 核心動機與研究定位
真實企業網路環境中，紅隊（攻擊方）與藍隊（防禦方）的對抗是動態博弈過程。然而直接在實體企業網路訓練強化學習會帶來不可逆的破壞風險。
微軟提出了基於 Python OpenAI Gym 的抽象模擬環境 **CyberBattleSim**，將電腦網絡建模為有向圖（Directed Graph），讓強化學習智能體可以在高度模擬但安全的環境中探索最優攻擊路徑。

---

## 3. 網絡攻擊環境形式化 (RL Environment Formulation)

1. **圖譜狀態表示 (Graph-based State Space)**：
   - 網絡表示為拓撲圖 $G = (V, E)$，節點 $v \in V$ 代表主機、路由器或資料庫，邊 $e \in E$ 代表連線許可。
   - 每個節點具備多個屬性：作業系統版本、開放服務協定（SMB、HTTP、SSH）、已知漏洞（CVE）。
2. **攻擊者動作空間 (Action Space)**：
   - **Local Attack**：在已攻陷節點上進行特權提升。
   - **Remote Exploit**：從已攻陷節點發起遠端攻擊，嘗試感染鄰近可見節點。
   - **Connect & Authenticate**：使用竊取到的帳號密碼憑證，合法登入其他節點。
3. **獎勵函數設計 (Reward Function)**：
   - 發現新節點給予小額獎勵（$+1$）。
   - 成功取得目標節點權限給予中額獎勵（$+10$）。
   - 攻陷核心網域控制站或客戶資料庫給予最高獎勵（$+100$）。
   - 發起無效攻擊或觸發防禦警報給予懲罰（$-1$）。

---

## 4. 核心發現與意義
- 證實了 DRL（深度 Q 網絡 DQN）在拓撲結構隨機變動的動態網路中，能夠學會「最短路徑橫向移動感染策略」。
- 成為後續 Raiju、DeepExploit 等研究驗證強化學習演算法有效性的標準基礎概念模型。

---

## 5. 關聯詞條
- [[Pham2024-Raiju.md]]
- [[Autonomous Penetration Testing]]
- [[POMDP in Cyber Operations]]
- [[Deng2023-PentestGPT.md]]
