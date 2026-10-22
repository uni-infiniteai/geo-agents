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
Skill: easygeo-text-detail

Commands:
  batch-detail <id>  # GEO文案-批次详情
  detail <id>  # GEO文案-分项详情
  logs   # GEO文案-分项结果列表
EOF
  exit 1
}

[[ -n "$CMD" ]] || usage

case "$CMD" in
  batch-detail)
    # GEO文案-批次详情
    ID="${1:?用法: query.sh batch-detail <id>}"
    qs=""
    if [[ -n "${ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsid=${ID}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/text/create/batch/log/detail?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/text/create/batch/log/detail" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  detail)
    # GEO文案-分项详情
    ID="${1:?用法: query.sh detail <id>}"
    qs=""
    if [[ -n "${ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsid=${ID}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/text/log/detail?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/text/log/detail" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  logs)
    # GEO文案-分项结果列表
    BATCH_ID="${1:-}"
    START="${2:-}"
    SIZE="${3:-}"
    qs=""
    if [[ -n "${BATCH_ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsbatch_id=${BATCH_ID}"
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
      curl -s -X GET "$BASE/aigc/geo/text/create/logs?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/text/create/logs" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  *)
    usage
    ;;
esac
