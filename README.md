# AI Experience Store

This repository stores **AI-generated experience documents** from multiple devices or sessions.  
It supports **automatic merge, versioning, branch-based management, and PRs** via GitHub Actions.

## 目录结构

```
AI_FLOW/
├── .github/workflows/
│   └── auto-update-experience-docs.yml   # Workflow 定义
├── experience-docs/                       # 所有经验文档 (JSON格式.txt文件)
│   ├── 00_system_identity_and_principles.txt
│   ├── 01_pre_action_system_state_rules.txt
│   ├── 02_engineering_invariants_code_quality.txt
│   ├── 03_self_audit_and_rollback_rules.txt
│   ├── 04_experience_document_template.txt
│   ├── 05_experience_enforcement_rule.txt
│   ├── 06_experience_management.txt
│   └── 07_experience_doc_management.txt
├── scripts/
│   └── merge_experience_docs.py           # Python 合并脚本
├── experience_master.json                 # 合并后的主文件 (自动生成)
├── requirements.txt                       # Python 依赖
└── README.md
```

## Workflow 工作流程

### 触发条件
- **手动触发**: 通过 GitHub Actions 界面的 `workflow_dispatch`
- **自动触发**: 当 `experience-docs/` 目录下的 `.txt` 文件有变更并推送到 `master`/`main` 分支时

### 执行步骤
1. ✅ Checkout 仓库代码
2. ✅ 配置 Python 3.11 环境
3. ✅ 安装 `requirements.txt` 中的依赖
4. ✅ 运行 `merge_experience_docs.py` 合并所有经验文档
5. ✅ 检测是否有变更
6. ✅ 如有变更，创建时间戳分支并推送
7. ✅ 自动创建 PR 到主分支

## 使用方法

### 添加新经验文档
1. 在 `experience-docs/` 目录下添加新的 `.txt` 文件
2. 文件内容应为 JSON 格式
3. 推送到 `master` 分支，workflow 将自动触发

### 手动触发合并
1. 进入 GitHub 仓库的 **Actions** 页面
2. 选择 **Auto Update Experience Docs** workflow
3. 点击 **Run workflow** 按钮

### 本地运行合并脚本
```bash
# 安装依赖
pip install -r requirements.txt

# 运行合并脚本
python scripts/merge_experience_docs.py
```

## 经验文档格式

每个经验文档应为 JSON 格式，包含以下结构：

```json
{
  "role": "system",
  "category_name": {
    "purpose": "文档目的描述",
    "key_field_1": [...],
    "key_field_2": {...}
  }
}
```

## 合并输出格式

`experience_master.json` 包含以下字段：

| 字段 | 说明 |
|------|------|
| `schema_version` | Schema 版本号 |
| `generated_at_utc` | UTC 生成时间 |
| `total_documents` | 文档总数 |
| `source_directory` | 源目录 |
| `documents` | 所有文档数组 |
| `index` | 文件名到索引的映射 |

每个文档条目包含：
- `source_file`: 原始文件名
- `file_path`: 文件路径
- `content_hash`: 内容 MD5 哈希（用于变更检测）
- `file_modified_utc`: 文件修改时间
- `parsed_at_utc`: 解析时间
- `content`: 解析后的 JSON 内容

## 注意事项

- Workflow 通过分支保留历史记录，便于追溯旧版本经验
- 每次合并会创建带时间戳的分支（如 `update-experience-20260106-120000`）
- 自动创建的 PR 带有 `automated` 和 `experience-docs` 标签
- 如果没有检测到变更，workflow 将跳过 PR 创建步骤

## License

MIT
