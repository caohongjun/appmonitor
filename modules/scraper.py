"""
模块1：榜单数据爬取主程序
整合 App Store 和 Google Play 爬虫
"""

import sys
import os
import argparse
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_simple import (
    APP_STORE_CATEGORIES,
    GOOGLE_PLAY_CATEGORIES,
    SCRAPER_CONFIG,
    DATA_DIR,
    LOG_DIR
)
from scrapers.app_store_scraper import AppStoreScraper
from scrapers.google_play_scraper import GooglePlayScraper, GOOGLE_PLAY_AVAILABLE
from utils.logger import setup_logger
from utils.data_storage import save_to_json, get_data_file_path
from utils.date_utils import get_today, is_valid_date


class RankingMonitorScraper:
    """榜单监控爬虫主类"""

    def __init__(self, date_str=None):
        """
        初始化爬虫

        Args:
            date_str: 日期字符串（YYYY-MM-DD），默认今天
        """
        self.date = date_str or get_today()
        self.logger = setup_logger(
            "scraper",
            os.path.join(LOG_DIR, "scraper.log")
        )

        # 初始化爬虫实例
        app_store_config = SCRAPER_CONFIG["app_store"]
        self.app_store_scraper = AppStoreScraper(
            country=app_store_config["country"],
            limit=app_store_config["limit"],
            delay=app_store_config["delay"],
            timeout=SCRAPER_CONFIG["timeout"]
        )

        if GOOGLE_PLAY_AVAILABLE:
            google_play_config = SCRAPER_CONFIG["google_play"]
            self.google_play_scraper = GooglePlayScraper(
                country=google_play_config["country"],
                collection=google_play_config["collection"],
                limit=google_play_config["limit"],
                delay=google_play_config["delay"],
                timeout=SCRAPER_CONFIG["timeout"]
            )
        else:
            self.google_play_scraper = None
            self.logger.warning("Google Play 爬虫不可用（缺少依赖）")

    def scrape_app_store(self, categories=None):
        """
        爬取 App Store 榜单

        Args:
            categories: 指定要爬取的分类列表，None表示全部
        """
        print("\n" + "=" * 60)
        print("📱 开始爬取 App Store 榜单")
        print("=" * 60)

        target_categories = categories or list(APP_STORE_CATEGORIES.keys())
        success_count = 0
        total_apps = 0

        for category_key in target_categories:
            if category_key not in APP_STORE_CATEGORIES:
                self.logger.warning(f"未知分类: {category_key}")
                continue

            category_info = APP_STORE_CATEGORIES[category_key]
            category_name = category_info["name_cn"]
            genre_id = category_info["genre_id"]

            try:
                # 爬取数据
                apps = self.app_store_scraper.scrape_category(genre_id, category_name)

                if apps:
                    # 保存数据
                    data = {
                        "date": self.date,
                        "platform": "App Store",
                        "category": category_name,
                        "category_key": category_key,
                        "total_apps": len(apps),
                        "apps": apps
                    }

                    file_path = get_data_file_path(
                        self.date, "app_store", category_key, DATA_DIR
                    )

                    if save_to_json(data, file_path):
                        success_count += 1
                        total_apps += len(apps)
                        self.logger.info(f"App Store - {category_name} 保存成功")
                    else:
                        self.logger.error(f"App Store - {category_name} 保存失败")
                else:
                    self.logger.warning(f"App Store - {category_name} 未获取到数据")

            except Exception as e:
                self.logger.error(f"App Store - {category_name} 爬取异常: {e}")

        print(f"\n✓ App Store 爬取完成")
        print(f"  成功: {success_count}/{len(target_categories)} 个分类")
        print(f"  应用总数: {total_apps}")

    def scrape_google_play(self, categories=None):
        """
        爬取 Google Play 榜单

        Args:
            categories: 指定要爬取的分类列表，None表示全部
        """
        if not self.google_play_scraper:
            print("\n⚠️  Google Play 爬虫不可用，请安装: pip install google-play-scraper")
            return

        print("\n" + "=" * 60)
        print("🤖 开始爬取 Google Play 榜单")
        print("=" * 60)

        target_categories = categories or list(GOOGLE_PLAY_CATEGORIES.keys())
        success_count = 0
        total_apps = 0

        for category_key in target_categories:
            if category_key not in GOOGLE_PLAY_CATEGORIES:
                self.logger.warning(f"未知分类: {category_key}")
                continue

            category_info = GOOGLE_PLAY_CATEGORIES[category_key]
            category_name = category_info["name_cn"]
            category_en = category_info["name_en"]

            try:
                # 爬取数据
                apps = self.google_play_scraper.scrape_category(category_en, category_name)

                if apps:
                    # 保存数据
                    data = {
                        "date": self.date,
                        "platform": "Google Play",
                        "category": category_name,
                        "category_key": category_key,
                        "total_apps": len(apps),
                        "apps": apps
                    }

                    file_path = get_data_file_path(
                        self.date, "google_play", category_key, DATA_DIR
                    )

                    if save_to_json(data, file_path):
                        success_count += 1
                        total_apps += len(apps)
                        self.logger.info(f"Google Play - {category_name} 保存成功")
                    else:
                        self.logger.error(f"Google Play - {category_name} 保存失败")
                else:
                    self.logger.warning(f"Google Play - {category_name} 未获取到数据")

            except Exception as e:
                self.logger.error(f"Google Play - {category_name} 爬取异常: {e}")

        print(f"\n✓ Google Play 爬取完成")
        print(f"  成功: {success_count}/{len(target_categories)} 个分类")
        print(f"  应用总数: {total_apps}")

    def scrape_all(self, platform=None, categories=None):
        """
        爬取所有榜单

        Args:
            platform: 指定平台（app_store / google_play），None表示全部
            categories: 指定分类列表，None表示全部
        """
        start_time = datetime.now()
        print("\n" + "=" * 60)
        print(f"🚀 榜单监控 - 数据爬取")
        print(f"📅 日期: {self.date}")
        print("=" * 60)

        if platform is None or platform == "app_store":
            self.scrape_app_store(categories)

        if platform is None or platform == "google_play":
            self.scrape_google_play(categories)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 60)
        print(f"✓ 全部爬取完成，耗时: {duration:.1f} 秒")
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="模块1：榜单数据爬取",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python scraper.py                           # 爬取今天所有数据
  python scraper.py --date 2026-02-12         # 爬取指定日期
  python scraper.py --platform app_store      # 只爬取 App Store
  python scraper.py --platform google_play    # 只爬取 Google Play
  python scraper.py --category health_fitness # 只爬取指定分类
        """
    )

    parser.add_argument(
        "--date",
        type=str,
        help="指定日期（YYYY-MM-DD），默认今天"
    )

    parser.add_argument(
        "--platform",
        type=str,
        choices=["app_store", "google_play"],
        help="指定平台"
    )

    parser.add_argument(
        "--category",
        type=str,
        help="指定分类（如 health_fitness）"
    )

    args = parser.parse_args()

    # 验证日期
    if args.date and not is_valid_date(args.date):
        print(f"错误: 无效的日期格式: {args.date}")
        print("请使用格式: YYYY-MM-DD")
        sys.exit(1)

    # 处理分类参数
    categories = [args.category] if args.category else None

    # 创建爬虫实例并执行
    scraper = RankingMonitorScraper(args.date)
    scraper.scrape_all(args.platform, categories)


if __name__ == "__main__":
    main()
