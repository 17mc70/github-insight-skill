# GitHub Insight

深度解读 GitHub 仓库的 Claude Skill，帮助 Claude 智能体分析任意 GitHub 项目的用途、技术栈和应用领域，并提供保姆级本地运行指南。

---

## 什么是 GitHub Insight？

GitHub Insight 是一个专为 **Claude AI 助手** 设计的 Claude Skill。安装后，Claude 能够：

| 能力 | 说明 |
|------|------|
| **深度分析仓库** | 解析任意公开仓库的 README、语言统计、元数据 |
| **推荐热门项目** | 根据用户兴趣推荐对应领域的优质开源项目 |
| **生成使用指南** | 提供从零开始的本地安装、配置、运行教程 |
| **评估项目质量** | 分析仓库活跃度、Issue/PR 活动、社区参与度 |

---

## Skill 触发条件

当用户在对话中出现以下意图时触发：

- 想了解某个 GitHub 仓库（"帮我看看这个项目"、"分析一下 xxx"）
- 需要推荐热门项目（"推荐些 xxx 相关的项目"、"有什么 xxx 项目"）
- 询问如何本地运行某个项目（"怎么运行"、"如何安装"）

---

## 安装方法

### 方式一：直接导入 Skill 文件

1. 下载本仓库中的 `github-insight.skill` 文件
2. 打开 Claude Settings → Claude Skills
3. 点击 "Import Skill"，选择下载的 `.skill` 文件
4. 导入成功后即可使用

### 方式二：本地开发

```bash
# 克隆仓库
git clone https://github.com/17mc70/github-insight-skill.git
cd github-insight-skill

# 安装依赖
pip install -r requirements.txt

# 可选：设置 GitHub Token 提升 API 限制
export GITHUB_TOKEN="ghp_你的token"
```

---

## 使用示例

### 示例 1：分析指定仓库

```
用户：帮我分析一下 langchain-ai/langchain 这个仓库
```

**Claude 执行流程：**
1. 调用 `get_github_repo.py langchain-ai/langchain`
2. 分析返回的仓库数据
3. 生成深度解读报告，包含：
   - 项目概述（Stars、描述、更新时间）
   - 核心功能与用途
   - 技术栈（Python、主要框架）
   - 应用领域（AI/LLM 应用开发）
   - 本地安装指南（GPU/CPU 版本）
   - 活跃度评估

### 示例 2：推荐热门项目

```
用户：推荐一些机器学习相关的项目
```

**Claude 执行流程：**
1. 询问用户具体兴趣领域
2. 用户选择 "machine-learning"
3. 调用 `get_trending_repos.py --language machine-learning --limit 3`
4. 对返回的 3 个仓库逐个调用 `get_github_repo.py`
5. 生成 3 个仓库的对比分析报告

### 示例 3：获取本地运行指南

```
用户：帮我看看这个项目怎么本地运行？
```

**Claude 执行流程：**
1. 解析用户输入中的仓库地址
2. 调用 `get_github_repo.py` 获取仓库信息
3. 根据项目类型（AI/Web/后端/工具）生成对应指南：
   - Git 安装
   - 仓库克隆
   - 环境配置
   - 依赖安装
   - 运行项目
   - GPU/CPU 适配（AI 项目）
   - 常见问题

---

## 对话触发方式

| 用户输入 | Claude 响应 |
|---------|-------------|
| "分析一下 pytorch/pytorch" | 调用仓库分析脚本 |
| "推荐几个 Web 开发工具" | 调用热门推荐脚本 |
| "这个项目怎么运行？" | 生成本地运行指南 |
| "帮我看看这个仓库" | 触发分析流程 |

---

## Python 脚本说明

### 1. get_github_repo.py

**功能：** 获取 GitHub 仓库的详细信息

```bash
python scripts/get_github_repo.py owner/repo
```

**参数：**
- `owner/repo` - 仓库标识（必需）

**返回数据：**
```
{
  "name": "仓库名",
  "description": "描述",
  "stars": 12345,
  "forks": 1234,
  "language": "Python",
  "updated_at": "2024-01-01",
  "readme": "# README 内容...",
  "topics": ["machine-learning", "ai", ...]
}
```

### 2. get_trending_repos.py

**功能：** 获取指定领域的热门仓库列表

```bash
python scripts/get_trending_repos.py --language python --limit 3
```

**参数：**
- `--language` - 领域关键词（必需）
- `--limit` - 返回数量（默认 3）

**支持的领域：**
```
machine-learning, deep-learning, large-language-model,
javascript, typescript, python, java, go, rust,
web, frontend, backend, devops, tools, cli,
data-science, computer-vision, nlp, ...
```

---

## 本地运行脚本

### 环境要求

- Python 3.8+
- Git

### 安装

```bash
pip install -r requirements.txt
```

### 配置 GitHub Token（可选）

**提升 API 速率限制：** 60次/小时 → 5000次/小时

```bash
# Linux/macOS
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Windows (CMD)
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Windows (PowerShell)
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

---

## 项目结构

```
github-insight-skill/
├── README.md                      # 本文档
├── github-insight.skill           # Claude Skill 安装包（可直接导入）
├── github-insight/                # Skill 源码目录
│   ├── SKILL.md                  # Skill 配置和完整说明
│   ├── scripts/
│   │   ├── get_github_repo.py    # 仓库分析脚本
│   │   └── get_trending_repos.py # 热门推荐脚本
│   └── references/
│       └── github-usage-guide.md  # 本地使用指南详情
└── requirements.txt              # Python 依赖
```

---

## 依赖

```
requests>=2.31.0          # HTTP 请求库
beautifulsoup4>=4.12.0     # HTML 解析
lxml>=5.0.0                # XML/HTML 解析器
```

---

## 注意事项

- **速率限制**：GitHub 公共 API 限制 60次/小时，建议配置 Token
- **仓库权限**：仅能访问公开仓库
- **分析数量**：推荐时建议每次不超过 3 个仓库
- **解读生成**：脚本负责获取数据，深度解读由 Claude 智能体生成

---

## License

MIT

---

## 贡献

欢迎提交 Issues 和 Pull Requests！

