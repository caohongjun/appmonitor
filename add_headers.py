"""
为现有数据添加表头
创建新的带表头的工作表
"""

from feishu_sheet_storage import FeishuSheetStorage
from datetime import datetime
import config


def main():
    print("=" * 70)
    print("为表格添加表头")
    print("=" * 70)

    storage = FeishuSheetStorage(
        app_id=config.FEISHU_APP_ID,
        app_secret=config.FEISHU_APP_SECRET,
        spreadsheet_token=config.FEISHU_SPREADSHEET_TOKEN
    )

    if not storage.get_tenant_access_token():
        print("❌ 认证失败")
        return

    today = datetime.now().strftime('%Y%m%d')

    # 处理 App Store 工作表
    print(f"\n处理 AppStore_{today}...")
    old_sheet = f"AppStore_{today}"
    new_sheet = f"AppStore_{today}_final"

    # 读取旧数据
    old_data = storage.read_data(old_sheet, "A1:G200")

    if old_data:
        print(f"✅ 读取到 {len(old_data)} 行数据")

        # 创建新工作表
        new_sheet_id = storage.add_sheet(new_sheet)

        if new_sheet_id:
            print(f"✅ 创建新工作表: {new_sheet}")

            # 添加表头
            headers = [['平台 Platform', '应用ID App ID', '排名 Rank', '名称 Name', '开发者 Developer', '图标 Icon URL', '抓取时间 Timestamp']]

            # 添加表头和数据
            all_data = headers + old_data
            if storage.append_data(new_sheet, all_data):
                print(f"✅ 已添加表头和 {len(old_data)} 行数据")
            else:
                print("❌ 数据保存失败")
        else:
            print("❌ 创建工作表失败")
    else:
        print("❌ 读取数据失败")

    # 处理 Google Play 工作表
    print(f"\n处理 GooglePlay_{today}...")
    old_sheet = f"GooglePlay_{today}"
    new_sheet = f"GooglePlay_{today}_final"

    # 读取旧数据
    old_data = storage.read_data(old_sheet, "A1:G200")

    if old_data:
        print(f"✅ 读取到 {len(old_data)} 行数据")

        # 创建新工作表
        new_sheet_id = storage.add_sheet(new_sheet)

        if new_sheet_id:
            print(f"✅ 创建新工作表: {new_sheet}")

            # 添加表头
            headers = [['平台 Platform', '应用ID App ID', '排名 Rank', '名称 Name', '开发者 Developer', '图标 Icon URL', '抓取时间 Timestamp']]

            # 添加表头和数据
            all_data = headers + old_data
            if storage.append_data(new_sheet, all_data):
                print(f"✅ 已添加表头和 {len(old_data)} 行数据")
            else:
                print("❌ 数据保存失败")
        else:
            print("❌ 创建工作表失败")
    else:
        print("❌ 读取数据失败")

    print("\n" + "=" * 70)
    print("✅ 完成！新的工作表已包含清晰的表头")
    print("工作表名称:")
    print(f"  - AppStore_{today}_final")
    print(f"  - GooglePlay_{today}_final")
    print("=" * 70)


if __name__ == "__main__":
    main()
