#!/usr/bin/env python3
"""
System Prompt Exporter

Exports system rules as a single JSON block that can be copied
to ANY AI model (ChatGPT, Claude, Gemini, etc.)

Usage:
  python scripts/export_system_prompt.py          # Print to stdout
  python scripts/export_system_prompt.py --copy   # Copy to clipboard (macOS)
  python scripts/export_system_prompt.py --file   # Save to generated/system_prompt.txt
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SYSTEM_RULES_FILE = "system_rules.json"
OUTPUT_FILE = "generated/system_prompt.txt"


def load_system_rules() -> dict:
    """Load system rules from JSON file."""
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
    """Copy text to clipboard (macOS)."""
    try:
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception:
        return False


def main():
    rules = load_system_rules()
    prompt = format_for_ai(rules)
    
    if "--copy" in sys.argv:
        if copy_to_clipboard(prompt):
            print("✅ System prompt copied to clipboard!")
            print(f"   Length: {len(prompt)} chars")
        else:
            print("❌ Failed to copy to clipboard")
            print(prompt)
    
    elif "--file" in sys.argv:
        output_path = Path(OUTPUT_FILE)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✅ Saved to {OUTPUT_FILE}")
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


if __name__ == "__main__":
    main()

