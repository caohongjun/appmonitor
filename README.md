# 应用商店榜单监控工具

这是一个用于监控 App Store 和 Google Play 应用排行榜的 Python 工具，支持按分类监控。

## 🎯 功能特性

### 按分类监控（推荐）

- ✅ **App Store 4 个分类**：健康与健身、社交网络、生活方式、游戏
- ✅ **Google Play 6 个分类**：健康与健身、社交、生活方式、游戏、约会、工具
- ✅ **每个分类独立 Sheet**：数据清晰，便于分析
- ✅ **商店链接**：点击即可跳转到应用详情
- ✅ **自动延迟保护**：避免请求过于频繁
- ✅ **中英文表头**：易于理解

### 数据字段

| 字段 | 说明 |
|------|------|
| 平台 Platform | App Store / Google Play |
| 分类 Category | 应用分类 |
| 应用ID App ID | 应用唯一标识 |
| 排名 Rank | 分类内排名 |
| 名称 Name | 应用名称 |
| 开发者 Developer | 开发者名称 |
| 商店链接 Store URL | 可点击的应用商店链接 |
| 抓取时间 Timestamp | 数据抓取时间 |

---

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd appmoitor
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置飞书 API

#### 4.1 复制配置文件

```bash
cp config.example.py config.py
```

#### 4.2 获取飞书 API 密钥

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 App ID 和 App Secret
4. 添加电子表格权限
5. 发布应用版本

详细步骤请查看：[`FEISHU_API_SETUP.md`](FEISHU_API_SETUP.md)

#### 4.3 填写配置信息

编辑 `config.py`：

```python
FEISHU_APP_ID = "cli_xxxxxxxxxx"  # 你的 App ID
FEISHU_APP_SECRET = "xxxxxxxx"    # 你的 App Secret
FEISHU_SPREADSHEET_TOKEN = ""      # 留空，首次运行会自动创建
```

---

## 🚀 使用方法

### 方式 1：使用启动脚本（推荐）

```bash
chmod +x run_by_category.sh
./run_by_category.sh
```

### 方式 2：直接运行

```bash
source venv/bin/activate
python ranking_monitor_by_category.py
```

### 菜单选项

```
1. 执行每日抓取任务（所有分类）
   - 抓取 10 个分类（约 1000 个应用）
   - 自动保存到飞书电子表格

2. 对比今天和昨天的榜单（所有分类）
   - 分析每个分类的榜单变化
   - 找出新上榜的应用

3. 退出
```

---

## 📊 数据量说明

| 平台 | 分类数 | 每分类应用数 | 总应用数 |
|------|--------|-------------|---------|
| App Store | 4 | 100 | 400 |
| Google Play | 6 | ~100 | ~600 |
| **总计** | **10** | - | **~1000** |

---

## ⏰ 定时任务

### 每天自动抓取（推荐）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上 9 点执行）
0 9 * * * cd /path/to/appmoitor && ./run_by_category.sh << EOF
1
EOF
```

---

## 🛡️ 安全说明

### 频率限制

- ✅ **推荐频率**：每天 1 次
- ⚠️ **谨慎频率**：每 12 小时 1 次
- ❌ **避免**：每小时或更频繁

详细信息请查看：
- [`RATE_LIMIT_GUIDE.md`](RATE_LIMIT_GUIDE.md) - 频率限制详细指南
- [`SAFETY_SUMMARY.md`](SAFETY_SUMMARY.md) - 安全性快速参考

### 敏感信息保护

⚠️ **重要**：`config.py` 包含敏感信息，已在 `.gitignore` 中

上传到 Git 前请查看：[`SECURITY_CHECK.md`](SECURITY_CHECK.md)

---

## 📖 文档说明

| 文档 | 说明 |
|------|------|
| `README.md` | 项目总览（本文档） |
| `README_CATEGORY.md` | 分类监控详细使用指南 |
| `FEISHU_API_SETUP.md` | 飞书 API 配置教程 |
| `RATE_LIMIT_GUIDE.md` | 频率限制和风险说明 |
| `SAFETY_SUMMARY.md` | 安全性快速参考 |
| `SECURITY_CHECK.md` | 上传 Git 前安全检查清单 |
| `VERSION_COMPARISON.md` | 新旧版本对比 |

---

## 🗂️ 项目结构

```
appmoitor/
├── config.example.py              # 配置文件示例 ⭐
├── config_categories.py           # 分类配置
├── app_store_scraper_by_category.py
├── google_play_scraper_by_category.py
├── feishu_sheet_storage.py
├── ranking_monitor_by_category.py # 主程序 ⭐
├── run_by_category.sh             # 启动脚本 ⭐
├── requirements.txt               # Python 依赖
├── .gitignore                     # Git 忽略规则
└── docs/                          # 文档目录
```

---

## ⚙️ 自定义配置

### 添加或修改分类

编辑 `config_categories.py`：

```python
APP_STORE_CATEGORIES = {
    "新分类": {
        "name_cn": "新分类",
        "name_en": "New Category",
        "genre_id": "分类ID",
        "url": "RSS_URL"
    }
}
```

---

## ❓ 常见问题

### Q1: 如何获取飞书 API 密钥？
**A**: 参考 [`FEISHU_API_SETUP.md`](FEISHU_API_SETUP.md)

### Q2: 可以每天运行多次吗？
**A**: 可以，但推荐每天 1 次。详见 [`RATE_LIMIT_GUIDE.md`](RATE_LIMIT_GUIDE.md)

### Q3: Google Play 数据为什么不准确？
**A**: 使用的免费库通过搜索方式获取，不是官方榜单。如需准确数据，建议使用付费 API。

### Q4: 如何查看抓取的数据？
**A**: 在飞书中搜索 "AppRankingMonitor"，打开电子表格查看。

### Q5: 配置文件丢失怎么办？
**A**: 从 `config.example.py` 复制并重新填写配置。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn/)
- [Apple RSS Feed Generator](https://rss.applemarketingtools.com/)
- [google-play-scraper](https://github.com/JoMingyu/google-play-scraper)

---

## ⚠️ 免责声明

本工具仅供学习和研究使用。请遵守相关平台的使用条款和 API 限制。

- App Store: 使用官方 RSS API
- Google Play: 使用第三方库，非官方方式

使用本工具产生的任何后果由使用者自行承担。

---

**快速开始**：
1. 安装依赖：`pip install -r requirements.txt`
2. 配置飞书：编辑 `config.py`
3. 运行工具：`./run_by_category.sh`

有任何问题欢迎提 Issue！🚀
