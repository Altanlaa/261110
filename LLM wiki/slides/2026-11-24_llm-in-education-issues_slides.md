---
title: "LLM 在教學上的運用問題與技術挑戰簡報企劃"
date: "2026-11-24"
source_note: "notes/2026-11-24_llm-in-education-issues.md"
style: "Clean Academic White"
total_slides: 8
---

# LLM 在教學上的運用問題與技術挑戰簡報企劃

---

## Slide 1: 封面 (Title Slide)
- **Title**: LLM 在教學上的運用問題與技術瓶頸
- **Subtitle**: 從推理可靠性、Reasoning Tax 到蘇格拉底式教學的架構落差
- **Visual Cue**: 簡約居中排版、學術海軍藍焦點色、標註 Wiki Grounded
- **Speaker Notes**:
  > 各位好，今天我們探討大語言模型導入教學應用時面臨的深層技術挑戰。我們將結合 Wiki 庫中的最新模型機制與評測數據，剖析為何「會解題的 AI」並不等同於「會教學的好老師」。

---

## Slide 2: 核心衝突：直接解答 vs. 蘇格拉底式引導
- **Title**: 教學範式衝突：直接解答 vs. 認知鷹架
- **Core Bullets**:
  - **模型的優化目標**：依據 [[DeepSeek-R1]] 機制，模型目標在於最大化單次輸出的正確率與長思維鏈 (Long CoT)。
  - **教學法的核心精神**：教育講求「引導思考（Socratic Scaffolding）」，鼓勵學生自主推理與發現錯誤。
  - **教學負面後果**：模型往往直接傾瀉完整計算過程與答案，造成學生「表面學習（Superficial Learning）」與深度思考退化。
- **Visual Cue**: 左右兩欄對照卡片（左：AI 解題導向 vs 右：教育引導導向）
- **Speaker Notes**:
  > 當前所有強大的推理模型，其訓練目標都是以最短路徑直接給出答案。但在教學中，直接給答案往往是破壞學習動機的罪魁禍首。學生缺乏自己碰撞、試錯的過程，形成了嚴重的認知依賴。

---

## Slide 3: 數理推理的誤差與誤導風險
- **Title**: 推理可靠性：Pass@1 誤差在教學中的放大效應
- **Core Bullets**:
  - **高難度題目仍具誤差**：依據 [[Math Reasoning Benchmarks]]，即使前沿模型在小學數學 GSM8K >95%，但在競賽級 AIME 2024 的 Pass@1 仍落在約 $79.8\%$。
  - **權威口吻下的幻覺誤導**：LLM 即使推導出錯，依然能以極具說服力且邏輯流暢的語氣輸出，初學者難以分辨對錯。
  - **多數決表決不可行**：評測使用的多數決 $Cons@64$（採樣 64 次表決）在日常即時教學對話中運算成本過高。
- **Visual Cue**: 指標卡片（Pass@1: 79.8% vs Cons@64: 92.3%）+ 警示對照方塊
- **Speaker Notes**:
  > 評測數據看起來很漂亮，但請大家注意：Pass@1 達到 80%，意味著每 5 題就有 1 題出錯。如果沒有專業老師把關，學生很容易把 AI 自信給出的錯誤公式當作真理記下來，形成難以糾正的認知盲點。

---

## Slide 4: Reasoning Tax 與推論延遲
- **Title**: Reasoning Tax：長思維鏈帶來的互動障礙
- **Core Bullets**:
  - **推論延遲 (Inference Latency)**：依據 [[Test-Time Compute]]，長思維鏈需自發生成數千個 `<think>` Token，單次回應等待可能達 30–60 秒以上。
  - **即時回饋感斷裂**：課堂或互動家教強調「即時、微步反饋」，過長延遲破壞了學習者的心流（Flow）。
  - **過度思考 (Over-thinking)**：面對基礎概念問答時，長思考模型容易產生冗長推導，增加初學者的認知負荷 (Cognitive Overload)。
- **Visual Cue**: 時間軸圖解（即時教學對話所需秒數 <2s vs 長 CoT 延遲 30s+）
- **Speaker Notes**:
  > 測試期計算量的延伸讓模型在後台深思熟慮，但教學現場講究的是眼神交流與快速的啟發式問答。讓學生盯著旋轉游標等待 40 秒，對注意力本就有限的學習者來說是一大災難。

---

## Slide 5: 軟性學科之評估困境
- **Title**: 評估困境：缺乏客觀確定性驗證器
- **Core Bullets**:
  - **數理有解，人文無解**：依據 [[DeepSeek2025-R1: Incentivizing Reasoning Capability in LLMs via RL]]，純 RL 成功的基石在於數學與程式碼擁有客觀的確定性驗證器 (Accuracy Reward, 0/1)。
  - **軟性學科評估缺失**：語文寫作、歷史批判、哲學思考缺乏單一真值標準。
  - **獎勵作弊 (Reward Hacking)**：缺乏確定性驗證時，模型容易陷入「詞藻華麗卻論述空洞」的假性評分，無法勝任申論題評閱。
- **Visual Cue**: 硬性客觀學科 (數學/程式碼) vs 軟性主觀學科 (人文/寫作) 矩陣對照表
- **Speaker Notes**:
  > 強化學習之所以能教模型做數學，是因為有編譯器和客觀標準答案。但語文寫作、閱讀理解有標準答案嗎？沒有。目前模型在非數理的軟性學科中，往往只會堆砌排比句，缺乏實質的批判性診斷。

---

## Slide 6: 資料污染與學習評量失效
- **Title**: 資料污染 (Data Contamination) 與評量失真
- **Core Bullets**:
  - **記憶假象而非真理解**：依據 [[Scaling Laws]]，預訓練資料達數十兆 Tokens，歷屆考題與經典教科書早已高度滲透。
  - **評量指標失效**：學生利用 AI 解題，取得高分往往是 AI 提取了記憶庫的現成解析，而非真正達成知識建構。
  - **傳統作業機制崩解**：紙筆作業與課後習題失去診斷學習成效的功能，倒逼教學端必須重構評量方式。
- **Visual Cue**: 警示流程圖（題庫早已洩漏進預訓練資料 $\rightarrow$ 記憶模式命中 $\rightarrow$ 假性滿分）
- **Speaker Notes**:
  > 另一個致命傷是資料污染。網路上所有經典考題早就在模型肚子裡了。學生拿題目去問，AI 其實是在「背答案」，而不是在現場推理。這讓老師出的作業完全失去了診斷學生懂不懂的功能。

---

## Slide 7: 技術應對策略與教學落地架構
- **Title**: 技術突破方向：教學專用架構構想
- **Core Bullets**:
  - **過程引導限制 (Prompt & Architecture Constraint)**：強制限制模型不得輸出終端答案，僅能給予階梯式提示 (Hints)。
  - **過程獎勵模型 (Process Reward Model, PRM)**：針對學生每一個思考步驟單獨給予反饋，而非僅以最後對錯給分。
  - **輕量化即時推論 (Inference Optimization)**：對簡單概念調用蒸餾小模型（低延遲），難題才切換至長思考模型。
- **Visual Cue**: 三層教學引導架構圖（提示層 $\rightarrow$ 步驟診斷層 $\rightarrow$ 分流推論層）
- **Speaker Notes**:
  > 要解決這些問題，技術上必須給 AI 戴上「緊箍咒」：第一，用 Prompt 或微調強制它「打死不能直接講答案」；第二，導入過程評估模型，像好家教一樣，只在學生卡關的地方輕輕推一把。

---

## Slide 8: 總結與建議待收錄文獻 (Pending Ingestion)
- **Title**: 總結與建議待收錄教育文獻
- **Core Bullets**:
  - **Wiki 現有總結**：生成目標衝突、可靠性誤差、Reasoning 延遲與缺乏確定性驗證，構成了教育導入的四大鴻溝。
  - **外部文獻推薦**：點擊以下官方論文直接下載 PDF，啟動下一輪 Wiki 吸收：
    - 📥 [Large Language Models for Education: A Survey (arXiv:2405.13001)](https://arxiv.org/pdf/2405.13001)
    - 📥 [Opportunities and Challenges of LLMs in Education (arXiv:2507.22753)](https://arxiv.org/pdf/2507.22753)
    - 📥 [Challenges and Opportunities of Moderating Usage in Education (arXiv:2312.14969)](https://arxiv.org/pdf/2312.14969)
- **Visual Cue**: 條列式卡片清單，附帶點擊下載連結圖示
- **Speaker Notes**:
  > 總結來說，AI 在教學上最大的價值不是當「解題槍手」，而是如何演進為「能引導自主思考的對話者」。文末收錄的 3 篇頂級教育文獻已附上下載連結，可隨後納入知識庫深度分析。感謝大家！
