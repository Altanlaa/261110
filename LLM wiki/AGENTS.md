# 論文 LLM Wiki 知識庫與 HTML 簡報系統 - AGENTS.md 治理手冊

> **本檔案為本專案的「行為憲章與系統架構指引」。**
> 任何 AI Agent 在維護、擴充或新增內容時，**必須先閱讀並嚴格遵守本規範**。
> 本專案遵循 **Andrej Karpathy 的「LLM Wiki」** 核心概念，建立「寫入時編譯」的活體知識庫，並以**「零依賴、純代碼圖解的學術白底風 HTML 互動簡報」**作為核心終端輸出。

---

## 一、核心規範與語言原則 (Mandatory Rules)

1. **語言與用語習慣**：
   - 全面使用 **繁體中文（台灣習慣用語）** 撰寫內文（例如：最佳化、推論、快取、演算法、資訊、權限提升、橫向移動）。
   - **關鍵技術術語、模型名稱、評測指標與論文標題強制保留英文原文**。
     - 正確範例：`Self-Attention`、`Ablation Study`、`Loss Function`、`Pass@1`、`Actor-Critic`、`Backtracking`、`Cold-Start`。
2. **檔案命名標準 (Naming Conventions)**：
   - **論文頁（Paper Pages）**：一律採用 **選項 A（簡潔代號＋簡稱）**：`AuthorYear-Topic.md`，存放於 `wiki/papers/`。
     - 範例：`Pham2024-Raiju.md`、`DeepSeek2025-R1.md`、`Vaswani2017-Transformer.md`。
   - **概念頁（Concept Pages）**：使用英文小寫 kebab-case 命名，存放於 `wiki/concepts/`、`wiki/techniques/` 或 `wiki/architectures/`。
     - 範例：`test-time-compute.md`、`scaling-laws.md`、`grpo.md`。
3. **數學推導、Loss Function 與虛擬碼要求**：
   - **必須完整保留關鍵數學推導、Loss Function、Objective Function 或演算法虛擬碼**。
   - 數學公式嚴格採用標準 LaTeX 格式：
     - 行內公式：`$...$`
     - 獨立多行公式：`$$...$$`
4. **PDF 來源保存規範 (PDF Storage Rules)**：
   - 若使用者在對話中上傳 PDF 論文，**請存入 `raw/papers/` 資料夾中**。
   - 若提供 arXiv 或學術網址連結，**請下載 PDF 存入 `raw/papers/` 資料夾中**。
5. **視覺呈現：純代碼圖解（免手動截圖）**：
   - **使用者無需手動截圖**！AI 必須透過 Mermaid.js、KaTeX 數學公式、論文三線對比表與純 CSS 卡片圖解所有架構與流程。

---

## 二、專案目錄結構與放置原則

```
LLM wiki/
├── AGENTS.md                 # 【系統大腦】AI 治理與擴充行為手冊（本檔案）
├── README.md                 # 專案公開說明文件
├── index.html                # 【GitHub Pages 首頁】公開入口網站與所有簡報導覽門戶
├── scripts/                  # 自動化工具腳本
│   ├── ingest.py / .ps1      # 原始論文前處理
│   └── rebuild_index.py / .ps1 # 全局主索引與反向圖譜自動編譯
├── raw/                      # 【原始與中繼層】
│   ├── papers/               # 存放原始論文 PDF（對話上傳或 arXiv 下載存於此）
│   └── entries/              # 標準化 Markdown 輸入條目（含 YAML 前言）
├── wiki/                     # 【知識維基層】編譯後主題知識圖譜（Markdown + [[wikilinks]]）
│   ├── _index.md             # 全局主索引（自動統計分類、別名與被引用次數）
│   ├── _backlinks.json       # 全局反向連結拓撲圖
│   ├── _absorb_log.json      # 已吸收文獻紀錄
│   ├── papers/               # 論文專頁（嚴格依選項 A: AuthorYear-Topic.md 命名）
│   ├── models/               # 代表性模型與框架（如 deepseek-r1, raiju-framework）
│   ├── techniques/           # 演算法與訓練技術（如 grpo, a2c-vs-ppo）
│   ├── architectures/        # 神經網絡架構與機制（如 mla, gqa）
│   ├── evaluations/          # 評測指標與基準測試（如 math-reasoning-benchmarks）
│   └── concepts/             # 底層科學與現象（如 test-time-compute, scaling-laws）
├── notes/                    # 【研究筆記層】嚴格依據 Wiki 撰寫之深度論文綜述（含 LaTeX）
├── slides/                   # 【企劃層】8 頁標準簡報大綱、視覺指示與講者逐字稿
├── presentations/            # 【簡報展示層】單檔自包含 HTML 簡報（支援全螢幕、KaTeX 與講稿）
└── assets/                   # 【靜態資產層】自訂圖檔備用（免手動截圖，純代碼視覺為主）
```

---

## 三、HTML 簡報視覺風格標準（簡約優雅學術白底風）

本專案所有產出的 HTML 簡報，統一採用**「簡約優雅學術白底風（Clean Academic White）」**：

### 1. 色彩體系 (Color Palette)
- **外圍畫布背景**：`#F1F5F9`（柔和淺冷灰，對比舒適）
- **投影片卡片背景**：`#FFFFFF`（純白）
- **邊框與分隔線**：`#E2E8F0`（1px 細邊框，帶極輕微陰影）
- **文字主色**：`#0F172A`（深石墨色，清晰銳利）
- **次要說明文字**：`#475569`（沉穩冷灰）
- **學術焦點色**：`#0284C7`（海軍藍，用於標題、強調與進度條）
- **輔助高亮色**：`#0D9488`（鼠尾草綠，用於演算法重點與成功指標）

### 2. 字體階層 (Typography)
- **簡報標題**：經典學術襯線體 `'Charter', 'Cambria', 'Georgia', serif`
- **正文內容**：高可讀性無襯線體 `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **代碼與標籤**：等寬字體 `'JetBrains Mono', Consolas, monospace`

### 3. 圖解原則：純代碼可視化（免手動截圖）
AI 必須利用以下方式呈現視覺效果，**絕不要求使用者手動截圖**：
- **架構與流程圖**：以 Mermaid.js 語法繪製流程圖（`flowchart TD` / `LR`）。
- **數學推導**：整合輕量 KaTeX 引擎，行內 `$..$` 與獨立區塊 `$$..$$` 即時渲染。
- **對照表格**：採用論文級學術三線表（上方粗線、標題欄細線、底端粗線）。
- **關鍵指標**：採用超大字號卡片（如 `79.8%`、`>84%`）突顯核心實驗成果。

### 4. 互動與操控能力
- 支援標準熱鍵：`Space` / `→` 下一頁、`←` 上一頁、`F` 全螢幕演示、`P` 開啟講者備忘錄抽屜、`Home` 回封面。
- 頂部包含進度條（Progress Bar），右下角包含當前頁碼指示器。

---

## 四、AI 新增論文與內容的四階段標準作業流程 (SOP)

當收到一篇新論文（例如上傳或下載 PDF 存入 `raw/papers/NewPaper.pdf`）時，AI 必須嚴格執行以下 4 步：

### 階段一：論文解析與 Wiki 編譯 (Ingest & Absorb)
1. 確保 PDF 存放於 `raw/papers/` 中。
2. 閱讀論文，提取核心動機、數學公式、系統架構與實驗指標。
3. 建立論文專頁：`wiki/papers/AuthorYear-Topic.md`（依選項 A 命名，保留關鍵推導與虛擬碼）。
4. 橫向拆解核心技術與理論，建立或更新對應的 `wiki/techniques/`、`wiki/models/` 或 `wiki/concepts/` 詞條。
5. 詞條間以 `[[wikilinks]]` 互相串聯，並執行 `scripts/rebuild_index.ps1` 自動更新主索引 `_index.md` 與反向圖譜 `_backlinks.json`。

### 階段二：撰寫閉環研究筆記 (Research Notes in `notes/`)
1. 檔名格式：`notes/YYYY-MM-DD_<topic>.md`。
2. **正文 100% 嚴格僅引用 Wiki 庫內事實**，每段必須標註 `(來源: [[Wiki 詞條]])`。
3. 外網檢索之延伸文獻，統一隔離於文末「建議參考文獻（Pending Ingestion Backlog）」，包含論文標題、**點擊直接下載 PDF 連結**、核心摘要與建議 Wiki 分類。

### 階段三：生成 8 頁簡報逐頁企劃 (Slide Deck in `slides/`)
1. 檔名格式：`slides/YYYY-MM-DD_<topic>_slides.md`。
2. 規範標準 8 頁結構：
   - Slide 1: 封面（標題、副標、出處與團隊）
   - Slide 2: 核心痛點與研究背景
   - Slide 3: 核心突破與架構設計（附 Mermaid 或純代碼圖解指示）
   - Slide 4: 演算法機制與 LaTeX 數學推導
   - Slide 5: 演算法/架構橫向對比表
   - Slide 6: 關鍵工程細節或獎勵函數
   - Slide 7: 評測戰果與核心指標（大字號卡片）
   - Slide 8: 總結與延伸文獻直接下載卡片
3. **講者備忘稿 (Speaker Notes)**：每頁必須附帶 `<!-- speaker_notes -->` 逐字稿。

### 階段四：輸出 HTML 簡報並連動首頁 (Presentations & index.html)
1. 檔名格式：`presentations/YYYY-MM-DD_<topic>.html`。
2. 輸出零外部依賴、內嵌 CSS/JS 與 KaTeX 的自包含 HTML 檔案。
3. **自動連動首頁**：立即在專案根目錄的 `index.html` 的簡報展示區，新增該簡報的精美卡片與在線全螢幕體驗連結。

---

## 五、AI 編輯約束與安全手則

1. **語言純度**：一律使用繁體中文（台灣習慣用語），關鍵術語（如 `Self-Attention`, `Ablation Study` 等）不可強行翻譯，維持英文原文。
2. **命名不可違規**：論文頁檔名必須遵循 `AuthorYear-Topic.md`。
3. **公式不可簡化或省略**：關鍵推導與 Loss Function 必須以標準 LaTeX 完整寫出。
4. **來源路徑固定**：所有 PDF 論文必須確實歸檔於 `raw/papers/`。
5. **使用者體驗優先**：不可要求使用者做手動截圖等繁瑣雜務，所有圖解優先以純代碼實現。
