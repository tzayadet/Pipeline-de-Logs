import tempfile
import unittest
from pathlib import Path

from jsonl_rule_engine import load_rules, match


class PipelineTests(unittest.TestCase):
    def test_load_rules_reads_yaml_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules_path = Path(tmp) / "rules.yaml"
            rules_path.write_text(
                "- title: Failed login\n"
                "  level: medium\n"
                "  detection:\n"
                "    selection:\n"
                "      keyword: 'Failed password'\n",
                encoding="utf-8",
            )

            rules = load_rules(rules_path)

        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]["title"], "Failed login")

    def test_load_rules_rejects_non_list_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules_path = Path(tmp) / "rules.yaml"
            rules_path.write_text("title: not-a-list\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "YAML list"):
                load_rules(rules_path)

    def test_load_rules_rejects_non_mapping_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules_path = Path(tmp) / "rules.yaml"
            rules_path.write_text("- title: valid\n- invalid-entry\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "YAML mapping"):
                load_rules(rules_path)

    def test_match_is_case_insensitive(self):
        event = {"message": "Failed password for test"}
        rule = {"detection": {"selection": {"keyword": "failed password"}}}

        self.assertTrue(match(event, rule))

    def test_match_returns_false_when_keyword_is_missing(self):
        self.assertFalse(match({"event": "login"}, {"detection": {"selection": {}}}))

    def test_invalid_regex_does_not_crash_pipeline(self):
        rule = {"title": "broken", "detection": {"selection": {"keyword": "["}}}

        with self.assertLogs(level="ERROR"):
            self.assertFalse(match({"message": "event"}, rule))

    def test_malformed_detection_sections_are_ignored(self):
        self.assertFalse(match({"message": "event"}, {"detection": None}))
        self.assertFalse(match({"message": "event"}, {"detection": {"selection": None}}))

    def test_oversized_rule_pattern_is_rejected(self):
        rule = {
            "title": "oversized",
            "detection": {"selection": {"keyword": "a" * 257}},
        }
        with self.assertLogs(level="ERROR"):
            self.assertFalse(match({"message": "event"}, rule))

    def test_oversized_event_is_skipped(self):
        import jsonl_rule_engine

        event = {"message": "x" * (jsonl_rule_engine.MAX_EVENT_BYTES + 1)}
        rule = {"detection": {"selection": {"keyword": "event"}}}
        with self.assertLogs(level="WARNING"):
            self.assertFalse(match(event, rule))


if __name__ == "__main__":
    unittest.main()
