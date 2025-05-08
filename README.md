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
### 🐳 使用 Docker 執行
準備以下檔案於當前資料夾：

- credentials.json：你的 Google API 憑證（OAuth 2.0）

- token.json：授權後取得的存取憑證（access token & refresh token）

- .env：包含 Notion Token 與資料庫 ID，格式如下：
   
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

---
### 💻 本地開發
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python sync_gcal_to_notion.py
```

📂 開發加速：可使用 Makefile 快捷指令
- 目前支援的指令：

| 指令	| 說明 |
|---|---|
| make install | 安裝虛擬環境需要的所有套件 |
| make run | 執行主程式 sync_gcal_to_notion.py |
| make dev | 啟動虛擬環境並執行主程式 |
| make clean | 移除 Python 的暫存檔案（如 __pycache__） |
| make env | 顯示目前使用的python與pip |

---
### 🧠 GitHub Actions 自動同步
- 每天早上 08:00 自動同步 Google Calendar → Notion

- 請將 credentials、token 與 Notion Secret 加入 GitHub Secrets

- .github/workflows/sync.yml 內部會自動解碼並執行主程式
---
### 🖥️ 方式三：桌面版 Electron 手動同步工具（可選用）
📁 子資料夾：gcal-to-notion-desktop/

```bash
cd gcal-to-notion-desktop
npm install
npm start
```
- 適合不熟命令列者、需要隨時手動同步者

- 檔案仍需放置 credentials.json / token.json / .env

- 同步使用母資料夾的 Python 腳本，不影響 GitHub Actions
---
### ✨ 功能特色
- 📅 同步「未來 14 天內」的 Google Calendar 活動

- 🧠 自動排程（GitHub Actions）

- 🔁 已同步的事件不會重複建立（依 event_id 判斷）

- 🔒 OAuth 2.0 驗證，支援 refresh token 自動更新

- 🐳 完整 Docker 化 + 本地虛擬環境支援

---
#### 🔒 安全性說明

- 所有敏感資訊 (token.json, .env) 均已加至 .gitignore

- GitHub 使用 base64 加密儲存在 Secrets 中

- 桌面版不影響 GitHub Actions，自成一體

---

📝 other reference:
1. [OAuth 2.0 Authorization Flow api docs](https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html#google_auth_oauthlib.flow.InstalledAppFlow)
2. [InstalledAppFlow version: run_console error](https://stackoverflow.com/questions/75602866/google-oauth-attributeerror-installedappflow-object-has-no-attribute-run-co)
3. [notion api docs](https://developers.notion.com/reference/page-property-values)

---

📄 License:

本專案採用 GPL v3 授權，允許使用、修改與散布，唯須保留原作者資訊與授權聲明，並不得封閉原始碼。

