# GitHub Insight

深度解读 GitHub 仓库的 Claude Skill，全面分析任意仓库的用途、技术栈和应用领域，提供保姆级本地使用指南。

## 目录

- [简介](#简介)
- [功能特性](#功能特性)
- [安装](#安装)
- [使用](#使用)
  - [分析指定仓库](#分析指定仓库)
  - [查找热门仓库](#查找热门仓库)
- [GPU/CPU 支持](#gpucpu-支持)
- [项目结构](#项目结构)
- [配置](#配置)
- [云端 GPU 替代方案](#云端-gpu-替代方案)
- [依赖要求](#依赖要求)
- [常见问题](#常见问题)
- [License](#license)

---

## 简介

GitHub Insight 帮助您深入了解任何 GitHub 仓库。无论您有特定的仓库需要分析，还是正在探索新项目，本工具都能提供全面的分析报告，包括：

- 仓库概述与核心功能
- 技术栈与编程语言识别
- 应用领域分类
- 本地运行指南
- GPU/CPU 兼容性评估
- 社区活跃度分析

---

## 功能特性

| 功能 | 描述 |
|------|------|
| **仓库分析** | 解析任意 GitHub 仓库的 README、语言统计和元数据 |
| **热门推荐** | 根据兴趣领域筛选并推荐热门项目 |
| **本地指南** | 从零开始的本地安装运行教程 |
| **硬件检测** | 自动检测 CPU/GPU 环境，提供最优配置方案 |
| **多平台支持** | Windows、macOS、Linux 全面兼容 |
| **云端 GPU** | 本地无 GPU 时的云端解决方案 |

---

## 安装

### 前置条件

- Python 3.8 或更高版本
- Git 已安装
- （可选）GitHub Personal Access Token 用于提升 API 速率限制

### 安装步骤

```bash
# 克隆仓库
git clone <仓库地址>
cd <仓库名称>

# 安装依赖
pip install -r requirements.txt

# 可选：设置 GitHub Token 提升 API 限制
# 未认证：60 次/小时 → 认证后：5000 次/小时
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
```

---

## 使用

### 分析指定仓库

分析特定的 GitHub 仓库：

```bash
python scripts/get_github_repo.py owner/repo
# 示例：python scripts/get_github_repo.py tensorflow/tensorflow
```

**输出内容：**
- 基本信息（Stars、Forks、描述）
- 核心用途与功能
- 技术栈与编程语言
- 应用领域
- 本地安装指南（CPU/GPU 版本）
- 活跃度指标与社区健康度

### 查找热门仓库

发现特定领域的热门仓库：

```bash
python scripts/get_trending_repos.py --language <领域> --limit <数量>
# 示例：python scripts/get_trending_repos.py --language machine-learning --limit 3
```

**支持的领域：**
- LLM / 大语言模型
- AI / 机器学习
- Python 开发
- JavaScript / Web 开发
- 开发工具
- 设计 / UI
- 移动开发

---

## GPU/CPU 支持

### AI/机器学习项目

本工具会智能检测您的硬件环境，提供相应的安装指导。

#### 检测您的硬件

**Windows 系统：**
```powershell
# 右键点击"此电脑" → "管理" → "设备管理器" → "显示适配器"
# 或在任务管理器中查看"性能" → "GPU"
```

**macOS 系统：**
```bash
system_profiler SPDisplaysDataType
```

**Linux 系统：**
```bash
lspci | grep -i vga      # 查看显卡信息
nvidia-smi              # 检查 NVIDIA 驱动（需要 CUDA 工具包）
```

#### 性能对比

| 任务 | CPU | GPU |
|------|-----|-----|
| 小模型推理 | 秒级 | 毫秒级 |
| 大模型推理 | 分钟级 | 秒级 |
| 训练模型 | 小时/天级 | 小时级 |
| 图片生成 (SD) | 不可用 | 秒级 |

**GPU 通常比 CPU 快 10-100 倍**

#### 安装选项

**CPU 版本**（无需 GPU）：
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install tensorflow  # CPU 版本
```

**GPU 版本**（需要 NVIDIA 显卡）：
```bash
# 先安装 CUDA 工具包，然后：
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install tensorflow[and-cuda]
```

---

## 项目结构

```
.
├── README.md                                 # 本文档
├── github-insight.skill                     # Claude Skill 包
├── github-insight/
│   ├── SKILL.md                              # 完整 Skill 文档
│   ├── scripts/
│   │   ├── get_github_repo.py               # 仓库分析脚本
│   │   │   # 用法：python get_github_repo.py owner/repo
│   │   └── get_trending_repos.py             # 获取热门仓库脚本
│   │   # 用法：python get_trending_repos.py --language python --limit 3
│   └── references/
│       └── github-usage-guide.md             # 完整的本地使用指南
│           # 包含内容：
│           # - Git 安装
│           # - Python/Node.js 配置
│           # - GPU/CPU 适配
│           # - AI/Web/后端项目指南
│           # - 云端 GPU 替代方案
│           # - 常见问题解答
└── requirements.txt                          # Python 依赖
```

---

## 配置

### GitHub Token（推荐设置）

将 API 速率限制从 60 提升到 5000 次/小时：

```bash
# Linux/macOS
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"

# Windows (命令提示符)
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Windows (PowerShell)
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**生成 Token：** GitHub 设置 → 开发者设置 → Personal access tokens

### 环境变量

某些项目可能需要额外的配置：

```bash
# 从示例文件创建 .env
cp .env.example .env

# 常见变量：
# API_KEY=your_api_key
# DATABASE_URL=postgresql://...
# SECRET_KEY=your_secret
```

---

## 云端 GPU 替代方案

当本地没有 GPU 或性能不足时，可以使用以下云端服务：

| 服务 | 费用 | 特点 |
|------|------|------|
| **Google Colab** | 免费 | Tesla T4 GPU，约 12 小时会话限制 |
| **Kaggle Notebooks** | 免费 | 每周 30 小时 GPU，集成数据集 |
| **AutoDL** | 约 0.5-1 元/小时 | 国内网络，RTX 3090 |
| **GCP** | 按量付费 | 新用户赠送 300 美元免费额度 |
| **AWS** | 按量付费 | GPU 选择最丰富 |
| **Azure** | 按量付费 | 企业级集成 |

### 快速上手：Google Colab

1. 访问 https://colab.research.google.com/
2. 创建新笔记本
3. 运行时 → 更改运行时类型 → GPU
4. 开始使用 GPU 加速运行代码

```python
# 在 Colab 中安装依赖
!pip install torch torchvision transformers
```

---

## 依赖要求

### 核心依赖

```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
```

### 可选依赖（高级功能）

```
# 高级 ML 工作流
torch>=2.0.0
tensorflow>=2.13.0
transformers>=4.30.0

# 开发测试
pytest>=7.0.0
pytest-cov>=4.0.0
```

---

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| API 速率限制 | 设置 `GITHUB_TOKEN` 环境变量 |
| 下载速度慢 | 使用国内镜像源（清华、阿里云等） |
| CUDA 版本不匹配 | 匹配 PyTorch/TensorFlow 与 CUDA 版本 |
| 端口被占用 | 更换端口或终止占用进程 |
| 权限不足 | 使用 `pip install --user` 或管理员权限 |

### 获取帮助

- 查看项目的 GitHub Issues
- 参考 [github-usage-guide.md](github-insight/references/github-usage-guide.md)
- 在 Stack Overflow 搜索类似问题

---

## License

MIT License - 欢迎根据需要使用和修改。

---

## 贡献

欢迎贡献！欢迎提交 Issues 或 Pull Requests。
