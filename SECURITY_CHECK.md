# 安全检查清单

## ⚠️ 上传到 Git 前必读

### 🔒 敏感信息说明

以下文件包含敏感信息，**不应该**上传到 Git：

1. **`config.py`** - 包含飞书 API 密钥
   - `FEISHU_APP_ID` - 飞书应用 ID
   - `FEISHU_APP_SECRET` - 飞书应用密钥
   - `FEISHU_SPREADSHEET_TOKEN` - 电子表格 Token

2. **`credentials.json`** - Google API 凭证（如果使用）

3. **`venv/`** - Python 虚拟环境

4. **`__pycache__/`** - Python 缓存文件

---

## ✅ 已配置的保护

### `.gitignore` 文件

已经配置了 `.gitignore`，以下文件/目录会被自动忽略：

```gitignore
# 敏感信息
config.py
credentials.json

# Python
__pycache__/
*.pyc
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## 📋 上传前检查清单

### 第 1 步：验证 .gitignore

```bash
# 查看将要提交的文件
git status

# 确保 config.py 不在列表中
```

### 第 2 步：搜索敏感信息

```bash
# 搜索可能的敏感信息
grep -r "FEISHU_APP_SECRET\|cli_a902c\|xxRkmpx" --include="*.py" --include="*.md" --exclude="config.py" --exclude-dir=venv .

# 应该只在 config.py 中找到（config.py 不会被上传）
```

### 第 3 步：验证配置示例文件

确保 `config.example.py` 不包含真实的密钥：

```bash
cat config.example.py
# 所有值应该为空字符串 ""
```

---

## 🚀 首次配置（供其他人使用）

其他人克隆你的仓库后，需要：

### 1. 复制配置文件

```bash
cp config.example.py config.py
```

### 2. 填写配置信息

编辑 `config.py`，填入：
- 飞书 App ID
- 飞书 App Secret
- 飞书电子表格 Token（可选）

### 3. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 运行测试

```bash
./run_by_category.sh
```

---

## 🔍 定期检查

### 检查是否有敏感信息泄露

```bash
# 检查 Git 历史中是否有敏感信息
git log --all --full-history --source -- config.py

# 检查当前暂存区
git diff --cached
```

### 如果不小心提交了敏感信息

```bash
# 从最新提交中移除
git rm --cached config.py
git commit --amend

# 如果已经推送，需要更严格的处理
# 参考：https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
```

---

## 📄 可以安全上传的文件

以下文件不包含敏感信息，可以安全上传：

✅ `config.example.py` - 配置模板（空值）
✅ `config_categories.py` - 分类配置（只导入，不存储）
✅ `*.py` - 所有其他 Python 文件
✅ `*.md` - 所有文档文件（已移除敏感链接）
✅ `*.sh` - 所有脚本文件
✅ `requirements.txt` - 依赖列表
✅ `.gitignore` - Git 忽略规则

---

## 🔐 安全建议

1. **定期更换密钥**
   - 如果怀疑密钥泄露，立即更换
   - 在飞书开放平台重新生成 App Secret

2. **限制 API 权限**
   - 只授予必要的权限
   - 定期审查权限设置

3. **不要在文档中包含**
   - 真实的 API 密钥
   - 真实的表格 Token
   - 真实的表格链接

4. **使用环境变量（可选）**
   ```bash
   # 更安全的方式是使用环境变量
   export FEISHU_APP_ID="your_app_id"
   export FEISHU_APP_SECRET="your_app_secret"
   ```

---

## ✅ 验证通过标准

上传前确认：

- [ ] `config.py` 在 `.gitignore` 中
- [ ] `config.example.py` 不包含真实密钥
- [ ] `git status` 不显示 `config.py`
- [ ] 搜索敏感信息只在 `config.py` 中找到
- [ ] 所有文档移除了真实的表格链接
- [ ] 已测试 `config.example.py` 格式正确

---

## 📞 需要帮助？

如果不确定某个文件是否包含敏感信息：

1. 在本地搜索文件内容
2. 检查是否包含 API 密钥、Token、邮箱等
3. 有疑问时，先不要上传

**安全第一！** 🔒
