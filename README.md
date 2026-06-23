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
| `briefs/cili_pilares_completo.md` | Dolores/deseos/certezas/avatar reales de CiLi + su framework propio de copywriting (P/B/C/S/TI/I/CN), extraído de `Pilares de contenido (2).xlsx` |
| `prompts/reference_banco_temas_cili.md` | Banco real de temas por certificación (Yellow/Green/Black Belt) + 5 ejemplos ya redactados, extraído del mismo Excel |
| `pipeline/brief_schema.py` | Valida que un brief esté completo y correcto (se queda en código) |
| `pipeline/output_formatter.py` | Genera el Excel/MD/checklist final (se queda en código) |
| `skills/estrategia-copy/SKILL.md` | ✅ **Skill construido** — genera estrategia + copy del mes en un solo paso, usando el framework propio de CiLi |
| `skills/imagenes/SKILL.md` | ✅ **Skill construido** — genera la imagen de cada post vía Ideogram 3.0, alineada a marca |

> **Nota:** los generadores de estrategia, copy e imagen (que antes eran scripts
> Python sueltos) se retiraron de este repo. Según `PLAN_MAESTRO.md`, esa lógica
> se construye como **skills de OpenClaw** (instrucciones en `SKILL.md`, no CLI
> manual). Ambos ya están construidos (`skills/estrategia-copy/`, `skills/imagenes/`).

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
