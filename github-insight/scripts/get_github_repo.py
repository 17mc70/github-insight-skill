#!/usr/bin/env python3
"""
获取GitHub仓库详细信息
使用GitHub官方REST API获取仓库元数据、README、编程语言等信息
"""

import os
import sys
import base64
import json
from coze_workload_identity import requests


def get_github_repo(repo_name: str, token: str = None) -> dict:
    """
    获取GitHub仓库的详细信息
    
    参数:
        repo_name: 仓库名称，格式为 "owner/repo" (如 "openai/gpt")
        token: GitHub Personal Access Token (可选，提高API速率限制)
    
    返回:
        包含仓库详细信息的字典:
        {
            "basic_info": { ... },  # 基本信息
            "readme": "...",        # README内容
            "languages": {...},     # 编程语言统计
            "topics": [...]          # 仓库标签
        }
    """
    owner, repo = parse_repo_name(repo_name)
    
    # 构建请求头
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    # 1. 获取仓库基本信息
    basic_info = get_repo_info(owner, repo, headers)
    if not basic_info:
        raise Exception(f"无法获取仓库 {repo_name} 的信息")
    
    # 2. 获取README内容
    readme_content = get_readme(owner, repo, headers)
    
    # 3. 获取编程语言统计
    languages = get_languages(owner, repo, headers)
    
    # 4. 组装结果
    result = {
        "basic_info": {
            "name": basic_info.get("name"),
            "full_name": basic_info.get("full_name"),
            "description": basic_info.get("description"),
            "owner": basic_info.get("owner", {}).get("login"),
            "url": basic_info.get("html_url"),
            "homepage": basic_info.get("homepage"),
            "stars": basic_info.get("stargazers_count"),
            "forks": basic_info.get("forks_count"),
            "watchers": basic_info.get("watchers_count"),
            "open_issues": basic_info.get("open_issues_count"),
            "created_at": basic_info.get("created_at"),
            "updated_at": basic_info.get("updated_at"),
            "language": basic_info.get("language"),
            "license": basic_info.get("license", {}).get("name") if basic_info.get("license") else None,
            "is_fork": basic_info.get("fork"),
            "size": basic_info.get("size"),
        },
        "readme": readme_content,
        "languages": languages,
        "topics": basic_info.get("topics", [])
    }
    
    return result


def parse_repo_name(repo_name: str) -> tuple:
    """
    解析仓库名称
    
    参数:
        repo_name: 仓库名称，可以是 "owner/repo" 或完整URL
    
    返回:
        (owner, repo) 元组
    """
    # 移除可能的 GitHub URL 前缀
    repo_name = repo_name.replace("https://github.com/", "")
    repo_name = repo_name.replace("http://github.com/", "")
    repo_name = repo_name.rstrip("/")
    
    # 解析 owner/repo
    parts = repo_name.split("/")
    if len(parts) != 2:
        raise ValueError(f"无效的仓库名称格式: {repo_name}。应为 'owner/repo' 格式")
    
    return parts[0], parts[1]


def get_repo_info(owner: str, repo: str, headers: dict) -> dict:
    """获取仓库基本信息"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 404:
        raise Exception(f"仓库 {owner}/{repo} 不存在或无权访问")
    elif response.status_code == 403:
        raise Exception("API速率限制已超限，请提供GitHub token以提高限额")
    elif response.status_code != 200:
        raise Exception(f"获取仓库信息失败: HTTP {response.status_code}")
    
    return response.json()


def get_readme(owner: str, repo: str, headers: dict) -> str:
    """获取README内容"""
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 404:
        return "该仓库没有README文件"
    elif response.status_code != 200:
        return "获取README失败"
    
    data = response.json()
    
    # 解码base64内容
    content = data.get("content", "")
    try:
        decoded_content = base64.b64decode(content).decode("utf-8")
        return decoded_content
    except Exception:
        return "README解码失败"


def get_languages(owner: str, repo: str, headers: dict) -> dict:
    """获取编程语言统计"""
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code != 200:
        return {}
    
    return response.json()


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python get_github_repo.py <owner/repo> [github_token]")
        print("示例: python get_github_repo.py openai/gpt")
        print("示例: python get_github_repo.py openai/gpt ghp_xxx")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    token = sys.argv[2] if len(sys.argv) > 2 else os.getenv("GITHUB_TOKEN")
    
    try:
        result = get_github_repo(repo_name, token)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
