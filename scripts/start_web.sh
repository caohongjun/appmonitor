#!/bin/bash
# 启动Web服务器（支持静态文件 + API接口）

cd "$(dirname "$0")/.."

# 确保虚拟环境中有必要的依赖
source venv/bin/activate

# 启动Web服务器
python simple_server.py
