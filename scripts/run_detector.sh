#!/bin/bash
# 运行新上榜产品识别脚本

cd "$(dirname "$0")/.."

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 运行识别器
python modules/detector.py "$@"
