#!/usr/bin/env python3
"""Read newline-delimited JSON events and evaluate simple YAML detection rules."""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


def load_rules(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        rules = yaml.safe_load(handle) or []
    if not isinstance(rules, list):
        raise ValueError("Rules file must contain a YAML list")
    return [rule for rule in rules if isinstance(rule, dict)]


def match(event: dict, rule: dict) -> bool:
    detection = rule.get("detection", {})
    selection = detection.get("selection", {})
    pattern = selection.get("keyword")
    if not pattern:
        return False
    try:
        return re.search(str(pattern), json.dumps(event, ensure_ascii=False), re.IGNORECASE) is not None
    except re.error as exc:
        logging.error("Invalid regex in rule %r: %s", rule.get("title", "unnamed"), exc)
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-r", "--rules", type=Path, default=Path("rules.yaml"))
    args = parser.parse_args()
    rules = load_rules(args.rules)
    for line_number, line in enumerate(sys.stdin, start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("event must be a JSON object")
        except (json.JSONDecodeError, ValueError) as exc:
            logging.warning("Skipping invalid JSON at line %d: %s", line_number, exc)
            continue
        alerts = [
            {"title": rule.get("title", "Untitled rule"), "level": rule.get("level", "unknown")}
            for rule in rules if match(event, rule)
        ]
        if alerts:
            logging.warning("%s", json.dumps({"event": event, "alerts": alerts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
