#!/usr/bin/env python3
"""
获取GitHub热门仓库
从GitHub Trending页面爬取热门仓库信息
"""

import re
import json
from coze_workload_identity import requests
from bs4 import BeautifulSoup


def get_trending_repos(language: str = "", period: str = "daily", limit: int = 10) -> list:
    """
    获取GitHub热门仓库
    
    参数:
        language: 编程语言或领域筛选 (如 "python", "javascript", "machine-learning")
        period: 时间周期 ("daily" 今日, "weekly" 本周, "monthly" 本月)
        limit: 返回的仓库数量
    
    返回:
        热门仓库列表，每个仓库包含:
        {
            "name": "owner/repo",
            "description": "...",
            "stars": "...",
            "forks": "...",
            "url": "...",
            "language": "...",
            "stars_today": "..."
        }
    """
    # 构建trending页面URL
    base_url = "https://github.com/trending"
    params = {}
    
    # 处理语言参数（GitHub使用连字符分隔，如 machine-learning）
    if language:
        language = language.lower().replace(" ", "-")
        params["language"] = language
    
    # 处理时间周期
    if period == "daily":
        params["since"] = "daily"
    elif period == "weekly":
        params["since"] = "weekly"
    elif period == "monthly":
        params["since"] = "monthly"
    
    # 设置请求头模拟浏览器
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        raise Exception(f"获取GitHub Trending失败: {str(e)}")
    
    # 解析HTML
    soup = BeautifulSoup(response.text, "html.parser")
    repos = []
    
    # 查找所有仓库条目
    repo_articles = soup.find_all("article", class_="Box-row")
    
    for article in repo_articles[:limit]:
        try:
            repo_info = extract_repo_info(article)
            if repo_info:
                repos.append(repo_info)
        except Exception as e:
            # 跳过解析失败的仓库
            continue
    
    return repos


def extract_repo_info(article) -> dict:
    """
    从HTML元素中提取仓库信息
    
    参数:
        article: BeautifulSoup元素
    
    返回:
        仓库信息字典
    """
    # 获取仓库名称和链接
    title_link = article.find("h2", class_="h3").find("a")
    if not title_link:
        return None
    
    href = title_link.get("href", "")
    name = href.lstrip("/")
    
    # 获取描述
    description_elem = article.find("p", class_="col-9")
    description = description_elem.get_text(strip=True) if description_elem else ""
    
    # 获取语言
    language_elem = article.find("span", itemprop="programmingLanguage")
    language = language_elem.get_text(strip=True) if language_elem else ""
    
    # 获取星标数
    stars_link = article.find("a", href=re.compile(r"/stargazers"))
    stars = stars_link.get_text(strip=True) if stars_link else "0"
    
    # 获取fork数
    forks_link = article.find("a", href=re.compile(r"/forks"))
    forks = forks_link.get_text(strip=True) if forks_link else "0"
    
    # 获取今日星标数
    stars_today_elem = article.find("span", class_="d-inline-block float-sm-right")
    stars_today = ""
    if stars_today_elem:
        stars_today_text = stars_today_elem.get_text(strip=True)
        # 提取数字，如 "1,234 stars today" -> "1,234"
        match = re.search(r"[\d,]+", stars_today_text)
        if match:
            stars_today = match.group()
    
    return {
        "name": name,
        "description": description,
        "stars": stars,
        "forks": forks,
        "url": f"https://github.com{name}",
        "language": language,
        "stars_today": stars_today
    }


def suggest_repos_by_category(category: str, limit: int = 10) -> list:
    """
    根据类别推荐仓库
    
    参数:
        category: 类别名称 (如 "LLM", "AI", "设计", "开发工具")
        limit: 返回数量
    
    返回:
        热门仓库列表
    """
    # 类别到编程语言/关键字的映射
    category_mapping = {
        "LLM": "machine-learning",
        "大模型": "machine-learning",
        "AI": "machine-learning",
        "人工智能": "machine-learning",
        "python": "python",
        "javascript": "javascript",
        "设计": "design",
        "开发工具": "development",
        "web": "web",
        "前端": "javascript",
        "后端": "python",
    }
    
    # 查找匹配的语言
    language = category_mapping.get(category.lower(), "")
    
    return get_trending_repos(language=language, limit=limit)


def list_available_categories() -> list:
    """
    列出可用的类别
    
    返回:
        类别列表
    """
    return [
        {"name": "LLM", "desc": "大语言模型相关"},
        {"name": "AI", "desc": "人工智能与机器学习"},
        {"name": "Python", "desc": "Python编程语言"},
        {"name": "JavaScript", "desc": "JavaScript/前端开发"},
        {"name": "Web", "desc": "Web开发"},
        {"name": "开发工具", "desc": "开发者工具"},
        {"name": "设计", "desc": "设计与UI"},
    ]


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="获取GitHub热门仓库")
    parser.add_argument("--language", "-l", help="编程语言或领域", default="")
    parser.add_argument("--period", "-p", choices=["daily", "weekly", "monthly"], 
                        default="daily", help="时间周期")
    parser.add_argument("--limit", "-n", type=int, default=10, help="返回数量")
    parser.add_argument("--list-categories", action="store_true", help="列出可用类别")
    
    args = parser.parse_args()
    
    if args.list_categories:
        categories = list_available_categories()
        print("可用类别:")
        for cat in categories:
            print(f"  - {cat['name']}: {cat['desc']}")
        return
    
    try:
        repos = get_trending_repos(
            language=args.language,
            period=args.period,
            limit=args.limit
        )
        print(json.dumps(repos, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
