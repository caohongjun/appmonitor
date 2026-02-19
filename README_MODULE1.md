# 模块1：榜单数据爬取

## 📋 功能说明

自动爬取 App Store 和 Google Play 的榜单数据，支持10个分类，每个分类获取前100名应用。

### 支持的分类

**App Store（4个）**：
- 健康与健身
- 社交网络
- 生活方式
- 游戏

**Google Play（6个）**：
- 健康与健身
- 社交
- 生活方式
- 游戏
- 约会
- 工具

### 获取的数据字段

- 平台（App Store / Google Play）
- 分类
- 应用ID
- 排名
- 应用名称
- 开发者
- 商店链接
- 图标链接
- 抓取时间

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements_module1.txt
```

### 2. 运行爬虫

```bash
# 方式1：使用脚本（推荐）
./scripts/run_scraper.sh

# 方式2：直接运行
python3 modules/scraper.py
```

---

## 📖 使用方法

### 基础用法

```bash
# 爬取今天所有数据（10个分类）
python3 modules/scraper.py

# 爬取指定日期
python3 modules/scraper.py --date 2026-02-12
```

### 指定平台

```bash
# 只爬取 App Store
python3 modules/scraper.py --platform app_store

# 只爬取 Google Play
python3 modules/scraper.py --platform google_play
```

### 指定分类

```bash
# 只爬取健康与健身分类
python3 modules/scraper.py --category health_fitness

# 组合使用：只爬取 App Store 的游戏分类
python3 modules/scraper.py --platform app_store --category games
```

### 查看帮助

```bash
python3 modules/scraper.py --help
```

---

## 📁 数据存储结构

```
data/
└── raw/
    └── 2026-02-12/           # 按日期组织
        ├── app_store/
        │   ├── health_fitness.json
        │   ├── social.json
        │   ├── lifestyle.json
        │   └── games.json
        └── google_play/
            ├── health_fitness.json
            ├── social.json
            ├── lifestyle.json
            ├── games.json
            ├── dating.json
            └── tools.json
```

### JSON文件格式

```json
{
  "date": "2026-02-12",
  "platform": "App Store",
  "category": "健康与健身",
  "category_key": "health_fitness",
  "total_apps": 100,
  "apps": [
    {
      "platform": "App Store",
      "category": "健康与健身",
      "app_id": "com.example.app",
      "rank": 1,
      "name": "Fitness App",
      "developer": "Example Inc.",
      "store_url": "https://...",
      "icon_url": "https://...",
      "timestamp": "2026-02-12 09:00:00"
    }
  ]
}
```

---

## ⏱️ 预估时间

- **单个分类**：30秒 - 1分钟
- **全部10个分类**：5-10分钟
- **只 App Store（4个）**：2-4分钟
- **只 Google Play（6个）**：3-6分钟

---

## 📝 日志

日志文件保存在 `logs/scraper.log`

查看日志：
```bash
tail -f logs/scraper.log
```

---

## ⚙️ 配置文件

配置文件：`config_simple.py`

可以修改以下配置：
- 国家代码（默认 us）
- 每个分类爬取数量（默认 100）
- 请求延迟时间（默认 2-3秒）
- 请求超时时间（默认 30秒）

---

## ❓ 常见问题

### Q1: 缺少依赖怎么办？
```bash
pip install -r requirements_module1.txt
```

### Q2: Google Play 爬取失败？
Google Play 使用非官方库，可能因为网络问题或 Google 限流导致失败。可以：
- 增加延迟时间（修改 config_simple.py 中的 delay）
- 稍后重试
- 只爬取 App Store：`python3 modules/scraper.py --platform app_store`

### Q3: 如何定时运行？
使用 crontab 定时任务：
```bash
# 编辑 crontab
crontab -e

# 添加：每天早上9点执行
0 9 * * * cd /path/to/appmonitor && python3 modules/scraper.py
```

### Q4: 数据保存在哪里？
`data/raw/{日期}/{平台}/{分类}.json`

---

## 🎯 下一步

模块1完成后，可以继续实施：
- **模块2**：新上榜产品识别
- **模块3**：AI 智能分析
- **网页界面**：数据可视化
