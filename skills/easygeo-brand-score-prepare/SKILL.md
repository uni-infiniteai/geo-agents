---
name: easygeo-brand-score-prepare
description: 根据产品服务列表生成品牌诊断用的主题关键词与竞品。在用户做品牌曝光得分前的 prepare 步骤使用。品牌名不参与拆词。
---

# GEO品牌得分-准备

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

### GEO品牌得分-模型选项

`GET /aigc/geo/brand_score/model/options`

返回品牌得分检测可用评估模型（可联网）。调用 prepare/eval 前先取 models。

无请求参数。

### GEO品牌得分-生成关键词与竞品

`POST /aigc/geo/brand_score/prepare`

同步：仅按「产品服务」拆解主题关键词与竞争对手（品牌名不参与生成，仅用于排除自有品牌；品牌描述仅回显）。客户端确认/修改后调用「GEO品牌得分-发起检测」。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| brand | body | 是 | 品牌名称（不参与关键词生成，仅用于排除竞品中的自有品牌） |
| description | body | 是 | 品牌描述（不参与生成，仅回显给报告，最长 500） |
| products | body | 是 | 产品服务列表（至少一个）；主题关键词与竞争对手均按此拆解 |

## 调用示例

### GEO品牌得分-模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/brand_score/model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO品牌得分-生成关键词与竞品

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/brand_score/prepare" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"brand": "示例品牌", "description": "品牌简介", "products": ["产品A"]}'
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

1. 收集 brand / description / products（至少一个产品）
2. POST /aigc/geo/brand_score/prepare
3. 展示 keywords / competitors 供用户确认或微调
4. 再进入 easygeo-brand-score-eval

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
