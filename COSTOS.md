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
| GPT Image 1 Mini (low) | ~$0.005 | Económico, calidad básica |
| **GPT Image 1.5 (medium)** | ~$0.05 | Equilibrio calidad/precio |
| GPT Image 1.5 (high) | ~$0.10 | Premium, para marca exigente |

> ⚠️ **Corrección importante:** DALL-E 3 fue **retirado de la API el 12 de mayo de 2026.**
> Nuestro código y el CONTEXTO.md aún lo mencionan — hay que cambiarlo a GPT Image 1.5.

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

### Imágenes (20 posts, 1 imagen c/u)
| Calidad | Cálculo | Costo USD |
|---|---|---|
| Económica (Mini) | 20 × $0.005 | $0.10 |
| **Media (GPT Image 1.5)** | 20 × $0.05 | $1.00 |
| Premium (high) | 20 × $0.10 | $2.00 |

### Total por cliente al mes (texto + imágenes + 30% de buffer por regeneraciones)
| Escenario | USD/mes | MXN/mes aprox |
|---|---|---|
| Económico | ~$0.80 | **~$15 MXN** |
| **Medio (recomendado)** | ~$2.00 | **~$37 MXN** |
| Premium | ~$3.25 | **~$60 MXN** |

> El **primer mes** de un cliente nuevo suma ~$0.30 USD extra (una vez) por el
> onboarding completo con lectura de su web y redes. Despreciable.

---

## EL TITULAR PARA LA JUNTA

> **Generar un mes completo de contenido para un cliente cuesta entre
> $15 y $60 pesos en APIs** (según calidad de imagen). El costo de tokens es
> prácticamente irrelevante frente a lo que se puede cobrar por el servicio.

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

**Recomendación:** Claude Sonnet 4.6 para texto (calidad en español), GPT Image 1.5
para imágenes. Costo combinado igual que cualquier alternativa, mejor resultado.

---

## ⚠️ OJO CON EL VIDEO (fase futura)

El video es **otro orden de magnitud.** Generar Reels/TikToks en video real
(video + voz + música) puede costar de **$10 a $50+ USD por cliente al mes**,
no centavos. Cuando lleguemos a esa fase hay que rehacer este cálculo y decidir
si se cobra como extra. Por ahora (texto + imágenes) el costo es trivial.

---

## Fuentes
- [Claude API Pricing 2026](https://platform.claude.com/docs/en/about-claude/pricing)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [OpenAI Image Pricing 2026](https://costgoat.com/pricing/openai-images)
