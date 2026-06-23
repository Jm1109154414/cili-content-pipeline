# PLAN MAESTRO — Pipeline de Marketing Automatizado con OpenClaw
## CiLi · Junio 2026 · v3.0

> Documento de visión para la junta del equipo. Marca claramente qué es **AHORA**
> (lo que vamos a construir en esta etapa) y qué es **DESPUÉS** (fases futuras).

---

## PRINCIPIO RECTOR

> **OpenClaw orquesta todo, pero siempre guiado por nuestros skills.**
> Nuestros scripts ejecutan lo que debe ser idéntico siempre (validar el brief,
> armar el Excel final). Nuestros prompts blindados —dentro de los skills— guían
> lo creativo (estrategia, copy). Y nuestros estándares de marca escritos guían
> lo que OpenClaw genera con sus herramientas nativas (imágenes, video, voz, música).

**En una frase:** código solo donde se necesita precisión absoluta; skills con
prompts blindados para todo lo demás; OpenClaw como cerebro que coordina.

---

## ARQUITECTURA — 3 CAPAS

```
┌─────────────────────────────────────────────────────────┐
│  CAPA 1 — CANALES (cómo entra y sale la info)            │
│  WebChat (onboarding) · WhatsApp (notif/aprobación)      │
│  Cron (disparo automático mensual)                       │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│  CAPA 2 — OPENCLAW (el orquestador / cerebro)           │
│  Lee los skills, decide, ejecuta, coordina, recuerda    │
│  clientes y meses anteriores (memoria nativa)           │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│  CAPA 3 — NUESTROS SKILLS (el estándar y el control)    │
│  • SKILL.md → reglas de marca, plataformas, qué evitar  │
│  • Prompts blindados → estrategia, copy                 │
│  • Scripts Python (solo 2) → validar brief + armar Excel│
│  Para imágenes/video/voz/música: SKILL.md guía tools    │
│  nativas de OpenClaw                                     │
└─────────────────────────────────────────────────────────┘
```

---

## QUÉ NOS DA OPENCLAW (capacidades nativas que aprovechamos)

| Capacidad nativa | Para qué la usamos |
|---|---|
| WebChat | Canal del agente de onboarding |
| WhatsApp | Notificación y aprobación del equipo |
| Cron (scheduler) | Disparar el contenido el día 1 de cada mes (reemplaza n8n) |
| Memoria por sesión/cliente | Reanudar conversaciones, recordar clientes recurrentes |
| Navegador + búsqueda web | Pre-llenar el brief leyendo web y redes del cliente |
| image_generate | Generación de imágenes — **GPT Image 2** elegido (OpenAI, ~99% precisión de texto dentro de imagen, ~$0.05/img) |
| video_generate | Reels y TikToks en video real — **Kling 3.0** elegido ($0.10/seg, buen equilibrio calidad/precio). Fase futura |
| tts (texto a voz) | Voiceover de los Reels — OpenAI TTS (~$0.015/min). Fase futura |
| music_generate | Música de fondo sin copyright — Suno (~$0.05-0.11/canción). Fase futura |
| subagents | Generar varios posts en paralelo |
| read/write/edit | Crear brief.json, leer/editar el Excel sin tocar terminal |

Fuentes: docs.openclaw.ai · ClawHub (13,700+ skills)

---

## FLUJO COMPLETO

```
PASO 0 — ONBOARDING (agente conversacional, WebChat)
  • Cliente entra por un link de WebChat
  • ¿Cliente nuevo?
      → El agente PRE-LLENA leyendo su web y redes (auto-fill)
      → Solo pregunta/confirma lo que falta (no 35 preguntas)
      → Insiste con ejemplos concretos si una respuesta es vaga
  • ¿Cliente recurrente?
      → El agente ya lo recuerda (secciones A-E)
      → Solo pregunta lo del mes: tema, evento, objetivo (sección F)
  • El agente PRODUCE el brief él mismo (sin llenado manual de JSON)
        │
        ▼
PASO 1 — VALIDACIÓN (script Python, sin costo de API)
  • brief_schema valida que no falten campos ni estén mal
  • ❌ Falta algo → el agente regresa a preguntarlo
  • ✅ Completo → checkpoint 1: el cliente confirma el resumen
        │
        ▼
PASO 2 — GENERACIÓN (skills con prompts blindados)
  • Estrategia del mes (skill)
  • Copy por post y plataforma (skill)  ← puede usar subagentes
  • Imágenes (skill / nativo, guiado por estándares de marca)
  • Memoria: revisa meses anteriores para NO repetir contenido
        │
        ▼
PASO 3 — CHEQUEO DE MARCA (skill construido: skills/chequeo-marca/SKILL.md)
  • Verifica que ningún post viole "evitar" / "temas_a_evitar"
  • Verifica que las cifras citadas existan en el brief (no inventadas)
  • Marca los dudosos (estado: REVISAR_MARCA) sin detener el resto del mes
        │
        ▼
PASO 4 — ENTREGABLE (script Python)
  • resumen_calendario.xlsx (revisión del equipo)
  • resumen_calendario.md · checklist_publicacion.md
  • imagenes/ (carpeta por post: imagen + copy)
        │
        ▼
PASO 5 — APROBACIÓN (medio configurable)
  • OpenClaw notifica que está listo
  • Checkpoint 2: el equipo aprueba
       (por WhatsApp respondiendo / en el Excel / ambos — configurable)
  • Publicación MANUAL por ahora
```

---

## DOBLE CHECKPOINT (decisión de negocio)

- **Checkpoint 1 — el cliente confirma:** al final del onboarding, el agente
  muestra "esto entendí de tu negocio" y el cliente valida que se le entendió bien.
- **Checkpoint 2 — el equipo aprueba:** antes de publicar, el equipo da el visto
  bueno a la calidad del contenido generado.

Son dos cosas distintas (entendimiento vs. calidad), por eso se quedan ambas.

---

## VOCABULARIO ÚNICO DE ESTADOS (fuente de verdad — todos los skills deben usar esto)

Cada post tiene un único campo `estado`, escrito en distintos pasos del flujo.
Para evitar que un skill pise silenciosamente el resultado de otro, el campo
**se respeta por prioridad**: si un post ya tiene un estado de falla, ningún
paso posterior puede sobrescribirlo con un estado "limpio".

| Estado | Quién lo escribe | Significado | Prioridad |
|---|---|---|---|
| `PENDIENTE_MANUAL` | `estrategia-copy` | El texto del post falló al generarse | 1 (máxima — nunca se pisa) |
| `IMAGEN_PENDIENTE` | `imagenes` | La imagen del post falló al generarse | 1 (máxima — nunca se pisa) |
| `REVISAR_MARCA` | `chequeo-marca` | El chequeo de marca detectó un problema (cifra no verificada, tema prohibido, etc.) | 2 |
| `GENERADO` | `chequeo-marca` (al cerrar el ciclo automático) | Todo el contenido pasó limpio, listo para que el equipo lo revise | 3 (default si nada falló) |
| `APROBADO` | Skill de notificación/aprobación (pendiente de construir) | El equipo dio el visto bueno (checkpoint 2) | 4 |
| `PUBLICADO` | Marcado manualmente por el equipo | Ya está en redes | 5 |

**Regla para `chequeo-marca` (el que consolida el estado final por post):**
antes de escribir `estado`, revisa si el post ya trae `PENDIENTE_MANUAL` (de
`estrategia-copy`) o `IMAGEN_PENDIENTE` (de `imagenes`) — si trae cualquiera
de los dos, **respétalo y no lo toques**, solo agrega las `alertas_marca` que
encuentres. Únicamente escribe `GENERADO` o `REVISAR_MARCA` cuando el post no
tenía ya un estado de falla previo.

---

## CONVENCIÓN DE NOMBRES (fuente de verdad — todos los skills deben usar esto)

Varios skills construyen rutas de archivo (`briefs/{cliente}_{mes}.json`,
`output/{cliente}/{mes}/...`). Para que todos generen la misma ruta para el
mismo cliente, el slug se calcula siempre así:

- **`{cliente}`:** primera palabra de `empresa` (del brief), en minúsculas,
  sin acentos ni símbolos. Ej: `"CiLi — Continuous Improvement..."` → `cili`.
  `"Joyería Esperanza S.A."` → `joyeria`.
- **`{mes}`:** el campo `mes` del brief (ej. `"Julio 2026"`), en minúsculas,
  sin acentos, espacio reemplazado por `_`. Ej: `"Julio 2026"` → `julio_2026`.

### `briefs/` vs `clientes/{cliente}/` vs `examples/{cliente}/`

- **`briefs/{cliente}_{mes}.json`:** el brief mensual real de un cliente en
  producción, lo produce `onboarding`.
- **`clientes/{cliente}/`:** material de referencia propio de un cliente real
  que no cambia mes a mes (su versión de `{cliente}_pilares_completo.md`,
  `reference_banco_temas_{cliente}.md`, etc.) — **opcional**, solo si el
  cliente tiene este material. `estrategia-copy` lo busca aquí primero.
- **`examples/{cliente}/`:** material de **demostración**, no de producción.
  Es **desechable** — se puede borrar toda la carpeta `examples/` y el motor
  (skills + `pipeline/`) sigue funcionando igual para cualquier cliente nuevo.
  CiLi vive aquí (`examples/cili/`) como el caso piloto con el que se prueba
  el sistema; incluye su brief de ejemplo, su material de pilares/banco de
  temas, y la documentación de negocio específica de CiLi (`examples/cili/CONTEXTO.md`,
  `examples/cili/COSTOS.md`, `examples/cili/TARJETA_JUNTA.md`). Si `clientes/{cliente}/` no existe,
  `estrategia-copy` revisa `examples/{cliente}/` como alternativa (solo
  relevante mientras se prueba con CiLi).

Con esto: el brief de ejemplo de CiLi de julio 2026 vive en
`examples/cili/cili_julio_2026.json`, su material de referencia en
`examples/cili/cili_pilares_completo.md` y
`examples/cili/reference_banco_temas_cili.md`, y su output del mes (cuando se
corra de verdad) en `output/cili/julio_2026/`.

## IDENTIFICADOR DE POST (`post_id`) — para no emparejar por posición

`estrategia-copy` asigna a cada post un `post_id` secuencial (`post_01`,
`post_02`, ...). **Todos los skills posteriores (`imagenes`, `chequeo-marca`)
deben usar ese mismo `post_id` para referirse al post**, nunca la posición en
la lista — si algún paso reordena o salta un post, emparejar por índice
asignaría el estado o la imagen al post equivocado.

---

## QUÉ SE SIMPLIFICÓ (recorte de redundancias)

Gracias a que OpenClaw absorbe trabajo, pasamos de **8 archivos Python** a
**2 piezas duras + skills**:

| Pieza original | Destino |
|---|---|
| brief_schema.py | ✅ Se queda (validar entrada) |
| output_formatter.py | ✅ Se queda (armar Excel) |
| strategy_generator.py | → ✅ Skill construido: `skills/estrategia-copy/SKILL.md` |
| copy_generator.py | → ✅ Fusionado en el mismo skill `estrategia-copy` |
| image_generator.py | → ✅ Skill construido: `skills/imagenes/SKILL.md` (GPT Image 2) |
| image_prompt_generator.py | ❌ Se fusiona (un paso menos) |
| pipeline.py (orquestador) | ❌ Lo reemplaza OpenClaw |
| utils.py (retry + reanudación) | ❌ Innecesario (OpenClaw ya lo trae) |

**El formulario de onboarding NO se desperdicia:** sus preguntas se convierten
en el guión del skill conversacional.

---

## FASES

### AHORA (esta etapa) — bajo riesgo, alto valor
1. ✅ Agente de onboarding por WebChat — `skills/onboarding/SKILL.md` (auto-fill de web/redes, insiste en respuestas vagas, checkpoint 1 con el cliente)
2. ✅ Skills de estrategia y copy — `skills/estrategia-copy/SKILL.md`
3. ✅ Imágenes — `skills/imagenes/SKILL.md` (GPT Image 2)
4. ✅ Chequeo de marca — `skills/chequeo-marca/SKILL.md`
5. ✅ Validación (brief_schema) + Excel (output_formatter) en código
6. ❌ Notificación y aprobación por el medio configurable — pendiente
7. ❌ Memoria de meses anteriores (no repetir) — pendiente

### DESPUÉS — diferenciadores, requieren cuidar calidad
8. Video real para Reels/TikTok (Kling 3.0 + TTS + Suno) — **se cobra aparte**,
   el costo (~$150-185 MXN/mes por 4-5 Reels) ya no es trivial como texto/imagen.
   Se descartó CapCut: es editor manual sin API, no genera video desde prompt
   y rompería la automatización (requeriría simular clics en pantalla).
9. Disparo automático mensual por cron

### CON PINZAS — frágil o sin datos
10. Publicación automática vía navegador (siempre con humano aprobando)
11. Análisis de métricas / qué funcionó (requiere acceso a APIs de redes)

---

## PENDIENTES DE NEGOCIO (para la junta)

- **💰 Costo por cliente al mes:** ✅ ya estimado en `examples/cili/COSTOS.md`
  (~$36 MXN/mes texto+imagen; ~$150-195 MXN/mes extra si se agrega video,
  con el supuesto de ~20 posts/mes de CiLi — recalcular si otro cliente tiene
  otra frecuencia).
- **API keys:** las llaves de Claude y OpenAI **no van en este repo** — este
  repo ya no ejecuta llamadas a esas APIs directamente (ver "QUÉ SE SIMPLIFICÓ").
  Las llaves se configuran dentro de OpenClaw (`~/.openclaw/openclaw.json` en
  la máquina donde corre), que es quien invoca los skills. Falta hacer esa
  configuración en OpenClaw para poder probar el flujo de extremo a extremo.
- **Medio de aprobación:** queda configurable por cliente (WhatsApp / Excel / ambos).
