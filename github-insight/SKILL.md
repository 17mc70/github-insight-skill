---
name: github-insight
description: 深度解读GitHub仓库，提供仓库用途、领域行业分析及本地使用指南。支持分析指定仓库或根据用户兴趣推荐热门仓库并解读。
dependency:
  python:
    - requests>=2.31.0
    - beautifulsoup4>=4.12.0
    - lxml>=5.0.0
---

# GitHub仓库深度解读

## 任务目标
- 本Skill用于：深度分析GitHub开源项目，提供详细解读报告
- 能力包含：
  1. 分析指定仓库的用途、技术栈、应用领域
  2. 根据用户兴趣推荐热门仓库
  3. 生成工具/AI模型的本地使用指南
  4. 评估仓库活跃度和社区健康度
- 触发条件：用户表示想了解某个GitHub仓库，或需要推荐热门项目

## 前置准备
- 依赖说明：脚本所需的Python包
  ```
  requests>=2.31.0
  beautifulsoup4>=4.12.0
  lxml>=5.0.0
  ```
- GitHub Token（可选）：提供Personal Access Token可提升API速率限制（从60次/小时提升到5000次/小时）
  ```bash
  # 设置环境变量（推荐但非必需）
  export GITHUB_TOKEN="ghp_xxx"
  ```

## 操作步骤

### 标准流程

1. **引导用户选择模式**
   - 询问用户："您是否已经有感兴趣的GitHub仓库？"
   - 展示两个选项：
     - A. 我有仓库，请帮我分析
     - B. 我没有具体仓库，请推荐一些热门项目

2. **分支A：分析指定仓库**
   - 1.1. 请求用户提供仓库信息
     - 支持格式：`owner/repo`（如 `openai/gpt`）或完整URL
     - 示例："请输入您想分析的仓库名称，格式如 openai/gpt"
   
   - 1.2. 调用脚本获取仓库数据
     ```bash
     python scripts/get_github_repo.py <owner/repo>
     ```
     - 返回数据包括：基本信息、README、编程语言统计、仓库标签
   
   - 1.3. 生成深度解读报告
     - 智能体分析获取的数据，生成包含以下内容的报告：
       - **仓库概述**：名称、描述、星标数、更新时间
       - **主要用途**：基于README和描述提炼核心功能
       - **技术栈**：编程语言、主要框架/库
       - **应用领域与行业**：判断项目所属领域（AI、Web、工具、数据科学等）
       - **本地使用指南**（从零开始的保姆级操作）：
         - 根据项目类型（AI/ML、Web、后端、工具、桌面应用等）提供详细指导
         - **GPU/CPU适配说明**（AI/ML项目特有）：
           - 帮助用户判断是否有GPU
           - 说明GPU vs CPU的性能差距（10-100倍）
           - 判断仓库是否支持CPU
           - 提供**CPU版本**和**GPU版本**两套安装教程
           - 如果仓库**必须GPU**，友好提示并提供云端GPU替代方案
         - 参考 [references/github-usage-guide.md](references/github-usage-guide.md) 中的完整教程
         - 包含：Git安装、仓库克隆、环境配置、依赖安装、运行项目、常见问题解决
         - 分平台指导（Windows/macOS/Linux）
         - 提供完整的命令行操作步骤
         - **云端GPU替代方案**（针对无GPU但需要GPU功能的用户）：
           - Google Colab（免费）
           - Kaggle Notebooks（免费）
           - 国内平台（AutoDL、恒源云等）
           - 云服务商（GCP、AWS、Azure）
       - **活跃度评估**：
         - 最近更新时间
         - Issue和PR活动
         - 社区参与度

3. **分支B：推荐并分析热门仓库**
   - 2.1. 询问用户感兴趣的领域
     - 展示常见领域选项：
       - LLM/大模型
       - AI/机器学习
       - Python开发
       - JavaScript/Web开发
       - 开发工具
       - 设计/UI
       - 其他（用户自定义）
     - 用户选择一个领域
   
   - 2.2. 获取热门仓库列表
     ```bash
     python scripts/get_trending_repos.py --language <领域关键词> --limit 3
     ```
     - 根据领域筛选热门仓库
     - 返回3个仓库的基本信息
   
   - 2.3. 逐个深度分析推荐仓库
     - 对每个推荐的仓库，调用 `get_github_repo.py` 获取详细信息
     - 生成与分支A相同的深度解读报告
     - 按热度排序展示3个仓库的完整分析

### 可选分支

- **AI/机器学习项目的GPU/CPU适配**：
  - 询问用户："你的电脑有NVIDIA显卡（GPU）吗？"
  - 如果有GPU → 提供GPU版本完整教程（CUDA安装、GPU版PyTorch/TensorFlow）
  - 如果无GPU → 提供CPU版本教程，并说明性能预期（较慢但可用）
  - 如果仓库**必须GPU** → 友好提示并推荐云端GPU方案：
    - 学习/测试：Google Colab（免费）
    - 短期项目：AutoDL/恒源云（0.5-1元/小时）
    - 长期项目：云服务商GPU实例

- **根据项目类型提供差异化指导**：
  - **AI/机器学习项目**：
    - GPU/CPU检测方法
    - CPU版本安装教程（无GPU用户）
    - GPU版本完整教程（有GPU用户，含CUDA配置）
    - 预训练模型下载
    - 训练/推理示例代码
  - **Web前端项目**：
    - Node.js安装
    - npm/yarn依赖安装
    - 开发服务器启动
  - **后端/API项目**：
    - 环境变量配置
    - 数据库初始化
    - API服务启动
  - **工具/CLI项目**：
    - 全局安装步骤
    - 命令行使用示例
    - 编译配置（如需）

## 资源索引

- **必要脚本**：
  - [scripts/get_github_repo.py](scripts/get_github_repo.py) - 获取GitHub仓库详细信息（参数：`owner/repo` 格式的仓库名称）
  - [scripts/get_trending_repos.py](scripts/get_trending_repos.py) - 获取热门仓库列表（参数：`--language` 领域, `--limit` 数量）
- **保姆级使用指南**：
  - [references/github-usage-guide.md](references/github-usage-guide.md) - 从零开始的完整本地使用教程，包含：
    - 通用前置步骤（Git安装、仓库克隆）
    - **第零步：GPU/CPU适配说明**
      - 检测电脑是否有GPU的方法（Windows/macOS/Linux）
      - GPU vs CPU性能对比（10-100倍差距）
      - 判断仓库GPU要求的方法
      - CPU版本和GPU版本的安装教程
    - AI/机器学习项目完整流程
    - Web前端项目配置与运行
    - 后端/API项目部署
    - 工具/CLI项目安装使用
    - 桌面应用配置
    - **云端GPU替代方案**
      - Google Colab（免费）
      - Kaggle Notebooks（免费）
      - 国内平台（AutoDL、恒源云等）
      - 云服务商（GCP、AWS、Azure）
    - 常见问题解决方案（CPU慢、内存不足、CUDA不匹配等）

## 注意事项

- **速率限制**：GitHub公共API限制60次/小时，建议用户提供token提升限额
- **仓库权限**：仅能访问公开仓库
- **多仓库分析**：分支B模式下，避免一次性分析过多仓库，建议限制在3个以内
- **智能体角色**：脚本只负责数据获取，解读报告由智能体基于理解能力生成
- **错误处理**：
  - 仓库名称格式错误时，提示正确格式
  - 仓库不存在时，建议检查名称
  - API限流时，建议稍后重试或提供token

## 使用示例

### 示例1：分析指定仓库
```
用户：帮我分析一下 openai/gpt 这个仓库

执行流程：
1. 调用 get_github_repo.py openai/gpt
2. 分析返回的数据
3. 生成报告：OpenAI的GPT实现，用于大语言模型研究，主要使用Python...
```

### 示例2：推荐并分析AI领域热门仓库
```
用户：我对AI领域感兴趣，推荐一些项目

执行流程：
1. 询问领域选择（用户选择"AI"）
2. 调用 get_trending_repos.py --language machine-learning --limit 3
3. 对返回的3个仓库逐个调用 get_github_repo.py
4. 生成3个仓库的深度分析报告
```

### 示例3：分析Web开发工具
```
用户：我想找一个好用的Web开发工具

执行流程：
1. 调用 get_trending_repos.py --language javascript --limit 3
2. 分析每个仓库的用途
3. 重点生成工具的安装和使用指南
```
