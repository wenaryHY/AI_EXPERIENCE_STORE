#!/usr/bin/env python3
"""
Experience Document Generator

AI 可以调用此脚本生成新的经验文档。
用法: python scripts/generate_experience.py --task_id TASK001 --module core --summary "任务摘要"
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


# Configuration
OUTPUT_DIR = "generated/experiences"


def generate_experience_doc(
    task_id: str,
    module: str,
    summary: str,
    conversation_ctx: str = "",
    decisions: Optional[List[str]] = None,
    lessons: Optional[List[str]] = None,
    auto_push: bool = False
) -> Path:
    """
    生成经验文档并保存到文件。
    
    Args:
        task_id: 任务ID
        module: 模块名称
        summary: 任务摘要
        conversation_ctx: 对话上下文
        decisions: 关键决策列表
        lessons: 经验教训列表
        auto_push: 是否自动推送到 GitHub
        
    Returns:
        生成的文件路径
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d%H%M")
    
    doc = {
        "task_id": task_id,
        "module": module,
        "conversation_ctx": conversation_ctx or f"Task {task_id} completed",
        "generated_by": "Cursor",
        "summary": summary,
        "decisions": decisions or [],
        "lessons": lessons or [],
        "created_at": now.isoformat(),
        "branch": f"task-{task_id}",
        "merged": False
    }
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = f"exp_{module}_{task_id}_{timestamp}.json"
    output_path = output_dir / filename
    
    # Save document
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 经验文档已生成: {output_path}")
    
    # Auto push if requested
    if auto_push:
        push_to_github(task_id)
    
    return output_path


def push_to_github(task_id: str) -> bool:
    """推送变更到 GitHub。"""
    try:
        # Get repo root
        repo_root = Path(__file__).parent.parent
        
        # Git commands
        subprocess.run(["git", "add", "generated/"], cwd=repo_root, check=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        commit_msg = f"Add/Update exp {task_id} {timestamp}"
        
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_root, check=True)
        subprocess.run(["git", "push", "origin", "HEAD"], cwd=repo_root, check=True)
        
        print(f"📤 已推送到 GitHub: {commit_msg}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 推送失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="生成经验文档")
    parser.add_argument("--task_id", required=True, help="任务ID")
    parser.add_argument("--module", required=True, help="模块名称")
    parser.add_argument("--summary", required=True, help="任务摘要")
    parser.add_argument("--ctx", default="", help="对话上下文")
    parser.add_argument("--decisions", nargs="*", default=[], help="关键决策")
    parser.add_argument("--lessons", nargs="*", default=[], help="经验教训")
    parser.add_argument("--push", action="store_true", help="自动推送到 GitHub")
    
    args = parser.parse_args()
    
    generate_experience_doc(
        task_id=args.task_id,
        module=args.module,
        summary=args.summary,
        conversation_ctx=args.ctx,
        decisions=args.decisions,
        lessons=args.lessons,
        auto_push=args.push
    )


if __name__ == "__main__":
    main()

