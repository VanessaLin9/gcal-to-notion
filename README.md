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

🛠️ 使用說明
1. 準備需要的檔案
- credentials.json
  - 你的 Google API 憑證 (OAuth 2.0 用戶端 ID)
- token.json
  - 授權完成後取得的存取憑證（access token & refresh token）
- .env
  - 包含你的 Notion API 秘密金鑰與資料庫ID
   
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
✅
這樣會自動同步最近的 Google Calendar 活動到你的 Notion 資料庫。

3. 本地開發
- 本地開發使用虛擬環境
- 進入專案後進入虛擬環境安裝相關需要套件
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
📅 從 Google Calendar 自動讀取活動

📝 新增活動到 Notion 指定資料庫

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
