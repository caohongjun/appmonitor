# 模块2：新上榜产品识别

## 📋 功能说明

自动对比今天和昨天的榜单数据，识别新上榜的产品，并维护已分析产品记录以避免重复分析。

### 核心功能

- ✅ **榜单对比**：对比今天和昨天的所有分类榜单
- ✅ **智能回溯**：如果昨天数据不存在，自动向前查找最多3天
- ✅ **去重机制**：维护已分析产品列表，避免重复分析
- ✅ **命令行支持**：可指定日期、强制重新识别

---

## 🚀 快速开始

### 1. 确保有数据

运行模块2之前，需要有至少两天的榜单数据：

```bash
# 爬取今天的数据
python modules/scraper.py

# 爬取昨天的数据（如果没有）
python modules/scraper.py --date $(date -v-1d +%Y-%m-%d)
```

### 2. 运行识别

```bash
# 方式1：直接运行
python modules/detector.py

# 方式2：使用脚本
./scripts/run_detector.sh
```

---

## 📖 使用方法

### 基础用法

```bash
# 识别今天的新上榜产品
python modules/detector.py

# 识别指定日期的新上榜产品
python modules/detector.py --date 2026-02-12
```

### 高级用法

```bash
# 强制重新识别（不跳过已分析的产品）
python modules/detector.py --force

# 查看帮助
python modules/detector.py --help
```

---

## 🔍 工作原理

### 1. 查找对比日期

自动查找可用的历史数据：
- 优先使用昨天的数据
- 如果昨天数据不存在，向前查找（最多3天）
- 如果3天内都没有数据，提示用户先爬取

### 2. 对比榜单

对每个平台的每个分类：
1. 加载今天的榜单数据
2. 加载对比日期的榜单数据
3. 提取今天和对比日期的 `app_id` 集合
4. 计算差集：`新上榜 = 今天有 - 对比日期有`

### 3. 去重过滤

- 加载 `analyzed_apps.json` 中已分析的产品列表
- 过滤掉已经分析过的产品
- 只返回未分析过的新产品

### 4. 保存结果

- 将新上榜产品保存到 `data/new_apps/{日期}.json`
- 更新 `analyzed_apps.json` 记录

---

## 📁 数据结构

### 新上榜产品数据

**文件位置**：`data/new_apps/2026-02-12.json`

```json
{
  "date": "2026-02-12",
  "compare_date": "2026-02-11",
  "total_count": 5,
  "generated_at": "2026-02-12 14:06:40",
  "new_apps": [
    {
      "platform": "Google Play",
      "category": "约会",
      "app_id": "get.blender.app",
      "rank": 7,
      "name": "Blender Dating App Meet & Date",
      "developer": "Blender Soft Ltd",
      "store_url": "https://play.google.com/store/apps/details?id=get.blender.app",
      "icon_url": "https://...",
      "timestamp": "2026-02-12 09:00:00"
    }
  ]
}
```

### 已分析产品记录

**文件位置**：`data/analyzed_apps.json`

```json
{
  "analyzed_apps": [
    "get.blender.app",
    "com.taggedapp",
    "com.spark.christianmingle"
  ],
  "last_updated": "2026-02-12 14:06:40",
  "total_count": 3
}
```

---

## 🔄 去重机制

### 为什么需要去重？

避免对同一个产品重复进行AI分析（模块3），节省成本和时间。

### 去重逻辑

1. **首次运行**：识别新产品，保存到 `analyzed_apps.json`
2. **后续运行**：自动过滤已分析的产品
3. **强制模式**：使用 `--force` 参数可以跳过去重

### 示例

```bash
# 第一次运行
python modules/detector.py
# 输出：发现 5 个新上榜产品

# 第二次运行（当天再次执行）
python modules/detector.py
# 输出：发现 0 个新上榜产品（已过滤）

# 强制重新识别
python modules/detector.py --force
# 输出：发现 5 个新上榜产品
```

---

## 📊 识别结果示例

### 控制台输出

```
============================================================
🔍 新上榜产品识别
📅 今天: 2026-02-12
📅 对比: 2026-02-11
============================================================

📱 检测 App Store...
  - 健康与健身 - 无新上榜产品
  - 社交网络 - 无新上榜产品
  - 生活方式 - 无新上榜产品
  - 游戏 - 无新上榜产品

🤖 检测 Google Play...
  - 健康与健身 - 无新上榜产品
  - 社交 - 无新上榜产品
  - 生活方式 - 无新上榜产品
  - 游戏 - 无新上榜产品
  ✓ 约会 - 发现 5 个新上榜产品
  - 工具 - 无新上榜产品

✓ 结果已保存: data/new_apps/2026-02-12.json
============================================================
✓ 识别完成，共发现 5 个新上榜产品
============================================================
✓ 已更新分析记录（共 5 个产品）

⏱  耗时: 0.0 秒
```

---

## 🛠️ 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--date` | 指定要识别的日期 | `--date 2026-02-12` |
| `--force` | 强制重新识别（不跳过已分析产品） | `--force` |
| `--help` | 显示帮助信息 | `--help` |

---

## 📝 日志

日志文件：`logs/detector.log`

查看日志：
```bash
tail -f logs/detector.log
```

日志内容示例：
```
2026-02-12 14:06:40 - detector - INFO - 找到对比日期: 2026-02-11 (向前1天)
2026-02-12 14:06:40 - detector - INFO - 识别完成，共 5 个新上榜产品
```

---

## ⚙️ 配置

去重机制相关配置在代码中：

```python
# 最多向前查找的天数
max_lookback_days = 3

# 已分析产品记录文件位置
analyzed_apps_file = "data/analyzed_apps.json"
```

如需修改，编辑 `modules/detector.py`

---

## 🔗 与其他模块的关系

```
模块1 (scraper.py)
    ↓ 生成榜单数据
模块2 (detector.py)  ← 你在这里
    ↓ 识别新产品
模块3 (analyzer.py)
    ↓ AI分析
模块4 (网页展示)
```

---

## ❓ 常见问题

### Q1: 提示"未找到可用的历史数据"怎么办？

**A**: 需要先运行爬虫获取历史数据：

```bash
# 爬取昨天的数据
python modules/scraper.py --date $(date -v-1d +%Y-%m-%d)

# 或者爬取前天的数据
python modules/scraper.py --date $(date -v-2d +%Y-%m-%d)
```

### Q2: 为什么识别到0个新产品？

**A**: 可能的原因：
1. 今天和昨天的榜单没有变化
2. 新上榜的产品已经被分析过（查看 `analyzed_apps.json`）
3. 可以使用 `--force` 强制重新识别

### Q3: 如何清空已分析记录？

**A**: 删除记录文件即可：

```bash
rm data/analyzed_apps.json
```

下次运行时会重新创建。

### Q4: 识别逻辑是否准确？

**A**: 识别逻辑基于 `app_id` 对比：
- ✅ 准确：如果一个应用的 `app_id` 昨天不在榜单，今天在榜单，则判定为新上榜
- ⚠️ 注意：如果应用只是排名变化（但一直在榜），不会被识别为新上榜

### Q5: 可以跨多天对比吗？

**A**: 可以，但需要手动指定对比日期（目前不支持）。当前版本自动使用昨天或向前3天内最近的数据。

---

## 🎯 下一步

模块2完成后，数据会传递给：
- **模块3**：AI智能分析（对新上榜产品进行深度分析）
- **模块4**：网页展示（在网页中展示新产品列表）

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**快速开始**：
1. 确保有数据：`python modules/scraper.py`
2. 运行识别：`python modules/detector.py`
3. 查看结果：`cat data/new_apps/$(date +%Y-%m-%d).json`

祝你使用愉快！🚀
