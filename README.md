# Content Pipeline — skill pack para OpenClaw

Motor genérico de marketing de contenido orgánico: dado el brief de **cualquier
cliente**, conversa con él, genera la estrategia y copy del mes, las imágenes,
y un chequeo de marca, listo para que un equipo lo revise y publique. La
arquitectura completa está en [`PLAN_MAESTRO.md`](PLAN_MAESTRO.md) — léelo
primero.

## Instalación en OpenClaw

1. Descarga/clona este repo en la máquina donde corre tu OpenClaw.
2. Copia (o enlaza) la carpeta `skills/` dentro del workspace de OpenClaw,
   para que detecte los 4 skills (`onboarding`, `estrategia-copy`, `imagenes`,
   `chequeo-marca`) en su `<available_skills>`.
3. Configura tus API keys (Claude, OpenAI) **dentro de OpenClaw**
   (`~/.openclaw/openclaw.json`), no en este repo — este repo no las usa
   directamente (ver `.env.example`).
4. Instala las dependencias de Python de las 2 piezas de código que sí corren
   localmente (validación de brief + armado de Excel):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   ```
5. Corre los tests para confirmar que el motor genérico funciona en tu máquina:

   ```bash
   pytest -q
   ```

## Qué es el motor genérico (esto NO se borra, sirve para cualquier cliente)

| Carpeta/archivo | Qué es |
|---|---|
| `PLAN_MAESTRO.md` | Arquitectura completa: flujo, vocabulario de estados, convención de nombres |
| `skills/onboarding/SKILL.md` | Conversa con el cliente, pre-llena leyendo su web/redes, produce su brief |
| `skills/estrategia-copy/SKILL.md` | Genera estrategia + copy del mes a partir del brief |
| `skills/imagenes/SKILL.md` | Genera la imagen de cada post (GPT Image 2) |
| `skills/chequeo-marca/SKILL.md` | Revisa el contenido contra los estándares de marca antes de entregar |
| `briefs/FORMULARIO_ONBOARDING.md` | Guion de preguntas que usa `onboarding` |
| `briefs/_template_brief.json` | Plantilla vacía del brief — válida para cualquier cliente |
| `pipeline/brief_schema.py` | Valida que un brief esté completo y correcto |
| `pipeline/output_formatter.py` | Genera el Excel/MD/checklist final |
| `tests/` | Pruebas del motor — usan un fixture genérico propio (`tests/fixtures/`), no dependen de `examples/` |

Los briefs reales de clientes en producción se guardan en
`briefs/{cliente}_{mes}.json` (los crea `onboarding`). Si un cliente tiene
material de referencia propio (su framework de copywriting, su banco de
temas), va en `clientes/{cliente}/` — ver convención de nombres en
`PLAN_MAESTRO.md`.

## `examples/cili/` — caso de demostración, **se puede borrar**

Esta carpeta contiene el caso piloto (CiLi) usado para probar el sistema: su
brief de ejemplo, su material de pilares/banco de temas, y documentación de
negocio específica de CiLi (contexto, costos, notas de junta). **No es parte
del motor** — bórrala completa (`rm -rf examples/`) y el resto del repo sigue
funcionando igual para cualquier cliente nuevo. Se deja aquí para seguir
probando el flujo con datos reales mientras se valida el sistema.

## Lo que falta construir (ver `PLAN_MAESTRO.md`, sección FASES)

Notificación/aprobación del equipo (checkpoint 2) y memoria de meses
anteriores para no repetir contenido.
