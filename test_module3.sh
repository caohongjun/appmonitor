#!/bin/bash

# 模块3功能测试脚本

echo "================================"
echo "模块3：AI智能分析 - 功能测试"
echo "================================"
echo ""

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
echo "1. 检查依赖..."
pip list | grep -E "flask|anthropic" > /dev/null
if [ $? -ne 0 ]; then
    echo "   安装依赖..."
    pip install flask flask-cors anthropic
fi
echo "   ✓ 依赖已安装"
echo ""

# 检查API密钥
echo "2. 检查Anthropic API密钥..."
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "   ⚠️  警告：未设置ANTHROPIC_API_KEY环境变量"
    echo "   模块将尝试使用当前Claude Code环境的API"
else
    echo "   ✓ API密钥已设置"
fi
echo ""

# 检查数据目录
echo "3. 检查数据目录..."
mkdir -p data/analysis
echo "   ✓ 数据目录已创建"
echo ""

# 创建测试队列
echo "4. 创建测试队列..."
cat > data/analysis_queue.json << 'EOF'
[
  {
    "app_id": "test.example.app",
    "name": "测试应用",
    "platform": "App Store",
    "category": "健康与健身",
    "developer": "测试开发者",
    "rank": 1,
    "store_url": "https://example.com",
    "icon_url": "https://example.com/icon.png",
    "status": "pending",
    "added_time": "2026-02-13 10:00:00"
  }
]
EOF
echo "   ✓ 测试队列已创建"
echo ""

echo "================================"
echo "测试准备完成！"
echo "================================"
echo ""
echo "接下来的步骤："
echo ""
echo "1. 启动Web服务器："
echo "   ./start_web_server.sh"
echo ""
echo "2. 打开浏览器访问："
echo "   - 分析队列：file://$(pwd)/web/analyzer.html"
echo "   - 新产品：file://$(pwd)/web/detector.html"
echo ""
echo "注意：需要先启动Web服务器才能使用分析功能！"
echo ""
