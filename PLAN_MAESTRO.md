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
| image_generate | Generación de imágenes (DALL-E / SD / Midjourney) |
| video_generate | Reels y TikToks en video real (fase futura) |
| tts (texto a voz) | Voiceover de los Reels (fase futura) |
| music_generate | Música de fondo sin copyright (fase futura) |
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
PASO 3 — CHEQUEO DE MARCA (skill corto)
  • Verifica que ningún post viole "evitar" / "temas_a_evitar"
  • Marca los dudosos para revisión humana
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

## QUÉ SE SIMPLIFICÓ (recorte de redundancias)

Gracias a que OpenClaw absorbe trabajo, pasamos de **8 archivos Python** a
**2 piezas duras + skills**:

| Pieza original | Destino |
|---|---|
| brief_schema.py | ✅ Se queda (validar entrada) |
| output_formatter.py | ✅ Se queda (armar Excel) |
| strategy_generator.py | → Skill (prompt blindado) |
| copy_generator.py | → Skill (prompt blindado) |
| image_generator.py | → Skill / nativo OpenClaw |
| image_prompt_generator.py | ❌ Se fusiona (un paso menos) |
| pipeline.py (orquestador) | ❌ Lo reemplaza OpenClaw |
| utils.py (retry + reanudación) | ❌ Innecesario (OpenClaw ya lo trae) |

**El formulario de onboarding NO se desperdicia:** sus preguntas se convierten
en el guión del skill conversacional.

---

## FASES

### AHORA (esta etapa) — bajo riesgo, alto valor
1. Agente de onboarding por WebChat (con auto-fill de web/redes y memoria de cliente)
2. Skills de estrategia y copy (prompts blindados)
3. Imágenes (skill / nativo)
4. Chequeo de marca
5. Validación (brief_schema) + Excel (output_formatter) en código
6. Notificación y aprobación por el medio configurable
7. Memoria de meses anteriores (no repetir)

### DESPUÉS — diferenciadores, requieren cuidar calidad
8. Video real para Reels/TikTok (video_generate + tts + music_generate)
9. Disparo automático mensual por cron

### CON PINZAS — frágil o sin datos
10. Publicación automática vía navegador (siempre con humano aprobando)
11. Análisis de métricas / qué funcionó (requiere acceso a APIs de redes)

---

## PENDIENTES DE NEGOCIO (para la junta)

- **💰 Costo por cliente al mes:** generar un mes completo (20+ posts: texto +
  imágenes + quizá video) gasta dinero real en APIs. Hay que calcular el costo
  unitario para poder ponerle precio al servicio. → Pendiente de estimar.
- **API keys:** falta cargar ANTHROPIC_API_KEY y OPENAI_API_KEY para probar de
  extremo a extremo.
- **Medio de aprobación:** queda configurable por cliente (WhatsApp / Excel / ambos).
