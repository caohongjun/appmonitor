"""
模块2：新上榜产品识别主程序
对比今天和昨天的榜单，识别新上榜的产品
"""

import sys
import os
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Set

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_simple import (
    APP_STORE_CATEGORIES,
    GOOGLE_PLAY_CATEGORIES,
    DATA_DIR,
    LOG_DIR
)
from utils.logger import setup_logger
from utils.data_storage import load_from_json, save_to_json
from utils.date_utils import get_today, get_yesterday, get_date_before, is_valid_date


class NewAppDetector:
    """新上榜产品识别器"""

    def __init__(self, date_str=None):
        """
        初始化识别器

        Args:
            date_str: 日期字符串（YYYY-MM-DD），默认今天
        """
        self.date = date_str or get_today()
        self.logger = setup_logger(
            "detector",
            os.path.join(LOG_DIR, "detector.log")
        )

        # 已分析产品记录文件
        self.analyzed_apps_file = os.path.join(DATA_DIR, "analyzed_apps.json")

    def load_ranking_data(self, date_str: str, platform: str, category: str) -> List[Dict]:
        """
        加载指定日期的榜单数据

        Args:
            date_str: 日期字符串
            platform: 平台（app_store / google_play）
            category: 分类key

        Returns:
            List[Dict]: 应用列表
        """
        file_path = os.path.join(
            DATA_DIR, "raw", date_str, platform, f"{category}.json"
        )

        data = load_from_json(file_path)
        if not data:
            return []

        return data.get("apps", [])

    def get_app_ids(self, apps: List[Dict]) -> Set[str]:
        """
        从应用列表中提取app_id集合

        Args:
            apps: 应用列表

        Returns:
            Set[str]: app_id集合
        """
        return {app.get("app_id") for app in apps if app.get("app_id")}

    def find_new_apps(self, today_apps: List[Dict], yesterday_apps: List[Dict]) -> List[Dict]:
        """
        找出新上榜的应用

        Args:
            today_apps: 今天的应用列表
            yesterday_apps: 昨天的应用列表

        Returns:
            List[Dict]: 新上榜的应用列表
        """
        today_ids = self.get_app_ids(today_apps)
        yesterday_ids = self.get_app_ids(yesterday_apps)

        # 新上榜 = 今天有但昨天没有
        new_ids = today_ids - yesterday_ids

        # 返回完整的应用信息
        new_apps = [app for app in today_apps if app.get("app_id") in new_ids]

        return new_apps

    def find_compare_date(self, max_lookback_days=3) -> str:
        """
        查找可用的对比日期（向前查找最多N天）

        Args:
            max_lookback_days: 最多向前查找的天数

        Returns:
            str: 找到的日期，如果都不存在返回空字符串
        """
        for days in range(1, max_lookback_days + 1):
            compare_date = get_date_before(days)

            # 检查该日期是否有数据（检查一个文件即可）
            test_file = os.path.join(
                DATA_DIR, "raw", compare_date, "app_store", "health_fitness.json"
            )

            if os.path.exists(test_file):
                self.logger.info(f"找到对比日期: {compare_date} (向前{days}天)")
                return compare_date

        self.logger.warning(f"未找到可用的对比日期（向前查找{max_lookback_days}天）")
        return ""

    def load_analyzed_apps(self) -> Set[str]:
        """
        加载已分析的产品记录

        Returns:
            Set[str]: 已分析的app_id集合
        """
        data = load_from_json(self.analyzed_apps_file)
        return set(data.get("analyzed_apps", []))

    def save_analyzed_apps(self, app_ids: Set[str]):
        """
        保存已分析的产品记录

        Args:
            app_ids: app_id集合
        """
        data = {
            "analyzed_apps": list(app_ids),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_count": len(app_ids)
        }
        save_to_json(data, self.analyzed_apps_file)

    def detect_all_platforms(self, compare_date: str, skip_analyzed=True) -> Dict:
        """
        检测所有平台的新上榜产品

        Args:
            compare_date: 对比日期
            skip_analyzed: 是否跳过已分析的产品

        Returns:
            Dict: 检测结果
        """
        print("\n" + "=" * 60)
        print(f"🔍 新上榜产品识别")
        print(f"📅 今天: {self.date}")
        print(f"📅 对比: {compare_date}")
        print("=" * 60)

        all_new_apps = []
        analyzed_apps = self.load_analyzed_apps() if skip_analyzed else set()

        # 检测 App Store
        print("\n📱 检测 App Store...")
        for category_key, category_info in APP_STORE_CATEGORIES.items():
            category_name = category_info["name_cn"]

            today_apps = self.load_ranking_data(self.date, "app_store", category_key)
            yesterday_apps = self.load_ranking_data(compare_date, "app_store", category_key)

            if not today_apps:
                print(f"  ⚠️  {category_name} - 今天无数据")
                continue

            if not yesterday_apps:
                print(f"  ⚠️  {category_name} - 对比日期无数据")
                continue

            new_apps = self.find_new_apps(today_apps, yesterday_apps)

            # 过滤已分析的产品
            if skip_analyzed:
                new_apps = [app for app in new_apps if app.get("app_id") not in analyzed_apps]

            if new_apps:
                print(f"  ✓ {category_name} - 发现 {len(new_apps)} 个新上榜产品")
                all_new_apps.extend(new_apps)
            else:
                print(f"  - {category_name} - 无新上榜产品")

        # 检测 Google Play
        print("\n🤖 检测 Google Play...")
        for category_key, category_info in GOOGLE_PLAY_CATEGORIES.items():
            category_name = category_info["name_cn"]

            today_apps = self.load_ranking_data(self.date, "google_play", category_key)
            yesterday_apps = self.load_ranking_data(compare_date, "google_play", category_key)

            if not today_apps:
                print(f"  ⚠️  {category_name} - 今天无数据")
                continue

            if not yesterday_apps:
                print(f"  ⚠️  {category_name} - 对比日期无数据")
                continue

            new_apps = self.find_new_apps(today_apps, yesterday_apps)

            # 过滤已分析的产品
            if skip_analyzed:
                new_apps = [app for app in new_apps if app.get("app_id") not in analyzed_apps]

            if new_apps:
                print(f"  ✓ {category_name} - 发现 {len(new_apps)} 个新上榜产品")
                all_new_apps.extend(new_apps)
            else:
                print(f"  - {category_name} - 无新上榜产品")

        # 保存结果
        result = {
            "date": self.date,
            "compare_date": compare_date,
            "total_count": len(all_new_apps),
            "new_apps": all_new_apps,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        output_file = os.path.join(DATA_DIR, "new_apps", f"{self.date}.json")
        if save_to_json(result, output_file):
            print(f"\n✓ 结果已保存: {output_file}")
            self.logger.info(f"识别完成，共 {len(all_new_apps)} 个新上榜产品")
        else:
            print(f"\n✗ 结果保存失败")
            self.logger.error("结果保存失败")

        print("\n" + "=" * 60)
        print(f"✓ 识别完成，共发现 {len(all_new_apps)} 个新上榜产品")
        print("=" * 60)

        return result

    def run(self, force=False):
        """
        运行识别器

        Args:
            force: 是否强制重新识别（不跳过已分析产品）
        """
        start_time = datetime.now()

        # 1. 查找对比日期
        compare_date = self.find_compare_date(max_lookback_days=3)

        if not compare_date:
            print("❌ 错误: 未找到可用的历史数据（向前3天内）")
            print("   请先运行爬虫获取历史数据")
            return

        # 2. 检测新上榜产品
        result = self.detect_all_platforms(compare_date, skip_analyzed=not force)

        # 3. 更新已分析记录（如果不是force模式）
        if not force and result["new_apps"]:
            analyzed_apps = self.load_analyzed_apps()
            new_app_ids = {app["app_id"] for app in result["new_apps"]}
            analyzed_apps.update(new_app_ids)
            self.save_analyzed_apps(analyzed_apps)
            print(f"✓ 已更新分析记录（共 {len(analyzed_apps)} 个产品）")

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"\n⏱  耗时: {duration:.1f} 秒")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="模块2：新上榜产品识别",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python detector.py                    # 检测今天的新上榜产品
  python detector.py --date 2026-02-12  # 检测指定日期
  python detector.py --force            # 强制重新识别（不跳过已分析）
        """
    )

    parser.add_argument(
        "--date",
        type=str,
        help="指定日期（YYYY-MM-DD），默认今天"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重新识别（不跳过已分析的产品）"
    )

    args = parser.parse_args()

    # 验证日期
    if args.date and not is_valid_date(args.date):
        print(f"错误: 无效的日期格式: {args.date}")
        print("请使用格式: YYYY-MM-DD")
        sys.exit(1)

    # 创建识别器并运行
    detector = NewAppDetector(args.date)
    detector.run(force=args.force)


if __name__ == "__main__":
    main()
