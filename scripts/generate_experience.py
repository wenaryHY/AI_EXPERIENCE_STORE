#!/usr/bin/env python3
"""
Experience Document Generator

Cross-platform experience document generator.
Works on macOS, Windows, and Linux.

Usage:
  python scripts/generate_experience.py --task_id TASK001 --module core --summary "Task summary"
  python scripts/generate_experience.py --task_id TASK001 --module core --summary "Summary" --push
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


# Configuration
OUTPUT_DIR = "generated/experiences"


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent.resolve()


def run_git(args: list, cwd: Path) -> tuple[bool, str]:
    """
    Run a git command and return (success, output).
    Cross-platform compatible.
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout + result.stderr
    except FileNotFoundError:
        return False, "Git not found. Please install git."
    except Exception as e:
        return False, str(e)


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
    Generate an experience document and save to file.
    
    Args:
        task_id: Task ID
        module: Module name
        summary: Task summary
        conversation_ctx: Conversation context
        decisions: List of key decisions
        lessons: List of lessons learned
        auto_push: Whether to auto-push to GitHub
        
    Returns:
        Path to generated file
    """
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d%H%M")
    
    doc = {
        "task_id": task_id,
        "module": module,
        "conversation_ctx": conversation_ctx or f"Task {task_id} completed",
        "generated_by": "AI",
        "summary": summary,
        "decisions": decisions or [],
        "lessons": lessons or [],
        "created_at": now.isoformat(),
        "branch": f"task-{task_id}",
        "merged": False
    }
    
    # Ensure output directory exists (cross-platform)
    repo_root = get_repo_root()
    output_dir = repo_root / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    filename = f"exp_{module}_{task_id}_{timestamp}.json"
    output_path = output_dir / filename
    
    # Save document with UTF-8 encoding (cross-platform)
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Experience doc generated: {output_path}")
    
    # Auto push if requested
    if auto_push:
        push_to_github(task_id, repo_root)
    
    return output_path


def push_to_github(task_id: str, repo_root: Path) -> bool:
    """Push changes to GitHub."""
    print()
    print("📤 Pushing to GitHub...")
    
    # Git add
    success, output = run_git(['add', 'generated/'], repo_root)
    if not success:
        print(f"❌ Failed to stage: {output}")
        return False
    
    # Git commit
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    commit_msg = f"Add/Update exp {task_id} {timestamp}"
    
    success, output = run_git(['commit', '-m', commit_msg], repo_root)
    if not success:
        if "nothing to commit" in output:
            print("ℹ️  Nothing to commit")
            return True
        print(f"❌ Failed to commit: {output}")
        return False
    
    # Git push
    success, output = run_git(['push', 'origin', 'HEAD'], repo_root)
    if not success:
        print(f"❌ Failed to push: {output}")
        return False
    
    print(f"✅ Pushed to GitHub: {commit_msg}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate experience document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/generate_experience.py --task_id TASK001 --module core --summary "Completed feature X"
  python scripts/generate_experience.py --task_id TASK001 --module api --summary "Fixed bug" --push
  python scripts/generate_experience.py --task_id TASK001 --module ui --summary "Added button" --decisions "Used React" --lessons "Test early"
        """
    )
    parser.add_argument("--task_id", required=True, help="Task ID")
    parser.add_argument("--module", required=True, help="Module name")
    parser.add_argument("--summary", required=True, help="Task summary")
    parser.add_argument("--ctx", default="", help="Conversation context")
    parser.add_argument("--decisions", nargs="*", default=[], help="Key decisions")
    parser.add_argument("--lessons", nargs="*", default=[], help="Lessons learned")
    parser.add_argument("--push", action="store_true", help="Auto push to GitHub")
    
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
