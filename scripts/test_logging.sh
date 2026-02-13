#!/bin/bash

# 测试日志功能

echo "================================"
echo "🧪 测试日志功能"
echo "================================"
echo ""

cd "$(dirname "$0")/.."

# 1. 删除旧日志（如果存在）
if [ -f "logs/analyzer.log" ]; then
    echo "1. 删除旧日志..."
    rm logs/analyzer.log
    echo "   ✓ 已删除"
else
    echo "1. 日志文件不存在（正常）"
fi
echo ""

# 2. 确保日志目录存在
echo "2. 检查日志目录..."
if [ -d "logs" ]; then
    echo "   ✓ logs/ 目录存在"
else
    echo "   ✗ logs/ 目录不存在，创建中..."
    mkdir -p logs
fi
echo ""

# 3. 测试写入权限
echo "3. 测试写入权限..."
if touch logs/test_write.tmp 2>/dev/null; then
    echo "   ✓ logs/ 目录可写"
    rm logs/test_write.tmp
else
    echo "   ✗ logs/ 目录不可写"
    echo "   修复: chmod 755 logs"
    exit 1
fi
echo ""

# 4. 激活虚拟环境
echo "4. 激活虚拟环境..."
source venv/bin/activate
echo "   ✓ 虚拟环境已激活"
echo ""

# 5. 运行分析器（使用测试参数）
echo "5. 运行分析器..."
echo "   命令: python modules/analyzer.py --app-id test.log.check --platform Test"
echo ""
echo "================================"
python modules/analyzer.py --app-id "test.log.check" --platform "Test" 2>&1 | head -50
echo "================================"
echo ""

# 6. 检查日志文件是否生成
echo "6. 检查日志文件..."
if [ -f "logs/analyzer.log" ]; then
    echo "   ✓ 日志文件已生成"
    echo ""
    echo "   文件信息:"
    ls -lh logs/analyzer.log
    echo ""
    echo "   最近10行内容:"
    tail -10 logs/analyzer.log | sed 's/^/      /'
else
    echo "   ✗ 日志文件未生成"
    echo ""
    echo "   可能原因："
    echo "   1. analyzer.py 没有成功运行"
    echo "   2. 日志目录权限问题"
    echo "   3. 磁盘空间不足"
fi
echo ""

echo "================================"
echo "完成"
echo "================================"
