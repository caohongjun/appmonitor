#!/bin/bash

# 敏感信息检查脚本

echo "🔍 检查敏感信息..."
echo "=" >&2

# 检查是否有 config.py
if [ -f "config.py" ]; then
    echo "✅ config.py 存在（将被 .gitignore 忽略）"
else
    echo "⚠️  config.py 不存在"
fi

# 检查是否有 config.example.py
if [ -f "config.example.py" ]; then
    echo "✅ config.example.py 存在"

    # 检查示例文件是否包含真实密钥
    if grep -q "cli_a902c\|xxRkmpx\|ZSCXsjpjxh" config.example.py; then
        echo "❌ 错误: config.example.py 包含真实密钥！"
        exit 1
    else
        echo "✅ config.example.py 不包含真实密钥"
    fi
else
    echo "❌ config.example.py 不存在"
    exit 1
fi

# 检查 .gitignore
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore 存在"

    if grep -q "config.py" .gitignore; then
        echo "✅ .gitignore 包含 config.py"
    else
        echo "❌ 错误: .gitignore 未包含 config.py！"
        exit 1
    fi
else
    echo "❌ .gitignore 不存在"
    exit 1
fi

# 搜索可能的敏感信息（排除 config.py）
echo ""
echo "🔎 搜索敏感信息（排除 config.py）..."
FOUND=$(grep -r "cli_a902c0f13bb89bce\|xxRkmpxnexfuEJ5mmIkLuMQPOVwpq4xn\|ZSCXsjpjxhyjUjtEaEEcxQVnnEg" \
    --include="*.py" \
    --include="*.md" \
    --include="*.txt" \
    --include="*.sh" \
    --exclude="config.py" \
    --exclude="check_sensitive.sh" \
    --exclude-dir=venv \
    --exclude-dir=.git \
    . 2>/dev/null)

if [ -n "$FOUND" ]; then
    echo "❌ 发现敏感信息！"
    echo "$FOUND"
    exit 1
else
    echo "✅ 未发现敏感信息（config.py 已排除）"
fi

echo ""
echo "=" * 50
echo "✅ 检查通过！可以安全上传到 Git"
echo "=" * 50
echo ""
echo "下一步："
echo "1. git init"
echo "2. git add ."
echo "3. git commit -m 'Initial commit'"
echo "4. git remote add origin <your-repo-url>"
echo "5. git push -u origin main"
