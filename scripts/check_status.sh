#!/bin/bash

# 系统状态检查脚本

echo "================================"
echo "🔍 系统状态检查"
echo "================================"
echo ""

# 检查Web服务器
echo "1️⃣ 检查Web服务器状态..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "   ✓ Web服务器正在运行 (端口 8000)"
    ps aux | grep simple_server.py | grep -v grep
else
    echo "   ✗ Web服务器未运行"
    echo "   提示: 运行 ./scripts/start_web.sh 启动服务器"
fi
echo ""

# 检查分析进程
echo "2️⃣ 检查分析进程..."
if ps aux | grep analyzer.py | grep -v grep >/dev/null 2>&1; then
    echo "   ✓ 发现正在运行的分析进程:"
    ps aux | grep analyzer.py | grep -v grep
else
    echo "   ✗ 没有运行中的分析进程"
fi
echo ""

# 检查日志文件
echo "3️⃣ 检查日志文件..."
if [ -f "logs/analyzer.log" ]; then
    echo "   ✓ 分析日志存在: logs/analyzer.log"
    echo "   最近5条日志:"
    tail -5 logs/analyzer.log | sed 's/^/      /'
else
    echo "   ✗ 分析日志不存在: logs/analyzer.log"
fi
echo ""

# 检查虚拟环境
echo "4️⃣ 检查虚拟环境..."
if [ -d "venv" ]; then
    echo "   ✓ 虚拟环境存在"
    if [ -f "venv/bin/python" ]; then
        echo "   ✓ Python可执行文件存在"
        venv/bin/python --version
    else
        echo "   ✗ Python可执行文件不存在"
    fi
else
    echo "   ✗ 虚拟环境不存在"
    echo "   提示: 运行 python3.11 -m venv venv 创建虚拟环境"
fi
echo ""

# 检查anthropic库
echo "5️⃣ 检查anthropic库..."
if venv/bin/pip list 2>/dev/null | grep -q anthropic; then
    echo "   ✓ anthropic库已安装"
    venv/bin/pip show anthropic 2>/dev/null | grep Version | sed 's/^/      /'
else
    echo "   ✗ anthropic库未安装"
    echo "   提示: 运行 source venv/bin/activate && pip install anthropic"
fi
echo ""

# 检查API密钥
echo "6️⃣ 检查API密钥..."
if [ -n "$ANTHROPIC_API_KEY" ]; then
    echo "   ✓ ANTHROPIC_API_KEY 已设置"
    echo "   密钥长度: ${#ANTHROPIC_API_KEY} 字符"
else
    echo "   ⚠️  ANTHROPIC_API_KEY 未设置"
    echo "   提示: Claude Code环境会自动使用当前API密钥"
fi
echo ""

# 检查数据目录
echo "7️⃣ 检查数据目录..."
if [ -d "data/analysis" ]; then
    echo "   ✓ 分析结果目录存在"
    total=$(find data/analysis -name "*.json" 2>/dev/null | wc -l)
    echo "   已有分析结果: $total 个"
else
    echo "   ✗ 分析结果目录不存在"
    mkdir -p data/analysis
    echo "   ✓ 已创建目录"
fi
echo ""

# 检查最近的分析结果
echo "8️⃣ 最近的分析结果..."
if [ -d "data/analysis" ]; then
    latest=$(find data/analysis -name "*.json" -type f 2>/dev/null | head -5)
    if [ -n "$latest" ]; then
        echo "$latest" | while read file; do
            echo "   - $file"
        done
    else
        echo "   (无)"
    fi
else
    echo "   (无)"
fi
echo ""

echo "================================"
echo "💡 常用命令"
echo "================================"
echo "查看实时日志:"
echo "  tail -f logs/analyzer.log"
echo ""
echo "查看Web服务器输出:"
echo "  (在启动服务器的终端窗口查看)"
echo ""
echo "手动测试分析:"
echo "  source venv/bin/activate"
echo "  python modules/analyzer.py --app-id test.app --platform 'App Store'"
echo ""
echo "重启Web服务器:"
echo "  pkill -f simple_server.py"
echo "  ./scripts/start_web.sh"
echo ""
