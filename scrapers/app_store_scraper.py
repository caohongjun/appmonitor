"""
App Store 爬虫模块
使用 iTunes RSS API 获取榜单数据
"""

import requests
import time
from typing import List, Dict, Optional
from datetime import datetime
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class AppStoreScraper:
    """App Store 爬虫类"""

    def __init__(self, country="us", limit=100, delay=2, timeout=30):
        """
        初始化爬虫

        Args:
            country: 国家代码（默认 us）
            limit: 每个分类爬取数量（默认 100）
            delay: 请求延迟（秒）
            timeout: 请求超时时间（秒）
        """
        self.country = country
        self.limit = limit
        self.delay = delay
        self.timeout = timeout
        self.base_url = "https://itunes.apple.com"

    def scrape_category(self, category_id: str, category_name: str) -> List[Dict]:
        """
        爬取指定分类的榜单

        Args:
            category_id: 分类ID（genre_id）
            category_name: 分类名称（中文）

        Returns:
            List[Dict]: 应用列表
        """
        url = f"{self.base_url}/{self.country}/rss/topfreeapplications/limit={self.limit}/genre={category_id}/json"

        try:
            print(f"  正在爬取 App Store - {category_name}...")

            # 添加请求头，模拟真实浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.9'
            }

            # 使用session，并禁用SSL验证（如果仍然失败）
            session = requests.Session()
            session.headers.update(headers)

            response = session.get(url, timeout=self.timeout, verify=True)
            response.raise_for_status()

            data = response.json()
            entries = data.get("feed", {}).get("entry", [])

            if not entries:
                print(f"  ⚠️  {category_name} 未获取到数据")
                return []

            apps = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for rank, entry in enumerate(entries, start=1):
                app = self._parse_app_entry(entry, rank, category_name, timestamp)
                if app:
                    apps.append(app)

            print(f"  ✓ {category_name} 爬取成功，共 {len(apps)} 个应用")
            time.sleep(self.delay)  # 延迟避免请求过快
            return apps

        except requests.RequestException as e:
            print(f"  ✗ {category_name} 爬取失败: {e}")
            return []
        except Exception as e:
            print(f"  ✗ {category_name} 解析失败: {e}")
            return []

    def _parse_app_entry(self, entry: Dict, rank: int, category: str, timestamp: str) -> Optional[Dict]:
        """
        解析单个应用数据

        Args:
            entry: RSS feed 中的单个条目
            rank: 排名
            category: 分类名称
            timestamp: 时间戳

        Returns:
            Optional[Dict]: 应用数据字典
        """
        try:
            # 获取应用ID
            app_id = entry.get("id", {}).get("attributes", {}).get("im:bundleId", "")

            # 获取应用名称
            name = entry.get("im:name", {}).get("label", "")

            # 获取开发者
            developer = entry.get("im:artist", {}).get("label", "")

            # 获取商店链接（link是一个列表，取第一个元素）
            link = entry.get("link", [])
            if link and isinstance(link, list) and len(link) > 0:
                store_url = link[0].get("attributes", {}).get("href", "")
            else:
                store_url = ""

            # 获取图标链接（取最大尺寸）
            images = entry.get("im:image", [])
            if images and isinstance(images, list) and len(images) > 0:
                # images是一个list，每个元素可能是dict或其他类型
                last_image = images[-1]
                if isinstance(last_image, dict):
                    icon_url = last_image.get("label", "")
                else:
                    icon_url = ""
            else:
                icon_url = ""

            return {
                "platform": "App Store",
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
            import traceback
            # print(f"    解析应用数据失败: {e}")
            # traceback.print_exc()  # 取消注释以查看详细错误
            return None


if __name__ == "__main__":
    # 测试代码
    scraper = AppStoreScraper()
    apps = scraper.scrape_category("6013", "健康与健身")
    print(f"\n共获取 {len(apps)} 个应用")
    if apps:
        print(f"第一个应用: {apps[0]}")
