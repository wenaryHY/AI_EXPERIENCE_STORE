# AI 经验存储库

[English](README.md)

通用 AI 经验管理工作流。支持 **任何 AI 模型**（ChatGPT、Claude、Gemini、Cursor 等）

## 目录结构

```
AI_FLOW/
├── system_rules.json              # 🤖 通用 AI 规则 (JSON格式，英文)
├── experience-docs/               # 📝 规则模板 (仅供参考)
├── generated/
│   ├── experience_master.json     # 合并后的经验文档
│   └── experiences/               # AI 生成的经验文件
├── scripts/
│   ├── merge_experience_docs.py   # 合并所有文档
│   ├── generate_experience.py     # 生成新经验文档
│   ├── export_system_prompt.py    # 导出规则给任何 AI
│   └── push_experience.sh         # 快速推送脚本
├── .cursorrules                   # Cursor 专用 (自动读取)
└── .github/workflows/
    └── auto-update-experience-docs.yml
```

## 快速开始

### 1. 导出规则给任何 AI

```bash
# 打印到终端 (手动复制)
python scripts/export_system_prompt.py

# 复制到剪贴板 (macOS)
python scripts/export_system_prompt.py --copy

# 保存到文件
python scripts/export_system_prompt.py --file
```

然后将输出粘贴给 **任何 AI 模型** 作为系统提示。

### 2. AI 生成经验文档

AI 完成任务后：

```bash
python scripts/generate_experience.py \
  --task_id TASK001 \
  --module core \
  --summary "完成了功能X" \
  --decisions "使用了方案A" \
  --lessons "需要提前考虑边界情况" \
  --push  # 自动推送到 GitHub
```

### 3. 自动工作流

当你推送变更到 `experience-docs/` 目录时，GitHub Actions 会自动：
1. 合并所有文档到 `experience_master.json`
2. 创建带时间戳的分支
3. 创建 PR 供审核

## 系统规则格式

`system_rules.json` - AI 可解析的紧凑 JSON：

```json
{
  "agent_config": { "mode": "ENGINEERING_LONG_TERMISM", "lang": "zh-CN" },
  "priorities": ["problem_understanding > implementation", ...],
  "code_rules": ["delete > add", "reuse > create", ...],
  "exp_doc_rules": { "file_pattern": "exp_{module}_{taskid}_{ts}.json", ... }
}
```

## 通用使用方式

| AI 模型 | 如何加载规则 |
|---------|-------------|
| **ChatGPT** | 将 `system_rules.json` 内容粘贴为系统消息 |
| **Claude** | 粘贴为第一条消息 或使用 Projects 功能 |
| **Gemini** | 粘贴为系统指令 |
| **Cursor** | 自动读取 `.cursorrules` 文件 |
| **其他** | 粘贴 JSON 作为初始上下文 |

## 常用命令

```bash
# 导出规则给任何 AI
python scripts/export_system_prompt.py --copy

# 生成经验文档
python scripts/generate_experience.py --task_id X --module Y --summary "Z"

# 合并所有经验文档
python scripts/merge_experience_docs.py

# 快速推送
./scripts/push_experience.sh TASK_ID
```

## 工作流程图

```
┌─────────────────────────────────────────────────────────────┐
│                      使用流程                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 导出规则                                                 │
│     python scripts/export_system_prompt.py --copy           │
│                         ↓                                   │
│  2. 粘贴给任何 AI (ChatGPT/Claude/Gemini/...)              │
│                         ↓                                   │
│  3. AI 按规范工作，完成任务                                  │
│                         ↓                                   │
│  4. 生成经验文档                                             │
│     python scripts/generate_experience.py --push            │
│                         ↓                                   │
│  5. 自动推送到 GitHub                                        │
│                         ↓                                   │
│  6. GitHub Actions 合并 & 创建 PR                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 是否需要 Clone 仓库？

| 场景 | 是否需要 Clone |
|------|---------------|
| 让 AI 读取规范 | ❌ 不需要 - 复制 JSON 内容即可 |
| 生成经验文档 | ✅ 需要 - 在本地生成文件 |
| 推送到 GitHub | ✅ 需要 - 需要本地 git 仓库 |
| 手动触发 workflow | ❌ 不需要 - 在 GitHub 网页操作 |

## 许可证

MIT

