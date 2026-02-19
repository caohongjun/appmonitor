# 🚀 模块3快速开始指南（简化版）

## 已完成的功能

✅ **一体化Web服务器** (`simple_server.py`)
- 静态文件服务（web目录和data目录）
- API接口（触发分析、获取结果）
- 无需单独启动多个服务器

✅ **后端AI分析模块** (`modules/analyzer.py`)
- 使用Claude Sonnet 4.5进行深度分析
- 5个维度的专业分析
- 保存JSON和Markdown格式结果

✅ **优化的产品选择弹窗**
- 美观的居中弹窗设计
- 两个操作按钮（加入队列/立即分析）
- 平滑动画效果

✅ **分析队列管理** (`web/analyzer.html`)
- 查看待分析应用
- 一键触发AI分析
- 实时状态更新

✅ **分析详情页面** (`web/analysis-detail.html`)
- 美观的Markdown渲染
- 完整的分析报告展示
- 支持复制和返回

---

## 🎯 使用流程（超简单！）

### 第一步：启动Web服务器

```bash
cd /Users/caohongjun/workspace/appmonitor
./scripts/start_web.sh
```

服务器将在 **http://localhost:8000** 启动

### 第二步：在浏览器中使用

1. **打开新产品页面**
   ```
   http://localhost:8000/web/detector.html
   ```

2. **点击任何产品名称**
   - 会弹出美观的选择窗口
   - 选择"加入待分析队列"或"立即分析"

3. **查看分析队列**
   ```
   http://localhost:8000/web/analyzer.html
   ```
   - 点击"开始分析"按钮
   - AI会自动开始分析（约1-2分钟）
   - 状态会自动更新

4. **查看分析结果**
   - 分析完成后点击"查看结果"
   - 跳转到详情页面
   - 查看完整的Markdown格式分析报告

---

## ✨ 特点

### 1. **一键启动，无需多个服务器**
- 只需运行 `./scripts/start_web.sh`
- 同时提供静态文件服务和API接口
- 不需要单独启动Flask或其他服务

### 2. **点击即分析**
- 不需要手动运行命令
- 点击网页按钮就能触发AI分析
- 自动更新分析状态

### 3. **美观的界面**
- 优化的弹窗设计
- 专业的Markdown渲染
- 流畅的动画效果

### 4. **实时反馈**
- Toast提示消息
- 自动状态更新（每10秒检查）
- 分析完成自动通知

### 5. **实时查看分析进度**
- 分析中也可以点击"查看进度"
- 页面每5秒自动刷新
- 分析完成后立即显示结果
- 无需手动刷新页面

---

## 📂 数据文件位置

```
data/
└── analysis/                     # 分析结果
    └── 2026-02-13/              # 按日期组织
        ├── com.example.app.json  # JSON格式
        └── com.example.app.md    # Markdown格式
```

---

## 💡 使用技巧

### 1. 批量分析多个应用

在detector.html中，给多个应用点击"加入待分析队列"，然后到analyzer.html统一处理。

### 2. 手动批量分析（可选）

如果你想通过命令行批量分析所有新产品：

```bash
source venv/bin/activate
python modules/analyzer.py
```

分析脚本会自动扫描`new_apps`目录，找到所有未分析的产品。

### 3. 查看分析日志

```bash
tail -f logs/analyzer.log
```

### 4. 查看Markdown文件

```bash
# 查看最新分析结果
ls -lt data/analysis/$(date +%Y-%m-%d)/
cat data/analysis/$(date +%Y-%m-%d)/*.md
```

---

## 🔧 故障排查

### 问题1：Web服务器无法启动

**症状**：运行 `./scripts/start_web.sh` 后报错

**解决方案**：
```bash
# 检查端口是否被占用
lsof -i :8000

# 如果被占用，修改simple_server.py中的端口号
# 将最后一行改为：run_server(port=8001)
```

### 问题2：点击"开始分析"没有反应

**症状**：点击按钮后状态不变

**解决方案**：
1. 确认Web服务器已启动（查看终端输出）
2. 打开浏览器控制台（F12）查看错误
3. 检查浏览器是否显示CORS错误
4. 刷新页面重试

### 问题3：分析一直显示"分析中"

**症状**：状态长时间不更新

**解决方案**：
```bash
# 查看日志
tail -30 logs/analyzer.log

# 检查服务器终端输出
# 如果看到错误，可能是API密钥问题

# 手动测试分析
source venv/bin/activate
python modules/analyzer.py --app-id test.app --platform "App Store"
```

### 问题4：API返回错误

**症状**：浏览器控制台显示API错误

**解决方案**：
1. 检查ANTHROPIC_API_KEY是否设置
2. 检查虚拟环境是否激活
3. 查看服务器终端的错误输出

---

## 🎨 界面预览

### 1. 产品选择弹窗
- 🎨 渐变色头部
- 📱 居中弹出
- 🖼️ 显示应用图标和详细信息
- 🎯 两个清晰的操作按钮

### 2. 分析队列页面
- 左侧：状态筛选（全部/待分析/分析中/已完成）
- 右侧：应用列表（表格形式）
- 操作：开始分析、查看结果、移除

### 3. 分析详情页面
- 顶部：应用信息卡片
- 中间：Markdown格式的5维度分析
- 底部：操作按钮

---

## 🔗 相关文档

- [README_MODULE3.md](README_MODULE3.md) - 完整文档
- [README_MODULE2.md](README_MODULE2.md) - 新产品识别
- [README_MODULE1.md](README_MODULE1.md) - 榜单爬取

---

## ✅ 快速验证

### 1. 启动服务器
```bash
./scripts/start_web.sh
```

### 2. 访问页面
在浏览器中打开：`http://localhost:8000/web/detector.html`

### 3. 测试功能
- 点击任意产品名称
- 选择"立即分析"
- 等待分析完成（约1-2分钟）
- 查看结果

---

## 💰 成本说明

使用Claude Sonnet 4.5：
- 每个应用：~2300 tokens
- 每次分析成本：~$0.0069
- 每天10个应用：~$0.07
- 每月成本：~$2

---

## 🎯 完整工作流程

```
启动服务器
    ↓
打开detector.html
    ↓
点击产品名称
    ↓
选择分析方式
    ↓
(立即分析)
    ↓
API触发analyzer.py
    ↓
调用Claude API分析
    ↓
保存JSON + Markdown
    ↓
前端自动检测完成
    ↓
更新状态为"已完成"
    ↓
点击"查看结果"
    ↓
展示Markdown报告
```

---

**就这么简单！** 🎉

1. `./scripts/start_web.sh` - 启动服务器
2. 打开 `http://localhost:8000/web/detector.html`
3. 点击产品 → 选择分析 → 查看结果

一切都在浏览器中完成，无需手动运行命令！

祝您使用愉快！🚀
