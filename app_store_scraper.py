"""
App Store 抓取模块
使用 Apple RSS API 获取美国区免费榜 Top 100
"""

import requests
from datetime import datetime
from typing import List, Dict


class AppStoreScraper:
    def __init__(self, rss_url: str):
        self.rss_url = rss_url

    def fetch_top_free(self) -> List[Dict]:
        """
        获取 App Store 美国区免费榜 Top 100

        Returns:
            List[Dict]: 包含 app_id, rank, name, developer, icon_url, timestamp 的字典列表
        """
        try:
            response = requests.get(self.rss_url, timeout=30)
            response.raise_for_status()
            data = response.json()

            apps = []
            entries = data.get('feed', {}).get('entry', [])

            for idx, entry in enumerate(entries, start=1):
                app_info = {
                    'platform': 'App Store',
                    'app_id': entry.get('id', {}).get('attributes', {}).get('im:id', 'N/A'),
                    'rank': idx,
                    'name': entry.get('im:name', {}).get('label', 'N/A'),
                    'developer': entry.get('im:artist', {}).get('label', 'N/A'),
                    'icon_url': self._get_icon_url(entry),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                apps.append(app_info)

            print(f"成功抓取 App Store {len(apps)} 个应用")
            return apps

        except requests.RequestException as e:
            print(f"抓取 App Store 数据失败: {e}")
            return []

    def _get_icon_url(self, entry: Dict) -> str:
        """提取图标 URL（选择最大尺寸）"""
        images = entry.get('im:image', [])
        if images:
            # 返回最后一个（通常是最大尺寸）
            return images[-1].get('label', 'N/A')
        return 'N/A'


if __name__ == "__main__":
    # 测试代码
    from config import APP_STORE_RSS_URL

    scraper = AppStoreScraper(APP_STORE_RSS_URL)
    apps = scraper.fetch_top_free()

    if apps:
        print(f"\n前 5 名:")
        for app in apps[:5]:
            print(f"{app['rank']}. {app['name']} - {app['developer']}")
