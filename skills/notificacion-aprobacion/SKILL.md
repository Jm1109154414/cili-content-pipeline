---
name: notificacion-aprobacion
description: Notifica al equipo que el contenido del mes está listo para revisar (checkpoint 2), por el medio configurado en el brief (WhatsApp/Excel/ambos), y registra cuando el equipo aprueba o pide cambios. Usar después de pipeline.output_formatter.generate_output(). También dispara este skill si el operador pregunta "¿ya está listo el contenido de [cliente]?", "apruébame el mes de [cliente]" o responde directamente a una notificación previa con cambios o un visto bueno.
---

# Notificación y aprobación del equipo

Avisas al equipo que opera la cuenta que el contenido del mes ya está
generado y revisado por `chequeo-marca`, y gestionas el checkpoint 2 (ver
`PLAN_MAESTRO.md`): el equipo da el visto bueno antes de publicar.

## Cuándo se usa

Justo después de que `pipeline.output_formatter.generate_output()` terminó
de generar `resumen_calendario.xlsx`, `resumen_calendario.md`,
`checklist_publicacion.md` y `contenido_final.json`. Es el último paso del
flujo (Paso 5 en `PLAN_MAESTRO.md`).

## Entrada

- Las rutas que devolvió `generate_output()` (`xlsx`, `md`, `checklist`, `historial`).
- El contenido final consolidado (mismo que se guardó en `contenido_final.json`):
  necesitas el `estado` y las `alertas_marca` de cada post para armar el resumen.
- `brief.medio_aprobacion` (`whatsapp` | `excel` | `ambos`, default `ambos`
  — ver `pipeline/brief_schema.py`). **Esto lo decide el equipo, no se le
  pregunta al cliente final** (ver `skills/onboarding/SKILL.md`).
- `brief.empresa`, `brief.mes`.

## Paso 1 — Armar el resumen

Cuenta los posts por `estado` (vocabulario único en `PLAN_MAESTRO.md`):
`GENERADO`, `REVISAR_MARCA`, `IMAGEN_PENDIENTE`, `PENDIENTE_MANUAL`. Para los
posts con `alertas_marca`, ordénalas por severidad (alta primero — cada
alerta trae `categoria`/`severidad`/`descripcion`, ver
`skills/chequeo-marca/SKILL.md`). Construye un mensaje corto:

> ✅ Contenido de {empresa} — {mes} listo: 18/20 posts limpios.
> ⚠️ 2 necesitan tu revisión antes de aprobar:
> - 🔴 Post 7 (legal, alta): cifra no verificada
> - Post 14 (IMAGEN_PENDIENTE): la imagen falló al generarse

Si `chequeo-marca` dejó un reporte de alertas (su "Reporte adicional"), úsalo
tal cual en vez de reconstruirlo.

## Paso 2 — Notificar según `medio_aprobacion`

- **`whatsapp`:** manda el resumen del Paso 1 al chat del equipo (tool de
  mensajería de OpenClaw) junto con la ruta/link de `resumen_calendario.xlsx`.
  La aprobación se espera **como respuesta a ese mensaje** (Paso 3).
- **`excel`:** no se manda nada por chat — el equipo revisa
  `resumen_calendario.xlsx` cuando le convenga y marca ahí mismo la columna
  "Estado" de cada post (de `GENERADO` a `APROBADO`, o escribe el ajuste
  necesario). La aprobación se detecta releyendo el Excel (Paso 3).
- **`ambos`:** notifica por WhatsApp con el resumen, y aclara en el mensaje
  que la aprobación formal se registra marcando el Excel.

## Paso 3 — Registrar la aprobación

**Si la respuesta llega por WhatsApp:**
- Si el equipo responde algo equivalente a "aprobado" / "todo bien" sin
  mencionar posts puntuales: actualiza a `"estado": "APROBADO"` **solo** los
  posts que estaban en `GENERADO` (vocabulario único — nunca subas a
  `APROBADO` un post que sigue en `REVISAR_MARCA`, `IMAGEN_PENDIENTE` o
  `PENDIENTE_MANUAL` sin que el equipo lo haya resuelto explícitamente).
- Si el equipo pide un cambio puntual ("cambia el post 7", "regenera la
  imagen del post 14"): no apruebes nada todavía — identifica el `post_id`
  mencionado y vuelve a correr únicamente ese post por `estrategia-copy`
  y/o `imagenes` (no el mes completo), luego repite el chequeo de marca de
  ese post antes de volver a notificar.

**Si el medio es `excel` (o `ambos` y no hubo respuesta por WhatsApp):**
- Vuelve a leer `resumen_calendario.xlsx` y compara la columna "Estado" contra
  el `contenido_final.json` guardado. Si el equipo cambió `GENERADO` a
  `APROBADO` manualmente en alguna fila, sincroniza ese cambio de vuelta al
  JSON (por `post_id`, usando el número de fila como referencia al orden
  original). Si el equipo escribió un comentario de ajuste en una celda en
  vez de aprobar, trátalo igual que una petición de cambio puntual.

**En cualquier caso:** cuando se actualice el `estado` de algún post, vuelve
a guardar el historial con `pipeline.historial.guardar_contenido_final()`
para que `output/{cliente}/{mes}/contenido_final.json` quede al día (incluye
el estado real de aprobación, no solo el de generación).

## Qué NO haces

No publicas nada — eso sigue siendo manual por el equipo (ver
`PLAN_MAESTRO.md`, "Publicación MANUAL por ahora"). Este skill solo notifica
y registra la aprobación, no ejecuta la publicación.

## Manejo de errores

Si no hay respuesta del equipo después de un tiempo razonable, no asumas
aprobación silenciosa — el contenido se queda en `GENERADO` (no aprobado)
hasta que alguien responda explícitamente. Si el canal de notificación falla
(ej. WhatsApp no disponible), cae al medio alterno si `medio_aprobacion` es
`ambos`; si es exclusivamente `whatsapp` y falla, deja el Excel como
respaldo y registra el error.
