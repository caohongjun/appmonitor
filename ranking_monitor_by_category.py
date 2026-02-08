"""
按分类榜单监控主程序
支持 App Store 和 Google Play 的多分类监控
"""

from datetime import datetime, timedelta
from typing import List, Dict, Set
from app_store_scraper_by_category import AppStoreScraperByCategory
from google_play_scraper_by_category import GooglePlayScraperByCategory
from feishu_sheet_storage import FeishuSheetStorage
import config_categories as config
import time
import random


class RankingMonitorByCategory:
    def __init__(self):
        self.app_store_scraper = AppStoreScraperByCategory()
        self.google_play_scraper = GooglePlayScraperByCategory(
            country=config.GOOGLE_PLAY_COUNTRY
        )
        self.storage = FeishuSheetStorage(
            app_id=config.FEISHU_APP_ID,
            app_secret=config.FEISHU_APP_SECRET,
            spreadsheet_token=config.FEISHU_SPREADSHEET_TOKEN
        )

    def run_daily_scrape(self):
        """
        执行每日抓取任务（按分类）
        """
        print("=" * 70)
        print(f"开始执行每日抓取任务（按分类）- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # 认证飞书 API
        if not self.storage.get_tenant_access_token():
            print("❌ 飞书 API 认证失败")
            return

        print(f"\n📊 将抓取 {len(config.APP_STORE_CATEGORIES)} 个 App Store 分类")
        print(f"📊 将抓取 {len(config.GOOGLE_PLAY_CATEGORIES)} 个 Google Play 分类")
        print(f"📊 总共 {len(config.APP_STORE_CATEGORIES) + len(config.GOOGLE_PLAY_CATEGORIES)} 个分类\n")

        # 抓取 App Store 各分类
        print("=" * 70)
        print("📱 抓取 App Store 分类榜单")
        print("=" * 70)

        for idx, (key, category) in enumerate(config.APP_STORE_CATEGORIES.items(), 1):
            print(f"\n[{idx}/{len(config.APP_STORE_CATEGORIES)}] 抓取 App Store - {category['name_cn']} ({category['name_en']})...")

            apps = self.app_store_scraper.fetch_category(
                category_name=category['name_cn'],
                rss_url=category['url']
            )

            if apps:
                # 保存到飞书，每个分类一个 sheet
                platform_category = f"AppStore_{category['name_cn']}"
                if self.storage.save_apps(apps, platform_category):
                    print(f"  ✅ 已保存到工作表: {platform_category}_{{日期}}")
                else:
                    print(f"  ❌ 保存失败")
            else:
                print(f"  ❌ 抓取失败，跳过")

            # 添加随机延迟（2-4秒），避免请求过于频繁
            if idx < len(config.APP_STORE_CATEGORIES):
                delay = random.uniform(2, 4)
                print(f"  ⏱️  等待 {delay:.1f} 秒...")
                time.sleep(delay)

        # 抓取 Google Play 各分类
        print("\n" + "=" * 70)
        print("🤖 抓取 Google Play 分类榜单")
        print("=" * 70)

        for idx, (key, category) in enumerate(config.GOOGLE_PLAY_CATEGORIES.items(), 1):
            print(f"\n[{idx}/{len(config.GOOGLE_PLAY_CATEGORIES)}] 抓取 Google Play - {category['name_cn']} ({category['name_en']})...")

            apps = self.google_play_scraper.fetch_category(
                category_name=category['name_cn'],
                category_id=category['category_id'],
                limit=100
            )

            if apps:
                # 保存到飞书，每个分类一个 sheet
                platform_category = f"GooglePlay_{category['name_cn']}"
                if self.storage.save_apps(apps, platform_category):
                    print(f"  ✅ 已保存到工作表: {platform_category}_{{日期}}")
                else:
                    print(f"  ❌ 保存失败")
            else:
                print(f"  ❌ 抓取失败，跳过")

            # 添加随机延迟（3-6秒），Google Play 需要更长延迟
            if idx < len(config.GOOGLE_PLAY_CATEGORIES):
                delay = random.uniform(3, 6)
                print(f"  ⏱️  等待 {delay:.1f} 秒...")
                time.sleep(delay)

        print("\n" + "=" * 70)
        print("✅ 每日抓取任务完成")
        print("=" * 70)

    def get_new_apps(self, platform: str, category: str) -> List[Dict]:
        """
        获取新上榜的应用（对比今天和昨天的榜单）

        Args:
            platform: 平台名称，如 "AppStore" 或 "GooglePlay"
            category: 分类名称，如 "健康与健身"

        Returns:
            List[Dict]: 新上榜的应用列表
        """
        platform_category = f"{platform}_{category}"
        print(f"\n分析 {platform_category} 新上榜应用...")

        # 认证
        if not self.storage.get_tenant_access_token():
            print("❌ 飞书 API 认证失败")
            return []

        # 获取今天和昨天的日期
        today = datetime.now().strftime('%Y%m%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

        # 获取数据
        today_apps = self.storage.get_apps_by_date(platform_category, today)
        yesterday_apps = self.storage.get_apps_by_date(platform_category, yesterday)

        if not today_apps:
            print(f"⚠️  未找到 {platform_category} 今天的数据 ({today})")
            return []

        if not yesterday_apps:
            print(f"⚠️  未找到 {platform_category} 昨天的数据 ({yesterday})")
            print("如果这是第一次运行，这是正常的")
            return []

        # 提取昨天的 App ID 集合
        yesterday_app_ids: Set[str] = {app.get('应用ID App ID', '') for app in yesterday_apps}

        # 找出今天新出现的应用
        new_apps = []
        for app in today_apps:
            app_id = app.get('应用ID App ID', '')
            if app_id and app_id not in yesterday_app_ids:
                new_apps.append(app)

        # 输出结果
        print(f"\n📊 {platform_category} 榜单分析结果:")
        print(f"  今天榜单: {len(today_apps)} 个应用")
        print(f"  昨天榜单: {len(yesterday_apps)} 个应用")
        print(f"  新上榜: {len(new_apps)} 个应用")

        if new_apps:
            print(f"\n✨ 新上榜的应用列表:")
            for app in new_apps:
                print(f"  - [{app.get('排名 Rank', 'N/A')}] {app.get('名称 Name', 'N/A')} ({app.get('开发者 Developer', 'N/A')})")
        else:
            print("\n  没有新上榜的应用")

        return new_apps

    def compare_all_categories(self):
        """
        对比所有分类的新上榜应用
        """
        print("\n" + "=" * 70)
        print("开始对比所有分类的榜单变化")
        print("=" * 70)

        results = {}

        # 对比 App Store 各分类
        print("\n📱 App Store 分类对比:")
        for key, category in config.APP_STORE_CATEGORIES.items():
            new_apps = self.get_new_apps("AppStore", category['name_cn'])
            results[f"AppStore_{category['name_cn']}"] = new_apps

        # 对比 Google Play 各分类
        print("\n🤖 Google Play 分类对比:")
        for key, category in config.GOOGLE_PLAY_CATEGORIES.items():
            new_apps = self.get_new_apps("GooglePlay", category['name_cn'])
            results[f"GooglePlay_{category['name_cn']}"] = new_apps

        print("\n" + "=" * 70)
        print("✅ 榜单对比完成")
        print("=" * 70)

        return results


def main():
    """
    主函数
    """
    monitor = RankingMonitorByCategory()

    print("应用商店榜单监控工具（按分类）")
    print("=" * 70)
    print("📊 监控的分类:")
    print("\nApp Store (4 个分类):")
    for key, cat in config.APP_STORE_CATEGORIES.items():
        print(f"  • {cat['name_cn']} ({cat['name_en']})")

    print("\nGoogle Play (6 个分类):")
    for key, cat in config.GOOGLE_PLAY_CATEGORIES.items():
        print(f"  • {cat['name_cn']} ({cat['name_en']})")

    print("\n" + "=" * 70)
    print("1. 执行每日抓取任务（所有分类）")
    print("2. 对比今天和昨天的榜单（所有分类）")
    print("3. 退出")
    print("=" * 70)

    choice = input("\n请选择操作 (1/2/3): ").strip()

    if choice == "1":
        monitor.run_daily_scrape()
    elif choice == "2":
        monitor.compare_all_categories()
    elif choice == "3":
        print("退出程序")
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()
