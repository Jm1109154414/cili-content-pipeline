---
name: imagenes
description: Genera la imagen final de cada post del mes (vía GPT Image 2 de OpenAI), a partir de la salida del skill estrategia-copy y los estándares de marca del brief. Usar después de que estrategia-copy produjo el contenido del mes, antes del chequeo de marca y del entregable final.
---

# Generación de imágenes

Generas la imagen final de cada post, alineada a la marca del cliente, usando
**GPT Image 2** (de OpenAI — mismo proveedor que ya usamos para validar texto
con modelos hermanos; ~99% de precisión de texto dentro de imagen, soporta 4K
y texto denso/multilenguaje — el motor elegido en `COSTOS.md` y `PLAN_MAESTRO.md`).

## Cuándo se usa

Después de que el skill `estrategia-copy` generó el contenido del mes (un post
por entrada, cada uno con `idea_visual`, `plataforma` y `tipo`). Antes del
chequeo de marca y de armar el entregable final (`output_formatter.py`).

## Entrada

- La salida de `estrategia-copy`: lista de posts, cada uno con al menos
  `post_id`, `fecha`, `plataforma`, `tipo`, `idea_visual`, `gancho`/`copy_completo`
  y `estado`.
- El brief del cliente: `colores_hex`, `estilo_visual`, `evitar` y
  `tres_palabras_marca` para que la imagen respete la identidad de marca, más
  `credenciales`/`testimonios`/`casos_exito` cuando el post necesite mostrar
  una cifra real dentro de la imagen (Paso 1).

## Antes de generar — respeta el `estado` previo

Si un post ya viene con `"estado": "PENDIENTE_MANUAL"` (el texto falló en
`estrategia-copy`), **no generes su imagen** — no tiene sentido gastar en una
imagen para un post cuyo copy no existe todavía. Pasa ese post directo a la
salida con el mismo `estado: "PENDIENTE_MANUAL"` y sin `ruta_imagen`, y sigue
con el resto.

## Paso 1 — Construir el prompt de imagen (por post)

Estructura el prompt siguiendo este orden — **Sujeto + Escenario + Estilo +
Iluminación + Composición + Técnico** — así no se te olvida ningún elemento:

> Ejemplo: "Bold typographic infographic [sujeto] on dark navy background
> [escenario], minimalist corporate style [estilo], high contrast lighting
> [iluminación], centered headline with supporting data point below
> [composición], 1080x1350px clean vector aesthetic [técnico]."

Para cada post, escribe un prompt en **inglés** para GPT Image 2 que incluya:

- **Estilo:** uno de `tipographic | infographic | abstract | diagram | dark_corporate`,
  elegido según `estilo_visual` del brief y el `tipo` del post.
- **Colores:** deben respetar `colores_hex` del brief — menciónalos explícitamente
  en el prompt (GPT Image 2 sigue bien instrucciones de paleta y composición).
- **Texto/datos dentro de la imagen:** si el post lleva un dato, cifra o frase
  corta (el `gancho`, o un número del brief como "+2,000 certificados"),
  inclúyelo explícitamente en el prompt — GPT Image 2 tiene la mayor precisión
  de texto del mercado (~99% de caracteres correctos), úsala.
- **Jerarquía visual:** como GPT Image 2 es más fuerte en precisión de texto
  que en "instinto de diseño editorial", sé explícito en el prompt sobre qué
  es título vs. subtítulo vs. dato de apoyo — no asumas que lo va a priorizar solo.
- **Qué evitar:** nunca fotografía de stock de personas sonriendo en oficina,
  nunca watermarks, nunca texto genérico de relleno. Respeta también el campo
  `evitar` del brief.
- **Mood:** referencia las `tres_palabras_marca` del brief.

Reglas duras (no negociables, igual para cualquier cliente):
- Prioriza diseño tipográfico/gráfico sobre fotografía de personas.
- Si el post lleva datos o números, deben aparecer legibles en la imagen.
- Sin watermarks, sin texto de relleno, sin personas de stock obvias.
- La imagen debe verse premium y diferenciada, nunca genérica de IA.

## Paso 2 — Dimensiones por plataforma

| Plataforma / tipo | Dimensiones |
|---|---|
| Instagram post | 1080x1350px |
| Instagram reel cover | 1080x1920px |
| LinkedIn | 1200x627px |
| Facebook | 1200x630px |
| TikTok cover | 1080x1920px |

## Paso 3 — Generar con GPT Image 2

Usa la tool nativa de imagen de OpenClaw apuntando a GPT Image 2, calidad
"medium" (~$0.05/imagen — ver `COSTOS.md`). Si GPT Image 2 no está disponible
o falla, plan B en este orden: Ideogram 4.0 → Imagen 4 (Google).

Guarda cada imagen en `output/{cliente}/{mes}/imagenes/{post_id}_{plataforma}_{fecha}/imagen.png`
(usa el `{cliente}`/`{mes}` slug de "Convención de nombres" en `PLAN_MAESTRO.md`
y el `post_id` que trajo el post, no inventes uno nuevo), y junto a ella un
`copy.txt` con el `copy_completo` de ese post (para que el equipo revise
imagen+texto juntos).

## Manejo de errores

Si la generación de una imagen falla:
1. Reintenta una vez.
2. Si vuelve a fallar, genera un placeholder simple (fondo de color de marca +
   el gancho del post como texto) y marca ese post como `"estado": "IMAGEN_PENDIENTE"`.
3. Continúa con el siguiente post — nunca detengas el lote completo por una imagen.
4. Registra el error en `output/{cliente}/{mes}/errores.log`
   (`timestamp | IMAGEN_ERROR | post_id | detalle`).

## Salida esperada (JSON)

```json
{
  "posts": [
    {
      "post_id": "post_01",
      "ruta_imagen": "output/cili/julio_2026/imagenes/post_01_linkedin_2026-07-03/imagen.png",
      "ruta_copy": "output/cili/julio_2026/imagenes/post_01_linkedin_2026-07-03/copy.txt",
      "estado": "GENERADO"
    }
  ]
}
```

Esta salida la consume `chequeo-marca`, que la empareja con los posts de
`estrategia-copy` **por `post_id`** (no por posición) para producir el
JSON final que recibe `pipeline/output_formatter.py`.
