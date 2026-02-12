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

            # 第一步：解析基本信息
            for rank, entry in enumerate(entries, start=1):
                app = self._parse_app_entry(entry, rank, category_name, timestamp)
                if app:
                    apps.append(app)

            # 第二步：批量获取详细信息（评分、评价数）
            if apps:
                print(f"  正在获取详细信息...")
                self._enrich_app_details(apps, session)

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
            # 获取应用ID（iTunes ID，用于详细信息查询）
            itunes_id = entry.get("id", {}).get("attributes", {}).get("im:id", "")

            # 获取Bundle ID
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

            # 获取上架时间
            release_date = entry.get("im:releaseDate", {}).get("attributes", {}).get("label", "")

            return {
                "platform": "App Store",
                "category": category,
                "app_id": app_id,
                "itunes_id": itunes_id,  # 用于批量查询详细信息
                "rank": rank,
                "name": name,
                "developer": developer,
                "store_url": store_url,
                "icon_url": icon_url,
                "release_date": release_date,
                "rating": 0,  # 稍后通过Search API填充
                "rating_count": 0,  # 稍后通过Search API填充
                "timestamp": timestamp
            }

        except Exception as e:
            import traceback
            # print(f"    解析应用数据失败: {e}")
            # traceback.print_exc()  # 取消注释以查看详细错误
            return None

    def _enrich_app_details(self, apps: List[Dict], session: requests.Session):
        """
        批量获取应用详细信息（评分、评价数）

        Args:
            apps: 应用列表
            session: requests session
        """
        try:
            # 提取iTunes ID（最多200个）
            itunes_ids = [app.get("itunes_id") for app in apps if app.get("itunes_id")]
            if not itunes_ids:
                return

            # 分批查询（每批200个）
            batch_size = 200
            for i in range(0, len(itunes_ids), batch_size):
                batch_ids = itunes_ids[i:i + batch_size]
                ids_str = ",".join(batch_ids)

                # 调用iTunes Search API
                lookup_url = f"https://itunes.apple.com/lookup?id={ids_str}"
                response = session.get(lookup_url, timeout=self.timeout)

                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])

                    # 创建ID到详细信息的映射
                    details_map = {}
                    for result in results:
                        track_id = str(result.get("trackId", ""))
                        details_map[track_id] = {
                            "rating": result.get("averageUserRating", 0),
                            "rating_count": result.get("userRatingCount", 0),
                            "store_url": result.get("trackViewUrl", "")  # 使用正确的商店链接
                        }

                    # 更新应用信息
                    for app in apps:
                        itunes_id = app.get("itunes_id")
                        if itunes_id in details_map:
                            details = details_map[itunes_id]
                            app["rating"] = details.get("rating", 0)
                            app["rating_count"] = details.get("rating_count", 0)
                            # 修复商店链接
                            if details.get("store_url"):
                                app["store_url"] = details.get("store_url")

                time.sleep(1)  # 批量请求之间的延迟

        except Exception as e:
            print(f"    获取详细信息失败: {e}")
            # 即使失败也继续，使用默认值


if __name__ == "__main__":
    # 测试代码
    scraper = AppStoreScraper()
    apps = scraper.scrape_category("6013", "健康与健身")
    print(f"\n共获取 {len(apps)} 个应用")
    if apps:
        print(f"第一个应用: {apps[0]}")
