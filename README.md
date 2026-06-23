# CiLi Content Pipeline

Pipeline de contenido orgánico automatizado: dado el brief de un cliente, genera estrategia mensual, copies por plataforma, prompts de imagen y las imágenes finales (DALL-E 3), más un Excel/MD listos para revisión y publicación manual.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # y llena ANTHROPIC_API_KEY / OPENAI_API_KEY
```

## Uso

```bash
python -m pipeline.pipeline --brief briefs/cili_julio_2026.json
```

El resultado queda en `output/{empresa}/{mes}/`:
- `resumen_calendario.xlsx` — tabla para revisión del equipo
- `resumen_calendario.md` — misma info en texto plano
- `checklist_publicacion.md` — checklist post por post
- `imagenes/` — una carpeta por post con `imagen.png` y `copy.txt`
- `errores.log` — errores de generación de imagen, si los hay

El pipeline es reanudable: si `strategy.json`, `copies.json` o `image_prompts.json` ya existen en la carpeta de salida, no se regeneran.

## Tests

```bash
pytest -q
```
