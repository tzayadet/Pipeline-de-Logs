# JSONL Detection Engine

Prototipo de motor de detección que procesa eventos JSON Lines y aplica reglas YAML para generar alertas.

[![Tests](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/python-syntax.yml) · [![Docker](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml/badge.svg)](https://github.com/tzayadet/Pipeline-de-Logs/actions/workflows/container-build.yml)

**Showcase source:** [docs/index.html](docs/index.html) · **Código:** [jsonl_rule_engine.py](jsonl_rule_engine.py) · **Reglas:** [rules.yaml](rules.yaml)

La demo es una simulación estática en el navegador; el motor Python real se ejecuta localmente.

## Requisitos

- Python 3.11 o superior.
- PyYAML.

```bash
python -m pip install -r requirements.txt
```

## Uso

Envía eventos JSONL por la entrada estándar:

```bash
cat events.jsonl | python jsonl_rule_engine.py --rules rules.yaml
```

Cada línea debe contener un objeto JSON. Las reglas se definen en YAML con los campos `title`, `level` y `detection.selection.keyword`.

Ejemplo de evento:

```json
{"event":"authentication_failed","message":"Failed password for test"}
```

## Pruebas

```bash
python -m unittest discover -s tests -v
```

La suite comprueba la carga de reglas, las coincidencias, las expresiones regulares inválidas y las entradas malformadas.

## Docker

```bash
docker build -t jsonl-detection-engine .
cat events.jsonl | docker run --rm -i jsonl-detection-engine
```

## Publicar el showcase

El showcase estático se encuentra en [docs/index.html](docs/index.html). Para publicarlo:

1. En **Settings → Pages**, selecciona **GitHub Actions** como origen.
2. En **Settings → Secrets and variables → Actions → Variables**, crea `ENABLE_PAGES` con valor `true`.
3. Ejecuta **Deploy Pipeline-de-Logs showcase to GitHub Pages** desde Actions.

La demo es una simulación estática en el navegador; el motor Python real se ejecuta localmente.

## Alcance y limitaciones

Es un ejercicio de detección sobre eventos JSONL, no un SIEM ni una implementación completa de Sigma. Evalúa el campo `keyword` mediante expresiones regulares sobre la representación JSON del evento. No incluye correlación temporal, normalización, persistencia ni gestión de alertas.

Utiliza datos de laboratorio o registros que tengas autorización para procesar.

## Licencia

Consulta [LICENSE](LICENSE).
