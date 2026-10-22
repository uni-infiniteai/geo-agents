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
Skill: easygeo-promo-link-detail

Commands:
  detail <id>  # GEO推广链接-详情
EOF
  exit 1
}

[[ -n "$CMD" ]] || usage

case "$CMD" in
  detail)
    # GEO推广链接-详情
    ID="${1:?用法: query.sh detail <id>}"
    qs=""
    if [[ -n "${ID}" ]]; then
      [[ -n "$qs" ]] && qs="$qs&"
      qs="$qsid=${ID}"
    fi
    if [[ -n "$qs" ]]; then
      curl -s -X GET "$BASE/aigc/geo/promo_link/log/detail?$qs" -H "Authorization: Bearer $API_KEY"
    else
      curl -s -X GET "$BASE/aigc/geo/promo_link/log/detail" -H "Authorization: Bearer $API_KEY"
    fi
    ;;
  *)
    usage
    ;;
esac
