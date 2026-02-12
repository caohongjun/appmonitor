"""
数据存储工具模块
"""

import json
import os
from datetime import datetime
from typing import List, Dict


def save_to_json(data: Dict, file_path: str) -> bool:
    """
    保存数据到JSON文件

    Args:
        data: 要保存的数据
        file_path: 文件路径

    Returns:
        bool: 是否成功
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {e}")
        return False


def load_from_json(file_path: str) -> Dict:
    """
    从JSON文件加载数据

    Args:
        file_path: 文件路径

    Returns:
        Dict: 加载的数据，失败返回空字典
    """
    try:
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败: {e}")
        return {}


def get_data_file_path(date_str: str, platform: str, category: str, base_dir: str) -> str:
    """
    获取数据文件路径

    Args:
        date_str: 日期字符串（YYYY-MM-DD）
        platform: 平台（app_store / google_play）
        category: 分类
        base_dir: 基础目录

    Returns:
        str: 文件路径
    """
    return os.path.join(base_dir, "raw", date_str, platform, f"{category}.json")
