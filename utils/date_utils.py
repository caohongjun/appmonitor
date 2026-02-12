"""
日期处理工具模块
"""

from datetime import datetime, timedelta


def get_today() -> str:
    """获取今天的日期字符串（YYYY-MM-DD）"""
    return datetime.now().strftime("%Y-%m-%d")


def get_yesterday() -> str:
    """获取昨天的日期字符串（YYYY-MM-DD）"""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def get_date_before(days: int) -> str:
    """
    获取N天前的日期字符串

    Args:
        days: 天数

    Returns:
        str: 日期字符串（YYYY-MM-DD）
    """
    return (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")


def is_valid_date(date_str: str) -> bool:
    """
    验证日期字符串是否有效

    Args:
        date_str: 日期字符串（YYYY-MM-DD）

    Returns:
        bool: 是否有效
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
