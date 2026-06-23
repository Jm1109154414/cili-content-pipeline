# ESTIMACIÓN DE COSTOS — Costo por cliente al mes
## CiLi · Junio 2026 · Para la junta

> Estimación del costo de **APIs** para generar un mes de contenido por cliente.
> Supuesto: **~20 posts/mes** (5 por semana × 4 semanas), texto + imagen por post.
> Tipo de cambio usado: **~$18.5 MXN/USD**.

---

## PRECIOS ACTUALES DE LAS APIs (junio 2026)

### Texto (estrategia + copy + chequeo de marca)
| Modelo | Input ($/millón tokens) | Output ($/millón tokens) | Nota |
|---|---|---|---|
| **Claude Sonnet 4.6** | $3.00 | $15.00 | Mejor calidad en español (nuestra elección) |
| GPT-5.4 (medio) | $2.50 | $15.00 | Prácticamente el mismo costo |
| GPT-5.5 (flagship) | $5.00 | $30.00 | El doble, no se justifica para esto |

### Imágenes
| Modelo | Costo por imagen | Nota |
|---|---|---|
| **GPT Image 2 medium (elegido)** | **~$0.05** | OpenAI, mismo proveedor que para texto. ~99% de precisión de texto dentro de imagen, 4K, texto denso/multilenguaje |
| Ideogram 4.0 turbo | $0.03 | Plan B — mejor "instinto de diseño editorial" (jerarquía título/subtítulo), pero menos preciso en caracteres que GPT Image 2 |
| Imagen 4 (Google) | $0.02-0.06 | Plan C — también fuerte en texto legible |
| Flux 2 Pro | $0.04-0.055 | Descartado — fuerte en fotorrealismo, que justo evitamos |

> ⚠️ **Corrección importante:** DALL-E 3 fue **retirado de la API el 12 de mayo de 2026**
> y ya tampoco existe GPT Image 1 (reemplazado por GPT Image 1.5 y ahora **GPT Image 2**,
> abril 2026 — la generación vigente). El código y `CONTEXTO.md` (histórico) mencionan
> el motor viejo — ya corregido en los skills a **GPT Image 2**.
>
> **Por qué GPT Image 2 y no Ideogram:** Ideogram tiene mejor "sentido de diseño"
> (jerarquía visual tipo cartel), pero GPT Image 2 es más preciso con texto/datos
> (~99% vs ~90-95% de caracteres correctos) y usamos OpenAI de cualquier forma.
> Se deja Ideogram 4.0 como plan B si la jerarquía visual no sale bien.

### Video (fase futura — Reels/TikTok)
| Modelo | Costo | Nota |
|---|---|---|
| **Kling 3.0 (elegido)** | $0.10/seg (~$2/Reel de 20s) | Buen equilibrio calidad/precio, fuerte en consistencia de personaje |
| Wan 2.6 | $0.05/seg | Más barato, calidad menor |
| Sora 2 / Veo 3.1 | $0.10-$0.75/seg | Premium, no se justifica para contenido orgánico mensual |
| OpenAI TTS (voiceover) | ~$0.015/min | Centavos, irrelevante |
| Suno (música de fondo) | ~$0.05-0.11/canción | Centavos, irrelevante |

> **CapCut se descartó:** es un editor manual sin API pública — no genera video
> desde un prompt y no se puede automatizar sin simular clics (frágil, rompe la
> automatización). No entra al pipeline.

---

## CÁLCULO — Cliente recurrente (mes normal)

### Texto (con Claude Sonnet 4.6)
| Paso | Tokens entrada | Tokens salida | Costo USD |
|---|---|---|---|
| Estrategia del mes | ~3,000 | ~4,000 | $0.07 |
| Copy de 20 posts | ~8,000 | ~15,000 | $0.25 |
| Idea visual por post | ~5,000 | ~4,000 | $0.08 |
| Chequeo de marca | ~6,000 | ~1,000 | $0.03 |
| Onboarding del mes (solo sección F) | ~10,000 | ~3,000 | $0.07 |
| **Subtotal texto** | | | **~$0.50** |

### Imágenes (20 posts, 1 imagen c/u, con GPT Image 2 medium)
| Cálculo | Costo USD |
|---|---|
| 20 × $0.05 | **$1.00** |

### Total por cliente al mes — solo texto + imagen (con 30% de buffer)
| Componente | USD/mes | MXN/mes aprox |
|---|---|---|
| Texto (Claude Sonnet 4.6) | $0.50 | ~$9 MXN |
| Imágenes (GPT Image 2) | $1.00 | ~$19 MXN |
| + 30% buffer (regeneraciones) | +$0.45 | ~$8 MXN |
| **Total** | **~$1.95** | **~$36 MXN** |

> El **primer mes** de un cliente nuevo suma ~$0.30 USD extra (una vez) por el
> onboarding completo con lectura de su web y redes. Despreciable.

---

## EL TITULAR PARA LA JUNTA

> **Generar un mes completo de contenido (texto + imágenes) para un cliente
> cuesta ~$36 pesos en APIs.** El costo de tokens es prácticamente irrelevante
> frente a lo que se puede cobrar por el servicio.
>
> **Si el cliente quiere video (Reels con IA), eso se cobra aparte:**
> ~$150-185 MXN/mes adicionales por 4-5 Reels — ahí sí es un costo real.

**La conclusión real:** el costo de operación **no son las APIs**, es el **tiempo
humano de revisión y aprobación.** Ahí está el verdadero costo del servicio, no en
los tokens. Esto refuerza por qué conviene automatizar al máximo la revisión
(notificación + aprobación por WhatsApp).

---

## COMPARACIÓN DE PROVEEDORES — TEXTO

Para la carga mensual de texto (~32K tokens entrada, ~27K salida):

| Proveedor | Costo texto/mes | Veredicto |
|---|---|---|
| **Claude Sonnet 4.6** | ~$0.50 | ✅ Mejor español, mismo precio que GPT medio |
| GPT-5.4 | ~$0.49 | Empate en costo, calidad similar |
| GPT-5.5 | ~$0.97 | El doble, no se justifica |

**Recomendación:** Claude Sonnet 4.6 para texto (calidad en español), GPT Image 2
para imágenes (mayor precisión de texto/datos dentro de imagen, mismo proveedor
que ya usamos en otras partes del stack).

---

## ⚠️ VIDEO (fase futura) — cálculo detallado

Para 4-5 Reels/mes de 20 segundos con Kling 3.0 + TTS + Suno:

| Componente | Costo por Reel | 4-5 Reels/mes |
|---|---|---|
| Video (Kling 3.0, 20s) | ~$2.00 | ~$8.00-$10.00 |
| Voiceover (TTS) | ~$0.02 | ~$0.08-$0.10 |
| Música (Suno) | ~$0.05-0.11 | ~$0.20-$0.55 |
| **Total USD/mes** | | **~$8.30-$10.65** |
| **Total MXN/mes** | | **~$150-$195 MXN** |

A diferencia de texto/imagen (centavos), el video sí es un costo real —
**se debe cobrar como add-on aparte**, no incluido en el precio base del servicio.

---

## Fuentes
- [Claude API Pricing 2026](https://platform.claude.com/docs/en/about-claude/pricing)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [GPT Image 2 Pricing 2026 — WaveSpeed](https://wavespeed.ai/blog/posts/gpt-image-2-pricing-2026/)
- [GPT Image 2 vs Ideogram — PlyKit](https://plykit.ai/compare/gpt-image-2-vs-ideogram)
- [Ideogram 4 vs GPT Image 2 — Segmind](https://blog.segmind.com/ideogram-4-vs-gpt-image-2-a-design-and-text-showdown/)
- [Ideogram API Pricing](https://about.ideogram.ai/api-pricing)
- [Imagen 4 — Google Developers Blog](https://developers.googleblog.com/imagen-4-now-available-in-the-gemini-api-and-google-ai-studio/)
- [AI Video API Pricing — BuildMVPFast](https://www.buildmvpfast.com/api-costs/ai-video)
- [ElevenLabs / TTS Pricing — BuildMVPFast](https://www.buildmvpfast.com/api-costs/ai-voice)
- [Suno API Pricing 2026](https://sunor.cc/blog/suno-api-pricing-2026)
