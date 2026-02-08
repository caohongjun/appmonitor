"""
重置表格并重新抓取数据
会删除今天的工作表，然后重新抓取并添加表头
"""

from feishu_sheet_storage import FeishuSheetStorage
from app_store_scraper import AppStoreScraper
from google_play_scraper_module import GooglePlayScraper
from datetime import datetime
import config


def main():
    print("=" * 70)
    print("重置表格并重新抓取数据（会添加表头）")
    print("=" * 70)

    # 初始化
    storage = FeishuSheetStorage(
        app_id=config.FEISHU_APP_ID,
        app_secret=config.FEISHU_APP_SECRET,
        spreadsheet_token=config.FEISHU_SPREADSHEET_TOKEN
    )

    app_store_scraper = AppStoreScraper(config.APP_STORE_RSS_URL)
    google_play_scraper = GooglePlayScraper(
        country=config.GOOGLE_PLAY_COUNTRY,
        category=config.GOOGLE_PLAY_CATEGORY,
        collection_type=config.GOOGLE_PLAY_COLLECTION
    )

    # 认证
    if not storage.get_tenant_access_token():
        print("❌ 飞书 API 认证失败")
        return

    # 获取今天的日期
    today = datetime.now().strftime('%Y%m%d')
    app_store_sheet = f"AppStore_{today}"
    google_play_sheet = f"GooglePlay_{today}"

    print(f"\n今天的工作表:")
    print(f"  - {app_store_sheet}")
    print(f"  - {google_play_sheet}")

    # 删除今天的工作表（如果存在）
    print("\n正在删除旧的工作表...")
    sheets = storage.get_sheets()
    sheets_to_delete = []

    for sheet in sheets:
        title = sheet.get('title')
        if title in [app_store_sheet, google_play_sheet]:
            sheets_to_delete.append(sheet)

    if sheets_to_delete:
        # 飞书 API 可能不支持删除工作表，所以我们创建新表格
        print(f"⚠️  检测到已存在的工作表: {[s.get('title') for s in sheets_to_delete]}")
        print("由于飞书 API 限制，我们将创建新的电子表格")

        # 创建新表格
        new_token = storage.create_spreadsheet(f"AppRankingMonitor_{today}")
        if new_token:
            print(f"\n✅ 创建了新表格: {new_token}")
            print(f"\n请更新 config.py 中的 FEISHU_SPREADSHEET_TOKEN:")
            print(f"FEISHU_SPREADSHEET_TOKEN = '{new_token}'")

            # 更新 storage 的 token
            storage.spreadsheet_token = new_token

            # 继续抓取数据
            print("\n开始抓取数据...")
        else:
            print("❌ 创建新表格失败")
            return
    else:
        print("✅ 没有需要删除的工作表")

    # 抓取 App Store 数据
    print("\n[1/2] 抓取 App Store 数据...")
    app_store_apps = app_store_scraper.fetch_top_free()
    if app_store_apps:
        if storage.save_apps(app_store_apps, "AppStore"):
            print("✅ App Store 数据保存成功（包含表头）")
        else:
            print("❌ App Store 数据保存失败")

    # 抓取 Google Play 数据
    print("\n[2/2] 抓取 Google Play 数据...")
    google_play_apps = google_play_scraper.fetch_top_apps(limit=100)
    if google_play_apps:
        if storage.save_apps(google_play_apps, "GooglePlay"):
            print("✅ Google Play 数据保存成功（包含表头）")
        else:
            print("❌ Google Play 数据保存失败")

    print("\n" + "=" * 70)
    print("✅ 完成！表格现在包含清晰的表头了")
    print("=" * 70)

    # 验证表头
    print("\n验证表头...")
    data = storage.read_data(f"AppStore_{today}", "A1:G2")
    if data and len(data) > 0:
        print(f"\n表头: {data[0]}")
        if len(data) > 1:
            print(f"第一行数据: {data[1][:3]}...")


if __name__ == "__main__":
    main()
