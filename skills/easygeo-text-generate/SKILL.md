---
name: easygeo-text-generate
description: 根据关键词/种子提示词生成 GEO 建议写作方向（不是正文）。正式成文请用 easygeo-text-create。
---

# GEO文案-生成写作方向

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

### GEO文案-平台选项

`GET /aigc/geo/text/platform/options`

返回可写作目标平台 type/desc：wechat_public/weibo/toutiao/douyin_text/xiaohongshu/zhihu/baijiahao/netease/sohu/csdn/baidu_baike/wiki_baike 等。

无请求参数。

### GEO文案-大模型选项

`GET /aigc/geo/text/model/options`

返回文案生成可用大模型（id/title/pointsPer1kToken）。

无请求参数。

### GEO文案-图片模型选项

`GET /aigc/geo/text/image_model/options`

返回封面图可用图片模型；point 为每张封面积分。

无请求参数。

### GEO文案-写作角度选项

`GET /aigc/geo/text/angle/options`

返回建议写作方向可用角度：definition/how_to/comparison/scenario/faq/buying_guide/roi/trend/risk/practice。供「生成建议写作方向」的 angles 多选。

无请求参数。

### GEO文案-生成建议写作方向

`POST /aigc/geo/text/generate`

同步生成文章建议写作方向（不是完整正文）。正式成文时请一并传入：关键词 seed + 品牌植入 implant + 本条建议写作方向 prompt。count 默认 20，最大 50。

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| prompt | body | 是 | 关键词/种子提示词（主题检索词或内容方向） |
| model | body | 是 | 大模型 id，从 /aigc/geo/text/model/options 获取 |
| count | body | 否 | 生成条数，不传默认 20，范围 1~50 |
| implant | body | 否 | 品牌植入原文案（强烈建议传入） |
| angles | body | 否 | GEO 写作角度 type 列表，从 /angle/options 获取 |

## 调用示例

### GEO文案-平台选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/platform/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-大模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-图片模型选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/image_model/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-写作角度选项

```bash
curl -s -X GET "https://www.clawec.com/api/aigc/geo/text/angle/options" \
  -H "Authorization: Bearer $EASYGEO_API_KEY"
```

### GEO文案-生成建议写作方向

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/geo/text/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EASYGEO_API_KEY" \
  -d '{"prompt": "无线耳机选购", "model": "<model_id>", "count": "<count>", "implant": "品牌植入文案", "angles": "<angles>"}'
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

1. 取 model/options，可选 angle/options
2. POST /aigc/geo/text/generate（prompt/model，可选 count/implant/angles）
3. 编号列出方向供用户选择；选中后进入 create

## 输出建议

- 用表格呈现核心结果
- 给出 2–3 条可执行下一步
- 默认简体中文
