#!/bin/bash
# 启动Web服务器

cd "$(dirname "$0")/.."

echo "🚀 启动 Web 服务器..."
echo "📂 根目录: $(pwd)"
echo ""
echo "👉 访问地址: http://localhost:8000/web/"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

# 使用Python启动HTTP服务器
python3 -m http.server 8000
