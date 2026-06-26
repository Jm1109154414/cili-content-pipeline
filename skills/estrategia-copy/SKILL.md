---
name: estrategia-copy
description: Genera la estrategia de contenido del mes y el copy completo de cada post para un cliente de marketing orgánico (CiLi y futuros clientes), a partir de su brief validado. Usar cuando el brief de un cliente ya fue confirmado (checkpoint 1) y hay que producir el calendario del mes. Dispara este skill también si el operador pide "generar el contenido de [cliente] de este mes", "armar el calendario", "regenerar el post {post_id}" (un solo post puntual) o "necesito los copies de [cliente]" — no solo en el flujo automático completo.
---

# Estrategia + Copy del mes

Generas, en un solo paso, la estrategia de contenido del mes **y** el copy
completo de cada post, para un cliente cuyo brief ya fue validado y confirmado.

## Cuándo se usa

Después de que el agente de onboarding produjo el brief y el cliente lo
confirmó (checkpoint 1). Recibes el brief completo (formato `ClientBrief`,
ver `pipeline/brief_schema.py`) y, si el cliente tiene material de referencia
propio, también ese (ver "Entrada" abajo).

## Entrada

- El brief completo del cliente (JSON con las secciones A-F).
- **Busca material de referencia propio del cliente** antes de generar (ver
  "`briefs/` vs `clientes/{cliente}/` vs `examples/{cliente}/`" en
  `PLAN_MAESTRO.md`): primero en `clientes/{cliente}/{cliente}_pilares_completo.md`
  y `clientes/{cliente}/reference_banco_temas_{cliente}.md`; si no existe esa
  carpeta, intenta `examples/{cliente}/` (solo aplica a clientes de
  demostración, como CiLi). Si ninguno existe, sigue sin este material — no es
  obligatorio. CiLi es el caso piloto que hoy vive en `examples/cili/`, pero
  la regla aplica igual a cualquier cliente real con su propia carpeta en
  `clientes/`.
- **Temas ya usados en meses anteriores:** llama a
  `pipeline.historial.cargar_temas_anteriores("{cliente}")` (slug del
  cliente — ver "Convención de nombres") para obtener la lista de `tema` de
  todos los posts ya publicados. No repitas ninguno de esos temas este mes,
  salvo que el brief pida explícitamente revisitar uno (`evento_especial`,
  `descripcion_objetivo`).

## Reglas de la estrategia (qué publicar)

1. Distribuye los posts respetando `frecuencia_semanal` y las `plataformas`
   del brief, repartidos a lo largo del mes.
2. Cada post debe declarar:
   - `post_id` (secuencial: `post_01`, `post_02`, ... — ver "Convención de
     nombres" en `PLAN_MAESTRO.md`. **Los skills posteriores usan este id
     para referirse al post, nunca la posición en la lista.**)
   - `tema` (etiqueta corta de 2-4 palabras del tema de fondo, ej. "SIPOC",
     "5 S's", "Certificación Black Belt" — esto es lo que se guarda en el
     historial para que meses futuros no lo repitan; sé consistente con la
     etiqueta exacta del banco de temas del cliente si existe)
   - `fecha` (dentro del mes del brief)
   - `plataforma` (una de: Instagram, LinkedIn, Facebook, TikTok)
   - `tipo`: `imagen_sola` | `carrusel` | `reel` | `historia` | `video_corto`
   - `objetivo`: `awareness` | `educacion` | `credibilidad` | `conversion` | `comunidad`
3. Mezcla base de objetivos en el mes: ~40% educación, ~30% conversión, ~20%
   credibilidad, ~10% comunidad. **Ajusta este reparto según `objetivo_mes`
   del brief** (son dos vocabularios distintos — `objetivo_mes` es la meta
   del mes completo, `objetivo` es el tipo de cada post individual):

   | `objetivo_mes` del brief | Cómo ajustar la mezcla de `objetivo` por post |
   |---|---|
   | `awareness` | Sube `awareness` a ~30%, baja `conversion` a ~15% |
   | `leads` | Sube `conversion` a ~40% (con CTA hacia el lead magnet), mantén `credibilidad` en 20% |
   | `ventas` | Sube `conversion` a ~45-50%, baja `educacion` a ~25-30% |
   | `comunidad` | Sube `comunidad` a ~20-25%, baja `conversion` a ~20% |

   Si el brief además da `descripcion_objetivo`, sigue esa instrucción
   específica por encima de la tabla.
4. El mismo tema puede adaptarse a 2-3 plataformas con ajustes de formato,
   no hace falta un tema distinto por cada post.
5. **Si el cliente tiene un banco de temas propio** (ver "Entrada" arriba):
   elige los temas de ahí según el nivel/categoría que indique `tema_semana_N`
   del brief. No repitas un tema ya usado en un mes anterior del mismo cliente.
6. **Si el cliente no tiene banco de temas propio:** los temas salen del
   propio brief (`temas_que_funcionan`, `dolores`, `deseos`, `servicio_principal`).
7. **Usa `objeciones` del brief explícitamente** para los posts de objetivo
   `credibilidad` o que cubran el código `C` (Certeza, si el cliente usa el
   framework de códigos): cada objeción real del brief es una oportunidad de
   post que la responde directamente (ej. objeción "es muy caro" → post de
   certeza sobre el retorno de inversión).

## Reglas del copy (cómo escribir cada post)

### Framework de mensaje — usa el del cliente si existe, no inventes uno genérico

Si el material de referencia del cliente (ver "Entrada") define su propio
sistema de códigos para estructurar mensajes, **úsalo tal cual está
documentado ahí** — no lo sustituyas por uno genérico ni inventes otro.

> Ejemplo real: CiLi tiene su propio framework de 9 códigos (Pilar, Problema,
> Lead magnet, Beneficios, Certeza, Tiempo invertido, Sacrificio, Informativo,
> Conectar) documentado en `examples/cili/cili_pilares_completo.md`. Cuando el
> cliente sea CiLi, sigue ese framework exactamente como está ahí, no lo
> reescribas de memoria.

Cuando el cliente tenga un framework propio, cada post debe declarar en el
JSON de salida qué código(s) cubre (`codigos_framework: ["PR", "B"]`, usando
los códigos exactos del cliente). **Si el cliente no tiene framework propio**,
usa el reparto de objetivos genérico (sección anterior) sin forzar ningún
código.

### Patrón de gancho/CTA

El patrón validado en los ejemplos reales de CiLi es: **una pregunta directa
al dolor o deseo del prospecto** ("¿Te imaginas un sistema que permita a tu
equipo resolver problemas en tiempo real?"), con el CTA retomando esa misma
pregunta como invitación a actuar. Úsalo como default, pero **no abuses de un
solo patrón mes tras mes** — varía con estos otros tipos de gancho para que
el contenido no se sienta repetitivo:

- **Curiosidad:** "Esto es lo que nadie te dice sobre [tema]."
- **Historia:** "La semana pasada nos pasó algo que cambió cómo vemos [tema]."
- **Valor directo:** "3 señales de que tu proceso necesita [solución] (sin [dolor común])."
- **Contrarian:** "Todo mundo dice [creencia común]. Está mal. Esto es lo que sí funciona."

Elige el tipo de gancho según el `objetivo` del post: pregunta-al-dolor y
valor directo funcionan mejor para `conversion`/`credibilidad`; curiosidad e
historia para `educacion`/`comunidad`.

### Reglas por plataforma (obligatorias, no opcionales)

- **Instagram:** máximo 300 palabras en el cuerpo, emojis moderados, saltos de
  línea frecuentes, gancho en la primera línea (antes de "ver más").
- **LinkedIn:** 400-700 palabras, tono profesional y reflexivo, primeras 2-3
  líneas críticas (antes de "ver más"), pocos emojis (solo para organizar:
  →, ✅, 📌), 3-5 hashtags específicos del nicho.
- **Facebook:** 100-300 palabras, tono conversacional, cierra con una pregunta
  para generar comentarios, 1-3 hashtags.
- **TikTok:** caption máximo 150 caracteres + hashtags, el guion del video
  importa más que el caption.

### Guion de video corto (reel / video_corto / tiktok) — no dejes `script_video` vago

**Regla de los 3 segundos:** los primeros 3 segundos deben combinar al mismo
tiempo gancho visual + gancho verbal + texto en pantalla — si solo hay uno de
los tres, se pierde el scroll. No empieces el guion con una introducción
lenta ("Hola, hoy les voy a hablar de...").

Usa una de estas 3 estructuras (con marcas de tiempo reales, no genéricas):

- **Problema-solución** (15-30s): `[0-3s]` plantea el problema → `[3-10s]`
  por qué importa → `[10-25s]` la solución/tip → `[25-30s]` CTA.
- **Formato lista** (30-60s): `[0-3s]` "X cosas que..." → un punto cada
  5-8 segundos → CTA al final.
- **Tutorial** (30-60s): `[0-3s]` muestra el resultado final primero →
  `[3-8s]` "así se hace" → pasos rápidos → resultado + CTA.

**Subtítulos:** la mayoría ve sin sonido — el guion debe asumir que el texto
en pantalla lleva todo el peso. Máximo 2 líneas visibles a la vez, 3-5
palabras por línea, sincronizado con lo que se dice en ese momento (esto es
insumo para quien edite el video, no solo para el copy).

### Chequeo rápido de calidad antes de cerrar cada post

**Test "¿y entonces qué?":** por cada afirmación del cuerpo, pregúntate si
responde por qué le debería importar al lector. Una característica sin
beneficio conectado no convence — agrega el puente que falta.

> ❌ "Usamos un sistema de gestión de calidad certificado"
> ✅ "Usamos un sistema certificado — por eso detectamos errores antes de
> que lleguen a tu cliente, no después"

**Sé específico, no vago:**

| Vago | Específico |
|---|---|
| "Ahorra tiempo" | "Reduce 4 horas semanales de reportes" |
| "Muchos clientes" | "+2,000 certificados" (usa cifras reales del brief) |
| "Resultados rápidos" | "Resultados en 30 días" |
| "Mejora tu proceso" | "Reduce desperdicio del proceso en un 30%" |

**CTA con pérdida en vez de solo ganancia** (cuando el objetivo es
`conversion`): a veces enmarcar lo que se pierde por no actuar funciona mejor
que solo el beneficio de actuar. "No dejes que tus procesos sigan
desperdiciando recursos" puede pegar más que "mejora tus procesos" — pero no
fuerces esto si suena alarmista o no calza con el tono del cliente.

### Qué evitar siempre

Respeta `evitar` y `temas_a_evitar` del brief sin excepción. No prometas
resultados sin dato que los respalde. No uses lenguaje técnico sin explicarlo.
**No uses el campo `competidores` del brief para inspirarte en críticas** —
eso ya lo prohíbe `chequeo-marca`, pero evita la tentación desde la raíz.

## Salida esperada (JSON, una sola estructura)

```json
{
  "posts": [
    {
      "post_id": "post_01",
      "tema": "SIPOC",
      "fecha": "2026-07-03",
      "plataforma": "LinkedIn",
      "tipo": "carrusel",
      "objetivo": "educacion",
      "codigos_framework": ["PR", "I"],
      "estado": "GENERADO",
      "gancho": "...",
      "cuerpo": "...",
      "cta": "...",
      "hashtags": ["#leansixsigma", "..."],
      "copy_completo": "gancho + cuerpo + cta + hashtags, ya armado",
      "script_video": "solo si tipo es reel/video_corto/tiktok, con marcas [0-3s]...",
      "idea_visual": "descripción corta de qué debe mostrar la imagen/video — insumo para el skill de imagen"
    }
  ]
}
```

Este JSON alimenta directo `pipeline/output_formatter.py` (columnas Fecha,
Plataforma, Tipo, Objetivo, Gancho, Copy completo, Hashtags, CTA) y al skill
de generación de imágenes (usa `idea_visual`).

## Errores y reintentos

Cada post debe incluir un campo `estado` (ver vocabulario único en
`PLAN_MAESTRO.md`): por defecto `"estado": "GENERADO"`. Si la generación de un
post falla o queda incompleta, no detengas el resto del mes: marca ese post
con `"estado": "PENDIENTE_MANUAL"` y continúa con los siguientes. Los skills
posteriores (`imagenes`, `chequeo-marca`) deben **respetar** `PENDIENTE_MANUAL`
y no sobrescribirlo.
