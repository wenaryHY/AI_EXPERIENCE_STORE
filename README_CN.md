# AI 经验存储库

[English](README.md)

通用 AI 经验管理工作流。支持 **任何 AI 模型**（ChatGPT、Claude、Gemini、Cursor 等）

**跨平台支持**: macOS、Windows、Linux

---

## 工作流程概览

| 步骤 | 操作 | 命令 | 输出 |
|------|------|------|------|
| 1️⃣ | 导出规则 | `python scripts/export_system_prompt.py --copy` | JSON 复制到剪贴板 |
| 2️⃣ | 加载到 AI | 将 JSON 粘贴到任何 AI 模型 | AI 理解你的规则 |
| 3️⃣ | AI 工作 | AI 完成你的任务 | 任务完成，产生经验 |
| 4️⃣ | 生成文档 | `python scripts/generate_experience.py --task_id X --module Y --summary "Z"` | JSON 文件生成在 `generated/experiences/` |
| 5️⃣ | 推送 | `python scripts/push_experience.py` | 变更推送到 GitHub |
| 6️⃣ | 自动合并 | GitHub Actions 触发 | 自动创建 PR |

---

## 核心原则（AI 必须遵循）

| 原则 | 规则 | AI 行为 |
|------|------|---------|
| **问题优先** | 理解问题 > 技术实现 | 先明确问题，禁止为技术找问题 |
| **最好的代码** | 删除 > 复用 > 新增 | 删除优先，每行代码都是负债 |
| **规模即契约** | 可观察行为即契约 | Bug 也是 API，弃用≠删除 |
| **创新代币** | 创新是昂贵资源 | 非核心模块选择无聊但可靠的方案 |
| **抽象失效** | 抽象延迟复杂性 | 假设你会在凌晨3点独自值班 |
| **社会系统** | 共识 > 个人胜利 | 赢下争论可能输掉项目 |
| **指标成对** | 指标必须成对出现 | 速度vs质量，看趋势不看阈值 |
| **长期复利** | 时间不可再生 | 把经验沉淀为规则和自动化 |
| **底线规则** | 不可违反的红线 | 禁止不必要复杂性 |

---

## 使用案例

### 案例 1：首次配置 ChatGPT

| 项目 | 内容 |
|------|------|
| **使用场景** | 让 ChatGPT 遵循你的工程原则 |
| **操作步骤** | 1. 运行 `python scripts/export_system_prompt.py --copy`<br>2. 打开 ChatGPT → 设置 → 自定义指令<br>3. 粘贴 JSON |
| **预设 Prompt** | *(粘贴导出的 JSON 后，说)*<br>`请在我们所有的对话中遵循这些规则。` |
| **预期结果** | ChatGPT 将会：<br>- 默认使用中文回复<br>- 先问"要不要做"再问"怎么做"<br>- 优先删除/复用而非新增代码<br>- 选择无聊但可靠的技术方案<br>- 任务完成后生成经验文档 |

### 案例 2：使用 Claude 进行代码审查

| 项目 | 内容 |
|------|------|
| **使用场景** | 让 Claude 按照你的质量规则审查代码 |
| **操作步骤** | 1. 导出规则：`python scripts/export_system_prompt.py --copy`<br>2. 开始新的 Claude 对话<br>3. 先粘贴 JSON，再粘贴代码 |
| **预设 Prompt** | ```[粘贴 JSON]```<br><br>`请按照上面的规则审查这段代码：`<br>```python`<br>`def process_data(data):`<br>`    # 你的代码`<br>``` |
| **预期结果** | Claude 将会：<br>- 问"这个功能真的需要吗？"<br>- 优先建议删除冗余代码<br>- 指出"未来可能用到"的代码并建议删除<br>- 检查是否有可复用的现有模块<br>- 优先可读性而非技巧性<br>- 指出违反契约的变更风险 |

### 案例 3：Bug 修复后记录经验

| 项目 | 内容 |
|------|------|
| **使用场景** | 修复关键 Bug 后记录经验 |
| **操作步骤** | 修复 Bug 后，运行生成命令 |
| **命令** | ```bash<br>python scripts/generate_experience.py \<br>  --task_id BUG042 \<br>  --module auth \<br>  --summary "修复了JWT令牌过期不刷新的问题" \<br>  --decisions "使用滑动窗口刷新" "添加令牌黑名单" \<br>  --lessons "始终检查令牌生命周期" "为认证流程添加集成测试" \<br>  --push<br>``` |
| **预期结果** | 文件创建：`generated/experiences/exp_auth_BUG042_202601061200.json`<br>自动推送到 GitHub<br>经验被沉淀为可复用知识 |

### 案例 4：在 Cursor 中开发新功能

| 项目 | 内容 |
|------|------|
| **使用场景** | 在 Cursor IDE 中开发新功能 |
| **操作步骤** | 1. 用 Cursor 打开项目（自动读取 `.cursorrules`）<br>2. 向 AI 描述你的功能需求<br>3. AI 自动遵循规则工作 |
| **预设 Prompt** | `添加一个用户通知系统，支持邮件和推送通知。` |
| **预期结果** | Cursor AI 将会：<br>- 先问"这个需求解决什么用户痛点？"<br>- 问"如果不做会怎样？"<br>- 检查是否有现成方案可复用<br>- 选择成熟的通知库而非自建<br>- 避免过度设计和"技术动物园"<br>- 完成后提醒生成经验文档 |

### 案例 5：使用 Gemini 讨论架构决策

| 项目 | 内容 |
|------|------|
| **使用场景** | 与 Gemini 讨论架构选择 |
| **操作步骤** | 1. 导出规则并粘贴给 Gemini<br>2. 描述你的架构问题 |
| **预设 Prompt** | ```[粘贴 JSON]```<br><br>`我需要为我们的电商平台在微服务和单体架构之间做选择。我们有3个开发者，初期预计每日1万用户。请按照上面的工程原则进行分析。` |
| **预期结果** | Gemini 将会：<br>- 按"创新代币"原则推荐无聊但可靠的方案<br>- 考虑"抽象失效"：3人团队凌晨值班能力<br>- 按"社会系统"原则关注团队对齐而非技术完美<br>- 提醒"规模即契约"：架构选择将成为长期约束<br>- 给出成对指标（开发速度vs运维复杂度）<br>- 建议将决策记录为经验文档 |

### 案例 6：批量合并经验文档

| 项目 | 内容 |
|------|------|
| **使用场景** | 将所有经验模板合并到主文件 |
| **操作步骤** | 运行合并命令 |
| **命令** | `python scripts/merge_experience_docs.py` |
| **预期结果** | `experience-docs/` 中的所有文件合并到<br>`generated/experience_master.json`<br>形成可被AI引用的知识库 |

---

## 目录结构

```
AI_FLOW/
├── system_rules.json              # 🤖 通用 AI 规则 (压缩 JSON)
├── RULE_KEYS.json                 # 📖 规则缩写对照表 (AI 解析参考)
├── experience-docs/               # 📝 规则模板 (仅供参考)
├── generated/
│   ├── experience_master.json     # 合并后的经验文档
│   └── experiences/               # AI 生成的经验文件
├── scripts/
│   ├── merge_experience_docs.py   # 合并所有文档
│   ├── generate_experience.py     # 生成新经验文档
│   ├── export_system_prompt.py    # 导出规则给任何 AI
│   └── push_experience.py         # 推送到 GitHub
├── .cursorrules                   # Cursor 专用 (自动读取)
└── .github/workflows/
    └── auto-update-experience-docs.yml
```

---

## 命令参考

| 命令 | 描述 | 平台 |
|------|------|------|
| `python scripts/export_system_prompt.py` | 打印规则到终端 | 全平台 |
| `python scripts/export_system_prompt.py --copy` | 复制规则到剪贴板 | 全平台 |
| `python scripts/export_system_prompt.py --file` | 保存规则到文件 | 全平台 |
| `python scripts/generate_experience.py --task_id X --module Y --summary "Z"` | 生成经验文档 | 全平台 |
| `python scripts/generate_experience.py ... --push` | 生成并推送到 GitHub | 全平台 |
| `python scripts/merge_experience_docs.py` | 合并所有经验文档 | 全平台 |
| `python scripts/push_experience.py` | 推送变更到 GitHub | 全平台 |
| `python scripts/push_experience.py TASK_ID` | 带任务ID推送 | 全平台 |

---

## AI 平台集成

| AI 模型 | 集成方式 | 自动读取 | 备注 |
|---------|---------|---------|------|
| **ChatGPT** | 自定义指令 或 系统消息 | ❌ | 手动粘贴 JSON |
| **Claude** | 第一条消息 或 Projects | ❌ | 手动粘贴 JSON |
| **Gemini** | 系统指令 | ❌ | 手动粘贴 JSON |
| **Cursor** | `.cursorrules` 文件 | ✅ | 打开项目自动读取 |
| **GitHub Copilot** | 不直接支持 | ❌ | 使用注释提示 |
| **其他** | 初始上下文消息 | ❌ | 手动粘贴 JSON |

---

## 环境要求

| 需求 | 版本 | 备注 |
|------|------|------|
| Python | 3.7+ | 必需 |
| Git | 任意版本 | 用于推送功能 |
| xclip/xsel | 任意版本 | 仅 Linux，用于剪贴板 |

---

## 是否需要 Clone 仓库？

| 场景 | 是否需要 | 说明 |
|------|---------|------|
| 让 AI 读取规范 | ❌ 不需要 | 复制 JSON 内容即可 |
| 生成经验文档 | ✅ 需要 | 在本地生成文件 |
| 推送到 GitHub | ✅ 需要 | 需要本地 git 仓库 |
| 手动触发 workflow | ❌ 不需要 | 在 GitHub 网页操作 |

---

## 许可证

MIT
