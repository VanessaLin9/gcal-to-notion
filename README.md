# GCal to Notion Sync 📅➡️📒

[![Docker Pulls](https://img.shields.io/docker/pulls/vanessalin9/gcal-to-notion)](https://hub.docker.com/r/vanessalin9/gcal-to-notion)

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
   
  範例 .env：
```bash
NOTION_TOKEN=your-notion-integration-secret
NOTION_DATABASE_ID=your-notion-database-id
```
2. 執行指令
假設你已經把這些檔案放在當前目錄，執行以下指令：
```bash
docker run -it --env-file .env \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.json:/app/token.json \
  vanessalin9/gcal-to-notion:latest
```

✅
這樣會自動同步最近的 Google Calendar 活動到你的 Notion 資料庫。

---

📄 License:
本專案僅供個人學習與私人使用。
