# 模块3：AI智能分析

## 📋 功能说明

使用Claude API对新上榜产品进行5个维度的深度分析，并生成Markdown格式的分析报告。

### 核心功能

- ✅ **AI分析**：使用Claude Sonnet 4.5进行深度分析
- ✅ **5个维度**：基本信息、投放素材、产品功能、用户评价、思考总结
- ✅ **队列管理**：支持添加应用到分析队列，批量分析
- ✅ **Markdown展示**：分析结果以美观的Markdown格式展示
- ✅ **Web界面**：通过网页界面管理和查看分析结果

---

## 🚀 快速开始

### 1. 安装依赖

```bash
source venv/bin/activate && pip install flask flask-cors anthropic
```

### 2. 启动Web服务器

```bash
# 方式1：使用启动脚本
./start_web_server.sh

# 方式2：直接运行
source venv/bin/activate && python web_server.py
```

服务器将在 `http://localhost:5000` 启动

### 3. 使用Web界面

1. 打开 `web/detector.html` 查看新上榜产品
2. 点击产品名称，选择"加入待分析队列"或"立即分析"
3. 前往 `web/analyzer.html` 查看分析队列
4. 点击"开始分析"触发AI分析
5. 分析完成后，点击"查看结果"查看详细分析报告

---

## 📖 使用方法

### 通过Web界面（推荐）

**步骤1：启动Web服务器**
```bash
./start_web_server.sh
```

**步骤2：添加应用到队列**
- 访问 `web/detector.html`
- 点击产品名称
- 在弹窗中选择"加入待分析队列"或"立即分析"

**步骤3：查看分析进度**
- 访问 `web/analyzer.html`
- 查看队列中应用的状态：
  - 🟡 待分析（pending）
  - 🔵 分析中（analyzing）
  - 🟢 已完成（completed）

**步骤4：查看分析结果**
- 点击"查看结果"按钮
- 在详情页面查看完整的Markdown格式分析报告
- 可以复制分析内容

### 通过命令行

**分析单个应用**
```bash
source venv/bin/activate && python modules/analyzer.py \
  --app-id com.example.app \
  --platform "App Store"
```

**批量分析队列中的应用**
```bash
source venv/bin/activate && python modules/analyzer.py
```

**限制分析数量**
```bash
source venv/bin/activate && python modules/analyzer.py --max-apps 5
```

---

## 🔍 分析维度

### 1. 基本信息分析
- 产品发布时间和上线时长
- 主要市场和地区
- 开发商背景和其他产品
- 产品数据（评分、评论数等）

### 2. 投放素材分析
- 主要推广渠道
- 素材内容方向（视频、图片、文案）
- 目标用户画像

### 3. 产品功能分析
- 核心功能列表
- 创新点和差异化优势
- 用户体验亮点

### 4. 用户评价分析
- 正面评价关键点
- 负面评价常见问题
- 改进建议

### 5. 思考与总结
- 整体评估
- 成功因素分析
- 可借鉴之处
- 市场机会洞察

---

## 📁 数据结构

### 分析队列文件

**文件位置**：`data/analysis_queue.json`

```json
[
  {
    "app_id": "com.example.app",
    "name": "Example App",
    "platform": "App Store",
    "category": "健康与健身",
    "developer": "Example Inc.",
    "rank": 15,
    "store_url": "https://...",
    "icon_url": "https://...",
    "status": "pending",
    "added_time": "2026-02-13 10:00:00"
  }
]
```

### 分析结果文件

**文件位置**：`data/analysis/{日期}/{app_id}.json`

```json
{
  "app_id": "com.example.app",
  "name": "Example App",
  "platform": "App Store",
  "category": "健康与健身",
  "developer": "Example Inc.",
  "rank": 15,
  "store_url": "https://...",
  "icon_url": "https://...",
  "analysis_date": "2026-02-13 10:05:30",
  "analysis_markdown": "# 分析内容...",
  "tokens_used": {
    "input": 1500,
    "output": 800
  }
}
```

**Markdown文件**：`data/analysis/{日期}/{app_id}.md`

---

## 🌐 Web API接口

### POST /api/analyze
触发AI分析

**请求体**：
```json
{
  "app_id": "com.example.app",
  "platform": "App Store"
}
```

**响应**：
```json
{
  "success": true,
  "message": "分析任务已启动: com.example.app"
}
```

### GET /api/analysis/{app_id}
获取分析结果

**查询参数**：
- `platform`: 平台名称（必需）
- `date`: 日期（可选，默认今天）

**响应**：返回完整的分析结果JSON

### GET /api/analysis/list
获取分析列表

**查询参数**：
- `date`: 日期（可选，默认今天）

**响应**：
```json
{
  "analyses": [
    {
      "app_id": "...",
      "name": "...",
      "platform": "...",
      "category": "...",
      "analysis_date": "..."
    }
  ]
}
```

### GET /api/queue
获取分析队列

### POST /api/queue
更新分析队列（从前端同步）

---

## 💰 成本估算

使用Claude Sonnet 4.5进行分析：

- **每个应用**：约2000-3000 tokens
- **每天10个应用**：约25K tokens
- **每天成本**：~$0.075
- **每月成本**：~$2.25

---

## 🔄 工作流程

```
1. 用户在detector.html查看新产品
         ↓
2. 点击产品名称，添加到队列
         ↓
3. 队列数据保存到localStorage
         ↓
4. 用户访问analyzer.html查看队列
         ↓
5. 点击"开始分析"调用API
         ↓
6. API触发analyzer.py执行分析
         ↓
7. 调用Claude API进行深度分析
         ↓
8. 保存结果为JSON和Markdown
         ↓
9. 前端定期检查分析状态
         ↓
10. 完成后更新队列状态
         ↓
11. 用户点击"查看结果"
         ↓
12. 跳转到analysis-detail.html
         ↓
13. 使用marked.js渲染Markdown
         ↓
14. 展示美观的分析报告
```

---

## 🛠️ 配置说明

### API配置

分析模块会自动使用当前环境的Anthropic API密钥。确保已设置：

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 模型配置

默认使用 `claude-sonnet-4-5-20250929`，可在 `modules/analyzer.py` 中修改。

---

## 📝 日志

日志文件：`logs/analyzer.log`

查看日志：
```bash
tail -f logs/analyzer.log
```

---

## ❓ 常见问题

### Q1: Web服务器无法启动？

**A**: 检查端口是否被占用：
```bash
lsof -i :5000
```

如果被占用，可以在 `web_server.py` 中修改端口。

### Q2: 分析失败怎么办？

**A**:
1. 检查日志文件 `logs/analyzer.log`
2. 确认ANTHROPIC_API_KEY已设置
3. 检查网络连接
4. 查看队列文件是否正确

### Q3: 如何清空分析队列？

**A**:
```bash
rm data/analysis_queue.json
```

或在Web界面中逐个移除。

### Q4: 分析结果保存在哪里？

**A**:
- JSON格式：`data/analysis/{日期}/{app_id}.json`
- Markdown格式：`data/analysis/{日期}/{app_id}.md`

### Q5: 可以自定义分析维度吗？

**A**: 可以，修改 `modules/analyzer.py` 中的 `get_analysis_prompt()` 函数。

---

## 🎯 下一步

模块3完成后，所有核心功能已实现：
- ✅ **模块1**：榜单数据爬取
- ✅ **模块2**：新上榜产品识别
- ✅ **模块3**：AI智能分析
- ✅ **网页展示**：完整的Web界面

**建议**：
1. 设置定时任务自动运行
2. 优化分析Prompt以减少token消耗
3. 添加更多分析维度
4. 导出分析报告为PDF

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**快速开始**：
1. 启动服务器：`./start_web_server.sh`
2. 打开浏览器：访问 `web/detector.html`
3. 添加应用到队列
4. 触发AI分析
5. 查看分析结果

祝你使用愉快！🚀
