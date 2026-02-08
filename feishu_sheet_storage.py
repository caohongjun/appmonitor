"""
飞书电子表格存储模块
使用飞书开放平台 API 将数据存储到飞书电子表格
"""

import requests
import json
from datetime import datetime
from typing import List, Dict, Optional


class FeishuSheetStorage:
    def __init__(self, app_id: str, app_secret: str, spreadsheet_token: str = None):
        """
        初始化飞书电子表格存储

        Args:
            app_id: 飞书应用的 App ID
            app_secret: 飞书应用的 App Secret
            spreadsheet_token: 电子表格的 token（可选，如果为空则需要手动创建）
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.spreadsheet_token = spreadsheet_token
        self.tenant_access_token = None

        # 飞书 API 基础 URL
        self.base_url = "https://open.feishu.cn/open-apis"

    def get_tenant_access_token(self) -> bool:
        """
        获取 tenant_access_token（应用访问凭证）

        Returns:
            bool: 是否成功获取 token
        """
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"

        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                self.tenant_access_token = result.get("tenant_access_token")
                print("飞书 API 认证成功")
                return True
            else:
                print(f"获取 tenant_access_token 失败: {result.get('msg')}")
                return False

        except requests.RequestException as e:
            print(f"飞书 API 认证失败: {e}")
            return False

    def _get_headers(self) -> Dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.tenant_access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    def create_spreadsheet(self, title: str) -> Optional[str]:
        """
        创建新的电子表格

        Args:
            title: 表格标题

        Returns:
            Optional[str]: 电子表格的 token，失败返回 None
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return None

        url = f"{self.base_url}/sheets/v3/spreadsheets"

        payload = {
            "title": title
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                spreadsheet_token = result.get("data", {}).get("spreadsheet", {}).get("spreadsheet_token")
                spreadsheet_url = result.get("data", {}).get("spreadsheet", {}).get("url")
                print(f"成功创建电子表格: {title}")
                print(f"表格链接: {spreadsheet_url}")
                print(f"表格 Token: {spreadsheet_token}")
                self.spreadsheet_token = spreadsheet_token
                return spreadsheet_token
            else:
                print(f"创建电子表格失败: {result.get('msg')}")
                return None

        except requests.RequestException as e:
            print(f"创建电子表格失败: {e}")
            return None

    def get_sheets(self) -> List[Dict]:
        """
        获取电子表格中的所有工作表

        Returns:
            List[Dict]: 工作表列表
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return []

        if not self.spreadsheet_token:
            print("错误: 未设置 spreadsheet_token")
            return []

        url = f"{self.base_url}/sheets/v3/spreadsheets/{self.spreadsheet_token}/sheets/query"

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                return result.get("data", {}).get("sheets", [])
            else:
                print(f"获取工作表列表失败: {result.get('msg')}")
                return []

        except requests.RequestException as e:
            print(f"获取工作表列表失败: {e}")
            return []

    def add_sheet(self, title: str) -> Optional[str]:
        """
        添加新的工作表

        Args:
            title: 工作表标题

        Returns:
            Optional[str]: 工作表的 sheet_id，失败返回 None
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return None

        if not self.spreadsheet_token:
            print("错误: 未设置 spreadsheet_token")
            return None

        # 使用 v2 版本的 API
        url = f"{self.base_url}/sheets/v2/spreadsheets/{self.spreadsheet_token}/sheets_batch_update"

        payload = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": title,
                            "index": 0
                        }
                    }
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()

            if result.get("code") == 0:
                # v2 API 返回格式可能不同，尝试获取 sheet_id
                replies = result.get("data", {}).get("replies", [])
                if replies:
                    sheet_id = replies[0].get("addSheet", {}).get("properties", {}).get("sheetId")
                    if sheet_id:
                        print(f"成功创建工作表: {title}")
                        return sheet_id

                # 如果无法从响应中获取 sheet_id，则重新查询
                print(f"工作表 {title} 已创建，正在获取 ID...")
                sheets = self.get_sheets()
                for sheet in sheets:
                    if sheet.get("title") == title:
                        return sheet.get("sheet_id")

                print(f"创建工作表成功但无法获取 ID")
                return None
            else:
                print(f"创建工作表失败 (code={result.get('code')}): {result.get('msg')}")
                return None

        except requests.RequestException as e:
            print(f"创建工作表失败: {e}")
            return None

    def find_sheet_by_title(self, title: str) -> Optional[str]:
        """
        根据标题查找工作表

        Args:
            title: 工作表标题

        Returns:
            Optional[str]: 工作表的 sheet_id，未找到返回 None
        """
        sheets = self.get_sheets()
        for sheet in sheets:
            if sheet.get("title") == title:
                return sheet.get("sheet_id")
        return None

    def append_data(self, sheet_id_or_title: str, values: List[List]) -> bool:
        """
        向工作表追加数据

        Args:
            sheet_id_or_title: 工作表 ID 或标题
            values: 要追加的数据（二维数组）

        Returns:
            bool: 是否成功
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False

        if not self.spreadsheet_token:
            print("错误: 未设置 spreadsheet_token")
            return False

        url = f"{self.base_url}/sheets/v2/spreadsheets/{self.spreadsheet_token}/values_append"

        # 飞书 API 需要使用 sheetId，不能使用标题
        # 如果传入的看起来是标题（长字符串），需要转换为 sheetId
        sheet_id = sheet_id_or_title

        if len(sheet_id_or_title) > 10:  # 标题通常较长
            # 传入的是标题，需要获取对应的 sheetId
            sheets = self.get_sheets()
            found = False
            for sheet in sheets:
                if sheet.get("title") == sheet_id_or_title:
                    sheet_id = sheet.get("sheet_id")
                    found = True
                    break

            if not found:
                print(f"错误: 未找到工作表 '{sheet_id_or_title}'")
                return False

        payload = {
            "valueRange": {
                "range": f"{sheet_id}!A:Z",  # 使用 sheetId
                "values": values
            }
        }

        try:
            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )
            result = response.json()

            if result.get("code") == 0:
                return True
            else:
                print(f"追加数据失败 (code={result.get('code')}): {result.get('msg')}")
                print(f"详细错误: {result}")
                return False

        except requests.RequestException as e:
            print(f"追加数据失败 (请求异常): {e}")
            return False
        except Exception as e:
            print(f"追加数据失败 (未知异常): {e}")
            return False

    def read_data(self, sheet_id_or_title: str, range_str: str = "A1:Z1000") -> List[List]:
        """
        读取工作表数据

        Args:
            sheet_id_or_title: 工作表 ID 或标题
            range_str: 读取范围（默认 A1:Z1000）

        Returns:
            List[List]: 数据（二维数组）
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return []

        if not self.spreadsheet_token:
            print("错误: 未设置 spreadsheet_token")
            return []

        # 如果传入的看起来是标题（长字符串），需要转换为 sheetId
        sheet_id = sheet_id_or_title

        if len(sheet_id_or_title) > 10:  # 标题通常较长
            # 传入的是标题，需要获取对应的 sheetId
            sheets = self.get_sheets()
            found = False
            for sheet in sheets:
                if sheet.get("title") == sheet_id_or_title:
                    sheet_id = sheet.get("sheet_id")
                    found = True
                    break

            if not found:
                print(f"错误: 未找到工作表 '{sheet_id_or_title}'")
                return []

        url = f"{self.base_url}/sheets/v2/spreadsheets/{self.spreadsheet_token}/values/{sheet_id}!{range_str}"

        try:
            response = requests.get(
                url,
                headers=self._get_headers(),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("code") == 0:
                return result.get("data", {}).get("valueRange", {}).get("values", [])
            else:
                print(f"读取数据失败: {result.get('msg')}")
                return []

        except requests.RequestException as e:
            print(f"读取数据失败: {e}")
            return []

    def save_apps(self, apps: List[Dict], platform: str) -> bool:
        """
        保存应用数据到飞书电子表格

        Args:
            apps: 应用数据列表
            platform: 平台名称

        Returns:
            bool: 是否成功
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return False

        if not self.spreadsheet_token:
            print("错误: 请先设置 spreadsheet_token 或创建新表格")
            return False

        # 工作表名称：平台_日期
        sheet_title = f"{platform}_{datetime.now().strftime('%Y%m%d')}"

        # 查找或创建工作表
        sheet_id = self.find_sheet_by_title(sheet_title)

        if not sheet_id:
            sheet_id = self.add_sheet(sheet_title)
            if not sheet_id:
                return False

            # 添加表头（中英文双语，传入 sheet_title，让 append_data 自动转换为 sheetId）
            headers = [['平台 Platform', '分类 Category', '应用ID App ID', '排名 Rank', '名称 Name', '开发者 Developer', '商店链接 Store URL', '抓取时间 Timestamp']]
            if not self.append_data(sheet_title, headers):
                return False
        else:
            print(f"工作表 '{sheet_title}' 已存在，将追加数据")

        # 准备数据
        rows = []
        for app in apps:
            row = [
                str(app.get('platform', '')),
                str(app.get('category', '')),
                str(app.get('app_id', '')),
                str(app.get('rank', '')),
                str(app.get('name', '')),
                str(app.get('developer', '')),
                str(app.get('store_url', '')),
                str(app.get('timestamp', ''))
            ]
            rows.append(row)

        # 追加数据（传入 sheet_title，让 append_data 自动转换为 sheetId）
        if self.append_data(sheet_title, rows):
            print(f"成功保存 {len(apps)} 条数据到飞书电子表格")
            return True
        else:
            return False

    def get_apps_by_date(self, platform: str, date_str: str) -> List[Dict]:
        """
        获取指定日期的应用数据

        Args:
            platform: 平台名称
            date_str: 日期字符串（格式：YYYYMMDD）

        Returns:
            List[Dict]: 应用数据列表
        """
        if not self.tenant_access_token:
            if not self.get_tenant_access_token():
                return []

        if not self.spreadsheet_token:
            print("错误: 未设置 spreadsheet_token")
            return []

        # 工作表名称
        sheet_title = f"{platform}_{date_str}"

        # 查找工作表
        sheet_id = self.find_sheet_by_title(sheet_title)
        if not sheet_id:
            print(f"未找到工作表: {sheet_title}")
            return []

        # 读取数据
        data = self.read_data(sheet_id)

        if not data or len(data) < 2:  # 至少要有表头和一行数据
            return []

        # 转换为字典列表（第一行是表头）
        headers = data[0]
        apps = []

        for row in data[1:]:
            if len(row) >= len(headers):
                app = {headers[i]: row[i] for i in range(len(headers))}
                apps.append(app)

        return apps


if __name__ == "__main__":
    # 测试代码
    print("飞书电子表格存储模块测试")
    print("=" * 60)
    print("\n请确保已在 config.py 中配置了以下信息:")
    print("- FEISHU_APP_ID")
    print("- FEISHU_APP_SECRET")
    print("- FEISHU_SPREADSHEET_TOKEN (可选)")
    print("\n" + "=" * 60)

    from config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_SPREADSHEET_TOKEN

    storage = FeishuSheetStorage(
        app_id=FEISHU_APP_ID,
        app_secret=FEISHU_APP_SECRET,
        spreadsheet_token=FEISHU_SPREADSHEET_TOKEN
    )

    # 测试认证
    if storage.get_tenant_access_token():
        print("\n✓ 认证成功")

        # 如果没有 spreadsheet_token，创建新表格
        if not storage.spreadsheet_token:
            print("\n正在创建新的电子表格...")
            token = storage.create_spreadsheet("AppRankingMonitor")
            if token:
                print(f"\n✓ 创建成功！请将以下 token 保存到 config.py 中:")
                print(f"FEISHU_SPREADSHEET_TOKEN = '{token}'")
        else:
            print(f"\n✓ 使用现有表格: {storage.spreadsheet_token}")

            # 测试保存数据
            test_apps = [
                {
                    'platform': 'Test Platform',
                    'app_id': 'test.app.1',
                    'rank': 1,
                    'name': 'Test App',
                    'developer': 'Test Developer',
                    'icon_url': 'https://example.com/icon.png',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            ]

            if storage.save_apps(test_apps, "Test"):
                print("\n✓ 数据保存测试成功")
    else:
        print("\n✗ 认证失败")
