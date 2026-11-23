# AI 也能當駭客？——自動化滲透測試與強化學習智能體通識教學筆記

> **教學目標**：讓零資安與演算法背景的初學者，能以直觀的生活化比喻（迷宮尋寶、戰爭迷霧、球員教練），徹底理解人工智慧如何從早期的「亂槍打鳥腳本」，演進為能夠在複雜網路中自主決策、提權與橫向移動的「數位白帽駭客智能體」。  
> **知識庫閉環承諾**：本篇筆記之所有核心機制、實證數據與架構，100% 嚴格源自專案 Wiki 庫內已收錄之 5 篇核心文獻：[[Pham2024-Raiju.md]]、[[Deng2023-PentestGPT.md]]、[[Microsoft2021-CyberBattleSim.md]]、[[Takaesu2018-DeepExploit.md]] 與 [[Schwartz2019-POMDPPenTest.md]]。

---

## 一、直觀破冰：什麼是滲透測試？為什麼需要 AI 智能體？

想像一棟存放機密資料的超大型現代城堡（企業內部電腦網路）：
- **白帽駭客（道德滲透測試者）**：受城堡主人委託，扮演「神偷」，嘗試尋找城堡是否有沒上鎖的後門、鬆動的通風孔或偷懶守衛，並在壞蛋（黑帽駭客）入侵前提出修復報告。
- **傳統痛點**：現代企業網路動輒數萬台伺服器，資安專家每天要手動輸入成千上萬行終端機指令，人力極度匱乏；而傳統自動化工具只會「死板地把所有鑰匙（漏洞利用碼）一把一把硬插」，極易導致伺服器崩潰當機 (來源: [[Takaesu2018-DeepExploit.md]])。
- **解決方案**：賦予 AI「眼睛（掃描偵察）」、「大腦（強化學習與決策）」與「雙手（滲透工具鏈）」，打造自主滲透測試智能體 (來源: [[Autonomous Penetration Testing]])。

---

## 二、理論基石：戰爭迷霧下的遊戲（POMDP 數學形式化）

為什麼網路滲透不能像下圍棋一樣簡單？
- 圍棋是「完全資訊公開」的，棋盤上每顆棋子雙方都看得一清二楚；
- 網路滲透是**「帶有戰爭迷霧（Fog of War）的迷宮」**：站在城堡大門口，你根本不知道城堡內部有幾層樓、藏著什麼機關、守衛巡邏路線為何 (來源: [[Schwartz2019-POMDPPenTest.md]])。

### 數學建模：部分可觀察馬可夫決策過程 (POMDP)
Schwartz 等人將滲透測試形式化為 POMDP 七元組 $\langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, \gamma \rangle$：
1. **隱藏真實狀態 $\mathcal{S}$**：內網的真實拓撲與漏洞全貌（AI 看不見）。
2. **動作空間 $\mathcal{A}$**：探測、提權、嘗試攻擊。
3. **破碎觀測值 $\Omega$**：發送封包後回傳的有限狀態（如 Port 80 開啟、回傳 HTTP 403 錯誤碼）。
4. **信念狀態 (Belief State) $b(s)$**：AI 依據過去的探測經驗，在腦海中推算「城堡內部目前最可能是長什麼樣子」的機率分佈：
   $$b'(s') = \eta \cdot \mathcal{O}(o \mid s', a) \sum_{s \in \mathcal{S}} \mathcal{T}(s' \mid s, a) b(s)$$

---

## 三、技術演進一：從盲目射擊到深度強化學習 (DeepExploit & CyberBattleSim)

1. **破局者：DeepExploit 的 A3C 試驗** (來源: [[Takaesu2018-DeepExploit.md]])
   - 2018 年，三井物產資安團隊在 Black Hat 發表 DeepExploit，首次利用非同步優勢動作評價演算法（A3C）連接 Metasploit。
   - **大腦直覺**：神經網絡透過多執行緒並行訓練，學會「看到什麼服務版本，就只挑選最精準的 Exploit」，揮別盲目攻擊。
2. **沙盒模擬：微軟 CyberBattleSim** (來源: [[Microsoft2021-CyberBattleSim.md]])
   - 2021 年微軟開源 CyberBattleSim，將網絡抽象為有向圖 $G = (V, E)$，利用 DQN 訓練智能體在無害的虛擬模擬器中學會「橫向感染（Lateral Movement）」的最短路徑。

---

## 四、實戰突破：Raiju 的跨平台後滲透戰術

當 AI 突破大門進入電腦後，最危險的時刻才剛開始——**後滲透階段（Post-Exploitation）** (來源: [[Pham2024-Raiju.md]])。

### Raiju 框架的三大核心突破：
1. **10 維跨平台統一狀態向量**：打破過往研究只能測單一 OS 的局限，將 Windows UAC、管理員狀態與 Linux Root、核心漏洞編碼為緊湊特徵向量。
2. **99 個 Metasploit Exploit 封裝**：包含 95 個提權模組（PE）、2 個雜湊提取（GH）與 2 個 SMB 橫向移動（LM）。
3. **解決獎勵稀疏的 RW20 機制**：
   - 如果只在「拿下最高 Root 權限」給 $+100$ 分，AI 像大海撈針一樣很難學會。
   - Raiju 提出 **RW20 密集階梯獎勵**：收集資訊給小獎勵、成功提權給大獎勵、浪費時間重複無效嘗試給負懲罰。
4. **演算法對決：A2C 完勝 PPO**：
   - 實驗證實 Advantage Actor-Critic (A2C) 在滲透測試連續步驟中具備更高的探索效率，達到 **超過 84% 的平均利用成功率**！
   - 折扣累積回報推導：
     $$R_t = \sum_{i=t}^T \gamma^{i-t} r_i, \quad A(s_t, a_t) = R_t - V(s_t)$$

---

## 五、新世代浪潮：LLM 智慧指揮官 (PentestGPT)

雖然強化學習在封閉固定環境極強，但如果遇到從未見過的全新漏洞或複雜 Web 邏輯怎麼辦？
2024 年南洋理工大學在資安頂會 USENIX Security 發表了 **PentestGPT** (來源: [[Deng2023-PentestGPT.md]])：
- **三大模組分工解耦**：
  1. **Reasoning Module (參謀大腦)**：維護「滲透任務樹 (PTT)」，只看戰局大方向，不讀雜亂終端輸出，徹底解決上下文遺忘（Context Loss）。
  2. **Generation Module (前線部隊)**：將任務轉化為嚴格的命令語法（如 `nmap -sV`, `sqlmap`）。
  3. **Parsing Module (情報情報員)**：過濾並濃縮上萬行終端機輸出，僅提煉出核心情報呈報給參謀。
- **震撼成果**：在實戰靶場 HackTheBox (HTB) 中成功攻陷多台實體中高難度靶機，將任務完成率提高 $228\%$！

---

## 六、延伸學習文獻 (Literature Backlog)

欲深入探究網路自動化攻防智能體，推薦閱讀以下延伸文獻，文末提供直接下載連結：

1. **[AutoPT: Towards Autonomous Penetration Testing using LLM Agents](https://arxiv.org/pdf/2403.02517)** (arXiv:2403.02517)
   - 探討端到端自適應攻擊路徑生成與安全性邊界。
2. **[Reinforcement Learning for Cyber Defense: A Survey](https://arxiv.org/pdf/2303.03254)** (arXiv:2303.03254)
   - 全面綜述防守方如何利用 RL 反制自主攻擊智能體。
3. **[Automated Red Teaming at Scale with Language Models](https://arxiv.org/pdf/2406.12847)** (arXiv:2406.12847)
   - 探討如何利用多智能體大規模評估企業雲端防護缺口。
