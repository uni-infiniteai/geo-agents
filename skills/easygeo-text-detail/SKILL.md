---
name: easygeo-text-detail
description: 查询 GEO 成文批次详情、分项详情或分项列表。
---

# GEO文案-结果查询

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

### GEO文案-批次详情

`GET /aigc/geo/text/create/batch/log/detail`

按批次 id 查询文案生成批次汇总（成功/失败/生成中计数、分项引用等）。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| id | query | 是 | 批次记录 id（/create 返回的 batchId） |

### GEO文案-分项详情

`GET /aigc/geo/text/log/detail`

按分项记录 id 查询单平台文案生成结果（正文、封面等）。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| id | query | 是 | 分项记录 id |

### GEO文案-分项结果列表

`GET /aigc/geo/text/create/logs`

查询文案生成分项结果列表。可按 batch_id 过滤某批次下的平台分项。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| batch_id | query | 否 | 批次 id，0 或不传表示不过滤 |
| start | query | 否 | 分页起始 |
| size | query | 否 | 分页大小 |

## 调用示例

### GEO文案-批次详情

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/create/batch/log/detail?id=<id>" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-分项详情

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/log/detail?id=<id>" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-分项结果列表

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/create/logs?batch_id=<batch_id>&start=<start>&size=<size>" \
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

1. 批次：GET /aigc/geo/text/create/batch/log/detail?id=
2. 分项：GET /aigc/geo/text/log/detail?id=
3. 列表：GET /aigc/geo/text/create/logs?batch_id=

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
