---
name: "wechat-extraction"
description: "Use when the user asks to extract, export, validate, read, analyze, or summarize WeChat/Weixin chat records from their own local device. Follow a user-authorized, local-first workflow with privacy safeguards and structured outputs."
---

# WeChat Extraction

Help a user work with their own WeChat chat records on their own machine. This
skill is an agent workflow, not a bundled decryptor. It keeps raw data local,
asks for explicit scope, validates exported JSON, and turns authorized exports
into useful summaries, action lists, timelines, or evidence indexes.

## Scope

Use this skill for:

- Exporting a named WeChat contact or group chat with a user-provided local
  extractor.
- Validating an existing JSON export before analysis.
- Summarizing chats into decisions, timelines, owners, blockers, risks, and
  follow-up actions.
- Building reusable local runbooks for a user's own WeChat archive.

Do not use this skill for:

- Accessing someone else's account or device.
- Uploading private chat logs, database files, or key material to a third party.
- Bulk extraction without a clear user-approved target and purpose.
- Bypassing platform rules, legal restrictions, or device-owner consent.

## Safety Rules

Before touching data, confirm the user owns or is authorized to access the
device/account and ask for the smallest useful scope, such as one contact, one
group, or one date range.

Never print long raw chat logs in the final answer. Summarize and point to local
output files.

Treat all of the following as sensitive:

- WeChat database files
- decrypted database copies
- key files, memory dumps, and `all_keys.json`-style outputs
- raw JSON exports
- media attachments, voice notes, images, and transferred files

Do not commit, publish, paste, or upload sensitive artifacts.

## Generic Paths

macOS WeChat data is often under a path shaped like this:

```bash
$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<wechat-account-id>/
```

Use environment variables instead of hard-coded personal paths:

```bash
export WECHAT_DATA_ROOT="$HOME/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<wechat-account-id>"
export WECHAT_EXPORT_TOOL_DIR="$HOME/tools/wechat-export"
export WECHAT_OUTPUT_DIR="$HOME/wechat-exports"
```

## Workflow

1. Confirm authorization and scope.

   Ask for the target chat name, expected date range, and intended output.
   Prefer a named chat over account-wide extraction.

2. Inspect existing exports first.

   ```bash
   find "$WECHAT_OUTPUT_DIR" -maxdepth 2 -type f \( -name '*.json' -o -name '*.jsonl' \)
   ```

3. Export with the user's local tool.

   This skill does not ship a decryption tool. If the user already has an
   authorized local extractor, run it from their machine and write output to a
   local directory. Keep commands tool-specific and avoid exposing keys.

   Example placeholder:

   ```bash
   cd "$WECHAT_EXPORT_TOOL_DIR"
   python3 export_chat.py "Chat Name" "$WECHAT_OUTPUT_DIR/chat-name.json"
   ```

4. Validate the export.

   ```bash
   python3 scripts/validate_export.py "$WECHAT_OUTPUT_DIR/chat-name.json"
   ```

5. Analyze only the requested scope.

   Useful outputs include:

   - concise summary
   - timeline by date
   - participant / role roster
   - decisions and evidence snippets
   - owner / action list
   - open questions and missing media gaps
   - source file paths for local follow-up

6. Persist reusable work.

   Put reusable notes in local docs or a project memory file. Keep raw exports
   out of Git unless the user explicitly creates a sanitized fixture.

## Output Format

When responding to the user, include:

- what was read or exported
- local output path
- number of messages and date range
- most actionable findings
- missing media, voice, or attachment gaps
- clear note that raw private data stayed local

Keep the answer compact. Do not paste full private conversations.
