"""
Google Play 爬虫模块
通过 Node.js 版 google-play-scraper (facundoolano/google-play-scraper) 的 list() 接口
获取真正的分类榜单 Top N（Python 版无此接口，且 search 最多返回约 30 条）。

Python 通过 subprocess 调用 scrapers/gplay_node.js，传 JSON 参数，解析 JSON 返回。
"""

import os
import json
import time
import shutil
import subprocess
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Node 脚本路径（项目根目录下的 scrapers/gplay_node.js）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_NODE_SCRIPT = os.path.join(_SCRIPT_DIR, "gplay_node.mjs")
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)

# 检查 Node.js 是否可用
_NODE_BIN = shutil.which("node")
if _NODE_BIN:
    GOOGLE_PLAY_AVAILABLE = True
else:
    GOOGLE_PLAY_AVAILABLE = False
    print("警告: 未找到 node 可执行文件，Google Play 爬虫不可用。请安装 Node.js。")


class GooglePlayScraper:
    """Google Play 爬虫类"""

    def __init__(self, country="us", collection="TOP_FREE", limit=100, delay=3, timeout=60, logger=None):
        """
        初始化爬虫

        Args:
            country: 国家代码（默认 us）
            collection: 榜单类型（TOP_FREE / TOP_PAID / GROSSING / TRENDING）
            limit: 每个分类爬取数量（默认 100）
            delay: 请求延迟（秒）
            timeout: 子进程超时时间（秒）
            logger: 日志记录器（可选）
        """
        if not GOOGLE_PLAY_AVAILABLE:
            raise ImportError("Node.js 未安装，Google Play 爬虫不可用")

        self.country = country
        self.collection = collection
        self.limit = limit
        self.delay = delay
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    def scrape_category(self, category_key: str, category_name: str) -> List[Dict]:
        """
        爬取指定分类的榜单

        Args:
            category_key: 分类ID（对应 gplay.category 常量，如 "TOOLS"、"HEALTH_AND_FITNESS"）
            category_name: 分类名称（中文，用于日志和数据记录）

        Returns:
            List[Dict]: 应用列表
        """
        try:
            self.logger.info(f"正在爬取 Google Play - {category_name}...")

            # 构造传给 Node 脚本的参数
            payload = {
                "category": category_key,
                "collection": self.collection,
                "num": self.limit,
                "country": self.country,
                "lang": "en"
            }

            # 调用 Node 脚本（在项目根目录执行，确保能找到 node_modules）
            result = subprocess.run(
                [_NODE_BIN, _NODE_SCRIPT],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=_PROJECT_ROOT
            )

            # Node 脚本把日志写到 stderr，JSON 结果写到 stdout
            if result.stderr:
                for line in result.stderr.strip().splitlines():
                    self.logger.info(line)

            if result.returncode != 0:
                self.logger.error(f"{category_name} Node 脚本退出码 {result.returncode}")
                return []

            stdout = result.stdout.strip()
            if not stdout:
                self.logger.warning(f"{category_name} 未获取到数据（stdout 为空）")
                return []

            try:
                apps_data = json.loads(stdout)
            except json.JSONDecodeError as e:
                self.logger.error(f"{category_name} JSON 解析失败: {e}")
                return []

            if not apps_data:
                self.logger.warning(f"{category_name} 未获取到数据")
                return []

            apps = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for rank, app_data in enumerate(apps_data, start=1):
                app_info = self._parse_app_data(app_data, rank, category_name, timestamp)
                if app_info:
                    apps.append(app_info)

            self.logger.info(f"{category_name} 爬取成功，共 {len(apps)} 个应用")
            time.sleep(self.delay)  # 延迟避免请求过快
            return apps

        except subprocess.TimeoutExpired:
            self.logger.error(f"{category_name} 爬取超时（>{self.timeout}s）")
            return []
        except Exception as e:
            self.logger.error(f"{category_name} 爬取失败: {e}")
            return []

    def _parse_app_data(self, app_data: Dict, rank: int, category: str, timestamp: str) -> Optional[Dict]:
        """
        解析单个应用数据

        Args:
            app_data: Node 脚本返回的应用原始数据
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
            store_url = app_data.get("url", "") or f"https://play.google.com/store/apps/details?id={app_id}"

            # 评分与评价数（fullDetail=true 时返回 ratings/score）
            rating = app_data.get("scoreText")
            if rating is None:
                rating = 0
            else:
                try:
                    rating = float(rating)
                except (TypeError, ValueError):
                    rating = 0

            rating_count = app_data.get("ratings") or 0

            # 上架时间：fullDetail=true 返回 released 字段，格式如 "Dec 3, 2025"
            # 转换为 YYYY/MM/DD，与 App Store 数据格式一致
            release_date_raw = app_data.get("released", "")
            release_date = self._format_release_date(release_date_raw)

            return {
                "platform": "Google Play",
                "category": category,
                "app_id": app_id,
                "rank": rank,
                "name": name,
                "developer": developer,
                "store_url": store_url,
                "icon_url": icon_url,
                "release_date": release_date,
                "rating": rating,
                "rating_count": rating_count,
                "timestamp": timestamp
            }

        except Exception as e:
            self.logger.error(f"解析应用数据失败: {e}")
            return None

    def _format_release_date(self, date_str: str) -> str:
        """
        格式化上架时间为 YYYY/MM/DD 格式

        Args:
            date_str: 原始日期字符串，Google Play 格式如 "Dec 3, 2025"

        Returns:
            str: 格式化后的日期（如 "2025/12/03"），解析失败返回原字符串
        """
        if not date_str:
            return ""
        try:
            from datetime import datetime
            # 尝试解析 "Mon D, YYYY" 格式（如 "Dec 3, 2025"）
            dt = datetime.strptime(date_str, "%b %d, %Y")
            return dt.strftime("%Y/%m/%d")
        except (ValueError, TypeError):
            # 解析失败，返回原字符串
            return date_str


if __name__ == "__main__":
    # 测试代码
    if GOOGLE_PLAY_AVAILABLE:
        logging.basicConfig(level=logging.INFO, format="%(message)s")
        scraper = GooglePlayScraper()
        apps = scraper.scrape_category("TOOLS", "工具")
        print(f"\n共获取 {len(apps)} 个应用")
        if apps:
            print(f"第一个应用: {apps[0]}")
    else:
        print("请先安装 Node.js 和 npm 包: npm install google-play-scraper")
