"""
榜单监控主程序（飞书版本）
包含增量对比逻辑
"""

from datetime import datetime, timedelta
from typing import List, Dict, Set
from app_store_scraper import AppStoreScraper
from google_play_scraper_module import GooglePlayScraper
from feishu_sheet_storage import FeishuSheetStorage
import config


class RankingMonitor:
    def __init__(self):
        self.app_store_scraper = AppStoreScraper(config.APP_STORE_RSS_URL)
        self.google_play_scraper = GooglePlayScraper(
            country=config.GOOGLE_PLAY_COUNTRY,
            category=config.GOOGLE_PLAY_CATEGORY,
            collection_type=config.GOOGLE_PLAY_COLLECTION
        )
        self.storage = FeishuSheetStorage(
            app_id=config.FEISHU_APP_ID,
            app_secret=config.FEISHU_APP_SECRET,
            spreadsheet_token=config.FEISHU_SPREADSHEET_TOKEN
        )

    def run_daily_scrape(self):
        """
        执行每日抓取任务
        """
        print("=" * 60)
        print(f"开始执行每日抓取任务 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # 认证飞书 API
        if not self.storage.get_tenant_access_token():
            print("飞书 API 认证失败，无法继续")
            return

        # 如果没有 spreadsheet_token，创建新表格
        if not self.storage.spreadsheet_token:
            print("\n首次运行，正在创建新的飞书电子表格...")
            token = self.storage.create_spreadsheet("AppRankingMonitor")
            if token:
                print(f"\n✓ 创建成功！请将以下内容添加到 config.py:")
                print(f"FEISHU_SPREADSHEET_TOKEN = '{token}'")
                print("\n表格已创建，可以开始抓取数据")
            else:
                print("创建表格失败，无法继续")
                return

        # 抓取 App Store 数据
        print("\n[1/2] 抓取 App Store 数据...")
        app_store_apps = self.app_store_scraper.fetch_top_free()
        if app_store_apps:
            self.storage.save_apps(app_store_apps, "AppStore")

        # 抓取 Google Play 数据
        print("\n[2/2] 抓取 Google Play 数据...")
        google_play_apps = self.google_play_scraper.fetch_top_apps(limit=100)
        if google_play_apps:
            self.storage.save_apps(google_play_apps, "GooglePlay")

        print("\n" + "=" * 60)
        print("每日抓取任务完成")
        print("=" * 60)

    def get_new_apps(self, platform: str = "AppStore") -> List[Dict]:
        """
        获取新上榜的应用（对比今天和昨天的榜单）

        Args:
            platform: 平台名称，"AppStore" 或 "GooglePlay"

        Returns:
            List[Dict]: 新上榜的应用列表
        """
        print(f"\n分析 {platform} 新上榜应用...")

        # 认证飞书 API
        if not self.storage.get_tenant_access_token():
            print("飞书 API 认证失败，无法继续")
            return []

        # 获取今天和昨天的日期
        today = datetime.now().strftime('%Y%m%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

        # 获取今天和昨天的数据
        today_apps = self.storage.get_apps_by_date(platform, today)
        yesterday_apps = self.storage.get_apps_by_date(platform, yesterday)

        if not today_apps:
            print(f"警告: 未找到 {platform} 今天的数据 ({today})")
            return []

        if not yesterday_apps:
            print(f"警告: 未找到 {platform} 昨天的数据 ({yesterday})")
            print("如果这是第一次运行，这是正常的")
            return []

        # 提取昨天的 App ID 集合
        yesterday_app_ids: Set[str] = {app.get('App ID', '') for app in yesterday_apps}

        # 找出今天新出现的应用
        new_apps = []
        for app in today_apps:
            app_id = app.get('App ID', '')
            if app_id and app_id not in yesterday_app_ids:
                new_apps.append(app)

        # 输出结果
        print(f"\n{platform} 榜单分析结果:")
        print(f"  今天榜单: {len(today_apps)} 个应用")
        print(f"  昨天榜单: {len(yesterday_apps)} 个应用")
        print(f"  新上榜: {len(new_apps)} 个应用")

        if new_apps:
            print(f"\n新上榜的应用列表:")
            for app in new_apps:
                print(f"  - [{app.get('Rank', 'N/A')}] {app.get('Name', 'N/A')} ({app.get('Developer', 'N/A')})")
        else:
            print("\n没有新上榜的应用")

        return new_apps

    def compare_all_platforms(self):
        """
        对比所有平台的新上榜应用
        """
        print("\n" + "=" * 60)
        print("开始对比今天和昨天的榜单变化")
        print("=" * 60)

        # 对比 App Store
        app_store_new = self.get_new_apps("AppStore")

        # 对比 Google Play
        google_play_new = self.get_new_apps("GooglePlay")

        print("\n" + "=" * 60)
        print("榜单对比完成")
        print("=" * 60)

        return {
            'AppStore': app_store_new,
            'GooglePlay': google_play_new
        }


def main():
    """
    主函数 - 演示如何使用
    """
    monitor = RankingMonitor()

    print("应用商店榜单监控工具（飞书版）")
    print("=" * 60)
    print("1. 执行每日抓取任务")
    print("2. 对比今天和昨天的榜单（查找新上榜应用）")
    print("3. 退出")
    print("=" * 60)

    choice = input("\n请选择操作 (1/2/3): ").strip()

    if choice == "1":
        monitor.run_daily_scrape()
    elif choice == "2":
        monitor.compare_all_platforms()
    elif choice == "3":
        print("退出程序")
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()
