# 飞书 API 配置教程

飞书 API 配置比 Google API 简单很多！只需要 3 个步骤。

## 📋 配置概览

1. 创建飞书企业自建应用
2. 获取 App ID 和 App Secret
3. 配置应用权限

预计时间：**3-5 分钟**

---

## 第一步：创建飞书应用

### 1.1 访问飞书开放平台

- 打开浏览器，访问：**https://open.feishu.cn/**
- 点击右上角 **"登录"** 或 **"开发者后台"**
- 使用你的飞书账号登录（如果没有账号，先注册一个）

### 1.2 进入开发者后台

- 登录后，点击右上角的 **"进入开发者后台"**
- 或直接访问：**https://open.feishu.cn/app**

### 1.3 创建企业自建应用

1. 点击 **"创建企业自建应用"** 按钮
2. 填写应用信息：

   ```
   应用名称：App Ranking Monitor
   应用描述：应用商店榜单监控工具
   ```

3. 上传应用图标（可选）
4. 点击 **"创建"** 按钮

---

## 第二步：获取 App ID 和 App Secret

### 2.1 进入应用管理页面

- 在应用列表中，点击刚创建的 **"App Ranking Monitor"** 应用
- 进入应用管理页面

### 2.2 查看凭证信息

1. 在左侧菜单中，点击 **"凭证与基础信息"**
2. 你会看到以下信息：

   ```
   App ID: cli_xxxxxxxxxx
   App Secret: [点击显示]
   ```

3. **记录这两个值**：
   - 复制 **App ID**
   - 点击 **"点击显示"** 查看 App Secret，然后复制

### 2.3 保存到配置文件

打开 `/Users/caohongjun/workspace/appmoitor/config.py`，填入刚才复制的信息：

```python
# 飞书配置
FEISHU_APP_ID = "cli_xxxxxxxxxx"  # 粘贴你的 App ID
FEISHU_APP_SECRET = "xxxxxxxxxxxxxxx"  # 粘贴你的 App Secret
FEISHU_SPREADSHEET_TOKEN = ""  # 保持为空，首次运行时会自动创建
```

---

## 第三步：配置应用权限

### 3.1 添加电子表格权限

1. 在左侧菜单中，点击 **"权限管理"**
2. 在搜索框中搜索：**"电子表格"** 或 **"spreadsheet"**
3. 勾选以下权限：

   ✅ **查看、评论、编辑和管理电子表格**（spreadsheets:spreadsheet）

   或者更细粒度的权限：
   - ✅ 查看电子表格
   - ✅ 创建电子表格
   - ✅ 编辑电子表格内容
   - ✅ 管理电子表格

4. 点击右上角的 **"批量开通"** 按钮

### 3.2 发布应用版本（重要！）

**权限配置后必须发布应用版本才能生效！**

1. 在左侧菜单中，点击 **"版本管理与发布"**
2. 点击 **"创建版本"** 按钮
3. 填写版本信息：

   ```
   版本号：1.0.0
   更新说明：初始版本，添加电子表格权限
   ```

4. 点击 **"保存"**
5. 点击 **"申请线上发布"**（或 "申请发布到线上版本"）
6. 填写审核说明（简单说明用途即可）
7. 提交审核

**注意**：
- 如果是企业内部使用，审核通常很快（几分钟到几小时）
- 也可以选择 **"仅企业内部可用"**，这样不需要审核

---

## ✅ 配置完成检查清单

- [ ] 已创建飞书企业自建应用
- [ ] 已获取 App ID 和 App Secret
- [ ] 已将 App ID 和 App Secret 填入 config.py
- [ ] 已添加电子表格权限
- [ ] 已发布应用版本（或设置为企业内部可用）

---

## 🎯 测试配置

### 方式 1：运行测试脚本

```bash
cd /Users/caohongjun/workspace/appmoitor
python feishu_sheet_storage.py
```

如果看到 **"✓ 认证成功"**，说明配置正确！

程序还会自动创建一个新的电子表格，并输出表格链接和 Token。

### 方式 2：运行主程序

```bash
python ranking_monitor_feishu.py
```

选择 **"1"** 执行每日抓取任务。

首次运行时，程序会：
1. 自动创建名为 **"AppRankingMonitor"** 的飞书电子表格
2. 输出表格 Token（请保存到 config.py）
3. 开始抓取数据

---

## 📝 重要说明

### 关于 FEISHU_SPREADSHEET_TOKEN

- **首次运行时保持为空**
- 程序会自动创建新表格，并输出 Token
- **将输出的 Token 保存到 config.py**，以后就会使用这个表格

示例：
```python
# 首次运行后，程序输出：
# FEISHU_SPREADSHEET_TOKEN = 'shtcnxxxxxxxxxxxxxx'

# 将这个值填入 config.py：
FEISHU_SPREADSHEET_TOKEN = "shtcnxxxxxxxxxxxxxx"
```

### 查看电子表格

- 程序创建表格后，会输出表格链接
- 在浏览器中打开链接即可查看数据
- 或者在飞书中搜索 "AppRankingMonitor"

---

## 🔄 与 Google Sheet 的对比

| 特性 | Google Sheet | 飞书电子表格 |
|------|--------------|-------------|
| 配置复杂度 | ⭐⭐⭐⭐ | ⭐ |
| 需要服务账号 | ✅ 需要 | ❌ 不需要 |
| 需要共享表格 | ✅ 需要 | ❌ 不需要 |
| API 速度 | 较快 | 快 |
| 国内访问 | 可能不稳定 | 稳定 |
| 配置时间 | 10 分钟 | 3 分钟 |

---

## ❓ 常见问题

### Q1: 提示 "app_access_token is invalid"？
**A:** 检查 App ID 和 App Secret 是否正确复制到 config.py。

### Q2: 提示 "Permission Denied" 或权限不足？
**A:**
1. 确保已添加电子表格权限
2. 确保已发布应用版本
3. 等待几分钟让权限生效

### Q3: 如何查看已创建的表格？
**A:**
- 在飞书中打开"云文档"
- 搜索 "AppRankingMonitor"
- 或使用程序输出的表格链接

### Q4: 可以使用现有的电子表格吗？
**A:**
可以！步骤：
1. 打开飞书电子表格
2. 查看 URL，格式为：`https://xxx.feishu.cn/sheets/shtcnxxxxxx`
3. 复制 `shtcnxxxxxx` 部分（这是 spreadsheet_token）
4. 填入 config.py 的 `FEISHU_SPREADSHEET_TOKEN`

### Q5: 应用审核需要多久？
**A:**
- 企业内部应用：通常几分钟到几小时
- 如果急用，可以在创建应用时选择 **"仅企业内部可用"**，无需审核

---

## 🎉 完成！

配置完成后，就可以开始使用了：

```bash
# 运行主程序
python ranking_monitor_feishu.py

# 选择 1：执行每日抓取
# 选择 2：对比今天和昨天的榜单
```

有任何问题随时问我！ 🚀
