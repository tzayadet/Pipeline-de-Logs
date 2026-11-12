# JSONL Detection Engine

A Python prototype that processes JSON Lines events and applies YAML-defined rules to generate detection alerts. The repository includes a static browser showcase; the actual engine runs locally.

<p align="center">
  <a href="https://tzayadet.github.io/Pipeline-de-Logs/"><img src="https://img.shields.io/badge/SHOWCASE-OPEN-00a86b?style=flat-square" alt="Showcase"></a>
  <a href="https://github.com/tzayadet/Pipeline-de-Logs"><img src="https://img.shields.io/badge/SOURCE-GITHUB-161b22?style=flat-square&logo=github" alt="Source"></a>
</p>

[![Tests](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml)

## What it does

- Reads JSONL events from standard input.
- Loads detection rules from YAML.
- Evaluates keyword patterns and regular expressions.
- Emits structured alerts for matching events.
- Includes a container build and automated tests.

## Requirements

- Python 3.11 or later.
- PyYAML.

```bash
python -m pip install -r requirements.txt
```

## Run locally

Pipe newline-delimited JSON events into the engine:

```bash
cat events.jsonl | python jsonl_rule_engine.py --rules rules.yaml
```

Each line must contain a JSON object. Rules use YAML fields such as `title`, `level` and `detection.selection.keyword`.

Example event:

```json
{"event":"authentication_failed","message":"Failed password for test"}
```

## Docker

```bash
docker build -t jsonl-detection-engine .
cat events.jsonl | docker run --rm -i jsonl-detection-engine
```

## Tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers rule loading, matching, invalid regular expressions and malformed input.

## Showcase and deployment

The [static showcase](https://tzayadet.github.io/Pipeline-de-Logs/) is a browser simulation. It does not run the Python engine or process uploaded logs. GitHub Pages deployment is defined in `.github/workflows/pages.yml`; enable Pages with GitHub Actions and set the `ENABLE_PAGES=true` Actions variable before deployment.

## Scope and limitations

This is a small rule-based exercise, not a SIEM or a full Sigma implementation. It evaluates the `keyword` field using regular expressions over the JSON representation of each event. It does not provide temporal correlation, normalization, persistence or alert management.

Use only lab data or logs you are authorized to process.

## License

See [LICENSE](LICENSE) for the repository's licensing terms.
