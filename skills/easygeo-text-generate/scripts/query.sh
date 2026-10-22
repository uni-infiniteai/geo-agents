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
Skill: easygeo-text-generate

Commands:
  platform-options   # GEO文案-平台选项
  model-options   # GEO文案-大模型选项
  image-model-options   # GEO文案-图片模型选项
  angle-options   # GEO文案-写作角度选项
  generate <prompt> <model>  # GEO文案-生成建议写作方向
EOF
  exit 1
}

[[ -n "$CMD" ]] || usage

case "$CMD" in
  platform-options)
    # GEO文案-平台选项
    curl -s -X GET "$BASE/aigc/geo/text/platform/options" -H "Authorization: Bearer $API_KEY"
    ;;
  model-options)
    # GEO文案-大模型选项
    curl -s -X GET "$BASE/aigc/geo/text/model/options" -H "Authorization: Bearer $API_KEY"
    ;;
  image-model-options)
    # GEO文案-图片模型选项
    curl -s -X GET "$BASE/aigc/geo/text/image_model/options" -H "Authorization: Bearer $API_KEY"
    ;;
  angle-options)
    # GEO文案-写作角度选项
    curl -s -X GET "$BASE/aigc/geo/text/angle/options" -H "Authorization: Bearer $API_KEY"
    ;;
  generate)
    # GEO文案-生成建议写作方向
    if [[ "${1:-}" == \{* ]]; then
      PAYLOAD="$1"
    else
      KEYS='["prompt", "model", "count", "implant", "angles"]'
      REQUIRED='["prompt", "model"]'
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
    curl -s -X POST "$BASE/aigc/geo/text/generate" -H "Content-Type: application/json" -H "Authorization: Bearer $API_KEY" -d "$PAYLOAD"
    ;;
  *)
    usage
    ;;
esac
