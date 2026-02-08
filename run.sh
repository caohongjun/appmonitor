#!/bin/bash

# 应用商店榜单监控工具启动脚本

# 激活虚拟环境
source venv/bin/activate

# 运行主程序
python ranking_monitor_feishu.py

# 退出虚拟环境
deactivate
