# EasyGEO Agents

## 关于 EasyGEO

**EasyGEO** 是面向 GEO（生成式引擎优化）的 AI 工作台：挖提问词、测 AI 引用、品牌曝光诊断、推广链接检测、多平台投放成文。帮助品牌在 ChatGPT / Gemini 等生成式引擎中被看见、被引用。

官网：[https://geo.clawec.com](https://geo.clawec.com)

## 本仓库

**EasyGEO Agents** 是 EasyGEO 的 Agent 开源仓库：面向 GEO 场景的 **AI Agent** 定义与安装脚本。每个 Agent 负责理解业务意图、调度 `.easygeo/skills/` 下的 API 能力，并按规定格式交付结果；可安装到 Cursor、Claude Code 等主流 AI 编程工具中使用。

当前技能覆盖关键词联想、品牌得分、引用评估/监测、推广链接检测、GEO 文案共 **15** 个 API Skill（对齐 `server/docs/插件库-GEO接口.json`）。

与站内 WorkBuddy 专家（`geo/workbuddy/experts-mcp`）能力对齐，并额外提供推广链接检测 Agent。

## Agents

| Agent | 说明 | 技能数 | 站内 | 定义 |
|-------|------|--------|------|------|
| **easygeo-keyword** | 挖 GEO 提问词：关键词联想、备选词库 | 3 | [/keyword](https://www.clawec.com/keyword?source=q-github-geo) | [agents/easygeo-keyword/AGENT.md](agents/easygeo-keyword/AGENT.md) |
| **easygeo-citation** | 测 AI 引用：多模型评估、旁路信号、定时监测 | 3 | [/citation-eval](https://www.clawec.com/citation-eval?source=q-github-geo) | [agents/easygeo-citation/AGENT.md](agents/easygeo-citation/AGENT.md) |
| **easygeo-brand-score** | 品牌曝光得分：prepare → eval → 详情 | 3 | [/brand-score](https://www.clawec.com/brand-score?source=q-github-geo) | [agents/easygeo-brand-score/AGENT.md](agents/easygeo-brand-score/AGENT.md) |
| **easygeo-content** | 写 GEO 投放文：写作方向 + 多平台成文 | 3 | [/text](https://www.clawec.com/text?source=q-github-geo) | [agents/easygeo-content/AGENT.md](agents/easygeo-content/AGENT.md) |
| **easygeo-promo-link** | 测推广链接：抓取问题 + 多模型检测 | 3 | [/promo-link](https://www.clawec.com/promo-link?source=q-github-geo) | [agents/easygeo-promo-link/AGENT.md](agents/easygeo-promo-link/AGENT.md) |

## 仓库结构

```text
geo-agents/
├── README.md
├── agents/                    # Agent 源定义
│   └── easygeo-<agent-name>/AGENT.md
├── skills/                    # EasyGEO API 技能源（安装时同步到用户项目的 .easygeo/skills/）
│   └── easygeo-<skill-name>/SKILL.md
└── scripts/install.sh
```

---

## 安装与使用

### Supported Tools

| 工具 | 输出位置 | 安装命令 |
|------|----------|----------|
| **Cursor** | `.cursor/skills/<agent>/SKILL.md` | `./scripts/install.sh --tool cursor .` |
| **Claude Code** | `.claude/agents/*.md`（可选 `--global` → `~/.claude/agents/`） | `./scripts/install.sh --tool claude-code .` |
| **Codex** | `.agents/skills/<agent>/SKILL.md` | `./scripts/install.sh --tool codex .` |
| **GitHub Copilot** | `~/.github/agents/` + `~/.copilot/agents/` | `./scripts/install.sh --tool copilot .` |
| **Antigravity** | `~/.gemini/antigravity/skills/easygeo-<agent>/` | `./scripts/install.sh --tool antigravity .` |
| **Gemini CLI** | `~/.gemini/extensions/geo-agents/` | `./scripts/install.sh --tool gemini-cli .` |
| **OpenCode** | `.opencode/agents/` | `./scripts/install.sh --tool opencode .` |
| **Aider** | `./CONVENTIONS.md` | `./scripts/install.sh --tool aider .` |
| **Windsurf** | `./.windsurfrules` | `./scripts/install.sh --tool windsurf .` |
| **OpenClaw** | `~/.openclaw/geo-agents/<agent>/` | `./scripts/install.sh --tool openclaw .` |
| **Qwen Code** | `.qwen/agents/` | `./scripts/install.sh --tool qwen .` |
| **Kimi Code** | `~/.config/kimi/agents/<agent>/` | `./scripts/install.sh --tool kimi .` |

交互式多选安装（自动检测本机已安装工具）：

```bash
./scripts/install.sh --tool all
# 或非交互：./scripts/install.sh --no-interactive --tool all
# 并行：./scripts/install.sh --no-interactive --tool all --parallel
```

所有工具安装时，除 `--rules-only` 外都会将本仓库 **`skills/`** 同步到目标项目的 **`.easygeo/skills/`**（EasyGEO API 文档；Agent 内链接亦会改写为该路径）。

**快速安装：**

```bash
git clone https://github.com/uni-infiniteai/geo-agents.git
cd your-project

# Cursor
/path/to/geo-agents/scripts/install.sh --tool cursor .

# Claude Code
/path/to/geo-agents/scripts/install.sh --tool claude-code .
```

一条命令安装：

```bash
export EASYGEO_SKILLS_GIT="https://github.com/uni-infiniteai/geo-agents.git"
curl -fsSL https://raw.githubusercontent.com/uni-infiniteai/geo-agents/main/scripts/install.sh | bash -s -- --tool claude-code .
```

仅更新 Agent 定义（已有 `.easygeo/skills/`）：`./scripts/install.sh --tool <工具> . --rules-only`

### 前置条件

- macOS / Linux / WSL，已安装 `bash`
- 在**业务项目根目录**执行安装（命令中的 `.` 或你的项目路径）
- 已配置 **EasyGEO API Key**（见下一节）

### API Key 获取与环境变量

各 `.easygeo/skills/` 下的接口调用都需要 API Key。Agent 与脚本优先从环境变量 **`EASYGEO_API_KEY`** 读取（兼容 `CLAWEC_API_KEY`），请勿把 Key 写进代码或提交到 git。

#### 1. 获取 Key

1. 打开 [注册页](https://geo.clawec.com) 注册账号  
2. 登录后打开 [API Key 页面](https://www.clawec.com/api-key?source=q-github-geo) 创建或复制 Key  

#### 2. 写入环境变量

**当前终端会话（临时，关闭终端后失效）：**

```bash
export EASYGEO_API_KEY="你的密钥"
```

**长期生效（推荐，macOS / Linux zsh）：**

```bash
echo 'export EASYGEO_API_KEY="你的密钥"' >> ~/.zshrc
source ~/.zshrc
```

## 与 clawec-agents / WorkBuddy 的关系

| 产物 | 用途 |
|------|------|
| **geo-agents**（本仓库） | 可安装到 Cursor 等工具的 Agent + Skill 文档/脚本 |
| **clawec-agents** | 跨境电商平台（Amazon/TikTok/Shopee/Ozon）选品与数据分析 |
| **geo/workbuddy/experts-mcp** | WorkBuddy 内置 MCP 专家包（同能力，走 MCP 工具调用） |

## License

本项目采用 [MIT License](LICENSE)。
