# 大語言模型如何學會思考？——LLM 推理機制與強化學習入門教學研討筆記

> **教學目標**：讓零機器學習背景的學習者，能夠徹底理解大語言模型（LLM）如何從單純的「字詞預測接話機」，演進為具備邏輯推理、多步驟問題求解與自主自我反思能力的「深度思考系統」。
> **知識庫閉環承諾**：本篇教學筆記之所有核心機制與論據，100% 嚴格源自專案 Wiki 庫內已編譯詞條。

---

## 一、直觀破冰：接話機器人 vs 深度思考者

許多初學者對 ChatGPT 等模型的直觀印象是「它什麼都懂，問什麼都能秒回」。然而在經典認知科學（Daniel Kahneman《快思慢想》）中，人類思維被分為兩種模式：
1. **系統一（System 1 / 快思）**：直覺反射、自動化聯想（例如：看到 $2 + 2$ 瞬間回答 $4$，不經大腦思索）。傳統自回歸 Transformer 預訓練模型本質上是在執行系統一——僅根據上文統計機率「預測下一個最可能的字（Next-Token Prediction）」(來源: [[Scaling Laws]])。
2. **系統二（System 2 / 慢想）**：需要調用工作記憶、逐步列式、邏輯查驗與自我反思（例如：計算 $47 \times 89$ 或解國際象棋殘局）。

早期大模型面對複雜數學與邏輯題目時經常慘敗，正是因為被強迫「直接吐出答案」，缺乏系統二的思考緩衝區。要讓 AI 學會真正的推理，科學家們在過去三年間發展出了三大關鍵階梯。

---

## 二、階梯一：思維鏈 (Chain of Thought) —— 給 AI 一張大腦草稿紙

傳統 Prompt 要求模型看到題目 $X$ 就直接回答 $Y$：
$$P(Y \mid X)$$
如果題目是一道需要四個步驟的小學應用題，模型在生成第一個字的幾毫秒內，就必須在單次前向傳播（Forward Pass）中暗中完成所有推理，這在神經網絡計算能力上是不可能的 (來源: [[Chain of Thought (CoT)]])。

- **草稿紙機制**：Wei 等人發現，只要在提示中示範或加入「Let's think step by step」，讓模型先生成中間的思考步驟 $C = (c_1, c_2, \dots, c_k)$：
  $$P(C, Y \mid X) = P(C \mid X) \cdot P(Y \mid X, C)$$
- **為什麼有效？** (來源: [[Wei2022-ChainOfThought: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]])
  因為每一個新產生的思考 Token 都會被餵回 Attention 機制中。模型等於是在自己的草稿紙上一邊寫、一邊看著自己算出的中間結果，再推導下一步。在 GSM8K 數學基準測試上，僅僅增加草稿紙，大模型的答對率就從 $17.9\%$ 爆衝至 $56.9\%$！

---

## 三、階梯二：自我一致性 (Self-Consistency) —— 集體智慧的多數表決

有了草稿紙之後，另一個致命問題浮現：**「一旦草稿紙上第一步算錯，後面就全盤皆輸」**。這是因為傳統貪婪解碼（Greedy Search）只要遇到局部隨機擾動，就無法回頭 (來源: [[Self-Consistency]])。

- **多數決機制**：Wang 等人提出的自我一致性（Self-Consistency），源自一個極為生活化的常理：「一道複雜題目，解題路徑可能有千百種，但算對的答案往往只有一個」(來源: [[Wang2022-SelfConsistency: Self-Consistency Improves Chain of Thought Reasoning in Language Models]])。
- **演算法核心**：
  1. 提高隨機性（Temperature > 0），讓模型從不同思考角度並行寫出 $N$ 份草稿。
  2. 統計這 $N$ 份草稿結尾的答案，進行多數決投票：
     $$\hat{y} = \arg\max_{y} \sum_{i=1}^N \mathbf{1}(y^{(i)} = y)$$
- 這項技術證實了**「推理時多花算力（Test-Time Compute）」**可以直接換取更高的可靠性，進一步將數學解題率推升至 $74.4\%$ (來源: [[Test-Time Compute]])。

---

## 四、階梯三：強化學習 (RL) —— 用獎勵引導思考演化

前兩階段雖然強大，但本質上仍依賴「人類手把手教 AI 怎麼寫草稿」。AI 是否能像 AlphaGo 一樣，在完全沒有人類示範的情況下，自己探索出解決問題的最優思維路徑？

1. **從胡蘿蔔與大棒開始 (RLHF & PPO)**：
   - InstructGPT (來源: [[Ouyang2022-InstructGPT: Training language models to follow instructions with human feedback]]) 確立了用獎勵模型引導模型行為的機制，並透過近端策略最佳化（PPO）調整參數：
     $$\mathcal{L}_{\text{PPO}}(\phi) = \hat{\mathbb{E}}_t \left[ \min\left( r_t(\phi) \hat{A}_t, \, \text{clip}(r_t(\phi), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$
   - 在自動化滲透測試中，Raiju 框架也採用此架構引導 Agent 自主探索系統漏洞 (來源: [[Pham2024-Raiju.md]])。
2. **終極突破：純強化學習與自我反思 (DeepSeek-R1)**：
   - 傳統 RLHF 需要昂貴的人類評分員。DeepSeek-R1 (來源: [[DeepSeek2025-R1.md]]) 大膽拔除人類 Critic 網絡，改用規則型客觀獎勵（符號判定對錯）與群體相對策略最佳化（GRPO）：
     $$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta}{\pi_{\text{old}}} A_i, \, \text{clip}\left(\frac{\pi_\theta}{\pi_{\text{old}}}, 1-\epsilon, 1+\epsilon\right) A_i \right) - \beta D_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}}) \right) \right]$$
   - **「頓悟時刻 (Aha Moment)」**：模型在純 RL 訓練數千輪後，在沒有任何人類教導下，自發湧現出了 `<think>` 標籤，學會了在解題卡關時寫出「等等，我前面推導有瑕疵，讓我重新換個變數檢查」，真正具備了自我驗證與回溯能力！

---

## 五、現實代價：思考稅 (Reasoning Tax) 與未來挑戰

讓模型「學會思考」並非沒有代價：
1. **推論延遲（Latency）**：原本 0.5 秒秒回的對話，因為長思維鏈生成數千個思考 Token，需要等待 30–60 秒，產生顯著的互動摩擦 (來源: [[Test-Time Compute]])。
2. **軟性領域困境**：純 RL 在有標準答案的數理程式（Math/Code）大獲成功，但在人文寫作、倫理哲學等缺乏客觀判定器的領域，容易陷入獎勵作弊（Reward Hacking）(來源: [[DeepSeek-R1]])。

---

## 六、延伸學習與建議文獻 (Literature Backlog)

欲深入探究前沿推理機制與測試期計算擴展，推薦閱讀以下三篇文獻，可直接點擊下載 PDF 啟動 Wiki Ingest：

1. **[Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Parameters](https://arxiv.org/pdf/2408.03314)** (arXiv:2408.03314)
   - 核心探討：在推論期增加思考算力，何時能超越訓練一個十倍大模型？
2. **[Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking](https://arxiv.org/pdf/2403.09629)** (arXiv:2403.09629)
   - 核心探討：如何讓模型在預訓練階段就學會「開口前在內心靜默自言自語」？
3. **[Let's Verify Step by Step](https://arxiv.org/pdf/2305.20050)** (arXiv:2305.20050)
   - 核心探討：過程獎勵模型（Process Reward Model, PRM）如何對思考鏈的每一步進行逐步精確打分。
