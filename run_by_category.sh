#!/bin/bash

# 按分类监控启动脚本

# 激活虚拟环境
source venv/bin/activate

# 运行分类监控程序
python ranking_monitor_by_category.py

# 退出虚拟环境
deactivate
