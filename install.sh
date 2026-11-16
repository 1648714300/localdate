#!/usr/bin/env bash
# 约会军师 · LocalDate 一键安装
# 用法：curl -fsSL https://raw.githubusercontent.com/1648714300/localdate/main/install.sh | bash
set -e

REPO="https://github.com/1648714300/localdate.git"
SKILLS="${WORKBUDDY_SKILLS:-$HOME/.workbuddy/skills}"
ALT="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
TARGET="$SKILLS/localdate"

echo "== 约会军师 · LocalDate =="

if ! command -v git >/dev/null 2>&1; then
  echo "需要先装 git：https://git-scm.com/downloads"
  exit 1
fi

mkdir -p "$SKILLS"
if [ -d "$TARGET/.git" ]; then
  echo "已装过，拉取更新：$TARGET"
  git -C "$TARGET" pull --ff-only || echo "更新失败，继续用现有版本"
else
  echo "克隆到：$TARGET"
  git clone --depth 1 "$REPO" "$TARGET"
fi

# 留一个短名，以后只说 /date
ln -sfn "$TARGET" "$SKILLS/date" 2>/dev/null || true

# Claude Code 用户顺手套一份软链（存在才做）
if [ -d "$ALT" ]; then
  ln -sfn "$TARGET" "$ALT/localdate" 2>/dev/null || true
  ln -sfn "$TARGET" "$ALT/date" 2>/dev/null || true
  echo "已链接到 $ALT"
fi

echo
echo "装好了。下一步，直接对你的 AI 说："
echo "  /date 排这个周末的约会   （或）  约会军师，淮南，周六下午，预算 100"
echo
echo "它会先问四件事：城市包 / 白天还是晚上 / 对方体力与禁忌 / 预算。"
echo "之后每轮 15 个方案，你报编号排序，它把你的口味写进权重。"
