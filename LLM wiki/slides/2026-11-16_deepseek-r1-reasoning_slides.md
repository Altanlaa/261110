---
title: "DeepSeek-R1 推理機制與演算法演進簡報企劃"
date: "2026-11-16"
source_note: "notes/2026-11-16_deepseek-r1-reasoning.md"
style: "Clean Academic White"
total_slides: 8
---

# DeepSeek-R1 推理機制與演算法演進簡報企劃

---

## Slide 1: 封面 (Title Slide)
- **Title**: DeepSeek-R1 推理能力激發機制
- **Subtitle**: 從 GRPO 策略優化到測試期計算量擴展 (Test-Time Compute)
- **Visual Cue**: 簡約居中排版、學術藍色焦點、副標題與作者日期資訊
- **Speaker Notes**:
  > 各位好，今天我們探討大語言模型在推理架構上的最新演進。聚焦於 DeepSeek-R1 如何突破傳統 SFT 冷啟動限制，透過純強化學習與 GRPO 演算法，在數學與邏輯任務上激發出自發性反思與長思維鏈。

---

## Slide 2: 範式轉移：從 Pre-training Scaling 到 Test-Time Compute
- **Title**: 範式轉移：大模型算力配置的新維度
- **Core Bullets**:
  - **預訓練邊際效益遞減**：傳統 Scaling Laws ($C \approx 6ND$) 受限於高品質文字資料極限。
  - **推論期思維擴展**：允許模型在產出答案前進行思考探索、自我檢驗與回溯。
  - **算力分配重構**：固定參數規模下，藉由增加推理期 Token 數實現幾何級精度躍升。
- **Visual Cue**: 左右兩欄對照卡片（左：Pre-training Scaling vs 右：Test-Time Compute）
- **Speaker Notes**:
  > 過去幾年整個 AI 領域都在追逐預訓練參數量與資料規模。但到了 2024–2025 年，高質量人類語料即將耗盡。新的戰場轉移到了測試期計算量：讓模型學會「深思熟慮」，在輸出前自發探索替代路徑。

---

## Slide 3: 核心突破：DeepSeek-R1-Zero 的純 RL 湧現現象
- **Title**: DeepSeek-R1-Zero：無冷啟動的純強化學習
- **Core Bullets**:
  - **零人類示範 (Zero SFT)**：直接於預訓練底座上執行強化學習。
  - **純規則獎勵驅動**：客觀數學判題 ($0/1$) + `<think>` 格式約束，杜絕 Reward Hacking。
  - **自主認知行為湧現**：模型自發學會長思維鏈、回溯探索 (Backtracking) 與自我糾錯。
- **Visual Cue**: 居中流程圖（Base Model -> 純 RL (GRPO) -> 自發反思湧現），高亮「Wait, let me rethink...」
- **Speaker Notes**:
  > R1-Zero 最震撼學界的地方，在於它完全沒有使用任何人寫的 CoT 示範。僅僅給予客觀的對錯獎勵，模型在 RL 訓練中就自己學會了懷疑自己的前一步、自發拉長思考鏈，證明了長推理能力是底座模型的內在潛力。

---

## Slide 4: 演算法革新：GRPO 數學推導
- **Title**: Group Relative Policy Optimization (GRPO)
- **Core Bullets**:
  - **拔除 Critic 模型**：捨棄 PPO 的價值評估網絡，節省 40%–50% 訓練顯存。
  - **群組取樣相對歸一**：自同一 Prompt 取樣 $G$ 個輸出，計算組內優勢 $A_i$。
- **LaTeX Math Formula**:
  $$A_i = \frac{r_i - \mu}{\sigma}, \quad \mu = \frac{1}{G}\sum_{j=1}^G r_j, \quad \sigma = \sqrt{\frac{1}{G}\sum_{j=1}^G (r_j - \mu)^2}$$
  $$\mathcal{J}_{GRPO}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)} A_i, \text{clip}\left(\frac{\pi_\theta(o_i|q)}{\pi_{old}(o_i|q)}, 1\pm\epsilon\right) A_i \right) - \beta \mathbb{D}_{KL} \right) \right]$$
- **Visual Cue**: 淺灰色高亮公式卡片，優勢函數與目標函數分離排版
- **Speaker Notes**:
  > PPO 最大的痛點是 Critic 網絡。在大模型上，Critic 不僅吃掉大量顯存，還經常訓練不穩。GRPO 的智慧在於：既然生成了多個回答，直接用這群回答的相對高低分當作 Baseline，數學優雅且大幅提升系統吞吐量。

---

## Slide 5: 演算法橫向對比：PPO vs DPO vs GRPO
- **Title**: 策略優化演算法對比
- **Core Table**:
| 維度 | PPO | DPO | GRPO (DeepSeek) |
| :--- | :--- | :--- | :--- |
| **Critic 網絡** | 需額外大模型 ($1\times$ 參量) | 無需 | **完全無需 (群組 Baseline)** |
| **記憶體負載** | 極高 (常駐 4 個大模型) | 低 (離線靜態資料) | **極低 (僅 Actor + Ref)** |
| **探索能力** | 強 (在線動態採樣) | 弱 (受限於成對偏好) | **極強 (在線長思維鏈探索)** |
| **核心適用** | 人類主觀偏好對齊 | 一般問答指令微調 | **客觀邏輯/數學長推理** |
- **Speaker Notes**:
  > 這張對比表清晰說明了為什麼推理模型選擇 GRPO 而非 DPO。DPO 只能在靜態的成對資料中微調，無法自主探索未知的思考路徑；而 PPO 又太過沉重。GRPO 兼取兩者長處。

---

## Slide 6: 底層架構協同：MLA 注意力機制
- **Title**: Multi-Head Latent Attention (MLA)
- **Core Bullets**:
  - **長上下文 KV 瓶頸**：思考鏈拉長至數萬 Token 時，顯存頻寬成為致命瓶頸。
  - **低秩聯合壓縮**：將 Key-Value 投影至低維潛在空間 $c^{KV}$，大幅壓低顯存佔用。
  - **解耦式 RoPE**：內容向量與位置向量分離，保留 MHA 表達力的同時具備超高推論速度。
- **Visual Cue**: 雙欄佈局（左：傳統 MHA/GQA 顯存膨脹問題；右：MLA 潛在壓縮與解耦機制圖解）
- **Speaker Notes**:
  > 長思考模型不能只看演算法，如果底層架構沒跟上，推論時顯存瞬間爆發。DeepSeek 透過 MLA 將 KV Cache 壓縮到極致，才使得數萬 Token 的長思維鏈推論具備實際量產的性價比。

---

## Slide 7: 評測戰果與知識蒸餾能力躍遷
- **Title**: 評測突破與知識蒸餾
- **Core Bullets**:
  - **數學競賽戰果**：AIME 2024 Pass@1 達 **79.8%**（Cons@64 達 **92.3%**），MATH-500 達 **97.3%**。
  - **小模型能力躍遷**：以 R1 的 80 萬條數據蒸餾 Qwen-32B，AIME 得分達 **72.6%**。
  - **啟示**：大模型探索出的思維模式可高保真傳遞，證明推理能力具備可遷移性。
- **Visual Cue**: 雙指標卡片（79.8% AIME 2024 / 97.3% MATH-500）+ 蒸餾路徑流程箭頭
- **Speaker Notes**:
  > 在 AIME 2024 等權威競賽中，R1 達成了與閉源頂級模型 o1 相同的水平。更重要的是最後一項蒸餾實驗：小模型自己做 RL 做不出來的高階反思，透過大模型產生的優質思考軌跡微調，竟然能學會 90% 以上的能力。

---

## Slide 8: 總結與建議參考文獻 (Pending Ingestion)
- **Title**: 總結與建議待收錄文獻
- **Core Bullets**:
  - **Wiki 現有總結**：純 RL + GRPO + MLA 構築了當代最精練的長推理模型閉環。
  - **知識缺口與外部文獻**：點擊以下官方論文直接下載，作為下一階段 Wiki 擴充來源：
    - 📥 [DeepSeek-R1 官方技術報告 (arXiv:2501.12948)](https://arxiv.org/pdf/2501.12948)
    - 📥 [DeepSeek-V3 技術報告 (arXiv:2412.19437)](https://arxiv.org/pdf/2412.19437)
    - 📥 [Scaling LLM Test-Time Compute Optimally (arXiv:2408.03314)](https://arxiv.org/pdf/2408.03314)
- **Visual Cue**: 條列式卡片清單，附帶點擊下載連結圖示
- **Speaker Notes**:
  > 最後為大家總結本講的核心洞察。文末列出的 3 篇核心論文已附上官方下載 PDF 連結，隨後可直接匯入我們的知識庫執行進一步的細節編譯。感謝大家！
