#!/usr/bin/env bash
# =============================================================================
# sync-skills.sh — 把 FinSkills 源同步到 FastClaw 运行环境
# =============================================================================
# 单一真相源：~/finskills（git 仓库）。本脚本把指定技能 rsync 到：
#   · 全局共享层  ~/.fastclaw/skills/                （数据工具包，跨 agent 共用）
#   · 各 agent 私有 ~/.fastclaw/agents/<id>/agent/skills/  （分析技能）
#
# 为什么用拷贝而非软链：FastClaw 的技能扫描 (os.ReadDir + IsDir) 不识别
# 整目录 symlink，所以运行副本必须是真实目录。源改动后重跑本脚本即可对齐。
#
# 用法：
#   ./sync-skills.sh            # 全量同步
#   ./sync-skills.sh --dry-run  # 只打印将要做什么，不落盘
#   ./sync-skills.sh --prune    # 同步并删除运行副本里多余的技能（与映射表对齐）
# =============================================================================
set -euo pipefail

FINSKILLS="${FINSKILLS:-$HOME/finskills}"
FC_HOME="${FASTCLAW_HOME:-$HOME/.fastclaw}"
GLOBAL_SKILLS="$FC_HOME/skills"

DRY_RUN=0
PRUNE=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --prune)   PRUNE=1 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

# -----------------------------------------------------------------------------
# Agent ID 映射 —— 建好对应 agent 后把真实 agt_ ID 填进来。
# 留空的条目会被跳过并告警（方便先建 agent 再补 ID）。
# -----------------------------------------------------------------------------
AGENT_NEWS_CN="agt_9a7a50b8fa6de289b1c2"      # news-analyst（A股消息面）
AGENT_STOCK_CN="agt_1dc684cc47fb854b005b"     # stock-screener（A股选股）
AGENT_NEWS_US="${AGENT_NEWS_US:-agt_5bb1e62935afc80d77ce}"    # news-analyst-us
AGENT_STOCK_US="${AGENT_STOCK_US:-agt_4e85c80c71dc538a1139}"  # stock-screener-us

# -----------------------------------------------------------------------------
# 映射表：每行 "源相对路径 -> 目标桶"
#   桶 = global | <AGENT_VAR 名>
# 源相对路径相对于 $FINSKILLS。
# -----------------------------------------------------------------------------
read -r -d '' MAPPINGS <<'MAP' || true
# --- 全局共享数据工具包 ---
China-market/findata-toolkit-cn        global
US-market/findata-toolkit              global

# --- A股 · 消息面 agent ---
China-market/event-driven-detector     AGENT_NEWS_CN
China-market/sentiment-reality-gap     AGENT_NEWS_CN
China-market/insider-trading-analyzer  AGENT_NEWS_CN
China-market/sector-rotation-detector  AGENT_NEWS_CN

# --- A股 · 选股 agent ---
China-market/quant-factor-screener         AGENT_STOCK_CN
China-market/undervalued-stock-screener    AGENT_STOCK_CN
China-market/small-cap-growth-identifier   AGENT_STOCK_CN
China-market/financial-statement-analyzer  AGENT_STOCK_CN

# --- 美股 · 消息面 agent ---
US-market/event-driven-detector     AGENT_NEWS_US
US-market/sentiment-reality-gap     AGENT_NEWS_US
US-market/insider-trading-analyzer  AGENT_NEWS_US
US-market/sector-rotation-detector  AGENT_NEWS_US

# --- 美股 · 选股 agent ---
US-market/quant-factor-screener         AGENT_STOCK_US
US-market/undervalued-stock-screener    AGENT_STOCK_US
US-market/small-cap-growth-identifier   AGENT_STOCK_US
US-market/financial-statement-analyzer  AGENT_STOCK_US
MAP

# -----------------------------------------------------------------------------
# helpers
# -----------------------------------------------------------------------------
resolve_dest() {
  # $1 = bucket token -> echo absolute target skills dir, or empty if unresolved
  local bucket="$1"
  if [ "$bucket" = "global" ]; then
    echo "$GLOBAL_SKILLS"; return 0
  fi
  # 间接展开前先校验 bucket 是合法 shell 变量名，避免 set -u 下
  # 注释残留/全角字符触发 "unbound variable"。
  if ! [[ "$bucket" =~ ^[A-Za-z_][A-Za-z_0-9]*$ ]]; then
    echo ""; return 0
  fi
  local id="${!bucket:-}"      # indirect: AGENT_NEWS_US -> its value
  if [ -z "$id" ]; then
    echo ""; return 0
  fi
  echo "$FC_HOME/agents/$id/agent/skills"
}

run() {
  if [ "$DRY_RUN" = "1" ]; then
    echo "  [dry-run] $*"
  else
    eval "$*"
  fi
}

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
[ -d "$FINSKILLS" ] || { echo "FINSKILLS not found: $FINSKILLS" >&2; exit 1; }

echo "FinSkills 源 : $FINSKILLS"
echo "FastClaw home: $FC_HOME"
echo "模式         : $([ "$DRY_RUN" = 1 ] && echo dry-run || echo apply)$([ "$PRUNE" = 1 ] && echo " +prune")"
echo "----------------------------------------------------------------"

synced=0 skipped=0
declare -a planned_per_dest_keys=()

while IFS= read -r line; do
  line="${line%%#*}"                     # strip comments
  line="$(echo "$line" | xargs || true)" # trim
  [ -z "$line" ] && continue
  src_rel="$(echo "$line" | awk '{print $1}')"
  bucket="$(echo "$line" | awk '{print $2}')"
  src="$FINSKILLS/$src_rel"
  skill_name="$(basename "$src_rel")"

  if [ ! -d "$src" ]; then
    echo "⚠️  源缺失，跳过: $src_rel"; skipped=$((skipped+1)); continue
  fi
  dest_dir="$(resolve_dest "$bucket")"
  if [ -z "$dest_dir" ]; then
    echo "⏭️  未配置 agent ID ($bucket)，跳过: $src_rel"; skipped=$((skipped+1)); continue
  fi

  run "mkdir -p '$dest_dir'"
  # --delete 让单个技能目录内的文件与源严格一致（删掉源已移除的文件）
  run "rsync -a --delete '$src/' '$dest_dir/$skill_name/'"
  echo "✅ $src_rel  ->  ${dest_dir/#$HOME/~}/$skill_name"
  synced=$((synced+1))

  # 记录每个 dest 计划保留的技能名（供 --prune 用）
  planned_per_dest_keys+=("$dest_dir|$skill_name")
done <<< "$MAPPINGS"

# -----------------------------------------------------------------------------
# prune：删除运行副本里、映射表没声明的技能目录
# -----------------------------------------------------------------------------
if [ "$PRUNE" = "1" ]; then
  echo "----------------------------------------------------------------"
  echo "prune：清理映射表外的运行副本"
  # 收集所有出现过的 dest_dir
  declare -a dests=()
  for kv in "${planned_per_dest_keys[@]}"; do
    d="${kv%%|*}"; case " ${dests[*]} " in *" $d "*) ;; *) dests+=("$d");; esac
  done
  for d in "${dests[@]}"; do
    [ -d "$d" ] || continue
    for existing in "$d"/*/; do
      [ -d "$existing" ] || continue
      en="$(basename "$existing")"
      keep=0
      for kv in "${planned_per_dest_keys[@]}"; do
        [ "$kv" = "$d|$en" ] && { keep=1; break; }
      done
      if [ "$keep" = "0" ]; then
        echo "🗑️  prune: ${existing/#$HOME/~}"
        run "rm -rf '$existing'"
      fi
    done
  done
fi

echo "----------------------------------------------------------------"
echo "完成：同步 $synced 个，跳过 $skipped 个。"
if [ -z "$AGENT_NEWS_US" ] || [ -z "$AGENT_STOCK_US" ]; then
  echo ""
  echo "ℹ️  美股 agent ID 未填（AGENT_NEWS_US / AGENT_STOCK_US），美股分析技能已跳过。"
  echo "    建好 news-analyst-us / stock-screener-us 后，把真实 agt_ ID 填入脚本顶部，"
  echo "    或用环境变量临时跑：  AGENT_NEWS_US=agt_xxx AGENT_STOCK_US=agt_yyy ./sync-skills.sh"
fi
echo ""
echo "⚠️  改动技能后，FastClaw 下一轮对话会重新扫描；若 dashboard 未刷新可重启 gateway。"
