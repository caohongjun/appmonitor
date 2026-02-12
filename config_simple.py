"""
简化配置文件 - 模块1专用
只包含爬虫必需的配置
"""

import os

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# App Store 分类配置
APP_STORE_CATEGORIES = {
    "health_fitness": {
        "name_cn": "健康与健身",
        "name_en": "Health & Fitness",
        "genre_id": "6013"
    },
    "social": {
        "name_cn": "社交网络",
        "name_en": "Social Networking",
        "genre_id": "6005"
    },
    "lifestyle": {
        "name_cn": "生活方式",
        "name_en": "Lifestyle",
        "genre_id": "6012"
    },
    "games": {
        "name_cn": "游戏",
        "name_en": "Games",
        "genre_id": "6014"
    }
}

# Google Play 分类配置
GOOGLE_PLAY_CATEGORIES = {
    "health_fitness": {
        "name_cn": "健康与健身",
        "name_en": "HEALTH_AND_FITNESS"
    },
    "social": {
        "name_cn": "社交",
        "name_en": "SOCIAL"
    },
    "lifestyle": {
        "name_cn": "生活方式",
        "name_en": "LIFESTYLE"
    },
    "games": {
        "name_cn": "游戏",
        "name_en": "GAME"
    },
    "dating": {
        "name_cn": "约会",
        "name_en": "DATING"
    },
    "tools": {
        "name_cn": "工具",
        "name_en": "TOOLS"
    }
}

# 爬虫配置
SCRAPER_CONFIG = {
    "app_store": {
        "country": "us",
        "limit": 100,  # 每个分类爬取数量
        "delay": 2  # 请求延迟（秒）
    },
    "google_play": {
        "country": "us",
        "collection": "TOP_FREE",
        "limit": 100,
        "delay": 3  # 请求延迟（秒）
    },
    "retry_times": 3,  # 失败重试次数
    "timeout": 30  # 请求超时时间（秒）
}
