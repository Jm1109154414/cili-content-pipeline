---
name: estrategia-copy
description: Genera la estrategia de contenido del mes y el copy completo de cada post para un cliente de marketing orgánico (CiLi y futuros clientes), a partir de su brief validado. Usar cuando el brief de un cliente ya fue confirmado (checkpoint 1) y hay que producir el calendario del mes.
---

# Estrategia + Copy del mes

Generas, en un solo paso, la estrategia de contenido del mes **y** el copy
completo de cada post, para un cliente cuyo brief ya fue validado y confirmado.

## Cuándo se usa

Después de que el agente de onboarding produjo el brief y el cliente lo
confirmó (checkpoint 1). Recibes el brief completo (formato `ClientBrief`,
ver `pipeline/brief_schema.py`) y, si el cliente es CiLi, el material de
referencia adicional descrito abajo.

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
- Si existen meses anteriores del mismo cliente en `output/{cliente}/`, revísalos
  para **no repetir** temas ya publicados.

## Reglas de la estrategia (qué publicar)

1. Distribuye los posts respetando `frecuencia_semanal` y las `plataformas`
   del brief, repartidos a lo largo del mes.
2. Cada post debe declarar:
   - `post_id` (secuencial: `post_01`, `post_02`, ... — ver "Convención de
     nombres" en `PLAN_MAESTRO.md`. **Los skills posteriores usan este id
     para referirse al post, nunca la posición en la lista.**)
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

### Framework de mensaje — usar el de CiLi cuando aplique

Si el cliente es CiLi, cada post debe construirse con su propio sistema de
códigos (no inventar uno genérico):

| Código | Significado | Qué cubre el post |
|---|---|---|
| P | Pilar | El tema general del post |
| PR | Problema | El dolor concreto que dispara el contenido |
| LM | Lead magnet | Si el post invita a descargar/probar algo |
| B | Beneficios | Qué gana el lector |
| C | Certeza | Prueba social, garantía, dato de respaldo |
| TI | Tiempo invertido | Cuánto esfuerzo/tiempo le toma al cliente |
| S | Sacrificio | Qué tiene que invertir/sacrificar el cliente |
| I | Informativo | Valor puro, sin venta |
| CN | Conectar | Cercanía/comunidad, sin venta directa |

Cada post debe declarar en el JSON de salida qué código(s) cubre
(`codigos_framework: ["PR", "B"]`, por ejemplo). Para clientes que no sean
CiLi y no tengan su propio framework, usa el reparto de objetivos genérico
(sección anterior) sin forzar estos códigos.

### Patrón de gancho/CTA (validado en los ejemplos reales de CiLi)

El gancho es casi siempre **una pregunta directa al dolor o deseo del
prospecto** ("¿Te imaginas un sistema que permita a tu equipo resolver
problemas en tiempo real?"). El CTA cierra retomando esa misma pregunta como
invitación a actuar ("¿Estás listo para implementar un sistema así?"). Sigue
este patrón salvo que el objetivo del post sea puramente informativo/comunidad.

### Reglas por plataforma (obligatorias, no opcionales)

- **Instagram:** máximo 300 palabras en el cuerpo, emojis moderados, saltos de
  línea frecuentes, gancho en la primera línea (antes de "ver más").
- **LinkedIn:** 400-700 palabras, tono profesional y reflexivo, primeras 2-3
  líneas críticas (antes de "ver más"), pocos emojis (solo para organizar:
  →, ✅, 📌), 3-5 hashtags específicos del nicho.
- **Facebook:** 100-300 palabras, tono conversacional, cierra con una pregunta
  para generar comentarios, 1-3 hashtags.
- **TikTok:** caption máximo 150 caracteres + hashtags, el guion del video
  importa más que el caption — siempre incluye `script_video` con marcas de
  tiempo `[0-3s]`, `[3-10s]`, etc.

### Qué evitar siempre

Respeta `evitar` y `temas_a_evitar` del brief sin excepción. No prometas
resultados sin dato que los respalde. No uses lenguaje técnico sin explicarlo.

## Salida esperada (JSON, una sola estructura)

```json
{
  "posts": [
    {
      "post_id": "post_01",
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
