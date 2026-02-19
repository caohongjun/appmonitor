#!/bin/bash
# 启动Web服务器（支持静态文件 + API接口）

cd "$(dirname "$0")/.."

# 启动Web服务器（直接使用虚拟环境的Python）
./venv/bin/python simple_server.py
