---
name: chequeo-marca
description: Revisa el contenido ya generado (estrategia+copy+imagen) contra los estándares de marca del brief antes de entregarlo al equipo. Usar después de imagenes y antes de armar el entregable final (output_formatter.py).
---

# Chequeo de marca

Revisas el contenido completo de un mes (texto + descripción de imagen) contra
las reglas de marca del brief del cliente, **antes** de que llegue al equipo
para aprobación. No generas nada nuevo — solo detectas y marcas problemas.

## Cuándo se usa

Después de que `estrategia-copy` e `imagenes` ya generaron todo el mes. Antes
de `pipeline/output_formatter.py`. Es el último filtro automático antes del
checkpoint 2 (aprobación humana).

## Entrada

- La salida de `estrategia-copy`: todos los posts del mes (`post_id`, gancho,
  cuerpo, cta, copy_completo, idea_visual, etc.)
- La salida de `imagenes`: `ruta_imagen`/`ruta_copy`/`estado` por `post_id`
- El brief del cliente completo, en particular: `evitar`, `temas_a_evitar`,
  `tono`, `tres_palabras_marca`, `credenciales`/`testimonios` (para verificar
  que las cifras citadas existan en el brief, no inventadas)

## Paso 0 — Emparejar por `post_id`, nunca por posición

Antes de revisar nada, une cada post de `estrategia-copy` con su contraparte
de `imagenes` **buscando el mismo `post_id`** (no asumas que están en el mismo
orden en ambas listas — si un post se saltó o se reordenó, emparejar por
posición le pegaría la imagen equivocada al post equivocado).

## Qué revisar, post por post

Cada hallazgo tiene una **categoría** y una **severidad** — esto le ayuda al
equipo a priorizar qué revisar primero en vez de tratar todo igual (ver
"Salida esperada" abajo para el formato exacto).

**Categoría `marca`** (consistencia con la identidad del cliente):
1. **Temas prohibidos** (severidad alta): ¿el post toca algo de
   `temas_a_evitar`? (ej. para CiLi: política, temas sociales controversiales,
   críticas directas a competidores por nombre)
2. **Qué evitar** (severidad media-alta, según qué tan grave): ¿el post cae en
   algo de `evitar`? (ej. para CiLi: lenguaje técnico sin explicar, frases
   motivacionales genéricas tipo "frase del día")
3. **Tono** (severidad baja-media): ¿el post suena consistente con `tono` y
   `tres_palabras_marca`? (ej. CiLi: profesional pero accesible, basado en
   datos — no debe sonar como anuncio genérico de curso barato)
4. **Idea visual** (severidad media): ¿la `idea_visual`/prompt de imagen
   describe algo que el brief pide evitar? (ej. foto de stock de personas
   sonriendo en oficina)
5. **Nombres de competidores** (severidad alta): ¿el post menciona por nombre
   a alguien de `competidores`? Esto se prohíbe **siempre, para cualquier
   cliente**, no solo para CiLi.

**Categoría `legal`** (riesgo de credibilidad o reclamo, no solo estilo):
6. **Cifras y datos citados** (severidad alta): si el copy menciona un número
   o dato concreto (ej. "+2,000 certificados", "$121 MDD en ahorros"), debe
   **existir literalmente** en `credenciales`, `testimonios` o `casos_exito`
   del brief. Una cifra inventada o alterada no es un detalle de estilo —
   es una afirmación que el cliente no puede respaldar si alguien la cuestiona.
7. **Superlativos sin respaldo** (severidad media): palabras como "el mejor",
   "el más rápido", "el único" sin un dato o comparación que lo sostenga.
   Igual que el punto 6: no es solo tono, es una afirmación verificable.
8. **Testimonios sin atribución clara**: si el post cita un testimonio,
   confirma que venga literal de `testimonios` del brief (con nombre/cargo),
   no una paráfrasis inventada que suene a cita real.

## Qué NO haces

No reescribes el copy ni regeneras nada. Solo marcas. La corrección, si hace
falta, la hace el equipo en el checkpoint de aprobación o se vuelve a correr
ese post puntual por `estrategia-copy`/`imagenes`.

## Regla de precedencia de `estado` (no negociable)

Este skill consolida el `estado` final de cada post — ver el vocabulario único
en `PLAN_MAESTRO.md`. **Antes de escribir nada, revisa el `estado` que ya
trae el post** (de `estrategia-copy`) y el de su imagen correspondiente (de
`imagenes`, recibido en la entrada):

- Si el post ya tiene `"estado": "PENDIENTE_MANUAL"` (el texto falló) o su
  imagen tiene `"estado": "IMAGEN_PENDIENTE"` (la imagen falló): **respeta
  ese estado, no lo sobrescribas.** Solo agrega `alertas_marca` si encontraste
  algo adicional, pero el `estado` se queda como venía.
- Solo si el post no trae ya un estado de falla, escribe `GENERADO` (si no
  encontraste problemas) o `REVISAR_MARCA` (si encontraste alguno).

Esto evita que un chequeo de marca "limpio" tape silenciosamente que la
imagen de ese post nunca se generó.

## Salida esperada (JSON) — este es el JSON FINAL, único, que recibe `output_formatter.py`

Este skill es el que **consolida todo en una sola lista**: toma cada post de
`estrategia-copy`, le agrega `ruta_imagen`/`ruta_copy` de su contraparte en
`imagenes` (emparejado por `post_id`, Paso 0), resuelve el `estado` final
(regla de precedencia arriba) y agrega `alertas_marca`. Después de este paso
**no hace falta ninguna otra lista** — `pipeline/output_formatter.py` recibe
directamente este JSON.

```json
{
  "posts": [
    {
      "post_id": "post_01",
      "...": "todos los campos originales del post de estrategia-copy, sin alterar el texto",
      "ruta_imagen": "output/cili/julio_2026/imagenes/post_01_linkedin_2026-07-03/imagen.png",
      "ruta_copy": "output/cili/julio_2026/imagenes/post_01_linkedin_2026-07-03/copy.txt",
      "estado": "GENERADO",
      "alertas_marca": []
    },
    {
      "post_id": "post_02",
      "...": "post con problema detectado, pero su imagen sí se generó bien",
      "ruta_imagen": "output/cili/julio_2026/imagenes/post_02_instagram_2026-07-04/imagen.png",
      "estado": "REVISAR_MARCA",
      "alertas_marca": [
        {
          "categoria": "legal",
          "severidad": "alta",
          "descripcion": "Cifra '+5,000 certificados' no coincide con credenciales del brief (dice +2,000)"
        },
        {
          "categoria": "marca",
          "severidad": "alta",
          "descripcion": "El post menciona por nombre a 'CI Academy', que está en competidores"
        }
      ]
    },
    {
      "post_id": "post_03",
      "...": "post cuya imagen falló — el estado de imagenes se respeta, no se pisa",
      "ruta_imagen": "",
      "estado": "IMAGEN_PENDIENTE",
      "alertas_marca": []
    }
  ]
}
```

Los posts con `REVISAR_MARCA` o `IMAGEN_PENDIENTE` deben saltar a la vista del
equipo antes de aprobar el mes completo. No detengas el resto del mes por un
post con alerta: sigue revisando todos, entrega el reporte completo.

## Reporte adicional (para la notificación al equipo)

Junto con el JSON, genera un resumen de una línea por alerta encontrada, **ordenado
por severidad (alta primero)** — así el equipo prioriza qué revisar primero en
vez de leer la lista en orden aleatorio. Incluye esto en la notificación de
aprobación (WhatsApp/Excel — ver `PLAN_MAESTRO.md`, Paso 5). Ejemplo:

> ⚠️ 2 de 20 posts necesitan revisión antes de aprobar:
> - 🔴 Post 7 (legal, alta): cifra no coincide con el brief
> - 🟡 Post 14 (marca, media): tono más casual de lo habitual
