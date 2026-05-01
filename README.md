# 微信聊天记录提取 Skill（WeChat Extraction Skill）

一个面向 Codex、Claude Code、OpenClaw 等 agent 的通用技能：用于用户授权的
微信 / WeChat / Weixin 聊天记录本地导出、校验、读取、整理和总结。

关键词：微信聊天记录、微信导出、聊天记录提取、WeChat export、Weixin、
Claude Code skill、Codex skill、OpenClaw skill、Agent skill。

This repository packages a generic `SKILL.md` plus safe helper scripts and
documentation. It does not include private data, decryption keys, decrypted
databases, or raw chat exports.

## 这是什么

这个仓库不是微信破解工具，也不是聊天记录数据库。它是一个可复用的 agent
工作流，让 AI 助手在用户本机、用户授权、最小范围的前提下处理微信聊天记录：

- 用户拥有或被授权访问本机微信数据
- 导出发生在用户自己的机器上
- 原始聊天记录、密钥和数据库不上传
- agent 先校验导出文件，再做总结分析
- 输出适合项目复盘、时间线、待办、风险、角色名单和证据索引

## 安装

把这个仓库 clone 到你的 agent 支持的 skill 目录里。

Codex 本地 skill：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/zsn2003/wechat-extraction-skill ~/.codex/skills/wechat-extraction
```

Claude Code 项目内 skill：

```bash
mkdir -p .claude/skills
git clone https://github.com/zsn2003/wechat-extraction-skill .claude/skills/wechat-extraction
```

OpenClaw workspace skill：

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/zsn2003/wechat-extraction-skill ~/.openclaw/workspace/skills/wechat-extraction
```

安装后重启 agent runtime，让它重新发现 `SKILL.md`。

## 使用方式

可以这样问你的 agent：

```text
使用微信聊天记录提取 skill，校验这个本地导出文件并总结里面的决策：
~/wechat-exports/project-group.json
```

也可以这样：

```text
Use the WeChat extraction skill to validate this local export and summarize the decisions:
~/wechat-exports/project-group.json
```

或者：

```text
使用微信聊天记录提取 skill。我想从自己的 Mac 本地导出“项目群”的聊天记录，
并总结 4 月份的待办事项。
```

```text
Use the WeChat extraction skill. I want to export my own chat with "Project Group"
from my local Mac and summarize action items from April.
```

这个 skill 会确认授权和范围，优先读取已有本地导出，并避免在最终回答里倾倒
大段私人聊天原文。

## 导出格式

辅助脚本期望 JSON 大致长这样：

```json
{
  "chat": "Project Group",
  "username": "project_group",
  "exported_at": "2026-05-01T10:00:00Z",
  "is_group": true,
  "messages": [
    {
      "timestamp": 1777610400,
      "sender": "Alice",
      "type": "text",
      "content": "Please review the launch checklist."
    }
  ]
}
```

详见 [`examples/sample_export.json`](examples/sample_export.json) 和
[`examples/export.schema.json`](examples/export.schema.json).

## 校验导出文件

```bash
python3 scripts/validate_export.py examples/sample_export.json
```

校验器只输出消息数量、日期范围、发言人分布和消息类型分布，不打印私人聊天内容。

## 隐私模型

把它接到真实微信记录前，先读
[`docs/privacy-and-safety.md`](docs/privacy-and-safety.md)。

简短版：

- 原始导出只留在本地
- 不提交数据库、密钥或原始聊天记录
- 只导出最小必要范围
- 总结，不粘贴大段聊天原文
- 分享前必须清洗示例数据

## 相似项目

这个仓库不是微信自动化库，也不是公众号排版发布工具。它专注“本地授权的微信
聊天记录导出校验与 agent 分析流程”。相似项目调研见
[`docs/github-search-notes.md`](docs/github-search-notes.md)。

## License

MIT
