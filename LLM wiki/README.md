# 學術論文自動化知識庫與簡報系統 (Academic Paper Wiki & Presentation System)

> **這不是單次生成的靜態網頁，而是一套可持續擴充的學術生產線。**
> 本專案透過自訂的 [`AGENTS.md`](AGENTS.md) 治理規範，指導 AI Agent（如 Claude Code, Cursor, Antigravity）如何將原始論文 PDF 自動編譯為活體知識庫、嚴謹研究筆記，並自動產出「簡約優雅學術白底風」的互動式 HTML 簡報，直接發布於 GitHub Pages。

---

## 專案亮點：超越 Vibe Coding 的規則驅動架構

| 比較維度 | 一般 Vibe Coding | 本專案（AGENTS.md 規則驅動） |
| :--- | :--- | :--- |
| **核心目標** | 單純把「這一個網頁」做出來 | **建立一套規則，讓 AI 依照同一套 SOP 源源不絕製作新頁面** |
| **可維護性** | 換個對話或模型就風格失控、路徑錯亂 | **`AGENTS.md` 明確規範檔案放置、色彩代碼、頁數與格式標準** |
| **防幻覺機制** | AI 容易隨機腦補外部未知資訊 | **封閉世界假設（Strict Grounding）：正文嚴格只用 Wiki 已有事實** |
| **成果產出** | 零碎且孤立的文字 | **具備雙向連結的知識網絡 + 16:9 全螢幕互動 LaTeX 學術簡報** |

---

## 系統展示成果 (Live Demos)

本專案完全適配 **GitHub Pages**，根目錄首頁為 [`index.html`](index.html)，點擊即可直接於瀏覽器在線全螢幕演示：

1. **Raiju 論文互動簡報**：[`presentations/2026-11-16_raiju-post-exploitation.html`](presentations/2026-11-16_raiju-post-exploitation.html)
   - 來源論文：`data/papers/Raiju.pdf` (發表於 Computer Networks 2024)
   - 主題：強化學習導向之後滲透自動化安全評估（A2C vs. PPO 演算法實戰）
   - 特色：內嵌 KaTeX 數學公式、8 頁簡約學術白底風、按 `P` 鍵開啟講者備忘錄抽屜。
2. **DeepSeek-R1 旗艦簡報**：[`presentations/2026-11-16_deepseek-r1-reasoning.html`](presentations/2026-11-16_deepseek-r1-reasoning.html)
   - 主題：大語言模型純強化學習與測試期計算量擴展（GRPO 數學推導與 MLA 注意力架構）。

---

## 目錄架構

```
├── AGENTS.md                 # 【核心大腦】AI 運作與擴充規範手冊
├── README.md                 # 專案說明文件（本檔案）
├── index.html                # 【GitHub Pages 首頁】公開網站展示門戶
├── scripts/                  # 自動化處理腳本 (支援 Python 與 PowerShell)
├── data/papers/              # 【來源層】原始論文 PDF（如 Raiju.pdf，AI 唯讀）
├── raw/entries/              # 【中繼層】標準化 Markdown 輸入條目
├── wiki/                     # 【維基層】編譯後主題化知識圖譜（含 _index.md 與 _backlinks.json）
├── notes/                    # 【筆記層】嚴格依 Wiki 事實撰寫之深度研究筆記（含 LaTeX）
├── slides/                   # 【企劃層】8 頁標準結構投影片大綱與講者講稿
└── presentations/            # 【簡報層】自包含 HTML 互動簡報（支援全螢幕、KaTeX 與講者筆記）
```

---

## 新增一篇新論文的標準流程 (How to Add a New Paper)

當您未來要新增任何一篇新論文（例如 `MyPaper.pdf`）時，只需將檔案放進 `data/papers/`，並對 AI 說一句：
> *「請依照 AGENTS.md 規範，將 `data/papers/MyPaper.pdf` 編譯進 Wiki，並生成學術白底風簡報與更新首頁。」*

AI 閱讀 `AGENTS.md` 後將自動執行四階段生產線：
1. **解析與吸收**：將 PDF 提煉為 `raw/entries/` 並編譯進 `wiki/` 主題詞條，自動重建主索引。
2. **撰寫閉環筆記**：在 `notes/` 生成帶有 LaTeX 推導的深層筆記，正文只引用庫內事實，外部文獻放文末供一鍵下載。
3. **生成逐頁企劃**：在 `slides/` 生成 8 頁精簡結構與講者逐字稿。
4. **輸出 HTML 簡報並發布**：在 `presentations/` 生成零依賴的學術白底 HTML 簡報，並自動將卡片加入 `index.html` 首頁！

---

## GitHub 上傳與 GitHub Pages 發布指南

1. **初始化與提交至本機 Git**：
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit of academic paper wiki & presentation system"
   ```
2. **推送到 GitHub**：
   在 GitHub 上建立一個新的公開 Repository（例如 `academic-wiki-slides`），執行：
   ```bash
   git branch -M main
   git remote add origin https://github.com/<你的使用者名稱>/<你的倉庫名稱>.git
   git push -u origin main
   ```
3. **啟用 GitHub Pages**：
   - 進入 GitHub 倉庫的 **Settings** $\rightarrow$ **Pages**。
   - 在 **Build and deployment** $\rightarrow$ **Branch** 選擇 `main` 分支，資料夾選擇 `/ (root)`，點擊 **Save**。
   - 等待約 1 分鐘，即可透過 `https://<你的使用者名稱>.github.io/<你的倉庫名稱>/` 瀏覽正式上線的網站！
