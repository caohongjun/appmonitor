#!/bin/bash
# 启动增强版Web服务器（支持静态文件 + API接口）

cd "$(dirname "$0")/.."

# 确保虚拟环境中有必要的依赖
source venv/bin/activate

# 检查并安装anthropic（如果需要）
if ! pip list 2>/dev/null | grep -q anthropic; then
    echo "📦 安装anthropic库..."
    pip install anthropic -q
fi

# 启动增强版服务器
python simple_server.py
