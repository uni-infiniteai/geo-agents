#!/usr/bin/env bash
set -euo pipefail

API_KEY="${EASYGEO_API_KEY:-${CLAWEC_API_KEY:-}}"
if [[ -z "$API_KEY" ]]; then
  echo "请设置环境变量 EASYGEO_API_KEY（或 CLAWEC_API_KEY）" >&2
  exit 1
fi
BASE="https://www.clawec.com/api"

CMD="${1:-}"
shift || true

usage() {
  cat >&2 <<EOF
用法: query.sh <command> [args...]
Skill: easygeo-citation-monitor

Commands:
  monitor-add <name> <cron_date_type> <time> <models> <brand> <keywords>  # GEO引用监测-添加定时任务
  monitor-run <item_id>  # GEO引用监测-立即执行
  series <item_id>  # GEO引用监测-时间序列
  monitor-logs   # GEO引用监测-运行历史
  monitor-detail <id>  # GEO引用监测-运行详情
EOF
  exit 1
}

[[ -n "$CMD" ]] || usage

case "$CMD" in
  monitor-add)
    # GEO引用监测-添加定时任务
    if [[ "${1:-}" == \{* ]]; then
      PAYLOAD="$1"
    else
      KEYS='["name", "cron_date_type", "time", "weeks", "days", "day", "enable", "notifyEmail", "models", "brand", "competitors", "keywords"]'
      REQUIRED='["name", "cron_date_type", "time", "models", "brand", "keywords"]'
      PAYLOAD=$(KEYS="$KEYS" REQUIRED="$REQUIRED" python3 - "$@" <<'PY'
import json, os, sys
keys = json.loads(os.environ["KEYS"])
required = set(json.loads(os.environ["REQUIRED"]))
vals = list(sys.argv[1:])
body = {}
array_keys = {"products","keywords","competitors","models","questions","platforms","angles","weeks","days","image_prompts","signals"}
number_keys = {"count","cover_count","redditLimit","enable","promptId","groupId","batchId","cover"}
for idx, k in enumerate(keys):
    v = vals[idx] if idx < len(vals) else ""
    v = (v or "").strip()
    if not v:
        if k in required:
            raise SystemExit(f"{k} 不能为空")
        continue
    if k in array_keys:
        if v.startswith("["):
            body[k] = json.loads(v)
        else:
            body[k] = [x.strip() for x in v.split(",") if x.strip()]
    elif k in number_keys:
        try:
            body[k] = int(v)
        except ValueError:
            body[k] = v
    else:
        body[k] = v
print(json.dumps(body, ensure_ascii=False))
PY
)
    fi
    curl -s -X POST "$BASE/aigc/geo/citation_monitor/cron_task/add" -H "Content-Type: application/json" -H "Authorization: Bearer $API_KEY" -d "$PAYLOAD"
    ;;
  monitor-run)
    # GEO引用监测-立即执行
    Q_ITEM_ID="${1:?需要 item_id}"
    curl -s -X POST "$BASE/aigc/geo/citation_monitor/cron_task/run?item_id=$Q_ITEM_ID" -H "Authorization: Bearer $API_KEY"
    ;;
  series)
    # GEO引用监测-时间序列
    ITEM_ID="${1:?用法: query.sh series <item_id> <begin> <end> <limit>}"
    BEGIN="${2:-}"
    END="${3:-}"
    LIMIT="${4:-}"
    qs=""
    if [[ -n "${ITEM_ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsitem_id=${ITEM_ID}"
    fi
    if [[ -n "${BEGIN}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsbegin=${BEGIN}"
    fi
    if [[ -n "${END}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsend=${END}"
    fi
    if [[ -n "${LIMIT}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qslimit=${LIMIT}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/series?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/series" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  monitor-logs)
    # GEO引用监测-运行历史
    ITEM_ID="${1:-}"
    START="${2:-}"
    SIZE="${3:-}"
    qs=""
    if [[ -n "${ITEM_ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsitem_id=${ITEM_ID}"
    fi
    if [[ -n "${START}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsstart=${START}"
    fi
    if [[ -n "${SIZE}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qssize=${SIZE}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/logs?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/logs" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  monitor-detail)
    # GEO引用监测-运行详情
    ID="${1:?用法: query.sh monitor-detail <id>}"
    qs=""
    if [[ -n "${ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsid=${ID}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/log/detail?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/citation_monitor/log/detail" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  *)
    usage
    ;;
esac
