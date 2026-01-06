# AI Experience Store

[中文文档](README_CN.md)

Universal AI experience management workflow. Works with **ANY AI model** (ChatGPT, Claude, Gemini, Cursor, etc.)

## Directory Structure

```
AI_FLOW/
├── system_rules.json              # 🤖 Universal AI rules (JSON, English)
├── experience-docs/               # 📝 Rule templates (reference only)
├── generated/
│   ├── experience_master.json     # Merged experience docs
│   └── experiences/               # AI-generated experience files
├── scripts/
│   ├── merge_experience_docs.py   # Merge all docs
│   ├── generate_experience.py     # Generate new exp doc
│   ├── export_system_prompt.py    # Export rules for any AI
│   └── push_experience.sh         # Quick push script
├── .cursorrules                   # Cursor-specific (auto-read)
└── .github/workflows/
    └── auto-update-experience-docs.yml
```

## Quick Start

### 1. Export Rules for Any AI

```bash
# Print to terminal (copy manually)
python scripts/export_system_prompt.py

# Copy to clipboard (macOS)
python scripts/export_system_prompt.py --copy

# Save to file
python scripts/export_system_prompt.py --file
```

Then paste the output to **any AI model** as system prompt.

### 2. AI Generates Experience Doc

After AI completes a task:

```bash
python scripts/generate_experience.py \
  --task_id TASK001 \
  --module core \
  --summary "Completed feature X" \
  --decisions "Used approach A" \
  --lessons "Consider edge cases early" \
  --push  # Auto push to GitHub
```

### 3. Auto Workflow

When you push changes to `experience-docs/`, GitHub Actions will:
1. Merge all docs into `experience_master.json`
2. Create a timestamped branch
3. Create PR for review

## System Rules Format

`system_rules.json` - Compact JSON that AI can parse:

```json
{
  "agent_config": { "mode": "ENGINEERING_LONG_TERMISM", "lang": "zh-CN" },
  "priorities": ["problem_understanding > implementation", ...],
  "code_rules": ["delete > add", "reuse > create", ...],
  "exp_doc_rules": { "file_pattern": "exp_{module}_{taskid}_{ts}.json", ... }
}
```

## Universal Usage

| AI Model | How to Load Rules |
|----------|------------------|
| **ChatGPT** | Paste `system_rules.json` content as system message |
| **Claude** | Paste as first message or use Projects |
| **Gemini** | Paste as system instruction |
| **Cursor** | Auto-reads `.cursorrules` file |
| **Other** | Paste JSON as initial context |

## Commands

```bash
# Export rules for any AI
python scripts/export_system_prompt.py --copy

# Generate experience doc
python scripts/generate_experience.py --task_id X --module Y --summary "Z"

# Merge all experience docs
python scripts/merge_experience_docs.py

# Quick push
./scripts/push_experience.sh TASK_ID
```

## License

MIT
