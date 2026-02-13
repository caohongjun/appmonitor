#!/bin/bash

# 测试API是否正常工作

echo "================================"
echo "🧪 测试 API 接口"
echo "================================"
echo ""

# 检查服务器是否运行
echo "1. 检查Web服务器..."
if lsof -i :8000 >/dev/null 2>&1; then
    echo "   ✓ Web服务器正在运行"
else
    echo "   ✗ Web服务器未运行"
    echo "   请先运行: ./scripts/start_web.sh"
    exit 1
fi
echo ""

# 测试API健康检查
echo "2. 测试健康检查接口..."
response=$(curl -s http://localhost:8000/health)
echo "   响应: $response"
echo ""

# 触发分析
echo "3. 触发测试分析..."
echo "   发送POST请求到 /api/analyze"
echo ""

response=$(curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"app_id":"test.example.app","platform":"App Store"}')

echo "   API响应:"
echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
echo ""

# 等待几秒让分析开始
echo "4. 等待5秒..."
sleep 5
echo ""

# 检查日志
echo "5. 检查日志文件..."
if [ -f "logs/analyzer.log" ]; then
    echo "   ✓ 日志文件存在"
    echo ""
    echo "   最近的日志:"
    tail -20 logs/analyzer.log | sed 's/^/      /'
else
    echo "   ✗ 日志文件不存在"
fi
echo ""

# 检查进程
echo "6. 检查分析进程..."
if ps aux | grep analyzer.py | grep -v grep >/dev/null 2>&1; then
    echo "   ✓ 发现分析进程:"
    ps aux | grep analyzer.py | grep -v grep | sed 's/^/      /'
else
    echo "   ✗ 没有运行中的分析进程"
fi
echo ""

echo "================================"
echo "💡 提示"
echo "================================"
echo "查看Web服务器输出:"
echo "  在启动 ./scripts/start_web.sh 的终端查看"
echo ""
echo "实时查看日志:"
echo "  tail -f logs/analyzer.log"
echo ""
