#!/bin/bash

# 测试analyzer.py是否正常工作

echo "================================"
echo "🧪 测试 analyzer.py"
echo "================================"
echo ""

# 激活虚拟环境
echo "1. 激活虚拟环境..."
source venv/bin/activate
echo "   ✓ 虚拟环境已激活"
echo ""

# 检查Python和anthropic
echo "2. 检查环境..."
python --version
echo ""
if pip list | grep -q anthropic; then
    echo "   ✓ anthropic已安装"
else
    echo "   ✗ anthropic未安装"
    echo "   正在安装..."
    pip install anthropic
fi
echo ""

# 确保目录存在
echo "3. 确保目录存在..."
mkdir -p logs
mkdir -p data/analysis
echo "   ✓ 目录已创建"
echo ""

# 清空旧日志（可选）
echo "4. 准备日志文件..."
> logs/analyzer.log
echo "   ✓ 日志文件已清空"
echo ""

# 运行测试
echo "5. 运行analyzer.py..."
echo "================================"
echo ""

python modules/analyzer.py --app-id "test.example.app" --platform "App Store" 2>&1

echo ""
echo "================================"
echo ""

# 检查日志
echo "6. 检查日志输出..."
if [ -f "logs/analyzer.log" ]; then
    echo "   ✓ 日志文件已创建"
    echo ""
    echo "   最近10行日志:"
    tail -10 logs/analyzer.log | sed 's/^/      /'
else
    echo "   ✗ 日志文件未创建"
fi
echo ""

# 检查结果
echo "7. 检查分析结果..."
today=$(date +%Y-%m-%d)
if [ -f "data/analysis/$today/test.example.app.json" ]; then
    echo "   ✓ 分析结果已生成"
    echo "   文件: data/analysis/$today/test.example.app.json"
else
    echo "   ✗ 分析结果未生成"
fi
echo ""

echo "================================"
echo "测试完成"
echo "================================"
