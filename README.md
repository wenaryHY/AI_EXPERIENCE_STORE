# AI Experience Store

[中文文档](README_CN.md)

Universal AI experience management workflow. Works with **ANY AI model** (ChatGPT, Claude, Gemini, Cursor, etc.)

**Cross-platform**: macOS, Windows, Linux

---

## Workflow Overview

| Step | Action | Command | Output |
|------|--------|---------|--------|
| 1️⃣ | Export rules | `python scripts/export_system_prompt.py --copy` | JSON copied to clipboard |
| 2️⃣ | Load to AI | Paste JSON to any AI model | AI understands your rules |
| 3️⃣ | AI works | AI completes your task | Task completed with experience |
| 4️⃣ | Generate doc | `python scripts/generate_experience.py --task_id X --module Y --summary "Z"` | JSON file in `generated/experiences/` |
| 5️⃣ | Push | `python scripts/push_experience.py` | Changes pushed to GitHub |
| 6️⃣ | Auto merge | GitHub Actions triggered | PR created automatically |

---

## Core Principles (AI Must Follow)

| Principle | Rule | AI Behavior |
|-----------|------|-------------|
| **Problem First** | prob > impl | Clarify problem before implementation |
| **Best Code** | del > reuse > add | Deletion first, every line is debt |
| **Scale as Contract** | obs_is_contract | Bugs are API, deprecate ≠ delete |
| **Innovation Token** | expensive | Default to boring mature solutions |
| **Abstraction Failure** | delay_not_remove | Assume you're on-call at 3am alone |
| **Social System** | cons > indiv | Winning argument may lose project |
| **Metrics in Pairs** | pair | Speed vs quality, watch trends |
| **Long-term Compound** | time_non_renew | Crystallize experience into rules |
| **Red Lines** | f | No unnecessary complexity |

---

## Use Cases & Examples

### Case 1: First-time Setup with ChatGPT

| Item | Content |
|------|---------|
| **Scenario** | Configure ChatGPT to follow engineering principles |
| **Steps** | 1. Run `python scripts/export_system_prompt.py --copy`<br>2. Open ChatGPT → Settings → Custom Instructions<br>3. Paste the JSON |
| **Preset Prompt** | *(Paste the exported JSON, then say)*<br>`Follow these rules for all conversations.` |
| **Expected Result** | ChatGPT will:<br>- Reply in Chinese by default<br>- Ask "should we do this" before "how to do"<br>- Prefer delete/reuse over new code<br>- Choose boring but reliable tech<br>- Generate experience doc after task |

### Case 2: Code Review with Claude

| Item | Content |
|------|---------|
| **Scenario** | Claude reviews code following quality rules |
| **Steps** | 1. Export rules: `python scripts/export_system_prompt.py --copy`<br>2. Start new Claude conversation<br>3. Paste JSON first, then code |
| **Preset Prompt** | ```[Paste JSON]```<br><br>`Review this code following the rules above:`<br>```python`<br>`def process_data(data):`<br>`    # your code`<br>``` |
| **Expected Result** | Claude will:<br>- Ask "is this feature really needed?"<br>- Suggest removing redundant code first<br>- Flag "future maybe" code for deletion<br>- Check for reusable existing modules<br>- Prioritize readability over cleverness<br>- Warn about contract-breaking changes |

### Case 3: Bug Fix Documentation

| Item | Content |
|------|---------|
| **Scenario** | Record experience after fixing critical bug |
| **Steps** | After fixing bug, run generate command |
| **Command** | ```bash<br>python scripts/generate_experience.py \<br>  --task_id BUG042 \<br>  --module auth \<br>  --summary "Fixed JWT token expiration refresh" \<br>  --decisions "Sliding window refresh" "Token blacklist" \<br>  --lessons "Check token lifecycle" "Add auth integration tests" \<br>  --push<br>``` |
| **Expected Result** | File: `generated/experiences/exp_auth_BUG042_202601061200.json`<br>Auto-pushed to GitHub<br>Experience crystallized as reusable knowledge |

### Case 4: Feature Development with Cursor

| Item | Content |
|------|---------|
| **Scenario** | Develop new feature in Cursor IDE |
| **Steps** | 1. Open project in Cursor (auto-reads `.cursorrules`)<br>2. Describe feature to AI<br>3. AI follows rules automatically |
| **Preset Prompt** | `Add user notification system with email and push support.` |
| **Expected Result** | Cursor AI will:<br>- Ask "what user pain point does this solve?"<br>- Ask "what happens if we don't do this?"<br>- Check for existing reusable solutions<br>- Choose mature notification library<br>- Avoid over-engineering and tech zoo<br>- Remind to generate experience doc |

### Case 5: Architecture Decision with Gemini

| Item | Content |
|------|---------|
| **Scenario** | Discuss architecture options with Gemini |
| **Steps** | 1. Export rules and paste to Gemini<br>2. Describe architecture question |
| **Preset Prompt** | ```[Paste JSON]```<br><br>`Choose between microservices and monolith for e-commerce. 3 developers, 10k daily users initially. Analyze per engineering principles.` |
| **Expected Result** | Gemini will:<br>- Recommend boring reliable option (innovation token)<br>- Consider 3-person on-call capacity (abstraction failure)<br>- Focus on team alignment over tech perfection (social)<br>- Warn architecture choice becomes contract (scale)<br>- Provide paired metrics (dev speed vs ops complexity)<br>- Suggest documenting decision as experience |

### Case 6: Batch Experience Merge

| Item | Content |
|------|---------|
| **Scenario** | Merge all experience templates into master file |
| **Steps** | Run merge command |
| **Command** | `python scripts/merge_experience_docs.py` |
| **Expected Result** | All files in `experience-docs/` merged into<br>`generated/experience_master.json`<br>Forms AI-referenceable knowledge base |

---

## Directory Structure

```
AI_FLOW/
├── system_rules.json              # Universal AI rules (compact JSON)
├── RULE_KEYS.json                 # Key abbreviation reference for AI
├── experience-docs/               # Rule templates (reference)
├── generated/
│   ├── experience_master.json     # Merged experience docs
│   └── experiences/               # AI-generated experience files
├── scripts/
│   ├── merge_experience_docs.py   # Merge all docs
│   ├── generate_experience.py     # Generate new exp doc
│   ├── export_system_prompt.py    # Export rules for any AI
│   └── push_experience.py         # Push to GitHub
├── .cursorrules                   # Cursor-specific (auto-read)
└── .github/workflows/
    └── auto-update-experience-docs.yml
```

---

## Command Reference

| Command | Description | Platform |
|---------|-------------|----------|
| `python scripts/export_system_prompt.py` | Print rules to terminal | All |
| `python scripts/export_system_prompt.py --copy` | Copy rules to clipboard | All |
| `python scripts/export_system_prompt.py --file` | Save rules to file | All |
| `python scripts/generate_experience.py --task_id X --module Y --summary "Z"` | Generate experience doc | All |
| `python scripts/generate_experience.py ... --push` | Generate and push to GitHub | All |
| `python scripts/merge_experience_docs.py` | Merge all experience docs | All |
| `python scripts/push_experience.py` | Push changes to GitHub | All |
| `python scripts/push_experience.py TASK_ID` | Push with task ID | All |

---

## AI Platform Integration

| AI Model | Integration Method | Auto-read | Notes |
|----------|-------------------|-----------|-------|
| **ChatGPT** | Custom Instructions or System Message | No | Paste JSON manually |
| **Claude** | First message or Projects | No | Paste JSON manually |
| **Gemini** | System Instruction | No | Paste JSON manually |
| **Cursor** | `.cursorrules` file | Yes | Auto-read on project open |
| **GitHub Copilot** | Not directly supported | No | Use comment hints |
| **Other** | Initial context message | No | Paste JSON manually |

---

## Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.7+ | Required |
| Git | Any | For push functionality |
| xclip/xsel | Any | Linux only, for clipboard |

---

## License

MIT
