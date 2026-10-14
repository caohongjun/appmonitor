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
    },
    "education": {
        "name_cn": "教育",
        "name_en": "Education",
        "genre_id": "6017"
    },
    "productivity": {
        "name_cn": "生产力",
        "name_en": "Productivity",
        "genre_id": "6007"
    },
    "utilities": {
        "name_cn": "生活实用",
        "name_en": "Utilities",
        "genre_id": "6002"
    },
    "entertainment": {
        "name_cn": "娱乐",
        "name_en": "Entertainment",
        "genre_id": "6016"
    },
    "photo_video": {
        "name_cn": "照片和视频",
        "name_en": "Photo & Video",
        "genre_id": "6008"
    },
    "travel": {
        "name_cn": "旅行",
        "name_en": "Travel",
        "genre_id": "6003"
    },
    "graphics_design": {
        "name_cn": "绘图与设计",
        "name_en": "Graphics & Design",
        "genre_id": "6027"
    },
    "books": {
        "name_cn": "书籍",
        "name_en": "Books",
        "genre_id": "6018"
    },
    "shopping": {
        "name_cn": "购物",
        "name_en": "Shopping",
        "genre_id": "6024"
    },
    "business": {
        "name_cn": "商务",
        "name_en": "Business",
        "genre_id": "6000"
    },
    "sports": {
        "name_cn": "体育",
        "name_en": "Sports",
        "genre_id": "6004"
    },
    "weather": {
        "name_cn": "天气",
        "name_en": "Weather",
        "genre_id": "6001"
    },
    "news": {
        "name_cn": "新闻",
        "name_en": "News",
        "genre_id": "6009"
    },
    "music": {
        "name_cn": "音乐",
        "name_en": "Music",
        "genre_id": "6011"
    }
}

# Google Play 分类配置
# category 值对应 facundoolano/google-play-scraper 的 constants.category
GOOGLE_PLAY_CATEGORIES = {
    "tools": {
        "name_cn": "工具",
        "name_en": "TOOLS"
    },
    "health_fitness": {
        "name_cn": "健身与健康",
        "name_en": "HEALTH_AND_FITNESS"
    },
    "travel_local": {
        "name_cn": "旅行与当地",
        "name_en": "TRAVEL_AND_LOCAL"
    },
    "social": {
        "name_cn": "社交",
        "name_en": "SOCIAL"
    },
    "productivity": {
        "name_cn": "生产力",
        "name_en": "PRODUCTIVITY"
    },
    "lifestyle": {
        "name_cn": "生活方式",
        "name_en": "LIFESTYLE"
    },
    "games": {
        "name_cn": "游戏",
        "name_en": "GAME"
    },
    "entertainment": {
        "name_cn": "娱乐",
        "name_en": "ENTERTAINMENT"
    },
    "dating": {
        "name_cn": "约会",
        "name_en": "DATING"
    },
    "personalization": {
        "name_cn": "个性化",
        "name_en": "PERSONALIZATION"
    },
    "shopping": {
        "name_cn": "购物",
        "name_en": "SHOPPING"
    },
    "events": {
        "name_cn": "活动",
        "name_en": "EVENTS"
    },
    "family": {
        "name_cn": "家庭",
        "name_en": "FAMILY"
    },
    "house_home": {
        "name_cn": "家庭与家居",
        "name_en": "HOUSE_AND_HOME"
    },
    "comics": {
        "name_cn": "漫画",
        "name_en": "COMICS"
    },
    "beauty": {
        "name_cn": "美妆",
        "name_en": "BEAUTY"
    },
    "business": {
        "name_cn": "商务",
        "name_en": "BUSINESS"
    },
    "photography": {
        "name_cn": "摄影",
        "name_en": "PHOTOGRAPHY"
    },
    "video_players": {
        "name_cn": "视频播放器和编辑器",
        "name_en": "VIDEO_PLAYERS"
    },
    "books_reference": {
        "name_cn": "书籍和参考",
        "name_en": "BOOKS_AND_REFERENCE"
    },
    "sports": {
        "name_cn": "体育",
        "name_en": "SPORTS"
    },
    "weather": {
        "name_cn": "天气",
        "name_en": "WEATHER"
    },
    "medical": {
        "name_cn": "医疗",
        "name_en": "MEDICAL"
    },
    "art_design": {
        "name_cn": "艺术和设计",
        "name_en": "ART_AND_DESIGN"
    },
    "music_audio": {
        "name_cn": "音乐和音频",
        "name_en": "MUSIC_AND_AUDIO"
    },
    "parenting": {
        "name_cn": "育儿",
        "name_en": "PARENTING"
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
    "timeout": 120  # 请求超时时间（秒）；Google Play fullDetail 模式下 100 个 app 约需 30-60s
}
