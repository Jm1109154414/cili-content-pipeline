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
- Si el cliente es CiLi: lee también `briefs/cili_pilares_completo.md` (avatar
  real, dolores/deseos/certezas, framework de códigos) y
  `prompts/reference_banco_temas_cili.md` (banco de temas por certificación +
  5 ejemplos ya redactados de tono).
- Si existen meses anteriores del mismo cliente en `output/{cliente}/`, revísalos
  para **no repetir** temas ya publicados.

## Reglas de la estrategia (qué publicar)

1. Distribuye los posts respetando `frecuencia_semanal` y las `plataformas`
   del brief, repartidos a lo largo del mes.
2. Cada post debe declarar:
   - `fecha` (dentro del mes del brief)
   - `plataforma` (una de: Instagram, LinkedIn, Facebook, TikTok)
   - `tipo`: `imagen_sola` | `carrusel` | `reel` | `historia` | `video_corto`
   - `objetivo`: `awareness` | `educacion` | `credibilidad` | `conversion` | `comunidad`
3. Mezcla de objetivos en el mes: ~40% educación, ~30% conversión, ~20%
   credibilidad, ~10% comunidad — salvo que el brief pida otro reparto
   explícito (`objetivo_mes`, `descripcion_objetivo`).
4. El mismo tema puede adaptarse a 2-3 plataformas con ajustes de formato,
   no hace falta un tema distinto por cada post.
5. **Si el cliente es CiLi:** elige los temas del banco en
   `reference_banco_temas_cili.md` según el nivel de certificación que
   indique `tema_semana_N` del brief (Yellow / Green Lean / Green Six Sigma /
   Black Belt). No repitas un tema ya usado en un mes anterior de CiLi.
6. **Para cualquier otro cliente:** los temas salen del propio brief
   (`temas_que_funcionan`, `dolores`, `deseos`, `servicio_principal`).

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
      "fecha": "2026-07-03",
      "plataforma": "LinkedIn",
      "tipo": "carrusel",
      "objetivo": "educacion",
      "codigos_framework": ["PR", "I"],
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

Si la generación de un post falla o queda incompleta, no detengas el resto del
mes: marca ese post con `"estado": "PENDIENTE_MANUAL"` en el JSON y continúa
con los siguientes. El chequeo de marca (skill aparte) revisa el resultado
completo después.
