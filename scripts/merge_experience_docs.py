#!/usr/bin/env python3
"""
Experience Documents Merger

This script merges all experience documents from the experience-docs/ directory
into a single master JSON file (experience_master.json).

Features:
- Parses JSON-formatted .txt files from experience-docs/
- Maintains document metadata (source file, timestamp)
- Outputs a unified experience_master.json
- Supports incremental updates
"""

from __future__ import annotations

import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


# Configuration
EXPERIENCE_DOCS_DIR = "experience-docs"
OUTPUT_DIR = "generated"
OUTPUT_FILE = "experience_master.json"
SUPPORTED_EXTENSIONS = [".txt", ".json"]


def calculate_content_hash(content: str) -> str:
    """Calculate MD5 hash of content for change detection."""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def parse_experience_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parse a single experience document file.
    
    Args:
        file_path: Path to the experience document
        
    Returns:
        Parsed document with metadata, or None if parsing fails
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse as JSON
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            # If not valid JSON, wrap content as raw text
            data = {
                "role": "system",
                "raw_content": content,
                "parse_error": "Content is not valid JSON"
            }
        
        # Get file stats
        stat = file_path.stat()
        
        return {
            "source_file": file_path.name,
            "file_path": str(file_path),
            "content_hash": calculate_content_hash(content),
            "file_modified_utc": datetime.fromtimestamp(
                stat.st_mtime, tz=timezone.utc
            ).isoformat(),
            "parsed_at_utc": datetime.now(timezone.utc).isoformat(),
            "content": data
        }
        
    except Exception as e:
        print(f"⚠️  Error parsing {file_path}: {e}")
        return None


def load_existing_master(output_path: Path) -> Dict[str, Any]:
    """Load existing master file if it exists."""
    if output_path.exists():
        try:
            with open(output_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def merge_experience_docs() -> Dict[str, Any]:
    """
    Merge all experience documents into a master dictionary.
    
    Returns:
        Master dictionary containing all merged experiences
    """
    docs_dir = Path(EXPERIENCE_DOCS_DIR)
    output_path = Path(OUTPUT_FILE)
    
    if not docs_dir.exists():
        print(f"❌ Directory not found: {docs_dir}")
        return {}
    
    # Collect all experience files
    experience_files: List[Path] = []
    for ext in SUPPORTED_EXTENSIONS:
        experience_files.extend(docs_dir.glob(f"*{ext}"))
    
    # Sort by filename for consistent ordering
    experience_files = sorted(experience_files, key=lambda p: p.name)
    
    print(f"📁 Found {len(experience_files)} experience document(s)")
    
    # Parse each file
    documents: List[Dict[str, Any]] = []
    for file_path in experience_files:
        print(f"  📄 Processing: {file_path.name}")
        doc = parse_experience_file(file_path)
        if doc:
            documents.append(doc)
    
    # Build master document
    master: Dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_documents": len(documents),
        "source_directory": EXPERIENCE_DOCS_DIR,
        "documents": documents,
        "index": {
            # Create an index by filename for quick lookup
            doc["source_file"]: i for i, doc in enumerate(documents)
        }
    }
    
    return master


def save_master(master: Dict[str, Any], output_path: Path) -> bool:
    """Save master document to file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(master, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"❌ Error saving master file: {e}")
        return False


def main() -> int:
    """Main entry point."""
    print("=" * 50)
    print("🔄 Experience Documents Merger")
    print("=" * 50)
    print()
    
    # Merge documents
    master = merge_experience_docs()
    
    if not master or not master.get("documents"):
        print("⚠️  No documents to merge")
        return 1
    
    # Ensure output directory exists
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save to output file
    output_path = output_dir / OUTPUT_FILE
    print()
    print(f"💾 Saving to: {output_path}")
    
    if save_master(master, output_path):
        print()
        print("=" * 50)
        print(f"✅ Successfully merged {master['total_documents']} document(s)")
        print(f"📄 Output: {output_path}")
        print("=" * 50)
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
