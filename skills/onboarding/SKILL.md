---
name: onboarding
description: Conversa con un cliente nuevo o recurrente por WebChat para producir su brief de marketing (estructura ClientBrief), pre-llenando lo que pueda leyendo su web/redes y preguntando solo lo que falte. Usar al inicio de cualquier ciclo mensual, antes de estrategia-copy. Dispara este skill siempre que el operador diga cosas como "dar de alta un cliente nuevo", "vamos a hacer el onboarding de [cliente]", "necesito el brief de [cliente] para este mes", "actualizar la info de [cliente]" o "platica con [cliente] para sacar su brief" — incluso si no mencionan la palabra "brief" u "onboarding" explícitamente.
---

# Onboarding conversacional

Platicas con el cliente (dueño/marketing del negocio) por WebChat y produces
tú mismo su brief completo — sin que nadie llene un JSON a mano. Esta es la
puerta de entrada de todo el flujo (ver `PLAN_MAESTRO.md`, Paso 0).

## Antes de empezar — ¿cliente nuevo o recurrente?

Busca en tu memoria/`briefs/` si ya existe un brief de este cliente de un mes
anterior.

- **Si es recurrente:** ya tienes las secciones A-E (casi no cambian mes a
  mes). Saluda reconociéndolo y pregunta **solo la Sección F** (mes, tema,
  evento, objetivo). No repitas las 30 preguntas de las secciones A-E.
- **Si es nuevo:** sigue el flujo completo de abajo.

## Paso 1 — Pre-llenado automático (solo cliente nuevo)

Antes de preguntar nada, usa búsqueda web y navegador para leer el sitio web
y redes sociales (Instagram/LinkedIn/Facebook) que el cliente te dé. Intenta
sacar tú mismo:

- `empresa`, `industria`, `ciudad`, `web`, `redes_sociales`, `descripcion`
- `servicio_principal`, `que_incluye`, `diferenciadores` (de su propia página)
- `colores_hex`, `estilo_visual` (de las imágenes/branding que ya usan)
- `credenciales`, `testimonios`, `casos_exito` (si los publican)

No inventes nada que no puedas verificar en la fuente. Lo que no puedas sacar,
quedará pendiente para preguntarlo.

## Paso 2 — Conversación guiada (rellenar lo que falte)

Usa `briefs/FORMULARIO_ONBOARDING.md` como guion de las 6 secciones, pero
**no lo leas literal como cuestionario** — convérsalo de forma natural,
agrupando preguntas relacionadas, y **omite cualquier campo que ya hayas
pre-llenado en el Paso 1** (solo confírmalo de paso, no lo vuelvas a preguntar
completo).

Para el cliente, evita la jerga del JSON. Ejemplos de cómo traducir cada
sección a lenguaje natural:

- Sección A (identidad) → "Cuéntame de tu negocio: qué hacen, hace cuánto, y
  dónde los puedo encontrar en redes."
- Sección B (oferta) → "¿Qué quieres vender más este mes? ¿Qué incluye y qué
  te hace diferente de la competencia?"
- Sección C (cliente ideal) → "¿Quién es tu cliente típico, y qué problema
  tiene que lo hace buscarte? ¿Y hay alguien que claramente NO sea tu cliente
  ideal, aunque a veces te contacten?" (esta última es opcional —
  `anti_cliente` en el brief — útil para que el contenido no apunte
  accidentalmente al público equivocado, pero no insistas si no se les
  ocurre nada)
- Sección D (marca) → "¿Cómo quieres que suene tu marca? ¿Hay algo que nunca
  deberíamos publicar?"
- Sección E (credibilidad) → "¿Qué números o testimonios tienes para
  respaldar lo que ofreces? ¿Y quiénes consideras tu competencia directa?"
  (la respuesta de competencia es importante: el chequeo de marca usa esa
  lista para nunca mencionarlos por nombre en el contenido)
- Sección F (del mes) → "¿Qué tema quieres tocar este mes? ¿Hay algo especial
  que celebrar o lanzar?"

**No le preguntes al cliente** por `medio_aprobacion` — es una preferencia
interna de cómo el equipo que opera la cuenta revisa el contenido (WhatsApp,
Excel, o ambos), no algo que decida el cliente final. Si el brief no la trae,
queda en `"ambos"` por default (ver `pipeline/brief_schema.py`).

## Paso 3 — Insistir en respuestas vagas (regla dura, no opcional)

Si una respuesta es genérica ("buen servicio", "clientes contentos",
"profesional"), **siempre pide un ejemplo concreto** antes de avanzar al
siguiente campo. No aceptes la respuesta vaga ni la marques como "débil" —
repregunta hasta obtener algo específico (un número, un nombre, una cita
textual, un caso real). Esta es la regla de calidad de dato más importante de
todo el onboarding: el resto del pipeline (estrategia, copy, chequeo de marca)
depende de que estos campos tengan sustancia real, no relleno.

Ejemplo de repregunta: *"Entiendo que dan buen servicio — ¿me compartes un
ejemplo concreto, un testimonio real o un dato que lo demuestre?"*

**Campos que requieren mínimo 3 elementos concretos (no aceptes menos):**
`dolores`, `deseos`, `objeciones`. **Campos que requieren mínimo 1, idealmente
2+:** `testimonios`, `colores_hex`, `tres_palabras_marca`. Si el cliente da
menos de lo mínimo, sigue insistiendo en esos campos específicos antes de
avanzar — `pipeline/brief_schema.py` rechaza el brief si quedan vacíos.

## Paso 4 — Validar contra el schema

Cuando creas tener todo, construye el JSON con la estructura de
`pipeline/brief_schema.py` (secciones A-F, mismos nombres de campo) y
ejecuta la validación (`validate_and_report`). Si faltan campos obligatorios
o algún valor no es válido (plataformas, nivel_conciencia, objetivo_mes),
**regresa a preguntar específicamente eso** — no le digas al cliente "hay un
error", dile en lenguaje natural qué falta.

## Paso 5 — Checkpoint 1: el cliente confirma

Antes de guardar el brief como definitivo, muéstrale al cliente un resumen
breve en lenguaje natural de lo que entendiste (no el JSON crudo):

> "Esto es lo que entendí de tu negocio: [resumen de 5-6 líneas]. ¿Está
> correcto o falta/sobra algo?"

Si el cliente corrige algo, actualiza el brief y vuelve a validar. Solo
cuando confirme, continúa al paso final.

## Paso 6 — Guardar y entregar

Guarda el brief en `briefs/{cliente}_{mes}.json`. Si el cliente es nuevo,
queda guardado completo para reutilizar el mes siguiente (solo la Sección F
se repregunta). Notifica que el brief quedó listo para que el equipo que
opera el servicio proceda con la generación de contenido más adelante (no
aquí — este checkpoint es solo del cliente confirmando su brief, distinto del
checkpoint 2 donde el equipo aprueba el contenido ya generado).

## Manejo de errores

Si el cliente abandona la conversación a la mitad, guarda el progreso parcial
(lo que ya se confirmó) y, cuando vuelva, retómalo desde donde se quedó —
no reinicies desde cero.
