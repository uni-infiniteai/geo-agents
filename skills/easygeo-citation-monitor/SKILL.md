---
name: easygeo-citation-monitor
description: 创建/执行品牌引用定时监测任务，并查询时间序列与运行历史。适合持续跟踪品牌在 AI 中的曝光。
---

# GEO引用监测

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

### GEO引用监测-添加定时任务

`POST /aigc/geo/citation_monitor/cron_task/add`

创建引用定时监测任务：按日程对 keywords 逐词做引用评估。cron_date_type=day|week|month|once；week 填 weeks；month 填 days；once 填 day(yyyy-MM-dd)。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| name | body | 是 | 任务名称 |
| cron_date_type | body | 是 | 定时类型 day=每天 week=每周 month=每月 once=单次 |
| time | body | 是 | 执行时刻，如 00:00 / 00:30 / 01:30（每 30 分钟一档） |
| weeks | body | 否 | 每周星期几，cron_date_type=week 时必填；0=周日…6=周六，多选用英文逗号分隔 |
| days | body | 否 | 每月几号，cron_date_type=month 时必填，如 1,3,5,10 |
| day | body | 否 | 具体日期，cron_date_type=once 时必填，格式 2026-01-01 |
| enable | body | 否 | 是否开启 |
| notifyEmail | body | 否 | 完成后通知邮箱（选填） |
| models | body | 是 | 评估模型 ID 列表（与引用评估模型池相同） |
| brand | body | 是 | 目标品牌关键词 |
| competitors | body | 否 | 竞争对手品牌列表（可选，最多 8 个） |
| keywords | body | 是 | 监测查询关键词列表（每次跑任务会逐词评估） |

### GEO引用监测-立即执行

`POST /aigc/geo/citation_monitor/cron_task/run`

立即执行一次已配置的监测任务（不等待定时触发）。异步：立即返回汇总记录 id（status=appending），完成后用「GEO引用监测-运行详情」或 /logs 查看；子记录详情可复用「GEO引用评估-详情」。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| item_id | query | 是 | 定时监测任务 itemId |

### GEO引用监测-时间序列

`GET /aigc/geo/citation_monitor/series`

按监测任务 item_id 拉取时间序列数据，用于趋势图。可选 begin/end（时间戳）、limit（默认 200）。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| item_id | query | 是 | 监测任务 itemId（整型） |
| begin | query | 否 | 开始时间戳，0 表示不限 |
| end | query | 否 | 结束时间戳，0 表示不限 |
| limit | query | 否 | 返回条数上限，默认 200 |

### GEO引用监测-运行历史

`GET /aigc/geo/citation_monitor/logs`

监测任务运行历史列表。可选 item_id 过滤；分页参数与系统 PageBaseParam 一致（如 start/size）。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| item_id | query | 否 | 监测任务 itemId，0 或不传表示不过滤 |
| start | query | 否 | 分页起始 |
| size | query | 否 | 分页大小 |

### GEO引用监测-运行详情

`GET /aigc/geo/citation_monitor/log/detail`

按运行记录 id 查询一次监测汇总详情。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| id | query | 是 | 运行记录 id |

## 调用示例

### GEO引用监测-添加定时任务

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/citation_monitor/cron_task/add" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"name": "品牌日监测", "cron_date_type": "day", "time": "09:00", "weeks": "<weeks>", "days": "<days>", "day": "<day>", "enable": "<enable>", "notifyEmail": "<notifyEmail>", "models": ["<model_id>"], "brand": "示例品牌", "competitors": ["竞品A"], "keywords": ["提问词1"]}'
```

### GEO引用监测-立即执行

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/citation_monitor/cron_task/run" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{}'
```

### GEO引用监测-时间序列

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/citation_monitor/series?item_id=<item_id>&begin=<begin>&end=<end>&limit=<limit>" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO引用监测-运行历史

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/citation_monitor/logs?item_id=<item_id>&start=<start>&size=<size>" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO引用监测-运行详情

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/citation_monitor/log/detail?id=<id>" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
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

1. 添加：POST /aigc/geo/citation_monitor/cron_task/add
2. 立即跑：POST /aigc/geo/citation_monitor/cron_task/run?item_id=
3. 序列：GET /series；历史：GET /logs；详情：GET /log/detail

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
