#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate geo-agents skills + agents from GEO API plugin library."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_JSON = Path(__file__).resolve().parents[2] / "server/docs/插件库-GEO接口.json"
BASE = "https://www.clawec.com/api"
KEY_PAGE = "https://geo.clawec.com/zh-cn/api-key"
HOME = "https://geo.clawec.com"

with API_JSON.open(encoding="utf-8") as f:
    plugins = json.load(f)["plugins"]

by_title = {p["title"]: p for p in plugins}

SKILLS = [
    {
        "id": "easygeo-keyword-expand",
        "name": "GEO关键词联想",
        "description": "通过 EasyGEO API 根据核心词扩展 GEO 提问词。在用户需要挖词、关键词联想、扩展搜索问法时使用。先取模型选项再调用联想。",
        "plugins": ["GEO关键词联想-模型选项", "GEO关键词联想"],
        "workflow": [
            "确认核心关键词 keyword（保持用户原词语言）",
            "GET /aigc/geo/keyword/model/options 选取 model",
            "POST /aigc/geo/keyword/expand 传入 keyword + model",
            "整理扩展提问词表；可建议加入备选词库或继续引用评估/成文",
        ],
    },
    {
        "id": "easygeo-keyword-detail",
        "name": "GEO关键词联想详情",
        "description": "按记录 id 查询 EasyGEO 关键词联想历史详情。在用户回看某次扩词结果时使用。",
        "plugins": ["GEO关键词联想-详情"],
        "workflow": [
            "确认记录 id",
            "GET /aigc/geo/keyword/log/detail?id=",
            "摘要返回的关键词与 items",
        ],
    },
    {
        "id": "easygeo-keyword-candidate",
        "name": "GEO备选词库",
        "description": "将关键词加入 EasyGEO 备选词库或列出当前备选词。在用户要收藏提问词、管理词库时使用。",
        "plugins": ["GEO备选词-加入", "GEO备选词-列表"],
        "workflow": [
            "加入：POST /aigc/geo/keyword/candidate/add {keyword}",
            "列表：GET /aigc/geo/keyword/candidate/list",
            "重复词会被忽略，属正常行为",
        ],
    },
    {
        "id": "easygeo-brand-score-prepare",
        "name": "GEO品牌得分-准备",
        "description": "根据产品服务列表生成品牌诊断用的主题关键词与竞品。在用户做品牌曝光得分前的 prepare 步骤使用。品牌名不参与拆词。",
        "plugins": ["GEO品牌得分-模型选项", "GEO品牌得分-生成关键词与竞品"],
        "workflow": [
            "收集 brand / description / products（至少一个产品）",
            "POST /aigc/geo/brand_score/prepare",
            "展示 keywords / competitors 供用户确认或微调",
            "再进入 easygeo-brand-score-eval",
        ],
    },
    {
        "id": "easygeo-brand-score-eval",
        "name": "GEO品牌得分-发起检测",
        "description": "发起 EasyGEO 多模型品牌曝光得分检测（异步）。需先 prepare 并确认 keywords/competitors。",
        "plugins": ["GEO品牌得分-发起检测"],
        "workflow": [
            "GET /aigc/geo/brand_score/model/options 取 models",
            "POST /aigc/geo/brand_score/eval（models/brand/keywords/competitors 等）",
            "拿到记录 id 后用 easygeo-brand-score-detail 拉结果",
        ],
    },
    {
        "id": "easygeo-brand-score-detail",
        "name": "GEO品牌得分-详情",
        "description": "按记录 id 拉取品牌曝光得分异步结果并解读。",
        "plugins": ["GEO品牌得分-详情"],
        "workflow": [
            "GET /aigc/geo/brand_score/log/detail?id=",
            "若未完成则稍后重试",
            "输出得分、模型差异、竞品对比与行动建议",
        ],
    },
    {
        "id": "easygeo-promo-link-prepare",
        "name": "GEO推广链接-准备",
        "description": "抓取推广链接并智能生成检测问题。在用户要检查某篇文章/落地页在 AI 中的引用表现前使用。",
        "plugins": ["GEO推广链接-模型选项", "GEO推广链接-抓取并生成问题"],
        "workflow": [
            "确认 url",
            "POST /aigc/geo/promo_link/prepare {url}",
            "展示 title / questions 供确认",
            "再进入 easygeo-promo-link-eval",
        ],
    },
    {
        "id": "easygeo-promo-link-eval",
        "name": "GEO推广链接-发起检测",
        "description": "对推广链接发起多模型引用/提及检测（异步）。",
        "plugins": ["GEO推广链接-发起检测"],
        "workflow": [
            "GET /aigc/geo/promo_link/model/options 取 models",
            "POST /aigc/geo/promo_link/eval（models/url/questions，可选 title、questionMode）",
            "用 easygeo-promo-link-detail 拉结果",
        ],
    },
    {
        "id": "easygeo-promo-link-detail",
        "name": "GEO推广链接-详情",
        "description": "按记录 id 拉取推广链接检测结果。",
        "plugins": ["GEO推广链接-详情"],
        "workflow": [
            "GET /aigc/geo/promo_link/log/detail?id=",
            "摘要各模型引用/提及情况",
        ],
    },
    {
        "id": "easygeo-citation-eval",
        "name": "GEO引用评估",
        "description": "多模型检测 AI 回答中品牌是否被提及、引用来源与竞品对比。支持可选 Google Trends / Reddit 旁路信号。",
        "plugins": ["GEO引用评估-模型选项", "GEO引用评估-旁路信号选项", "GEO引用评估-发起"],
        "workflow": [
            "确认 brand、question 或 questions（1~20）、可选 competitors / signals",
            "GET model/options 与可选 signal/options",
            "POST /aigc/geo/citation_eval/eval",
            "用 easygeo-citation-detail 拉异步结果",
        ],
    },
    {
        "id": "easygeo-citation-detail",
        "name": "GEO引用评估-详情",
        "description": "按记录 id 拉取引用评估异步结果。",
        "plugins": ["GEO引用评估-详情"],
        "workflow": [
            "GET /aigc/geo/citation_eval/log/detail?id=",
            "表格汇总模型×提及×来源域名",
        ],
    },
    {
        "id": "easygeo-citation-monitor",
        "name": "GEO引用监测",
        "description": "创建/执行品牌引用定时监测任务，并查询时间序列与运行历史。适合持续跟踪品牌在 AI 中的曝光。",
        "plugins": [
            "GEO引用监测-添加定时任务",
            "GEO引用监测-立即执行",
            "GEO引用监测-时间序列",
            "GEO引用监测-运行历史",
            "GEO引用监测-运行详情",
        ],
        "workflow": [
            "添加：POST /aigc/geo/citation_monitor/cron_task/add",
            "立即跑：POST /aigc/geo/citation_monitor/cron_task/run?item_id=",
            "序列：GET /series；历史：GET /logs；详情：GET /log/detail",
        ],
    },
    {
        "id": "easygeo-text-generate",
        "name": "GEO文案-生成写作方向",
        "description": "根据关键词/种子提示词生成 GEO 建议写作方向（不是正文）。正式成文请用 easygeo-text-create。",
        "plugins": [
            "GEO文案-平台选项",
            "GEO文案-大模型选项",
            "GEO文案-图片模型选项",
            "GEO文案-写作角度选项",
            "GEO文案-生成建议写作方向",
        ],
        "workflow": [
            "取 model/options，可选 angle/options",
            "POST /aigc/geo/text/generate（prompt/model，可选 count/implant/angles）",
            "编号列出方向供用户选择；选中后进入 create",
        ],
    },
    {
        "id": "easygeo-text-create",
        "name": "GEO文案-正式成文",
        "description": "按平台正式生成 GEO 投放文（异步）。须带回 seed + implant + prompt（建议写作方向）。支持追加平台。",
        "plugins": ["GEO文案-正式生成", "GEO文案-追加平台写作"],
        "workflow": [
            "GET platform/options 选 platforms；取 model（及可选 image_model）",
            "POST /aigc/geo/text/create：platforms + prompt + seed + implant + model",
            "可选封面 cover_mode / image_* 参数",
            "用 easygeo-text-detail 拉 batchId 结果；追加平台用 /create/append",
        ],
    },
    {
        "id": "easygeo-text-detail",
        "name": "GEO文案-结果查询",
        "description": "查询 GEO 成文批次详情、分项详情或分项列表。",
        "plugins": ["GEO文案-批次详情", "GEO文案-分项详情", "GEO文案-分项结果列表"],
        "workflow": [
            "批次：GET /aigc/geo/text/create/batch/log/detail?id=",
            "分项：GET /aigc/geo/text/log/detail?id=",
            "列表：GET /aigc/geo/text/create/logs?batch_id=",
        ],
    },
]

ABOUT = f"""## 关于 EasyGEO

**EasyGEO** 是面向 GEO（生成式引擎优化）的 AI 工作台：挖提问词、测 AI 引用、品牌曝光诊断、多平台投放成文。帮助品牌在 ChatGPT / Gemini 等生成式引擎中被看见、被引用。

本技能调用 EasyGEO / clawEC 开放 API。
"""

AUTH = f"""## 认证与基址

- **Base URL**: `{BASE}`
- **API Key**: 在 {HOME} 注册账号，然后去 {KEY_PAGE} 获取 Key
- **请求头**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`

优先从环境变量 `EASYGEO_API_KEY` 读取密钥（兼容 `CLAWEC_API_KEY`）；未设置时向用户索取，勿硬编码。
"""

NICER = {
    "keyword": "无线耳机",
    "model": "<model_id>",
    "brand": "示例品牌",
    "description": "品牌简介",
    "products": ["产品A"],
    "keywords": ["提问词1"],
    "competitors": ["竞品A"],
    "models": ["<model_id>"],
    "url": "https://example.com/article",
    "questions": ["问题1"],
    "question": "哪款无线耳机适合通勤？",
    "prompt": "无线耳机选购",
    "seed": "无线耳机",
    "implant": "品牌植入文案",
    "platforms": ["wechat_public"],
    "name": "品牌日监测",
    "cron_date_type": "day",
    "time": "09:00",
}


def short_cmd(p: dict) -> str:
    path = p["path"]
    if path.endswith("/model/options"):
        return "model-options"
    if path.endswith("/signal/options"):
        return "signal-options"
    if path.endswith("/platform/options"):
        return "platform-options"
    if path.endswith("/image_model/options"):
        return "image-model-options"
    if path.endswith("/angle/options"):
        return "angle-options"
    if path.endswith("/candidate/add"):
        return "candidate-add"
    if path.endswith("/candidate/list"):
        return "candidate-list"
    if path.endswith("/create/batch/log/detail"):
        return "batch-detail"
    if path.endswith("/create/logs"):
        return "logs"
    if path.endswith("/create/append"):
        return "append"
    if path.endswith("/cron_task/add"):
        return "monitor-add"
    if path.endswith("/cron_task/run"):
        return "monitor-run"
    if path.endswith("/citation_monitor/series"):
        return "series"
    if path.endswith("/citation_monitor/logs"):
        return "monitor-logs"
    if path.endswith("/citation_monitor/log/detail"):
        return "monitor-detail"
    if path.endswith("/log/detail"):
        return "detail"
    return path.rstrip("/").split("/")[-1]


def fmt_inputs(plugin: dict) -> list[str]:
    rows = []
    for i in plugin.get("input") or []:
        req = "是" if i.get("required") else "否"
        rows.append(f"| {i['key']} | {i.get('type', '')} | {req} | {i.get('value', '')} |")
    return rows


def generate_query_sh(skill: dict) -> str:
    lines: list[str] = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        "",
        'API_KEY="${EASYGEO_API_KEY:-${CLAWEC_API_KEY:-}}"',
        'if [[ -z "$API_KEY" ]]; then',
        '  echo "请设置环境变量 EASYGEO_API_KEY（或 CLAWEC_API_KEY）" >&2',
        "  exit 1",
        "fi",
        f'BASE="{BASE}"',
        "",
        'CMD="${1:-}"',
        "shift || true",
        "",
        "usage() {",
        "  cat >&2 <<EOF",
        "用法: query.sh <command> [args...]",
        f'Skill: {skill["id"]}',
        "",
        "Commands:",
    ]

    unique: list[tuple[str, dict, str]] = []
    seen: set[str] = set()
    for title in skill["plugins"]:
        p = by_title[title]
        short = short_cmd(p)
        if short in seen:
            short = f"{short}-{p['path'].rstrip('/').split('/')[-1]}"
        seen.add(short)
        unique.append((short, p, title))
        args_hint = " ".join(f'<{i["key"]}>' for i in (p.get("input") or []) if i.get("required"))
        lines.append(f"  {short} {args_hint}  # {title}")

    lines += [
        "EOF",
        "  exit 1",
        "}",
        "",
        '[[ -n "$CMD" ]] || usage',
        "",
        'case "$CMD" in',
    ]

    py_payload = r"""import json, os, sys
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
"""

    for short, p, title in unique:
        method = p["method"].upper()
        path = p["path"]
        inputs = p.get("input") or []
        lines.append(f"  {short})")
        lines.append(f"    # {title}")
        if method == "GET":
            query_inputs = [i for i in inputs if i.get("type") == "query"]
            if not query_inputs:
                lines.append(f'    curl -s -X GET "$BASE{path}" -H "Authorization: Bearer $API_KEY"')
            else:
                hint = " ".join(f'<{x["key"]}>' for x in query_inputs)
                for i, inp in enumerate(query_inputs):
                    var = inp["key"].upper()
                    pos = i + 1
                    if inp.get("required"):
                        lines.append(f'    {var}="${{{pos}:?用法: query.sh {short} {hint}}}"')
                    else:
                        lines.append(f'    {var}="${{{pos}:-}}"')
                lines.append('    qs=""')
                for inp in query_inputs:
                    k = inp["key"]
                    ku = k.upper()
                    lines.append(f'    if [[ -n "${{{ku}}}" ]]; then')
                    lines.append('      [[ -n "$qs" ]] && qs="$qs&"')
                    lines.append(f'      qs="$qs{k}=${{{ku}}}"')
                    lines.append("    fi")
                lines.append('    if [[ -n "$qs" ]]; then')
                lines.append(f'      curl -s -X GET "$BASE{path}?$qs" -H "Authorization: Bearer $API_KEY"')
                lines.append("    else")
                lines.append(f'      curl -s -X GET "$BASE{path}" -H "Authorization: Bearer $API_KEY"')
                lines.append("    fi")
        else:
            body_inputs = [i for i in inputs if i.get("type") == "body"]
            query_inputs = [i for i in inputs if i.get("type") == "query"]
            if query_inputs and not body_inputs:
                for i, inp in enumerate(query_inputs):
                    lines.append(f'    Q_{inp["key"].upper()}="${{{i+1}:?需要 {inp["key"]}}}"')
                qjoin = "&".join(f'{inp["key"]}=$Q_{inp["key"].upper()}' for inp in query_inputs)
                lines.append(
                    f'    curl -s -X POST "$BASE{path}?{qjoin}" -H "Authorization: Bearer $API_KEY"'
                )
            else:
                keys = [i["key"] for i in body_inputs]
                req_keys = [i["key"] for i in body_inputs if i.get("required")]
                lines.append('    if [[ "${1:-}" == \\{* ]]; then')
                lines.append('      PAYLOAD="$1"')
                lines.append("    else")
                lines.append(f"      KEYS='{json.dumps(keys, ensure_ascii=False)}'")
                lines.append(f"      REQUIRED='{json.dumps(req_keys, ensure_ascii=False)}'")
                lines.append("      PAYLOAD=$(KEYS=\"$KEYS\" REQUIRED=\"$REQUIRED\" python3 - \"$@\" <<'PY'")
                lines.extend(py_payload.splitlines())
                lines.append("PY")
                lines.append(")")
                lines.append("    fi")
                lines.append(
                    f'    curl -s -X POST "$BASE{path}" '
                    f'-H "Content-Type: application/json" '
                    f'-H "Authorization: Bearer $API_KEY" '
                    f'-d "$PAYLOAD"'
                )
        lines.append("    ;;")

    lines += [
        "  *)",
        "    usage",
        "    ;;",
        "esac",
        "",
    ]
    return "\n".join(lines)


def write_skill(skill: dict) -> None:
    d = ROOT / "skills" / skill["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "scripts").mkdir(exist_ok=True)

    sections: list[str] = [
        "---",
        f'name: {skill["id"]}',
        f'description: {skill["description"]}',
        "---",
        "",
        f'# {skill["name"]}',
        "",
        ABOUT,
        "",
        AUTH,
        "",
        "## 接口",
        "",
    ]

    for title in skill["plugins"]:
        p = by_title[title]
        method = p["method"].upper()
        path = p["path"]
        sections.append(f"### {title}")
        sections.append("")
        sections.append(f"`{method} {path}`")
        sections.append("")
        sections.append(p.get("intro", ""))
        sections.append("")
        inputs = p.get("input") or []
        if inputs:
            sections.append("| 参数 | 位置 | 必填 | 说明 |")
            sections.append("|------|------|------|------|")
            sections.extend(fmt_inputs(p))
            sections.append("")
        else:
            sections.append("无请求参数。")
            sections.append("")

    sections.append("## 调用示例")
    sections.append("")
    for title in skill["plugins"]:
        p = by_title[title]
        method = p["method"].upper()
        path = p["path"]
        url = f"{BASE}{path}"
        sections.append(f"### {title}")
        sections.append("")
        sections.append("```bash")
        if method == "GET":
            q = [f"{i['key']}=<{i['key']}>" for i in (p.get("input") or []) if i.get("type") == "query"]
            qstr = ("?" + "&".join(q)) if q else ""
            sections.append(f'curl -s -X GET "{url}{qstr}" \\')
            sections.append('  -H "Authorization: Bearer $EASYGEO_API_KEY"')
        else:
            body = {}
            for i in p.get("input") or []:
                if i.get("type") == "body":
                    body[i["key"]] = NICER.get(i["key"], f'<{i["key"]}>')
            body_s = json.dumps(body, ensure_ascii=False)
            sections.append(f'curl -s -X POST "{url}" \\')
            sections.append('  -H "Content-Type: application/json" \\')
            sections.append('  -H "Authorization: Bearer $EASYGEO_API_KEY" \\')
            sections.append(f"  -d '{body_s}'")
        sections.append("```")
        sections.append("")

    sections.append("或使用脚本（见 `scripts/query.sh`，按子命令）。")
    sections.append("")
    sections.append("## 响应结构")
    sections.append("")
    sections.append("```json")
    sections.append('{')
    sections.append('  "status": 1,')
    sections.append('  "data": { ... }')
    sections.append("}")
    sections.append("```")
    sections.append("")
    sections.append("- `status`: `1` = 成功，`0` = 失败")
    sections.append("- 成功时解析 `data` 按用户需求整理为中文摘要（勿整段粘贴原始 JSON）")
    sections.append("- 异步类接口提交后返回记录 id，需再调详情接口")
    sections.append("")
    sections.append("## 工作流程")
    sections.append("")
    for i, step in enumerate(skill["workflow"], 1):
        sections.append(f"{i}. {step}")
    sections.append("")
    sections.append("## 输出建议")
    sections.append("")
    sections.append("- 用表格呈现核心结果")
    sections.append("- 给出 2–3 条可执行下一步")
    sections.append("- 默认简体中文")
    sections.append("")

    (d / "SKILL.md").write_text("\n".join(sections), encoding="utf-8")
    qpath = d / "scripts" / "query.sh"
    qpath.write_text(generate_query_sh(skill), encoding="utf-8")
    qpath.chmod(0o755)


AGENTS = [
    {
        "id": "easygeo-keyword",
        "title": "GEO关键词联想专家",
        "display": "EasyGEO·挖GEO提问词",
        "description": "GEO 关键词联想 Agent。调度 EasyGEO API 技能完成提问词扩展、备选词库管理。站内：/keyword",
        "skills": [
            ("easygeo-keyword-expand", "核心词扩展提问词（含模型选项）"),
            ("easygeo-keyword-detail", "回看某次联想历史"),
            ("easygeo-keyword-candidate", "备选词加入 / 列表"),
        ],
        "intent": [
            ("「扩词」「联想」「提问词」「用户会怎么问 AI」", "easygeo-keyword-expand"),
            ("「备选词」「收藏词」", "easygeo-keyword-candidate"),
            ("给出历史记录 id", "easygeo-keyword-detail"),
        ],
        "flows": [
            ("挖词闭环", "① expand → ② candidate 收藏优质词 → ③ 建议转引用评估 / 成文"),
        ],
        "accept": "GEO 提问词、词语联想、备选词库",
        "reject": "平台销量选品 → clawec-agents；完整成文 → easygeo-content；品牌曝光得分 → easygeo-brand-score；引用评估 → easygeo-citation",
        "path": "/keyword",
    },
    {
        "id": "easygeo-citation",
        "title": "GEO引用评估专家",
        "display": "EasyGEO·测AI引用",
        "description": "GEO 引用评估 Agent。多模型检测品牌提及与引用来源，支持旁路信号与定时监测。站内：/citation-eval /monitor",
        "skills": [
            ("easygeo-citation-eval", "发起多模型引用评估（含模型/信号选项）"),
            ("easygeo-citation-detail", "拉取评估详情"),
            ("easygeo-citation-monitor", "定时监测任务与历史序列"),
        ],
        "intent": [
            ("「引用评估」「品牌有没有被 AI 提到」「来源域名」", "easygeo-citation-eval"),
            ("「评估详情」「查结果」+ id", "easygeo-citation-detail"),
            ("「定时监测」「每天跑」「引用趋势」", "easygeo-citation-monitor"),
        ],
        "flows": [
            ("单次评估", "① eval → ② detail 轮询 → ③ 提及/域名/竞品结论"),
            ("持续监测", "① monitor-add → ② monitor-run / 等 cron → ③ series / logs"),
        ],
        "accept": "引用评估、品牌提及、来源域名、旁路信号、定时监测",
        "reject": "纯扩词 → easygeo-keyword；品牌得分全流程 → easygeo-brand-score；成文 → easygeo-content；推广链接检测 → easygeo-promo-link",
        "path": "/citation-eval",
    },
    {
        "id": "easygeo-brand-score",
        "title": "GEO品牌诊断专家",
        "display": "EasyGEO·品牌曝光得分",
        "description": "GEO 品牌诊断 Agent。prepare 生成关键词/竞品后发起多模型品牌曝光得分检测。站内：/brand-score",
        "skills": [
            ("easygeo-brand-score-prepare", "生成关键词与竞品"),
            ("easygeo-brand-score-eval", "发起检测"),
            ("easygeo-brand-score-detail", "拉取得分详情"),
        ],
        "intent": [
            ("「品牌得分」「曝光诊断」「准备关键词竞品」", "easygeo-brand-score-prepare"),
            ("「开始检测」「跑得分」", "easygeo-brand-score-eval"),
            ("「得分结果」+ id", "easygeo-brand-score-detail"),
        ],
        "flows": [
            ("诊断闭环", "① prepare → 用户确认 keywords/competitors → ② eval → ③ detail"),
        ],
        "accept": "品牌得分、曝光诊断、竞品对比",
        "reject": "单次提问引用深挖 → easygeo-citation；成文 → easygeo-content；纯扩词 → easygeo-keyword",
        "path": "/brand-score",
    },
    {
        "id": "easygeo-content",
        "title": "GEO内容投放专家",
        "display": "EasyGEO·写GEO投放文",
        "description": "GEO 内容投放 Agent。生成建议写作方向并多平台正式成文。站内：/text",
        "skills": [
            ("easygeo-text-generate", "生成建议写作方向（非正文）"),
            ("easygeo-text-create", "多平台正式成文 / 追加平台"),
            ("easygeo-text-detail", "批次/分项结果查询"),
        ],
        "intent": [
            ("「写作方向」「给几个角度」", "easygeo-text-generate"),
            ("「正式成文」「写公众号/小红书/知乎」", "easygeo-text-create"),
            ("「查批次」「成文结果」", "easygeo-text-detail"),
        ],
        "flows": [
            ("成文闭环", "①（可选）generate 选方向 → ② create（seed+implant+prompt+platforms）→ ③ detail"),
        ],
        "accept": "写作方向、多平台成文、追加平台、封面相关",
        "reject": "纯扩词 → easygeo-keyword；引用评估 → easygeo-citation；品牌得分 → easygeo-brand-score；电商主图套图 → clawec-agents",
        "path": "/text",
    },
    {
        "id": "easygeo-promo-link",
        "title": "GEO推广链接检测专家",
        "display": "EasyGEO·测推广链接",
        "description": "GEO 推广链接检测 Agent。抓取链接生成问题并多模型检测引用表现。站内：/promo-link",
        "skills": [
            ("easygeo-promo-link-prepare", "抓取链接并生成检测问题"),
            ("easygeo-promo-link-eval", "发起检测"),
            ("easygeo-promo-link-detail", "拉取检测详情"),
        ],
        "intent": [
            ("「推广链接」「这篇文章有没有被引用」「检测 URL」", "easygeo-promo-link-prepare"),
            ("「开始检测」", "easygeo-promo-link-eval"),
            ("「链接检测结果」+ id", "easygeo-promo-link-detail"),
        ],
        "flows": [
            ("检测闭环", "① prepare → 确认 questions → ② eval → ③ detail"),
        ],
        "accept": "推广链接抓取、问题生成、链接引用检测",
        "reject": "纯提问词评估（无 URL）→ easygeo-citation；成文 → easygeo-content",
        "path": "/promo-link",
    },
]


def write_agent(a: dict) -> None:
    d = ROOT / "agents" / a["id"]
    d.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f'name: {a["id"]}',
        f'description: {a["description"]}',
        "---",
        "",
        f'# {a["title"]}（{a["display"]}）',
        "",
        f'你是 **{a["id"]}**（{a["display"]}）。所有数据必须通过 `.easygeo/skills/` 下对应 Skill 调用 EasyGEO API 获取；禁止编造联想词、引用结果、品牌得分或成文内容。',
        "",
        "## 站内入口",
        "",
        "| 类型 | 路径 |",
        "|------|------|",
        f'| 站内功能 | {a["path"]} |',
        "| API Key | /api-key |",
        "| 完整站点 | https://geo.clawec.com |",
        "",
        "## 核心使命",
        "",
        "1. 理解用户的品牌 / 关键词 / 链接 / 平台与目标",
        "2. **选择并加载**正确的 Skill，严格按 `SKILL.md` 执行",
        "3. 将结果整理为**中文、可执行**的摘要",
        "",
        "## 认证与调用",
        "",
        "执行任何 `.easygeo/skills/` 技能前，须先阅读该 Skill 的 `SKILL.md`：其中包含 Base URL、环境变量、请求头与示例。密钥使用 `EASYGEO_API_KEY`。",
        "",
        "## 技能清单（执行细节在各 Skill 内，此处不重复）",
        "",
        "| Skill | 路径 | 何时使用 |",
        "|-------|------|----------|",
    ]
    for sid, when in a["skills"]:
        lines.append(
            f"| {sid} | [.easygeo/skills/{sid}/SKILL.md](../../skills/{sid}/SKILL.md) | {when} |"
        )
    lines += [
        "",
        "## 调度规则",
        "",
        "### 1. 按用户意图选 Skill",
        "",
        "| 用户意图 | 首选 Skill |",
        "|----------|------------|",
    ]
    for intent, sid in a["intent"]:
        lines.append(f"| {intent} | {sid} |")
    lines += [
        "",
        "### 2. 常见组合工作流",
        "",
        "| 场景 | 步骤 |",
        "|------|------|",
    ]
    for name, steps in a["flows"]:
        lines.append(f"| **{name}** | {steps} |")
    lines += [
        "",
        "每步开始前：**读取对应 SKILL.md**，按其中脚本/接口执行。",
        "",
        "## 边界（防串号）",
        "",
        f'- **接**：{a["accept"]}',
        f'- **不接**：{a["reject"]}',
        "",
        "## 必须遵守",
        "",
        "1. **先读 Skill 再调 API**：禁止跳过 `.easygeo/skills/easygeo-*/SKILL.md` 凭记忆拼请求",
        "2. **禁止虚构**：无 API 结果时明确说明，不编造词表、得分、引用或正文",
        "3. **不复制 Skill 正文**：本文件只做路由；参数、字段、脚本以各 Skill 为准",
        "4. **异步闭环**：eval/create 类接口提交后必须拉详情；未完成则说明状态并建议稍后重试",
        "5. **失败处理**：`status !== 1` 时报告错误并提示检查 Key 与必填参数（可能消耗积分）",
        "6. **输出语言**：默认简体中文；禁止整段粘贴原始 JSON",
        "",
        "## 标准输出结构",
        "",
        "```markdown",
        "## 任务摘要",
        "- 目标 / 品牌 / 关键词 / 链接",
        "- 使用的 Skill 列表",
        "",
        "## 数据结果",
        "（表格 + 关键指标）",
        "",
        "## 观察",
        "（2–5 条）",
        "",
        "## 建议下一步",
        "```",
        "",
        "## 激活方式",
        "",
        f'- 使用规则：`@{a["id"]}`',
        f'- 或说明：「使用 {a["id"]} Agent」',
        "",
    ]
    (d / "AGENT.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for skill in SKILLS:
        write_skill(skill)
        print("skill", skill["id"])
    for a in AGENTS:
        write_agent(a)
        print("agent", a["id"])
    print("done", len(SKILLS), "skills,", len(AGENTS), "agents")


if __name__ == "__main__":
    main()
