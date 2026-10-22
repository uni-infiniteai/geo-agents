---
name: easygeo-keyword-expand
description: 通过 EasyGEO API 根据核心词扩展 GEO 提问词。在用户需要挖词、关键词联想、扩展搜索问法时使用。先取模型选项再调用联想。
---

# GEO关键词联想

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

### GEO关键词联想-模型选项

`GET /aigc/geo/keyword/model/options`

返回关键词联想可用大模型列表（id/title/pointsPer1kToken）。调用「GEO关键词联想」前先取 model。

无请求参数。

### GEO关键词联想

`POST /aigc/geo/keyword/expand`

根据核心投放关键词同步生成约 10 条扩展搜索词，落库后直接返回完整结果（含记录 id），无需 WebSocket。model 从「GEO关键词联想-模型选项」获取。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| keyword | body | 是 | 核心投放关键词 |
| model | body | 是 | 大模型 ID，从 /aigc/geo/keyword/model/options 获取 |

## 调用示例

### GEO关键词联想-模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/keyword/model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO关键词联想

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/keyword/expand" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"keyword": "无线耳机", "model": "<model_id>"}'
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

1. 确认核心关键词 keyword（保持用户原词语言）
2. GET /aigc/geo/keyword/model/options 选取 model
3. POST /aigc/geo/keyword/expand 传入 keyword + model
4. 整理扩展提问词表；可建议加入备选词库或继续引用评估/成文

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
