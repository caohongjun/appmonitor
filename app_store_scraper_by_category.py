"""
App Store 按分类抓取模块
支持按分类获取免费榜单
"""

import requests
from datetime import datetime
from typing import List, Dict


class AppStoreScraperByCategory:
    def fetch_category(self, category_name: str, rss_url: str) -> List[Dict]:
        """
        获取指定分类的 App Store 免费榜

        Args:
            category_name: 分类名称（用于标识）
            rss_url: RSS API URL

        Returns:
            List[Dict]: 包含 app_id, rank, name, developer, icon_url, category, timestamp 的字典列表
        """
        try:
            response = requests.get(rss_url, timeout=30)
            response.raise_for_status()
            data = response.json()

            apps = []
            entries = data.get('feed', {}).get('entry', [])

            for idx, entry in enumerate(entries, start=1):
                app_id = entry.get('id', {}).get('attributes', {}).get('im:id', 'N/A')

                # 生成 App Store 商店链接
                store_url = f"https://apps.apple.com/us/app/id{app_id}" if app_id != 'N/A' else 'N/A'

                app_info = {
                    'platform': 'App Store',
                    'category': category_name,
                    'app_id': app_id,
                    'rank': idx,
                    'name': entry.get('im:name', {}).get('label', 'N/A'),
                    'developer': entry.get('im:artist', {}).get('label', 'N/A'),
                    'store_url': store_url,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                apps.append(app_info)

            print(f"✅ App Store [{category_name}] 成功抓取 {len(apps)} 个应用")
            return apps

        except requests.RequestException as e:
            print(f"❌ App Store [{category_name}] 抓取失败: {e}")
            return []



if __name__ == "__main__":
    # 测试代码
    from config_categories import APP_STORE_CATEGORIES

    scraper = AppStoreScraperByCategory()

    # 测试抓取健康与健身分类
    category = APP_STORE_CATEGORIES["健康与健身"]
    apps = scraper.fetch_category(
        category_name=category["name_cn"],
        rss_url=category["url"]
    )

    if apps:
        print(f"\n{category['name_cn']} 前 5 名:")
        for app in apps[:5]:
            print(f"  {app['rank']}. {app['name']} - {app['developer']}")
