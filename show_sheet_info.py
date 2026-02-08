"""
显示飞书电子表格信息
"""

from feishu_sheet_storage import FeishuSheetStorage
import config


def main():
    print("=" * 70)
    print("飞书电子表格信息")
    print("=" * 70)

    # 创建存储实例
    storage = FeishuSheetStorage(
        app_id=config.FEISHU_APP_ID,
        app_secret=config.FEISHU_APP_SECRET,
        spreadsheet_token=config.FEISHU_SPREADSHEET_TOKEN
    )

    # 认证
    if not storage.get_tenant_access_token():
        print("❌ 认证失败")
        return

    print("\n✅ 认证成功")
    print(f"\n📊 表格 Token: {config.FEISHU_SPREADSHEET_TOKEN}")

    # 获取工作表列表
    print("\n📋 工作表列表:")
    print("-" * 70)

    sheets = storage.get_sheets()

    if sheets:
        for idx, sheet in enumerate(sheets, 1):
            sheet_title = sheet.get('title', 'N/A')
            sheet_id = sheet.get('sheet_id', 'N/A')
            print(f"{idx}. {sheet_title} (ID: {sheet_id})")
    else:
        print("暂无工作表")

    print("\n" + "=" * 70)
    print("💡 提示:")
    print("   1. 在飞书中搜索 'AppRankingMonitor' 即可找到表格")
    print("   2. 或在'云文档' > '我的文档'中查看")
    print("   3. 表格 Token 已保存在 config.py 中")
    print("=" * 70)


if __name__ == "__main__":
    main()
