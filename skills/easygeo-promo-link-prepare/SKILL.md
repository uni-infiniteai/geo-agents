---
name: easygeo-promo-link-prepare
description: 抓取推广链接并智能生成检测问题。在用户要检查某篇文章/落地页在 AI 中的引用表现前使用。
---

# GEO推广链接-准备

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

### GEO推广链接-模型选项

`GET /aigc/geo/promo_link/model/options`

返回推广链接检查可用评估模型。调用 prepare/eval 前先取 models。

无请求参数。

### GEO推广链接-抓取并生成问题

`POST /aigc/geo/promo_link/prepare`

同步：抓取网页标题与正文摘要，并智能生成最多 5 个检测问题。确认/修改后调用「GEO推广链接-发起检测」。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| url | body | 是 | 推广链接 URL |

## 调用示例

### GEO推广链接-模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/promo_link/model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO推广链接-抓取并生成问题

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/promo_link/prepare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"url": "https://example.com/article"}'
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

1. 确认 url
2. POST /aigc/geo/promo_link/prepare {url}
3. 展示 title / questions 供确认
4. 再进入 easygeo-promo-link-eval

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
