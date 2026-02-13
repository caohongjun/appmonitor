#!/bin/bash

# AI智能分析运行脚本

echo "================================"
echo "🤖 AI智能分析"
echo "================================"
echo ""

# 激活虚拟环境
source venv/bin/activate

# 检查是否安装anthropic
if ! pip list | grep -q anthropic; then
    echo "📦 安装anthropic库..."
    pip install anthropic
fi

echo "📊 开始分析队列中的应用..."
echo ""

# 运行分析模块
python modules/analyzer.py "$@"

echo ""
echo "================================"
echo "✓ 分析完成"
echo "================================"
echo ""
echo "💡 提示："
echo "  - 刷新网页查看分析结果"
echo "  - 访问 web/analyzer.html 查看队列"
echo "  - 分析结果保存在 data/analysis/"
echo ""
