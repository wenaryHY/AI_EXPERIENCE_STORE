#!/usr/bin/env python3
"""
System Prompt Exporter

Exports system rules as a single JSON block that can be copied
to ANY AI model (ChatGPT, Claude, Gemini, etc.)

Cross-platform support: macOS, Windows, Linux

Usage:
  python scripts/export_system_prompt.py          # Print to stdout
  python scripts/export_system_prompt.py --copy   # Copy to clipboard
  python scripts/export_system_prompt.py --file   # Save to generated/system_prompt.txt
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path


SYSTEM_RULES_FILE = "system_rules.json"
OUTPUT_FILE = "generated/system_prompt.txt"


def get_script_dir() -> Path:
    """Get the directory where this script is located."""
    return Path(__file__).parent.resolve()


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return get_script_dir().parent


def load_system_rules() -> dict:
    """Load system rules from JSON file."""
    # Try relative to repo root first
    repo_root = get_repo_root()
    rules_path = repo_root / SYSTEM_RULES_FILE
    
    if not rules_path.exists():
        # Try current directory
        rules_path = Path(SYSTEM_RULES_FILE)
    
    if not rules_path.exists():
        print(f"❌ {SYSTEM_RULES_FILE} not found")
        sys.exit(1)
    
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_for_ai(rules: dict) -> str:
    """Format rules as compact JSON for AI consumption."""
    return json.dumps(rules, ensure_ascii=False, separators=(',', ':'))


def copy_to_clipboard(text: str) -> bool:
    """
    Copy text to clipboard.
    Cross-platform: macOS, Windows, Linux
    """
    system = platform.system()
    
    try:
        if system == "Darwin":  # macOS
            process = subprocess.Popen(
                ['pbcopy'],
                stdin=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            process.communicate(text.encode('utf-8'))
            return process.returncode == 0
            
        elif system == "Windows":
            process = subprocess.Popen(
                ['clip'],
                stdin=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                shell=True
            )
            process.communicate(text.encode('utf-16'))
            return process.returncode == 0
            
        elif system == "Linux":
            # Try xclip first, then xsel
            for cmd in [['xclip', '-selection', 'clipboard'], ['xsel', '--clipboard', '--input']]:
                try:
                    process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.DEVNULL
                    )
                    process.communicate(text.encode('utf-8'))
                    if process.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
            
            print("⚠️  Linux clipboard requires 'xclip' or 'xsel'")
            print("   Install: sudo apt install xclip  OR  sudo apt install xsel")
            return False
        else:
            print(f"⚠️  Clipboard not supported on {system}")
            return False
            
    except Exception as e:
        print(f"⚠️  Clipboard error: {e}")
        return False


def main():
    rules = load_system_rules()
    prompt = format_for_ai(rules)
    
    if "--copy" in sys.argv:
        if copy_to_clipboard(prompt):
            print("✅ System prompt copied to clipboard!")
            print(f"   Length: {len(prompt)} chars")
            print(f"   Platform: {platform.system()}")
        else:
            print("❌ Failed to copy to clipboard, printing instead:")
            print()
            print(prompt)
    
    elif "--file" in sys.argv:
        repo_root = get_repo_root()
        output_path = repo_root / OUTPUT_FILE
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✅ Saved to {output_path}")
        print(f"   Length: {len(prompt)} chars")
    
    else:
        print("=" * 60)
        print("📋 COPY THIS TO ANY AI MODEL:")
        print("=" * 60)
        print()
        print(prompt)
        print()
        print("=" * 60)
        print(f"Length: {len(prompt)} chars")
        print()
        print("💡 Tips:")
        print("   --copy  : Copy to clipboard")
        print("   --file  : Save to file")


if __name__ == "__main__":
    main()
