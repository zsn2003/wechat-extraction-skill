# Privacy And Safety

WeChat exports can contain personal messages, business records, identities,
files, images, voice notes, credentials, and legal or financial details. Treat
them as sensitive by default.

## Rules For Agents

- Confirm the user owns or is authorized to access the account and device.
- Ask for the smallest useful scope: one chat, one group, or one date range.
- Prefer existing local exports before creating new ones.
- Do not upload raw exports, database files, key files, media folders, or
  decrypted database copies.
- Do not paste full private conversations into the final answer.
- Summarize, cite local file paths, and keep evidence snippets short.
- Do not commit private artifacts to Git.

## Sensitive Artifacts

Keep these out of repositories and prompts:

- WeChat database files
- decrypted database files
- memory dumps
- key material such as `all_keys.json`
- raw JSON or JSONL exports
- voice, image, file, and video attachments
- screenshots containing real chats

## Recommended Local Layout

Use a private directory outside Git:

```bash
mkdir -p "$HOME/wechat-exports"
chmod 700 "$HOME/wechat-exports"
```

Keep sanitized fixtures separate:

```bash
examples/
  sample_export.json
```

Sanitized fixtures should use fake names, fake chat content, and fake dates.

## Publication Checklist

Before publishing a derived skill or report:

```bash
rg -n "wxid_|/Users/|all_keys|token|api[_-]?key|secret|password|private|\.db" .
```

Also manually inspect examples, screenshots, and generated summaries.
