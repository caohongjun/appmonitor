"""
Google Play 爬虫模块
使用 google-play-scraper 库获取榜单数据
"""

import time
from typing import List, Dict, Optional
from datetime import datetime

try:
    from google_play_scraper import search, app
    GOOGLE_PLAY_AVAILABLE = True
except ImportError:
    GOOGLE_PLAY_AVAILABLE = False
    print("警告: google-play-scraper 未安装，请运行: pip install google-play-scraper")


class GooglePlayScraper:
    """Google Play 爬虫类"""

    def __init__(self, country="us", collection="TOP_FREE", limit=100, delay=3, timeout=30):
        """
        初始化爬虫

        Args:
            country: 国家代码（默认 us）
            collection: 榜单类型（TOP_FREE / TOP_PAID / TRENDING）
            limit: 每个分类爬取数量（默认 100）
            delay: 请求延迟（秒）
            timeout: 请求超时时间（秒）
        """
        if not GOOGLE_PLAY_AVAILABLE:
            raise ImportError("google-play-scraper 未安装")

        self.country = country
        self.collection = collection
        self.limit = limit
        self.delay = delay
        self.timeout = timeout

    def scrape_category(self, category_key: str, category_name: str) -> List[Dict]:
        """
        爬取指定分类的榜单

        Args:
            category_key: 分类键（如 HEALTH_AND_FITNESS）
            category_name: 分类名称（中文）

        Returns:
            List[Dict]: 应用列表
        """
        try:
            print(f"  正在爬取 Google Play - {category_name}...")

            # 使用 search 方法搜索该分类的热门应用
            # 注意：google-play-scraper 没有官方榜单API，通过搜索热门关键词获取

            # 根据分类搜索相关热门应用
            category_keywords = {
                "HEALTH_AND_FITNESS": "fitness workout health",
                "SOCIAL": "social chat messaging",
                "LIFESTYLE": "lifestyle",
                "GAME": "game",
                "DATING": "dating meet",
                "TOOLS": "tools utility"
            }

            keyword = category_keywords.get(category_key, category_name)
            apps_data = search(
                keyword,
                lang="en",
                country=self.country,
                n_hits=self.limit
            )

            if not apps_data:
                print(f"  ⚠️  {category_name} 未获取到数据")
                return []

            apps = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for rank, app_data in enumerate(apps_data, start=1):
                app_info = self._parse_app_data(app_data, rank, category_name, timestamp)
                if app_info:
                    apps.append(app_info)

            print(f"  ✓ {category_name} 爬取成功，共 {len(apps)} 个应用")
            time.sleep(self.delay)  # 延迟避免请求过快
            return apps

        except Exception as e:
            print(f"  ✗ {category_name} 爬取失败: {e}")
            return []

    def _parse_app_data(self, app_data: Dict, rank: int, category: str, timestamp: str) -> Optional[Dict]:
        """
        解析单个应用数据

        Args:
            app_data: 应用原始数据
            rank: 排名
            category: 分类名称
            timestamp: 时间戳

        Returns:
            Optional[Dict]: 应用数据字典
        """
        try:
            app_id = app_data.get("appId", "")
            name = app_data.get("title", "")
            developer = app_data.get("developer", "")
            icon_url = app_data.get("icon", "")
            store_url = f"https://play.google.com/store/apps/details?id={app_id}"

            return {
                "platform": "Google Play",
                "category": category,
                "app_id": app_id,
                "rank": rank,
                "name": name,
                "developer": developer,
                "store_url": store_url,
                "icon_url": icon_url,
                "timestamp": timestamp
            }

        except Exception as e:
            print(f"    解析应用数据失败: {e}")
            return None


if __name__ == "__main__":
    # 测试代码
    if GOOGLE_PLAY_AVAILABLE:
        scraper = GooglePlayScraper()
        apps = scraper.scrape_category("HEALTH_AND_FITNESS", "健康与健身")
        print(f"\n共获取 {len(apps)} 个应用")
        if apps:
            print(f"第一个应用: {apps[0]}")
    else:
        print("请先安装: pip install google-play-scraper")
