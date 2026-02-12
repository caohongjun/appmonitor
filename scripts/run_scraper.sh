#!/bin/bash
# 运行爬虫脚本

cd "$(dirname "$0")/.."

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行爬虫
python modules/scraper.py "$@"
