---
name: easygeo-text-create
description: 按平台正式生成 GEO 投放文（异步）。须带回 seed + implant + prompt（建议写作方向）。支持追加平台。
---

# GEO文案-正式成文

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

### GEO文案-正式生成

`POST /aigc/geo/text/create`

正式生成文章。请传入 seed=关键词、implant=品牌植入、prompt=建议写作方向、platforms=目标平台列表、model。返回 batchId；多平台会先写批次再写分项。封面：cover_mode=none|single|multi。完成后 WebSocket common_text_batch_result_refresh / common_text_result_refresh，再用批次/分项详情拉取。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| platforms | body | 是 | 目标平台 type 列表，从 /platform/options 获取 |
| prompt | body | 是 | 建议写作方向 |
| seed | body | 否 | 关键词/种子（正式成文建议必传） |
| implant | body | 否 | 品牌植入原文案 |
| model | body | 否 | 大模型 id |
| cover | body | 否 | 是否生成封面（兼容旧字段；与 cover_mode 二选一） |
| cover_mode | body | 否 | 封面模式 none/single/multi；不传则按 cover 兼容 |
| cover_count | body | 否 | 多图张数；cover_mode=multi 时必填，2~9 |
| cover_prompt_mode | body | 否 | 多图提示词模式 ai_split / user_input；multi 时必填 |
| image_model | body | 否 | 图片大模型 id |
| image_prompt | body | 否 | 图片提示词；多图 user_input 可用 --- 分隔 |
| image_prompts | body | 否 | 多图用户输入提示词列表；user_input 时优先，条数=cover_count |
| groupId | body | 否 | 写作分类 itemId（可选） |
| promptId | body | 否 | 写作方向库 GeoPrompt.id（可选，成文后自动标记已使用） |

### GEO文案-追加平台写作

`POST /aigc/geo/text/create/append`

在已有批次上追加平台文案（不新建批次）。必传 batchId + platforms；其余字段不传则沿用批次原值。返回同一 batchId。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| batchId | body | 是 | 已有批次记录 id |
| platforms | body | 是 | 要追加的目标平台 type 列表 |
| prompt | body | 否 | 建议写作方向；不传则沿用批次 |
| seed | body | 否 | 关键词；不传则沿用批次 |
| implant | body | 否 | 品牌植入；不传则沿用批次 |
| model | body | 否 | 大模型 id；不传则沿用批次 |
| cover_mode | body | 否 | 封面模式 none/single/multi；不传则沿用批次 |
| image_model | body | 否 | 图片大模型 id；不传则沿用批次 |

## 调用示例

### GEO文案-正式生成

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/text/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"platforms": ["wechat_public"], "prompt": "无线耳机选购", "seed": "无线耳机", "implant": "品牌植入文案", "model": "<model_id>", "cover": "<cover>", "cover_mode": "<cover_mode>", "cover_count": "<cover_count>", "cover_prompt_mode": "<cover_prompt_mode>", "image_model": "<image_model>", "image_prompt": "<image_prompt>", "image_prompts": "<image_prompts>", "groupId": "<groupId>", "promptId": "<promptId>"}'
```

### GEO文案-追加平台写作

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/text/create/append" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"batchId": "<batchId>", "platforms": ["wechat_public"], "prompt": "无线耳机选购", "seed": "无线耳机", "implant": "品牌植入文案", "model": "<model_id>", "cover_mode": "<cover_mode>", "image_model": "<image_model>"}'
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

1. GET platform/options 选 platforms；取 model（及可选 image_model）
2. POST /aigc/geo/text/create：platforms + prompt + seed + implant + model
3. 可选封面 cover_mode / image_* 参数
4. 用 easygeo-text-detail 拉 batchId 结果；追加平台用 /create/append

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
