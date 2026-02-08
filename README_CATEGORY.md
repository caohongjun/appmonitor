# 按分类监控应用榜单 - 使用指南

## 🎯 功能说明

这个版本支持**按分类**监控 App Store 和 Google Play 的免费下载榜，每个分类一个独立的工作表（Sheet）。

## 📊 监控的分类

### App Store（4 个分类）

| 分类 | 英文名称 | 说明 |
|------|---------|------|
| 健康与健身 | Health & Fitness | 官方榜单，数据准确 |
| 社交网络 | Social Networking | 官方榜单，数据准确 |
| 生活方式 | Lifestyle | 官方榜单，数据准确 |
| 游戏 | Games | 官方榜单，数据准确 |

### Google Play（6 个分类）

| 分类 | 英文名称 | 说明 |
|------|---------|------|
| 健康与健身 | Health & Fitness | ⚠️ 基于搜索，非官方榜单 |
| 社交 | Social | ⚠️ 基于搜索，非官方榜单 |
| 生活方式 | Lifestyle | ⚠️ 基于搜索，非官方榜单 |
| 游戏 | Game | ⚠️ 基于搜索，非官方榜单 |
| 约会 | Dating | ⚠️ 基于搜索，非官方榜单 |
| 工具 | Tools | ⚠️ 基于搜索，非官方榜单 |

## 🗂️ 工作表命名规则

每个分类会创建一个独立的工作表，命名格式：

```
平台_分类_日期

例如：
- AppStore_健康与健身_20260208
- GooglePlay_社交_20260208
```

## 📋 数据字段

每个工作表包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| 平台 Platform | 应用平台 | App Store / Google Play |
| 分类 Category | 应用分类 | 健康与健身 |
| 应用ID App ID | 应用唯一标识 | 6448311069 |
| 排名 Rank | 当前排名 | 1 |
| 名称 Name | 应用名称 | ChatGPT |
| 开发者 Developer | 开发者名称 | OpenAI |
| **商店链接 Store URL** | 应用商店链接（可直接点击） | https://apps.apple.com/us/app/id6448311069 |
| 抓取时间 Timestamp | 数据抓取时间 | 2026-02-08 22:00:00 |

## 🚀 使用方法

### 方式 1：使用启动脚本（推荐）

```bash
./run_by_category.sh
```

### 方式 2：手动运行

```bash
source venv/bin/activate
python ranking_monitor_by_category.py
```

### 菜单选项

运行后会看到菜单：

```
1. 执行每日抓取任务（所有分类）
   - 抓取 4 个 App Store 分类（共 400 个应用）
   - 抓取 6 个 Google Play 分类（共 600 个应用）
   - 总计 10 个分类，约 1000 个应用

2. 对比今天和昨天的榜单（所有分类）
   - 分析每个分类的榜单变化
   - 找出新上榜的应用

3. 退出
```

## 📊 飞书表格结构

### 抓取后的表格结构

```
飞书电子表格: AppRankingMonitor
│
├── AppStore_健康与健身_20260208 (100 行数据)
├── AppStore_社交网络_20260208 (100 行数据)
├── AppStore_生活方式_20260208 (100 行数据)
├── AppStore_游戏_20260208 (100 行数据)
│
├── GooglePlay_健康与健身_20260208 (100 行数据)
├── GooglePlay_社交_20260208 (100 行数据)
├── GooglePlay_生活方式_20260208 (100 行数据)
├── GooglePlay_游戏_20260208 (100 行数据)
├── GooglePlay_约会_20260208 (100 行数据)
└── GooglePlay_工具_20260208 (100 行数据)
```

每个工作表包含该分类的 Top 100 应用数据。

## 🔗 商店链接说明

现在每条记录都包含**可直接点击的商店链接**：

- **App Store 链接格式**：`https://apps.apple.com/us/app/id{应用ID}`
- **Google Play 链接格式**：`https://play.google.com/store/apps/details?id={应用ID}`

在飞书表格中点击链接即可直接跳转到对应的应用商店页面！

## ⏰ 定时任务示例

### 每天早上 9 点自动抓取所有分类

```bash
# 编辑 crontab
crontab -e

# 添加以下行
0 9 * * * cd /Users/caohongjun/workspace/appmoitor && ./run_by_category.sh
```

## 📈 使用场景

### 第 1 天（2月8日）
运行抓取 → 选择"1"
- ✅ 创建 10 个工作表（每个分类一个）
- ✅ 保存今天的榜单数据

### 第 2 天（2月9日）
运行抓取 → 选择"1" → 选择"2"
- ✅ 创建新的 10 个工作表（2月9日）
- ✅ 对比昨天的榜单，找出每个分类的新上榜应用

## ⚙️ 自定义配置

如果需要修改监控的分类，编辑 `config_categories.py`：

### 添加 App Store 分类

```python
APP_STORE_CATEGORIES = {
    "新分类名": {
        "name_cn": "新分类名",
        "name_en": "New Category",
        "genre_id": "分类ID",  # 查询 Apple 文档获取
        "url": "https://itunes.apple.com/us/rss/topfreeapplications/limit=100/genre=分类ID/json"
    }
}
```

### 添加 Google Play 分类

```python
GOOGLE_PLAY_CATEGORIES = {
    "新分类名": {
        "name_cn": "新分类名",
        "name_en": "New Category",
        "category_id": "CATEGORY_ID"  # 如 "EDUCATION", "MUSIC_AND_AUDIO" 等
    }
}
```

## 🎯 与旧版本的对比

| 特性 | 旧版本 | 新版本（分类监控） |
|------|--------|-------------------|
| 监控范围 | 全部应用榜单 | 按分类监控 |
| 工作表数量 | 2 个（App Store + Google Play） | 10 个（每个分类一个） |
| 数据粒度 | 粗粒度 | 细粒度（按分类） |
| 商店链接 | ❌ 图标链接 | ✅ 可点击的商店链接 |
| 适用场景 | 全局监控 | 垂直领域分析 |

## ⚠️ 注意事项

1. **Google Play 数据说明**
   - 由于免费库限制，使用搜索方式获取数据
   - 结果是热门应用的近似列表，不是官方榜单
   - 如需官方数据，建议使用付费 API 服务

2. **抓取时间**
   - 抓取 10 个分类大约需要 2-3 分钟
   - 建议避免频繁抓取（每天 1-2 次即可）

3. **飞书 API 限制**
   - 注意飞书 API 的调用频率限制
   - 如遇到限制，可适当增加请求间隔

## 📝 文件说明

| 文件 | 说明 |
|------|------|
| `config_categories.py` | 分类配置文件（定义监控的分类） |
| `app_store_scraper_by_category.py` | App Store 分类抓取模块 |
| `google_play_scraper_by_category.py` | Google Play 分类抓取模块 |
| `ranking_monitor_by_category.py` | 分类监控主程序 |
| `run_by_category.sh` | 启动脚本 |

## 🆘 常见问题

### Q: 如何只抓取某几个分类？
**A**: 编辑 `config_categories.py`，删除或注释不需要的分类即可。

### Q: 可以修改每个分类抓取的数量吗？
**A**: 可以，修改 URL 中的 `limit=100` 参数（App Store）或代码中的 `limit` 参数（Google Play）。

### Q: Google Play 的数据为什么不准确？
**A**: 因为使用的免费库不支持官方榜单，只能通过搜索方式近似获取。如需准确数据，建议使用付费 API。

### Q: 商店链接在飞书中打不开？
**A**: 请确保链接格式正确，并且网络可以访问对应的应用商店。

---

有任何问题欢迎随时咨询！🚀
