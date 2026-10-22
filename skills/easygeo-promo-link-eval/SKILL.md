---
name: easygeo-promo-link-eval
description: 对推广链接发起多模型引用/提及检测（异步）。
---

# GEO推广链接-发起检测

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

### GEO推广链接-发起检测

`POST /aigc/geo/promo_link/eval`

异步：立即返回记录 id。questions 至少 1 个、最多 5 个；questionMode=auto|custom。完成后 WebSocket 通知，再用「GEO推广链接-详情」拉取。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| models | body | 是 | 模型 ID 列表，从 /aigc/geo/promo_link/model/options 获取 |
| url | body | 是 | 推广链接 URL |
| title | body | 否 | 文章标题（可由 prepare 回传；为空时 eval 会再抓一次） |
| questions | body | 是 | 检测问题列表，至少 1 个、最多 5 个 |
| questionMode | body | 否 | 问题来源：auto=智能匹配 custom=自定义 |

## 调用示例

### GEO推广链接-发起检测

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/promo_link/eval" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"models": ["<model_id>"], "url": "https://example.com/article", "title": "<title>", "questions": ["问题1"], "questionMode": "<questionMode>"}'
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

1. GET /aigc/geo/promo_link/model/options 取 models
2. POST /aigc/geo/promo_link/eval（models/url/questions，可选 title、questionMode）
3. 用 easygeo-promo-link-detail 拉结果

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
