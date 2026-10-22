---
name: easygeo-brand-score-eval
description: 发起 EasyGEO 多模型品牌曝光得分检测（异步）。需先 prepare 并确认 keywords/competitors。
---

# GEO品牌得分-发起检测

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

### GEO品牌得分-发起检测

`POST /aigc/geo/brand_score/eval`

异步：立即返回记录 id。完成后 WebSocket type=geo_brand_score_result_refresh；客户端用「GEO品牌得分-详情」拉取。models 从模型选项获取；keywords/competitors 至少各 1 个（通常来自 prepare 确认）。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| models | body | 是 | 模型 ID 列表（ContentModel.uuid），从 /aigc/geo/brand_score/model/options 获取 |
| brand | body | 是 | 品牌名称 |
| description | body | 否 | 品牌描述（可选，报告展示） |
| products | body | 否 | 产品服务列表 |
| keywords | body | 是 | 主题关键词列表（客户端确认后回传） |
| competitors | body | 是 | 竞争对手列表（客户端确认后回传） |

## 调用示例

### GEO品牌得分-发起检测

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/brand_score/eval" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"models": ["<model_id>"], "brand": "示例品牌", "description": "品牌简介", "products": ["产品A"], "keywords": ["提问词1"], "competitors": ["竞品A"]}'
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

1. GET /aigc/geo/brand_score/model/options 取 models
2. POST /aigc/geo/brand_score/eval（models/brand/keywords/competitors 等）
3. 拿到记录 id 后用 easygeo-brand-score-detail 拉结果

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
