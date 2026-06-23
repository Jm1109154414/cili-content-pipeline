# CiLi Content Pipeline

Pipeline de contenido orgánico automatizado. La visión y arquitectura vigentes
están en [`PLAN_MAESTRO.md`](PLAN_MAESTRO.md) — léelo primero.

## Qué hay en este repo

| Carpeta/archivo | Qué es |
|---|---|
| `PLAN_MAESTRO.md` | La arquitectura vigente (OpenClaw como orquestador + skills) |
| `COSTOS.md` | Estimación de costo de APIs por cliente al mes |
| `briefs/FORMULARIO_ONBOARDING.md` | Guion de preguntas — base del skill conversacional de onboarding |
| `briefs/_template_brief.json` | Plantilla vacía del brief de cliente |
| `briefs/*.json` | Briefs de clientes ya capturados |
| `pipeline/brief_schema.py` | Valida que un brief esté completo y correcto (se queda en código) |
| `pipeline/output_formatter.py` | Genera el Excel/MD/checklist final (se queda en código) |
| `prompts/*.txt` | Prompts de referencia — insumo para escribir los SKILL.md de OpenClaw |

> **Nota:** los generadores de estrategia, copy e imagen (que antes eran scripts
> Python sueltos) se retiraron de este repo. Según `PLAN_MAESTRO.md`, esa lógica
> se construye como **skills de OpenClaw** (prompts blindados dentro de
> `SKILL.md`), no como CLI manual. `prompts/*.txt` queda como insumo de
> referencia para escribir esos skills.

## Setup (para lo que sí es código)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Tests

```bash
pytest -q
```
