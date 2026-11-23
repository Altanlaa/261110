---
title: "Test-Time Compute"
type: "concept"
created: "2025-01-22"
last_updated: "2025-01-22"
aliases: ["測試期計算", "Inference-Time Scaling", "Test-Time Scaling"]
related: ["[[DeepSeek-R1]]", "[[Scaling Laws]]", "[[Group Relative Policy Optimization (GRPO)]]"]
sources: ["2025-01-22_2025-deepseek-r1"]
---

# Test-Time Compute

## 核心定義與演進範式
Test-Time Compute（測試期計算 / 推理期計算擴展）代表著大語言模型研發範式從「純預訓練規模擴展（Pre-training Scaling）」邁向「推理期動態思維擴展（Inference-time Scaling）」的重大轉變。

傳統大語言模型依賴 [[Scaling Laws]]，透過擴大模型參數量與預訓練資料規模來提升性能；然而，隨著高質量人類文字資料逼近極限與邊際收益遞減，研究者發現：**允許模型在生成最終答案之前投入更多的計算資源進行思考、自我驗證、錯誤回溯與分支探索，能夠使固定規模的模型在複雜任務上達成指數級的精確度提升**。

代表性的前沿體現包括 OpenAI-o1 系列與 [[DeepSeek-R1]]。

## 實現機制
測試期計算的擴展主要依循兩種維度：
1. **內部思考鏈拉長（Internal Long CoT）**：
   透過 [[Group Relative Policy Optimization (GRPO)]] 等純強化學習演算法，引導模型在生成答案前自主生成大量思考 Token（包含回溯、替代路徑檢驗、逐步推導）。
2. **外部搜索與驗證架構（Search and Verification）**：
   - **多數表決（Majority Voting / Self-Consistency）**：針對同一問題取樣 $N$ 個路徑並投票。
   - **樹狀搜索（MCTS / Best-of-N）**：結合過程獎勵模型（Process Reward Model, PRM）評估每個中間思考節點，篩選最佳解題路徑。

## 邊際效益與計算成本折衷
測試期計算並非免費的午餐。其核心挑戰在於延遲（Latency）與硬體推論開銷的暴增：
- 一個需要生成數萬個 `<think>` Token 的回答，其用戶端等待時間可能從 1 秒拉長至 30 秒以上。
- 系統吞吐量受限於長時間佔用 GPU 顯存與運算核心。
- 當前研究正朝向「思維鏈動態長度調適（Adaptive Reasoning）」與「小模型知識蒸餾」推進。
