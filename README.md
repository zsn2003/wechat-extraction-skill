# WeChat Extraction Skill

A local-first agent skill for user-authorized WeChat / Weixin chat export,
validation, and analysis workflows.

This repository packages a generic `SKILL.md` plus safe helper scripts and
documentation. It is designed for Codex, Claude Code, OpenClaw, and other
`SKILL.md`-compatible agent runtimes.

It does not include private data, decryption keys, decrypted databases, or raw
chat exports.

## Why this exists

There are useful WeChat-adjacent projects for automation, article publishing,
and persona-building. This skill focuses on a narrower workflow:

- the user owns or is authorized to access the local WeChat archive
- extraction happens locally on the user's machine
- raw data and keys are never uploaded
- agents validate exports before summarizing them
- outputs are structured for project work, reviews, timelines, and follow-ups

## Install

Clone this repository into a skill directory supported by your agent runtime.

For Codex-style local skills:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/zsn2003/wechat-extraction-skill ~/.codex/skills/wechat-extraction
```

For Claude Code project-local skills:

```bash
mkdir -p .claude/skills
git clone https://github.com/zsn2003/wechat-extraction-skill .claude/skills/wechat-extraction
```

For OpenClaw-style workspace skills:

```bash
mkdir -p ~/.openclaw/workspace/skills
git clone https://github.com/zsn2003/wechat-extraction-skill ~/.openclaw/workspace/skills/wechat-extraction
```

Restart the agent runtime after installation so it can discover `SKILL.md`.

## Usage

Ask your agent something like:

```text
Use the WeChat extraction skill to validate this local export and summarize the decisions:
~/wechat-exports/project-group.json
```

or:

```text
Use the WeChat extraction skill. I want to export my own chat with "Project Group"
from my local Mac and summarize action items from April.
```

The skill will ask for authorization and scope, prefer existing local exports,
and avoid dumping raw private conversations into the final response.

## Export format

The helper script expects a JSON file shaped like:

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

See [`examples/sample_export.json`](examples/sample_export.json) and
[`examples/export.schema.json`](examples/export.schema.json).

## Validate an export

```bash
python3 scripts/validate_export.py examples/sample_export.json
```

The validator prints counts, date range, sender distribution, and message type
distribution without printing private message content.

## Privacy model

Read [`docs/privacy-and-safety.md`](docs/privacy-and-safety.md) before adapting
this skill to a real archive.

Short version:

- keep raw exports local
- do not commit database files, keys, or raw logs
- extract the smallest useful scope
- summarize instead of pasting long chat logs
- sanitize examples before sharing

## Similar projects

This is not a replacement for WeChat automation libraries or WeChat article
publishing tools. It is a privacy-focused agent workflow for local exports.
See [`docs/github-search-notes.md`](docs/github-search-notes.md) for the quick
survey that informed this repository.

## License

MIT
