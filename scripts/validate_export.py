#!/usr/bin/env python3
"""Validate and summarize a local WeChat JSON export without printing content."""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


def parse_timestamp(value: Any) -> dt.datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        try:
            return dt.datetime.fromtimestamp(float(value), tz=dt.UTC)
        except (OverflowError, OSError, ValueError):
            return None
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        try:
            numeric = float(stripped)
            return dt.datetime.fromtimestamp(numeric, tz=dt.UTC)
        except ValueError:
            pass
        try:
            if stripped.endswith("Z"):
                stripped = stripped[:-1] + "+00:00"
            parsed = dt.datetime.fromisoformat(stripped)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=dt.UTC)
            return parsed.astimezone(dt.UTC)
        except ValueError:
            return None
    return None


def load_export(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("export root must be a JSON object")
    return data


def validate_export(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(data.get("chat"), str) or not data.get("chat", "").strip():
        errors.append("missing non-empty string field: chat")
    messages = data.get("messages")
    if not isinstance(messages, list):
        errors.append("missing array field: messages")
        return errors
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            errors.append(f"messages[{index}] must be an object")
            continue
        if "timestamp" not in message:
            errors.append(f"messages[{index}] missing timestamp")
        elif parse_timestamp(message.get("timestamp")) is None:
            errors.append(f"messages[{index}] has unparseable timestamp")
        if not isinstance(message.get("type"), str) or not message.get("type", "").strip():
            errors.append(f"messages[{index}] missing non-empty type")
    return errors


def summarize(data: dict[str, Any]) -> dict[str, Any]:
    messages = data.get("messages") or []
    timestamps = [
        parsed
        for parsed in (parse_timestamp(message.get("timestamp")) for message in messages)
        if parsed is not None
    ]
    senders = collections.Counter(
        message.get("sender", "<unknown>") or "<unknown>"
        for message in messages
        if isinstance(message, dict)
    )
    types = collections.Counter(
        message.get("type", "<unknown>") or "<unknown>"
        for message in messages
        if isinstance(message, dict)
    )
    return {
        "chat": data.get("chat"),
        "username": data.get("username"),
        "is_group": data.get("is_group"),
        "message_count": len(messages),
        "first_timestamp_utc": min(timestamps).isoformat() if timestamps else None,
        "last_timestamp_utc": max(timestamps).isoformat() if timestamps else None,
        "sender_counts": dict(senders.most_common()),
        "type_counts": dict(types.most_common()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and summarize a WeChat JSON export without printing message content."
    )
    parser.add_argument("export_json", type=Path, help="Path to an exported chat JSON file")
    args = parser.parse_args()

    try:
        data = load_export(args.export_json)
        errors = validate_export(data)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if errors:
        print("invalid export:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(json.dumps(summarize(data), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
