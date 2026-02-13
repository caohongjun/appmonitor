# 🔧 故障排查指南

## 快速诊断命令

```bash
# 运行快速测试（推荐 - 包含 API Key 检查）
./scripts/quick_test.sh

# 或运行完整诊断
./scripts/check_status.sh
```

---

## ⚠️ 最常见问题：环境变量未传递

### 症状
- 手动运行 `python modules/analyzer.py` 成功
- 但网页点击按钮后一直显示"分析中"
- Web 服务器终端没有看到分析进程输出

### 原因
Web 服务器启动时没有 `ANTHROPIC_API_KEY` 环境变量，导致子进程无法调用 Claude API。

### 解决方案

**步骤1：停止当前 Web 服务器**
```bash
# 在运行 Web 服务器的终端按 Ctrl+C
# 或在另一个终端运行：
pkill -f simple_server.py
```

**步骤2：设置环境变量并重启**
```bash
# 方案1：临时设置（仅当前终端会话）
export ANTHROPIC_API_KEY='your-api-key-here'
./scripts/start_web.sh

# 方案2：持久化设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo "export ANTHROPIC_API_KEY='your-api-key-here'" >> ~/.bashrc
source ~/.bashrc
./scripts/start_web.sh
```

**步骤3：验证**
```bash
# 运行快速测试
./scripts/quick_test.sh

# 应该看到：
# ✓ ANTHROPIC_API_KEY 已设置 (长度: xx)
```

**注意：** 如果在 Claude Code 环境中运行，通常会自动使用 Claude 的 API。但如果手动启动服务器，需要确保环境变量已设置。

---

## 问题1：一直显示"分析中"

### 诊断步骤

**1. 查看Web服务器终端输出**
- 在启动 `./scripts/start_web.sh` 的终端窗口查看输出
- 看是否有错误信息或进度输出

**2. 查看分析日志**
```bash
# 实时查看日志
tail -f logs/analyzer.log

# 查看最近的日志
tail -50 logs/analyzer.log
```

**3. 检查分析进程是否在运行**
```bash
ps aux | grep analyzer.py
```

**4. 手动测试分析**
```bash
source venv/bin/activate

# 测试分析（替换为实际的app_id）
python modules/analyzer.py --app-id "com.example.app" --platform "App Store"

# 查看输出，看是否有错误
```

### 常见原因和解决方案

#### 原因1：API密钥问题

**症状：** 日志显示"✗ 客户端初始化失败"或API相关错误

**解决方案：**
```bash
# 检查API密钥
echo $ANTHROPIC_API_KEY

# 如果未设置，Claude Code会自动使用环境的API
# 确保在Claude Code环境中运行

# 或手动设置（如果需要）
export ANTHROPIC_API_KEY="your-api-key"
```

#### 原因2：虚拟环境问题

**症状：** 日志显示"ModuleNotFoundError: No module named 'anthropic'"

**解决方案：**
```bash
# 激活虚拟环境
source venv/bin/activate

# 安装anthropic
pip install anthropic

# 重启Web服务器
pkill -f simple_server.py
./scripts/start_web.sh
```

#### 原因3：进程卡住或超时

**症状：** 进程存在但长时间无响应

**解决方案：**
```bash
# 杀掉卡住的进程
pkill -f analyzer.py

# 重启Web服务器
pkill -f simple_server.py
./scripts/start_web.sh

# 重新触发分析
```

#### 原因4：网络问题

**症状：** 日志显示连接超时或网络错误

**解决方案：**
- 检查网络连接
- 检查是否有代理设置
- 尝试使用VPN（如果需要）

---

## 问题2：分析失败，没有结果文件

### 诊断步骤

**1. 检查日志中的错误信息**
```bash
grep "✗" logs/analyzer.log | tail -20
```

**2. 检查数据目录权限**
```bash
ls -la data/
ls -la data/analysis/
```

**3. 手动创建测试文件**
```bash
mkdir -p data/analysis/$(date +%Y-%m-%d)
```

### 解决方案

```bash
# 确保数据目录存在且有写权限
mkdir -p data/analysis
chmod 755 data/analysis

# 重新运行分析
source venv/bin/activate
python modules/analyzer.py
```

---

## 问题3：Web服务器无法启动

### 诊断步骤

**1. 检查端口是否被占用**
```bash
lsof -i :8000
```

**2. 查看启动脚本输出**
```bash
./scripts/start_web.sh
# 查看终端输出的错误信息
```

### 解决方案

**如果端口被占用：**
```bash
# 方案1：杀掉占用进程
kill $(lsof -t -i:8000)

# 方案2：修改端口
# 编辑 simple_server.py，将最后一行改为：
# run_server(port=8001)
```

**如果虚拟环境问题：**
```bash
# 重新创建虚拟环境
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install anthropic

# 重新启动
./scripts/start_web.sh
```

---

## 问题4：浏览器显示CORS错误

### 症状
浏览器控制台（F12）显示跨域错误

### 解决方案
```bash
# 确保Web服务器正常运行
# simple_server.py已经配置了CORS头

# 确保通过 http://localhost:8000 访问，而不是 file://

# 正确的访问地址：
# http://localhost:8000/web/detector.html
# http://localhost:8000/web/analyzer.html
```

---

## 问题5：前端一直转圈，后台已完成

### 诊断步骤

**1. 检查分析结果文件是否存在**
```bash
# 查看今天的分析结果
ls -la data/analysis/$(date +%Y-%m-%d)/
```

**2. 手动访问API**
```bash
# 替换为实际的app_id和platform
curl "http://localhost:8000/api/analysis/com.example.app?platform=App%20Store&date=$(date +%Y-%m-%d)"
```

### 解决方案

**刷新浏览器页面：**
- 按 Ctrl+Shift+R（强制刷新）
- 或关闭页面重新打开

**清除localStorage：**
```javascript
// 在浏览器控制台（F12）执行
localStorage.clear()
location.reload()
```

---

## 调试技巧

### 1. 开启浏览器开发者工具

按 F12 打开开发者工具，查看：
- **Console** - JavaScript错误和日志
- **Network** - API请求状态
- **Application** → Local Storage - 队列数据

### 2. 查看详细日志

```bash
# 终端1：实时查看分析日志
tail -f logs/analyzer.log

# 终端2：查看Web服务器输出
# (在启动服务器的终端查看)

# 终端3：运行分析命令
source venv/bin/activate
python modules/analyzer.py
```

### 3. 手动测试完整流程

```bash
# 1. 确保虚拟环境激活
source venv/bin/activate

# 2. 测试analyzer.py
python modules/analyzer.py --app-id test.app --platform "App Store"

# 3. 检查输出目录
ls -la data/analysis/$(date +%Y-%m-%d)/

# 4. 查看生成的文件
cat data/analysis/$(date +%Y-%m-%d)/test.app.json
```

### 4. 完全重启

```bash
# 1. 停止所有相关进程
pkill -f simple_server.py
pkill -f analyzer.py

# 2. 清理日志（可选）
> logs/analyzer.log

# 3. 重新启动Web服务器
./scripts/start_web.sh

# 4. 刷新浏览器
```

---

## 获取帮助

如果以上方法都无法解决问题：

1. **收集信息**
   ```bash
   # 运行诊断脚本并保存输出
   ./scripts/check_status.sh > debug_info.txt

   # 查看最近的日志
   tail -100 logs/analyzer.log >> debug_info.txt
   ```

2. **查看完整错误信息**
   - Web服务器终端的完整输出
   - logs/analyzer.log的完整内容
   - 浏览器控制台的错误信息

3. **检查环境**
   ```bash
   # Python版本
   python --version

   # pip包列表
   pip list

   # 系统信息
   uname -a
   ```

---

## 预防措施

### 定期清理

```bash
# 清理旧的分析结果（保留最近7天）
find data/analysis -type d -mtime +7 -exec rm -rf {} \;

# 清理日志（可选）
> logs/analyzer.log
```

### 监控

```bash
# 创建监控脚本
watch -n 5 './scripts/check_status.sh'
```

---

**提示：** 大多数问题都可以通过查看日志和重启服务器解决。遇到问题时，首先运行 `./scripts/check_status.sh` 进行快速诊断。
