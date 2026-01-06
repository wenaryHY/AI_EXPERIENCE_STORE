#!/usr/bin/env python3
"""
Experience Document Push Script

Cross-platform push script for experience documents.
Works on macOS, Windows, and Linux.

Usage:
  python scripts/push_experience.py                    # Auto detect changes
  python scripts/push_experience.py TASK001           # With task ID
  python scripts/push_experience.py TASK001 "message" # With custom message
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path


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


def has_changes(repo_root: Path) -> bool:
    """Check if there are changes in generated/ directory."""
    # Check for modified files
    success, output = run_git(['diff', '--quiet', 'generated/'], repo_root)
    if not success and "generated/" in output or not success and output == "":
        return True
    
    # Check for untracked files
    success, output = run_git(
        ['ls-files', '--others', '--exclude-standard', 'generated/'],
        repo_root
    )
    if success and output.strip():
        return True
    
    return False


def get_changes(repo_root: Path) -> str:
    """Get list of changes in generated/ directory."""
    success, output = run_git(['status', '--short', 'generated/'], repo_root)
    return output if success else ""


def main():
    print("=" * 50)
    print("🚀 Experience Document Push Script")
    print("=" * 50)
    print()
    
    repo_root = get_repo_root()
    
    # Parse arguments
    task_id = sys.argv[1] if len(sys.argv) > 1 else "auto"
    custom_message = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check for changes
    if not has_changes(repo_root):
        print("ℹ️  No changes detected in generated/ directory")
        return 0
    
    # Show changes
    print("📝 Changes detected:")
    changes = get_changes(repo_root)
    print(changes)
    
    # Build commit message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    if custom_message:
        commit_msg = custom_message
    else:
        commit_msg = f"Add/Update exp {task_id} {timestamp}"
    
    # Git add
    print("💾 Staging changes...")
    success, output = run_git(['add', 'generated/'], repo_root)
    if not success:
        print(f"❌ Failed to stage: {output}")
        return 1
    
    # Git commit
    print("📦 Committing...")
    success, output = run_git(['commit', '-m', commit_msg], repo_root)
    if not success:
        if "nothing to commit" in output:
            print("ℹ️  Nothing to commit")
            return 0
        print(f"❌ Failed to commit: {output}")
        return 1
    
    # Git push
    print("📤 Pushing to remote...")
    success, output = run_git(['push', 'origin', 'HEAD'], repo_root)
    if not success:
        print(f"❌ Failed to push: {output}")
        print()
        print("💡 Tips:")
        print("   - Check your network connection")
        print("   - Verify remote is configured: git remote -v")
        print("   - Ensure you have push permission")
        return 1
    
    print()
    print("=" * 50)
    print("✅ Push successful!")
    print(f"   Message: {commit_msg}")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(main())

