---
name: easygeo-citation-eval
description: 多模型检测 AI 回答中品牌是否被提及、引用来源与竞品对比。支持可选 Google Trends / Reddit 旁路信号。
---

# GEO引用评估

## 关于 EasyGEO

**EasyGEO** 是面向 GEO（生成式引擎优化）的 AI 工作台：挖提问词、测 AI 引用、品牌曝光诊断、多平台投放成文。帮助品牌在 ChatGPT / Gemini 等生成式引擎中被看见、被引用。

本技能调用 EasyGEO / clawEC 开放 API。


## 认证与基址

- **Base URL**: `https://www.clawec.com/api`
- **API Key**: 在 https://geo.clawec.com 注册账号，然后去 https://geo.clawec.com/zh-cn/api-key 获取 Key
- **请求头**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <API_KEY>`

优先从环境变量 `EASYGEO_API_KEY` 读取密钥（兼容 `CLAWEC_API_KEY`）；未设置时向用户索取，勿硬编码。


## 接口

### GEO引用评估-模型选项

`GET /aigc/geo/citation_eval/model/options`

返回引用评估可用联网模型列表。

无请求参数。

### GEO引用评估-旁路信号选项

`GET /aigc/geo/citation_eval/signal/options`

返回可与引用评估一并拉取的旁路信号（如 google_trend / reddit），供 eval 的 signals 字段勾选。

无请求参数。

### GEO引用评估-发起

`POST /aigc/geo/citation_eval/eval`

异步多模型引用评估。question 与 questions 二选一（questions 优先，1~20 条，每问独立历史记录）。立即返回记录 id 列表；完成后 WebSocket type=geo_citation_eval_result_refresh，再用「GEO引用评估-详情」拉取。可选 signals、competitors、region、redditScene、redditLimit。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| models | body | 是 | 模型 ID 列表，从 /aigc/geo/citation_eval/model/options 获取 |
| brand | body | 是 | 目标品牌关键词 |
| question | body | 否 | 单问题（与 questions 二选一；批量时可不传） |
| questions | body | 否 | 一次提交多个问题（1~20）；与 question 同时传时以本字段为准 |
| competitors | body | 否 | 竞争对手品牌列表（可选，最多 8 个） |
| signals | body | 否 | 旁路信号勾选：google_trend / reddit（可多选） |
| region | body | 否 | Google Trends 地区，ISO 3166-1 alpha-2，默认 US（仅勾选 google_trend 时有效） |
| redditScene | body | 否 | Reddit 场景：空/common=语义搜索，biz=商机搜索 |
| redditLimit | body | 否 | Reddit 返回条数，默认 20，最大 50 |

## 调用示例

### GEO引用评估-模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/citation_eval/model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO引用评估-旁路信号选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/citation_eval/signal/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO引用评估-发起

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/citation_eval/eval" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"models": ["<model_id>"], "brand": "示例品牌", "question": "哪款无线耳机适合通勤？", "questions": ["问题1"], "competitors": ["竞品A"], "signals": "<signals>", "region": "<region>", "redditScene": "<redditScene>", "redditLimit": "<redditLimit>"}'
```

或使用脚本（见 `scripts/query.sh`，按子命令）。

## 响应结构

```json
{
  "status": 1,
  "data": { ... }
}
```

- `status`: `1` = 成功，`0` = 失败
- 成功时解析 `data` 按用户需求整理为中文摘要（勿整段粘贴原始 JSON）
- 异步类接口提交后返回记录 id，需再调详情接口

## 工作流程

1. 确认 brand、question 或 questions（1~20）、可选 competitors / signals
2. GET model/options 与可选 signal/options
3. POST /aigc/geo/citation_eval/eval
4. 用 easygeo-citation-detail 拉异步结果

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
