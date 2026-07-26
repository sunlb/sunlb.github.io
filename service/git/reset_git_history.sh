#!/usr/bin/env bash
set -e

echo "=== Git 全历史清除工具 ==="
echo "此脚本将删除所有历史提交，只保留当前文件状态。"
echo "⚠️ 该操作会覆盖远程历史，无法撤销！"
echo

read -p "确认继续？(yes/no): " confirm
if [[ "$confirm" != "yes" ]]; then
    echo "已取消操作。"
    exit 1
fi

# 1. 检查是否在 git 仓库内
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ 当前目录不是 Git 仓库！"
    exit 1
fi

# 2. 备份当前分支名
current_branch=$(git rev-parse --abbrev-ref HEAD)
backup_branch="backup_before_reset_$(date +%Y%m%d_%H%M%S)"

echo "• 当前分支：$current_branch"
echo "• 创建备份分支：$backup_branch"

git branch "$backup_branch"

# 3. 创建孤儿分支（无历史）
echo "• 创建 orphan 分支 latest_clean"
git checkout --orphan latest_clean

# 4. 添加所有文件
echo "• 添加文件"
git add -A

# 5. 创建新的初始提交
echo "• 创建新的初始提交"
git commit -m "Initial commit (history reset)"

# 6. 删除旧分支
echo "• 删除旧分支：$current_branch"
git branch -D "$current_branch"

# 7. 将最新分支重命名为 master（若你是 main 可改成 main）
echo "• 重命名分支 latest_clean → master"
git branch -m master

# 8. 强制推送覆盖远程
echo "• 强制推送到远程 origin/master"
git push -f origin master

# 9. 本地仓库 GC
echo "• 执行本地 Git GC"
git gc --aggressive --prune=all

echo
echo "=== 完成！历史已全部清除，仅保留一个初始提交 ==="
echo "旧历史备份在分支：$backup_branch"
echo "如需恢复，使用： git checkout $backup_branch"
