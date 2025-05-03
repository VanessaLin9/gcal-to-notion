# GCal to Notion Sync 📅➡️📒

[![Docker Pulls](https://img.shields.io/docker/pulls/vanessalin9/gcal-to-notion)](https://hub.docker.com/r/vanessalin9/gcal-to-notion)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Powered by Notion API](https://img.shields.io/badge/Powered%20by-Notion%20API-black)

同步你的 Google Calendar 活動到 Notion 資料庫的小工具。  
透過 Docker 部署，輕量快速、隨時可以啟動。

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
本專案僅供個人學習與私人使用。
