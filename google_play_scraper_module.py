"""
Google Play 抓取模块
使用 google-play-scraper 库获取美国区热门排行榜
注意：由于 google-play-scraper 库限制，我们使用搜索热门关键词的方式获取热门应用
"""

from google_play_scraper import search, app
from datetime import datetime
from typing import List, Dict


class GooglePlayScraper:
    def __init__(self, country: str = "us", category: str = "APPLICATION", collection_type: str = "TOP_FREE"):
        self.country = country
        self.category = category
        self.collection_type = collection_type

    def fetch_top_apps(self, limit: int = 100) -> List[Dict]:
        """
        获取 Google Play 美国区热门排行榜

        注意：由于 API 限制，此方法通过搜索热门关键词来获取热门应用
        结果可能不是官方榜单，而是基于搜索热度的应用列表

        Args:
            limit: 获取的应用数量，默认 100

        Returns:
            List[Dict]: 包含 app_id, rank, name, developer, icon_url, timestamp 的字典列表
        """
        try:
            print(f"⚠️  注意：Google Play 抓取使用搜索方式，非官方榜单")

            # 使用多个热门关键词搜索来获取热门应用
            # 这不是真正的榜单，而是基于搜索结果的近似
            popular_terms = ["game", "app", "video", "music", "social", "photo", "tool"]

            apps_dict = {}  # 用字典去重

            for term in popular_terms:
                try:
                    results = search(
                        term,
                        lang="en",
                        country=self.country.lower(),
                        n_hits=30  # 每个关键词搜索30个
                    )

                    for result in results:
                        app_id = result.get('appId')
                        if app_id and app_id not in apps_dict:
                            apps_dict[app_id] = {
                                'platform': 'Google Play',
                                'app_id': app_id,
                                'rank': 0,  # 临时占位，稍后更新
                                'name': result.get('title', 'N/A'),
                                'developer': result.get('developer', 'N/A'),
                                'icon_url': result.get('icon', 'N/A'),
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }

                        # 如果已经收集够了，停止
                        if len(apps_dict) >= limit:
                            break

                    if len(apps_dict) >= limit:
                        break

                except Exception as e:
                    print(f"搜索关键词 '{term}' 失败: {e}")
                    continue

            # 转换为列表并添加排名
            apps = []
            for idx, (app_id, app_info) in enumerate(apps_dict.items(), start=1):
                app_info['rank'] = idx
                apps.append(app_info)
                if idx >= limit:
                    break

            print(f"成功抓取 Google Play {len(apps)} 个应用（基于搜索）")
            return apps

        except Exception as e:
            print(f"抓取 Google Play 数据失败: {e}")
            return []


if __name__ == "__main__":
    # 测试代码
    from config import GOOGLE_PLAY_COUNTRY, GOOGLE_PLAY_CATEGORY, GOOGLE_PLAY_COLLECTION

    scraper = GooglePlayScraper(
        country=GOOGLE_PLAY_COUNTRY,
        category=GOOGLE_PLAY_CATEGORY,
        collection_type=GOOGLE_PLAY_COLLECTION
    )

    apps = scraper.fetch_top_apps(limit=100)

    if apps:
        print(f"\n前 5 名:")
        for app in apps[:5]:
            print(f"{app['rank']}. {app['name']} - {app['developer']}")
