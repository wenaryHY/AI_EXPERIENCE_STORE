#!/bin/bash
# 经验文档推送脚本
# 用法: ./scripts/push_experience.sh [task_id] [message]

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

TASK_ID="${1:-auto}"
MESSAGE="${2:-Update experience docs}"

echo "=================================================="
echo "🚀 Experience Document Push Script"
echo "=================================================="
echo ""

# 检查是否有变更
if git diff --quiet generated/ 2>/dev/null && [ -z "$(git ls-files --others --exclude-standard generated/)" ]; then
    echo "ℹ️  没有检测到 generated/ 目录的变更"
    exit 0
fi

# 显示变更
echo "📝 检测到以下变更:"
git status --short generated/
echo ""

# 添加并提交
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
COMMIT_MSG="Add/Update exp ${TASK_ID} ${TIMESTAMP}"

if [ "$MESSAGE" != "Update experience docs" ]; then
    COMMIT_MSG="$MESSAGE"
fi

echo "💾 提交变更..."
git add generated/
git commit -m "$COMMIT_MSG"

echo ""
echo "📤 推送到远程仓库..."
git push origin HEAD

echo ""
echo "=================================================="
echo "✅ 推送成功!"
echo "   提交信息: $COMMIT_MSG"
echo "=================================================="

