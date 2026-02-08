"""
Google Play 按分类抓取模块
使用 google-play-scraper 库按分类获取免费榜
"""

from google_play_scraper import search
from datetime import datetime
from typing import List, Dict


class GooglePlayScraperByCategory:
    def __init__(self, country: str = "us"):
        self.country = country

    def fetch_category(self, category_name: str, category_id: str, limit: int = 100) -> List[Dict]:
        """
        获取指定分类的 Google Play 热门应用

        注意：由于 API 限制，使用搜索方式获取该分类的热门应用
        结果基于分类关键词搜索，可能不是官方榜单

        Args:
            category_name: 分类名称（中文，用于标识）
            category_id: Google Play 分类 ID
            limit: 获取的应用数量，默认 100

        Returns:
            List[Dict]: 包含 app_id, rank, name, developer, icon_url, category, timestamp 的字典列表
        """
        try:
            print(f"⚠️  Google Play [{category_name}] 使用搜索方式，非官方榜单")

            # 根据分类定义搜索关键词
            category_keywords = {
                "HEALTH_AND_FITNESS": ["fitness", "health", "workout", "exercise", "meditation"],
                "SOCIAL": ["social", "chat", "messaging", "friends", "community"],
                "LIFESTYLE": ["lifestyle", "fashion", "beauty", "home", "living"],
                "GAME": ["game", "gaming", "play", "puzzle", "adventure"],
                "DATING": ["dating", "love", "match", "relationship", "singles"],
                "TOOLS": ["tools", "utility", "calculator", "converter", "manager"]
            }

            keywords = category_keywords.get(category_id, [category_name.lower()])

            apps_dict = {}  # 用字典去重

            for keyword in keywords:
                try:
                    results = search(
                        keyword,
                        lang="en",
                        country=self.country.lower(),
                        n_hits=30  # 每个关键词搜索30个
                    )

                    for result in results:
                        app_id = result.get('appId')
                        if app_id and app_id not in apps_dict:
                            # 生成 Google Play 商店链接
                            store_url = f"https://play.google.com/store/apps/details?id={app_id}"

                            apps_dict[app_id] = {
                                'platform': 'Google Play',
                                'category': category_name,
                                'app_id': app_id,
                                'rank': 0,  # 临时占位
                                'name': result.get('title', 'N/A'),
                                'developer': result.get('developer', 'N/A'),
                                'store_url': store_url,
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            }

                        if len(apps_dict) >= limit:
                            break

                    if len(apps_dict) >= limit:
                        break

                except Exception as e:
                    print(f"  搜索关键词 '{keyword}' 失败: {e}")
                    continue

            # 转换为列表并添加排名
            apps = []
            for idx, (app_id, app_info) in enumerate(apps_dict.items(), start=1):
                app_info['rank'] = idx
                apps.append(app_info)
                if idx >= limit:
                    break

            print(f"✅ Google Play [{category_name}] 成功抓取 {len(apps)} 个应用（基于搜索）")
            return apps

        except Exception as e:
            print(f"❌ Google Play [{category_name}] 抓取失败: {e}")
            return []


if __name__ == "__main__":
    # 测试代码
    from config_categories import GOOGLE_PLAY_CATEGORIES, GOOGLE_PLAY_COUNTRY

    scraper = GooglePlayScraperByCategory(country=GOOGLE_PLAY_COUNTRY)

    # 测试抓取健康与健身分类
    category = GOOGLE_PLAY_CATEGORIES["健康与健身"]
    apps = scraper.fetch_category(
        category_name=category["name_cn"],
        category_id=category["category_id"],
        limit=100
    )

    if apps:
        print(f"\n{category['name_cn']} 前 5 名:")
        for app in apps[:5]:
            print(f"  {app['rank']}. {app['name']} - {app['developer']}")
