# JSONL Detection Engine

Motor de detección de eventos JSON mediante reglas YAML y expresiones regulares. Lee eventos JSON Lines desde stdin y emite alertas cuando una regla coincide.

[![Python tests](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml) · [![Container build](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml)

## Requisitos

- Python 3.11+
- PyYAML

```bash
python -m pip install -r requirements.txt
```

## Uso

```bash
cat events.jsonl | python jsonl_rule_engine.py --rules rules.yaml
```

Cada línea de entrada debe ser un objeto JSON. Las reglas se definen como una lista YAML con `title`, `level` y `detection.selection.keyword`.

## Ejemplo de evento

```json
{"event":"authentication_failed","message":"Failed password for test"}
```

## Alcance y limitaciones

Este es un prototipo didáctico de detección JSONL, no un SIEM ni un motor Sigma completo. Solo evalúa el campo `keyword` de la selección mediante regex sobre la representación JSON del evento. No implementa condiciones Sigma, correlación temporal, normalización, gestión de estado ni almacenamiento de alertas.

Utilízalo con datos de laboratorio o registros que tengas autorización para procesar.

## Pruebas

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Las pruebas cubren la carga de reglas YAML, la coincidencia de patrones, las expresiones regulares inválidas y las estructuras malformadas.

## Docker

```bash
docker build -t log-pipeline .
cat events.jsonl | docker run --rm -i log-pipeline
```

## Licencia

Consulta [LICENSE](LICENSE).
