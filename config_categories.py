"""
分类配置文件
定义需要监控的应用分类
"""

# ===== App Store 分类配置 =====
# App Store RSS API 分类 ID (genreId)
# 文档: https://rss.applemarketingtools.com/

APP_STORE_CATEGORIES = {
    "健康与健身": {
        "name_cn": "健康与健身",
        "name_en": "Health & Fitness",
        "genre_id": "6013",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6013/json"
    },
    "社交网络": {
        "name_cn": "社交网络",
        "name_en": "Social Networking",
        "genre_id": "6005",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6005/json"
    },
    "生活方式": {
        "name_cn": "生活方式",
        "name_en": "Lifestyle",
        "genre_id": "6012",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6012/json"
    },
    "游戏": {
        "name_cn": "游戏",
        "name_en": "Games",
        "genre_id": "6014",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6014/json"
    },
    "教育": {
        "name_cn": "教育",
        "name_en": "Education",
        "genre_id": "6017",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6017/json"
    },
    "生产力": {
        "name_cn": "生产力",
        "name_en": "Productivity",
        "genre_id": "6007",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6007/json"
    },
    "生活实用": {
        "name_cn": "生活实用",
        "name_en": "Utilities",
        "genre_id": "6002",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6002/json"
    },
    "娱乐": {
        "name_cn": "娱乐",
        "name_en": "Entertainment",
        "genre_id": "6016",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6016/json"
    },
    "照片和视频": {
        "name_cn": "照片和视频",
        "name_en": "Photo & Video",
        "genre_id": "6008",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6008/json"
    },
    "旅行": {
        "name_cn": "旅行",
        "name_en": "Travel",
        "genre_id": "6003",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6003/json"
    },
    "绘图与设计": {
        "name_cn": "绘图与设计",
        "name_en": "Graphics & Design",
        "genre_id": "6027",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6027/json"
    },
    "书籍": {
        "name_cn": "书籍",
        "name_en": "Books",
        "genre_id": "6018",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6018/json"
    },
    "购物": {
        "name_cn": "购物",
        "name_en": "Shopping",
        "genre_id": "6024",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6024/json"
    },
    "商务": {
        "name_cn": "商务",
        "name_en": "Business",
        "genre_id": "6000",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6000/json"
    },
    "体育": {
        "name_cn": "体育",
        "name_en": "Sports",
        "genre_id": "6004",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6004/json"
    },
    "天气": {
        "name_cn": "天气",
        "name_en": "Weather",
        "genre_id": "6001",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6001/json"
    },
    "新闻": {
        "name_cn": "新闻",
        "name_en": "News",
        "genre_id": "6009",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6009/json"
    },
    "音乐": {
        "name_cn": "音乐",
        "name_en": "Music",
        "genre_id": "6011",
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=6011/json"
    }
}

# ===== Google Play 分类配置 =====
# Google Play 分类 ID
# 文档: https://developers.google.com/android-publisher/api-ref/rest/v3/applications

GOOGLE_PLAY_CATEGORIES = {
    "工具": {
        "name_cn": "工具",
        "name_en": "Tools",
        "category_id": "TOOLS"
    },
    "健身与健康": {
        "name_cn": "健身与健康",
        "name_en": "Health & Fitness",
        "category_id": "HEALTH_AND_FITNESS"
    },
    "旅行与当地": {
        "name_cn": "旅行与当地",
        "name_en": "Travel & Local",
        "category_id": "TRAVEL_AND_LOCAL"
    },
    "社交": {
        "name_cn": "社交",
        "name_en": "Social",
        "category_id": "SOCIAL"
    },
    "生产力": {
        "name_cn": "生产力",
        "name_en": "Productivity",
        "category_id": "PRODUCTIVITY"
    },
    "生活方式": {
        "name_cn": "生活方式",
        "name_en": "Lifestyle",
        "category_id": "LIFESTYLE"
    },
    "游戏": {
        "name_cn": "游戏",
        "name_en": "Game",
        "category_id": "GAME"
    },
    "娱乐": {
        "name_cn": "娱乐",
        "name_en": "Entertainment",
        "category_id": "ENTERTAINMENT"
    },
    "约会": {
        "name_cn": "约会",
        "name_en": "Dating",
        "category_id": "DATING"
    },
    "个性化": {
        "name_cn": "个性化",
        "name_en": "Personalization",
        "category_id": "PERSONALIZATION"
    },
    "购物": {
        "name_cn": "购物",
        "name_en": "Shopping",
        "category_id": "SHOPPING"
    },
    "活动": {
        "name_cn": "活动",
        "name_en": "Events",
        "category_id": "EVENTS"
    },
    "家庭": {
        "name_cn": "家庭",
        "name_en": "Family",
        "category_id": "FAMILY"
    },
    "家庭与家居": {
        "name_cn": "家庭与家居",
        "name_en": "House & Home",
        "category_id": "HOUSE_AND_HOME"
    },
    "漫画": {
        "name_cn": "漫画",
        "name_en": "Comics",
        "category_id": "COMICS"
    },
    "美妆": {
        "name_cn": "美妆",
        "name_en": "Beauty",
        "category_id": "BEAUTY"
    },
    "商务": {
        "name_cn": "商务",
        "name_en": "Business",
        "category_id": "BUSINESS"
    },
    "摄影": {
        "name_cn": "摄影",
        "name_en": "Photography",
        "category_id": "PHOTOGRAPHY"
    },
    "视频播放器和编辑器": {
        "name_cn": "视频播放器和编辑器",
        "name_en": "Video Players & Editors",
        "category_id": "VIDEO_PLAYERS"
    },
    "书籍和参考": {
        "name_cn": "书籍和参考",
        "name_en": "Books & Reference",
        "category_id": "BOOKS_AND_REFERENCE"
    },
    "体育": {
        "name_cn": "体育",
        "name_en": "Sports",
        "category_id": "SPORTS"
    },
    "天气": {
        "name_cn": "天气",
        "name_en": "Weather",
        "category_id": "WEATHER"
    },
    "医疗": {
        "name_cn": "医疗",
        "name_en": "Medical",
        "category_id": "MEDICAL"
    },
    "艺术和设计": {
        "name_cn": "艺术和设计",
        "name_en": "Art & Design",
        "category_id": "ART_AND_DESIGN"
    },
    "音乐和音频": {
        "name_cn": "音乐和音频",
        "name_en": "Music & Audio",
        "category_id": "MUSIC_AND_AUDIO"
    },
    "育儿": {
        "name_cn": "育儿",
        "name_en": "Parenting",
        "category_id": "PARENTING"
    }
}

# Google Play 配置
GOOGLE_PLAY_COUNTRY = "us"
GOOGLE_PLAY_COLLECTION = "TOP_FREE"  # 免费榜
