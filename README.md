# GCal to Notion Sync 📅➡️📒

[![Docker Pulls](https://img.shields.io/docker/pulls/vanessalin9/gcal-to-notion)](https://hub.docker.com/r/vanessalin9/gcal-to-notion)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Powered by Notion API](https://img.shields.io/badge/Powered%20by-Notion%20API-black)

將 Google Calendar 活動自動同步到 Notion 資料庫的小工具
支援多種執行方式，彈性又易於擴充：

🐳 Docker 執行：快速打包、跨平台部署

🧠 GitHub Actions 自動同步：每日排程、自動化管理

🖥️ Electron 桌面應用：一鍵手動同步，適合不習慣命令列的使用者

💻 本地 Python 開發：簡潔、可自訂同步邏輯。

---

## 🚀 Docker Hub

最新版本的 Docker 映像檔已發佈在 Docker Hub：  
👉 [vanessalin9/gcal-to-notion](https://hub.docker.com/r/vanessalin9/gcal-to-notion)

拉取最新映像檔：

```bash
docker pull vanessalin9/gcal-to-notion:latest
```

## 🛠️ 使用說明
### 🐳 方式一：使用 Docker 執行（適合快速體驗或部署）
準備以下檔案於當前資料夾：

credentials.json：你的 Google API 憑證（OAuth 2.0）

token.json：授權後取得的存取憑證（access token & refresh token）

.env：包含 Notion Token 與資料庫 ID，格式如下：
   
  請參考 .env.example 或下面寫法：
```bash
NOTION_TOKEN=your-notion-integration-secret
NOTION_DATABASE_ID=your-notion-database-id
```
2. 執行指令
- 假設你已經把這些檔案放在當前目錄，執行以下指令：
```bash
docker run -it --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.json:/app/token.json \
  vanessalin9/gcal-to-notion:latest
```
✅ 這樣會自動同步「未來 14 天內的所有 Google Calendar 活動」到你的 Notion 資料庫，已存在的活動會自動跳過避免重複。

---
### 💻 方式二：本地端開發環境（適合進一步修改與測試）
1. 建立虛擬環境並安裝依賴：
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. 準備憑證與設定：
```bash
credentials.json, token.json, .env 檔案同上
```
3. 執行同步：
```bash
python sync_gcal_to_notion.py
```
4. 開發加速：可使用 Makefile 快捷指令（詳見下節）

### 🧰 開發用快捷指令（Makefile）

| 指令	| 說明 |
|---|---|
| make install | 安裝虛擬環境需要的所有套件 |
| make run | 執行主程式 sync_gcal_to_notion.py |
| make dev | 啟動虛擬環境並執行主程式 |
| make clean | 移除 Python 的暫存檔案（如 __pycache__） |
| make env | 顯示目前使用的python與pip |

執行範例：
```bash
  make install
  make run
```
---
### 🖥️ 桌面版：Electron 手動同步工具（可選用）
本專案現在支援一個桌面版本，透過 Electron 打包成簡易的 GUI，讓你可以手動一鍵同步 Google Calendar 至 Notion，非常適合：

- 不想設定自動排程

- 希望自訂同步時間、即時確認結果

- 未來將支援參數設定介面

#### 📁 子資料夾說明
桌面版程式碼位於 gcal-to-notion-desktop/ 子資料夾中。
主要結構如下：

```bash
gcal-to-notion-desktop/
├── main.js         # Electron 主行程邏輯，負責呼叫 Python
├── preload.js      # 前後端通訊橋接
├── index.html      # 前端畫面
├── package.json    # npm 套件與啟動設定
├── ...
```
#### ▶️ 執行方式
進入子資料夾後，安裝依賴並啟動：

```bash
cd gcal-to-notion-desktop
npm install
npm start
```
#### 🔒 安全性說明
token.json 及 credentials.json 為 OAuth 授權用檔案

此資料只會存放於本地端，且已透過 .gitignore 排除在版本控制外

GitHub Actions 使用的金鑰由 Secrets 管理，與桌面版獨立，互不干擾

---

### 📄 功能特色

📅 自動同步 Google Calendar 中未來 14 天的所有活動

🕒 透過 GitHub Actions 定期排程，每日 00:00 自動執行

🐳 完全 Docker 化，不需手動安裝任何依賴

🔒 支援 OAuth 2.0 安全認證

🎯 最小可執行版本，易於後續擴充與部署

---

📝 other reference:
1. [OAuth 2.0 Authorization Flow api docs](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow)
2. [InstalledAppFlow version: run_console error](https://stackoverflow.com/questions/75602866/google-oauth-attributeerror-installedappflow-object-has-no-attribute-run-co)
3. [notion api docs](https://developers.notion.com/reference/page-property-values)

---

📄 License:

本專案使用 [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 授權。  
任何人皆可自由使用、修改與散布本專案程式碼，但需遵守開源原則，保留授權聲明與原作者資訊，且不得轉為閉源或專有軟體使用。

