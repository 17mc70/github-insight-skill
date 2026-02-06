# GitHub Insight Skill

深度解读 GitHub 仓库的 Claude Skill，提供仓库分析、热门推荐和本地使用指南。

## 功能特性

- **仓库分析**：解析任意 GitHub 仓库的用途、技术栈、应用领域
- **热门推荐**：根据兴趣领域推荐热门项目
- **保姆级指南**：从零开始的本地安装和使用教程
- **GPU/CPU 适配**：智能判断环境，提供 CPU/GPU 两套方案
- **云端替代**：无 GPU 时提供云端 GPU 解决方案

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 使用方法

```bash
# 分析指定仓库
python scripts/get_github_repo.py owner/repo

# 获取热门仓库
python scripts/get_trending_repos.py --language python --limit 3
```

### 可选配置

设置 GitHub Token 提升 API 速率限制：

```bash
export GITHUB_TOKEN="ghp_xxx"
```

## 项目结构

```
├── README.md                    # 项目说明
├── github-insight.skill         # Claude Skill 核心文件
├── github-insight/
│   ├── SKILL.md                 # Skill 详细文档
│   ├── scripts/
│   │   ├── get_github_repo.py      # 获取仓库信息
│   │   └── get_trending_repos.py    # 获取热门仓库
│   └── references/
│       └── github-usage-guide.md    # 本地使用指南
└── requirements.txt             # Python 依赖
```

## 依赖

- requests>=2.31.0
- beautifulsoup4>=4.12.0
- lxml>=5.0.0

## License

MIT
