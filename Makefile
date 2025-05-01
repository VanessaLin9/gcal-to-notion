# Makefile

# 本機執行程式
run:
	python sync_gcal_to_notion.py

# 啟動 venv + 執行
dev:
	source .venv/bin/activate && python sync_gcal_to_notion.py

# 安裝套件
install:
	pip install -r requirements.txt

# 清除暫存檔
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

# 顯示目前使用的 Python 和 pip
env:
	which python && which pip
