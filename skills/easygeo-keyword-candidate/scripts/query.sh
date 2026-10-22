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
Skill: easygeo-keyword-candidate

Commands:
  candidate-add <keyword>  # GEO备选词-加入
  candidate-list   # GEO备选词-列表
EOF
  exit 1
}

[[ -n "$CMD" ]] || usage

case "$CMD" in
  candidate-add)
    # GEO备选词-加入
    if [[ "${1:-}" == \{* ]]; then
      PAYLOAD="$1"
    else
      KEYS='["keyword"]'
      REQUIRED='["keyword"]'
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
    curl -s -X POST "$BASE/aigc/geo/keyword/candidate/add" -H "Content-Type: application/json" -H "Authorization: Bearer $API_KEY" -d "$PAYLOAD"
    ;;
  candidate-list)
    # GEO备选词-列表
    curl -s -X GET "$BASE/aigc/geo/keyword/candidate/list" -H "Authorization: Bearer $API_KEY"
    ;;
  *)
    usage
    ;;
esac
