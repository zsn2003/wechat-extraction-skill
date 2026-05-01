# Workflow

This workflow assumes the user has a local export tool or an existing export.
The skill itself does not include a decryptor.

## 1. Confirm Scope

Ask:

- Which chat or group should be processed?
- What date range matters?
- What output is useful: summary, timeline, action list, participant roster, or
  evidence index?
- Is this the user's own account/device or otherwise authorized?

## 2. Locate Existing Exports

```bash
export WECHAT_OUTPUT_DIR="$HOME/wechat-exports"
find "$WECHAT_OUTPUT_DIR" -maxdepth 2 -type f \( -name '*.json' -o -name '*.jsonl' \)
```

If an export already exists, validate it before extracting again.

## 3. Export Locally

Use the user's own local extractor. Keep the command specific to their setup
and avoid printing keys.

Placeholder:

```bash
export WECHAT_EXPORT_TOOL_DIR="$HOME/tools/wechat-export"
export WECHAT_OUTPUT_DIR="$HOME/wechat-exports"

cd "$WECHAT_EXPORT_TOOL_DIR"
python3 export_chat.py "Project Group" "$WECHAT_OUTPUT_DIR/project-group.json"
```

## 4. Validate

```bash
python3 scripts/validate_export.py "$WECHAT_OUTPUT_DIR/project-group.json"
```

If validation fails, inspect schema problems before analysis.

## 5. Analyze

Recommended structured outputs:

- Message count and date range
- Participant roster
- Timeline by date
- Decisions
- Action items with owner and due date when available
- Risks and blockers
- Unprocessed media gaps
- Local source paths

## 6. Preserve Reusable Results

Save summaries to a local project directory. Keep raw exports outside Git unless
they are sanitized fixtures.
