#!/bin/bash

# 快速测试脚本 - 诊断和测试分析功能

echo "================================"
echo "🔍 快速诊断"
echo "================================"
echo ""

# 1. 检查环境变量
echo "1. 检查 ANTHROPIC_API_KEY..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ⚠️  ANTHROPIC_API_KEY 未设置"
    echo "   这可能是问题所在！"
    echo ""
    echo "   解决方案："
    echo "   export ANTHROPIC_API_KEY='your-api-key'"
    echo "   或者在 Claude Code 环境中运行"
else
    key_length=${#ANTHROPIC_API_KEY}
    echo "   ✓ ANTHROPIC_API_KEY 已设置 (长度: $key_length)"
fi
echo ""

# 2. 检查虚拟环境
echo "2. 检查虚拟环境..."
if [ -f "venv/bin/python" ]; then
    echo "   ✓ venv/bin/python 存在"
    venv/bin/python --version
else
    echo "   ✗ venv/bin/python 不存在"
    echo "   请运行: python3.11 -m venv venv"
fi
echo ""

# 3. 检查 anthropic 库
echo "3. 检查 anthropic 库..."
if venv/bin/python -c "import anthropic" 2>/dev/null; then
    echo "   ✓ anthropic 已安装"
    venv/bin/pip show anthropic | grep Version
else
    echo "   ✗ anthropic 未安装"
    echo "   请运行: source venv/bin/activate && pip install anthropic"
fi
echo ""

# 4. 检查 Web 服务器
echo "4. 检查 Web 服务器..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "   ✓ Web 服务器正在运行 (端口 8000)"

    # 测试健康检查
    echo ""
    echo "   测试健康检查接口..."
    health_response=$(curl -s http://localhost:8000/health 2>&1)
    echo "   响应: $health_response"
else
    echo "   ✗ Web 服务器未运行"
    echo "   请运行: ./scripts/start_web.sh"
    exit 1
fi
echo ""

# 5. 测试 API
echo "5. 测试分析 API..."
echo "   发送测试请求..."
echo ""

api_response=$(curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"app_id":"test.quick.diagnostic","platform":"Test Platform"}' 2>&1)

echo "   API 响应:"
echo "$api_response" | python3 -m json.tool 2>/dev/null || echo "$api_response"
echo ""

echo "================================"
echo "💡 提示"
echo "================================"
echo ""
echo "如果 ANTHROPIC_API_KEY 未设置，需要："
echo "  1. 停止当前 Web 服务器 (Ctrl+C)"
echo "  2. 在同一终端设置 API Key："
echo "     export ANTHROPIC_API_KEY='your-api-key'"
echo "  3. 重新启动 Web 服务器："
echo "     ./scripts/start_web.sh"
echo ""
echo "查看 Web 服务器输出："
echo "  在启动 ./scripts/start_web.sh 的终端窗口"
echo "  应该能看到 '📥 收到分析请求' 和 '🚀 启动分析进程'"
echo ""
echo "查看分析日志："
echo "  tail -f logs/analyzer.log"
echo ""
