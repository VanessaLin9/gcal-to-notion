# Makefile

run:
	python sync_gcal_to_notion.py

# 用虛擬環境執行主程式
dev:
	.venv/bin/python sync_gcal_to_notion.py

# 安裝套件
install:
	pip install -r requirements.txt

# 清除暫存檔案
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

# 顯示目前使用的 Python 和 pip
env:
	which python && which pip

.PHONY: run dev install clean env
