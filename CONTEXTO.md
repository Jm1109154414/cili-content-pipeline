# CONTEXTO COMPLETO DEL PROYECTO
## Pipeline de Marketing Automatizado — CiLi
## Junio 2026 — v2.0

> ⚠️ **Documento histórico.** Este es el plan original (CLI manual en Python,
> DALL-E 3, n8n para automatizar). La arquitectura **vigente** está en
> [`PLAN_MAESTRO.md`](PLAN_MAESTRO.md) — OpenClaw como orquestador, skills en
> `/skills` (ya construidos: onboarding, estrategia-copy, imagenes, chequeo-marca),
> **GPT Image 2** para imagen, Kling 3.0 para video. Se conserva este archivo
> como bitácora del razonamiento de negocio (quién es CiLi, el SIPOC de
> 7 etapas, reglas de contenido por plataforma), que sigue siendo válido.

---
## QUIÉN ES CILI
**CiLi** — Continuous Improvement & Leadership Institute
- Consultora de Mejora Continua, Lean Six Sigma y Liderazgo
- Guadalajara, Jalisco, México. Desde 2010.
- Modelo propio: PMS (Productivity Management System)
- Producto estrella actual: **PMS IA** — PMS potenciado con Inteligencia Artificial
- Web: cili.org.mx
- Resultados: +2,000 personas certificadas, +13 países, +$121 MDD en ahorros y productividad

**Contexto del proyecto:**
CiLi está construyendo un sistema de marketing automatizado con IA para uso interno y para venderlo como servicio a clientes (empresas mexicanas que quieren crecer con marketing orgánico profesional y automatizado).

---
## EL PROCESO — SIPOC DE 7 ETAPAS

```
ETAPA 1 — Definir mercado y cliente ideal
  Entrada: Info del negocio, industria, mercado objetivo, competencia
  Salida: Avatar del cliente ideal, segmentos prioritarios, dolores/deseos/objeciones

ETAPA 2 — Diseñar producto y oferta
  Entrada: Necesidades del cliente, capacidades del servicio
  Salida: Oferta irresistible, stack de valor, bonos, diferenciadores, CTA

ETAPA 3 — Crear lead magnets alineados al cliente y la oferta
  Entrada: Avatar del cliente, dolores principales, casos de éxito
  Salida: Landing pages, PDFs, diagnósticos gratuitos, webinars, guías, formularios

ETAPA 4 — Contactar a contacto caliente
  Entrada: Lista de contactos calientes, historial de interacción, lead magnet
  Salida: Mensajes WhatsApp, correos, llamadas, invitaciones a diagnóstico

ETAPA 5 — Contacto en frío
  Entrada: Bases de datos, perfil de cliente ideal, lead magnet
  Salida: Correos fríos, mensajes LinkedIn, WhatsApps, secuencias de prospección

ETAPA 6 — Publicaciones orgánicas  ← MÓDULO A CONSTRUIR AHORA
  Entrada: Ideas de contenido, oferta, dolores del cliente, testimonios, calendario editorial
  Salida: Posts, Reels, Carruseles, Newsletters, Videos cortos, Historias, CTAs
  Audiencia: Seguidores, comunidad, prospectos orgánicos, leads entrantes

ETAPA 7 — Pauta/publicidad pagada
  Entrada: Oferta, lead magnet, avatar, copies, landing pages, presupuesto, segmentación
  Salida: Anuncios, campañas, tráfico a landing page, leads capturados, pruebas A/B
```

**PRIORIDAD ACTUAL: Construir el Módulo de Etapa 6 — Publicaciones Orgánicas**

---
## QUÉ SE ESTÁ CONSTRUYENDO AHORA

### Nombre: Pipeline de Contenido Orgánico Automatizado

**Objetivo:** Dado el perfil de un negocio (brief), el sistema genera automáticamente:
1. Estrategia de contenido del mes (qué publicar, cuándo, por qué, en qué plataforma)
2. Copy completo de cada post (adaptado por plataforma con sus reglas específicas)
3. Prompt visual optimizado para DALL-E por cada post
4. Imágenes generadas con DALL-E 3 vía OpenAI API
5. Archivo resumen con todo el calendario listo para publicar

**Lo que NO se construye en esta fase:**
- Publicación automática en redes (se hace manual por ahora)
- Dashboard web para el cliente
- Analytics y métricas
- Generación de video (fase 2)

---
## LENGUAJE Y STACK TÉCNICO

**Lenguaje principal: Python 3.11+**
- Es el lenguaje que domina el equipo
- Mejor ecosistema para APIs de IA
- Scripts simples, sin frameworks innecesarios

**Dependencias:**
```
anthropic          # Claude API para generación de texto y estrategia
openai             # DALL-E 3 para generación de imágenes
python-dotenv      # Manejo de variables de entorno
pydantic           # Validación del brief del cliente
openpyxl           # Generar el archivo Excel de salida
requests           # HTTP calls si se necesitan
```

**Variables de entorno (.env):**
```env
ANTHROPIC_API_KEY=sk-ant-...       # Claude API — generación de texto, estrategia, copies
OPENAI_API_KEY=sk-...              # OpenAI API — DALL-E 3 para imágenes
OUTPUT_DIR=./output                # Carpeta raíz donde se guardan todos los resultados
```

**Hardware donde corre:**
- Mac mini con OpenClaw (agente AI local)
- Accesible remotamente via Tailscale
- También puede correr en cualquier máquina con Python instalado

---
## ESTRUCTURA DE CARPETAS DEL PROYECTO

```
cili-content-pipeline/
│
├── .env                          # API keys (NO subir a git)
├── .env.example                  # Template de variables sin valores reales
├── requirements.txt              # Dependencias Python
├── README.md                     # Instrucciones de uso
│
├── briefs/                       # Briefs de clientes (JSON)
│   ├── cili_julio_2026.json
│   └── cliente_x_agosto_2026.json
│
├── pipeline/                     # Código principal
│   ├── __init__.py
│   ├── pipeline.py               # Orquestador principal — punto de entrada
│   ├── brief_schema.py           # Schema y validación del brief
│   ├── strategy_generator.py     # Genera estrategia del mes
│   ├── copy_generator.py         # Genera copies por plataforma
│   ├── image_prompt_generator.py # Genera prompts para DALL-E
│   ├── image_generator.py        # Llama a DALL-E y guarda imágenes
│   └── output_formatter.py       # Genera Excel/MD resumen
│
├── prompts/                      # Prompts del sistema (editables sin tocar código)
│   ├── strategy_prompt.txt       # Prompt para generar estrategia del mes
│   ├── copy_prompt.txt           # Prompt para generar copies
│   └── image_prompt.txt          # Prompt para generar prompts de DALL-E
│
├── output/                       # Todo lo generado (NO subir a git)
│   └── {cliente}/
│       └── {mes_año}/
│           ├── resumen_calendario.xlsx
│           ├── resumen_calendario.md
│           └── imagenes/
│               ├── post_01_instagram_lun_30jun/
│               │   ├── imagen.png
│               │   └── copy.txt
│               ├── post_02_linkedin_lun_30jun/
│               │   ├── imagen.png
│               │   └── copy.txt
│               └── ...
│
└── tests/                        # Tests básicos
    └── test_pipeline.py
```

---
## REGLAS DE CONTENIDO POR PLATAFORMA

### Instagram
- Límite: 2,200 caracteres (óptimo: 150-300 para posts normales, más para educativos)
- Gancho en la primera línea — es lo que se ve antes de "ver más"
- Saltos de línea frecuentes — facilita lectura en móvil
- Hashtags: 5-15, al final o en primer comentario
- Emojis: sí, con moderación, refuerzan el mensaje
- Formatos: Post imagen, Carrusel (2-10 slides), Reel (hasta 90s), Historia (24h)
- Tamaño imagen: 1080x1350px (portrait, 4:5) — el que más funciona
- Tamaño reel: 1080x1920px (9:16 vertical)

### LinkedIn
- Límite: 3,000 caracteres (óptimo: 800-1,500 para mayor alcance)
- Las primeras 2-3 líneas son críticas (se cortan antes de "ver más")
- Tono más profesional y reflexivo que Instagram
- Los posts que generan debate o hacen preguntas funcionan mejor
- Hashtags: 3-5 máximo, muy específicos del nicho
- Emojis: pocos, solo para organizar contenido (→, ✅, 📌)
- Formatos: Post texto, Post con imagen, Carrusel (documento PDF), Video
- Tamaño imagen: 1200x627px (landscape) o 1080x1350px (portrait)

### Facebook
- Límite: 63,206 caracteres (óptimo: 100-500 para mejor engagement)
- Tono conversacional, más cercano al usuario
- Preguntas directas generan más comentarios
- Funciona bien con contenido que invita a compartir
- Hashtags: 1-3, no son tan relevantes como en Instagram
- Emojis: sí, funcionan bien
- Formatos: Post texto, Post con imagen, Video, Encuesta
- Tamaño imagen: 1200x630px

### TikTok
- Caption: hasta 2,200 caracteres (pero se leen poco — el video es lo importante)
- Caption corto y directo con los hashtags
- El gancho debe ocurrir en los primeros 1-3 segundos del video
- Hashtags: 3-5, mezcla de nicho y trending
- Formatos: Video (15s-10min, óptimo 15-60s para orgánico), Foto carrusel
- Tamaño video: 1080x1920px (9:16 vertical obligatorio)
- El script del video es tan importante como el copy

---
## FLUJO COMPLETO DEL PIPELINE

```
[INPUT]
brief.json (perfil del cliente)
    │
    ▼
[PASO 1] strategy_generator.py
    → Claude API genera:
        - 4 temas semanales
        - Distribución de posts por día y plataforma
        - Objetivo de cada post (awareness/educación/conversión/comunidad)
        - Mix de formatos (imagen/carrusel/reel/historia)
    → Output: strategy.json
    │
    ▼
[PASO 2] copy_generator.py
    → Claude API genera por cada post:
        - Copy completo adaptado a la plataforma
        - Hashtags específicos
        - CTA concreto
        - Script si es Reel/TikTok
    → Output: copies.json
    │
    ▼
[PASO 3] image_prompt_generator.py
    → Claude API genera por cada post:
        - Prompt detallado para DALL-E (colores, estilo, texto, formato)
        - Especificaciones técnicas (tamaño, orientación)
    → Output: image_prompts.json
    │
    ▼
[PASO 4] image_generator.py
    → DALL-E 3 genera imagen por imagen
    → Manejo de errores: si falla, reintenta 2 veces, si sigue fallando
      guarda placeholder y continúa con el siguiente post
    → Guarda imagen en carpeta correspondiente
    → Guarda copy.txt junto a la imagen
    → Output: imágenes en /output/{cliente}/{mes}/imagenes/
    │
    ▼
[PASO 5] output_formatter.py
    → Genera resumen_calendario.xlsx con:
        - Una fila por post
        - Columnas: Fecha, Plataforma, Tipo, Objetivo, Copy, Hashtags, CTA, Ruta imagen, Estado
    → Genera resumen_calendario.md (alternativa legible)
    → Genera checklist_publicacion.md
    │
    ▼
[OUTPUT]
Carpeta /output/{cliente}/{mes}/ lista para que el equipo publique
```

---
## MANEJO DE ERRORES

**Principio:** El pipeline nunca debe detenerse completamente por un error en un post individual.

```python
# Comportamiento esperado por tipo de error:

# Error de API de Claude (generación de texto):
# → Reintenta hasta 3 veces con backoff exponencial
# → Si falla, guarda el post como "PENDIENTE_MANUAL" y continúa

# Error de DALL-E (generación de imagen):
# → Reintenta hasta 2 veces
# → Si falla, guarda imagen placeholder (color sólido con texto del brief)
# → Marca el post como "IMAGEN_PENDIENTE" en el Excel
# → Continúa con el siguiente post

# Error de validación del brief:
# → Detiene el pipeline ANTES de empezar
# → Muestra exactamente qué campos faltan o son incorrectos
# → No genera nada hasta que el brief esté completo

# Error de rate limit:
# → Espera automáticamente el tiempo indicado por la API
# → Continúa donde se quedó (no re-genera lo que ya está listo)

# Log de errores:
# → Guardar en /output/{cliente}/{mes}/errores.log
# → Formato: timestamp | tipo_error | post_afectado | detalle
```

---
## FLUJO DE APROBACIÓN HUMANA

El pipeline no publica nada automáticamente. El flujo de revisión es:

```
1. Pipeline genera todo → carpeta output
2. Equipo CiLi abre resumen_calendario.xlsx
3. Revisa copy de cada post en el Excel
4. Abre la carpeta de imágenes y revisa cada una
5. En el Excel, columna "Aprobado": marca ✅ o escribe ajuste necesario
6. Si hay ajuste: edita el copy directamente en el Excel
7. Si la imagen necesita cambio: re-corre solo ese post con ajuste en el brief
8. Cuando todo está ✅: equipo publica manualmente o via herramienta de scheduling
```

**Campo "Estado" en el Excel puede ser:**
- `GENERADO` — listo para revisión
- `APROBADO` — revisado y listo para publicar
- `PUBLICADO` — ya está en redes
- `IMAGEN_PENDIENTE` — imagen falló, necesita regenerarse
- `PENDIENTE_MANUAL` — copy falló, necesita escribirse manualmente

---
## EL BRIEF DEL CLIENTE — INPUT DEL SISTEMA

Se captura una vez en el onboarding y se reutiliza/actualiza cada mes.

### SECCIÓN A — Identidad del negocio
```json
{
  "empresa": "Nombre de la empresa",
  "industria": "Giro o sector",
  "ciudad": "Ciudad, Estado, País",
  "anos_mercado": 10,
  "web": "www.empresa.com",
  "redes_sociales": {
    "instagram": "@cuenta",
    "linkedin": "linkedin.com/company/cuenta",
    "facebook": "facebook.com/cuenta",
    "tiktok": "@cuenta"
  },
  "descripcion": "Qué hacen en 2-3 líneas. Para quién. Cómo."
}
```

### SECCIÓN B — Oferta y servicios
```json
{
  "servicio_principal": "El que más quieren vender este mes",
  "servicio_secundario": "Oferta de apoyo o complementaria",
  "precio_rango": "Desde $X hasta $Y MXN",
  "que_incluye": ["Item 1", "Item 2", "Item 3"],
  "duracion_o_entrega": "X semanas / X meses",
  "diferenciadores": ["Diferenciador 1", "Diferenciador 2"],
  "resultado_tipico": "Qué logra el cliente típicamente después del servicio"
}
```

### SECCIÓN C — Cliente ideal
```json
{
  "perfil_demografico": "Edad, género, cargo, industria, tamaño de empresa",
  "dolores": [
    "Dolor principal que los mueve a buscar solución",
    "Segundo dolor relevante",
    "Tercer dolor relevante"
  ],
  "deseos": [
    "Lo que más quieren lograr",
    "Segunda meta importante",
    "Tercera meta"
  ],
  "objeciones": [
    "Por qué NO comprarían (objeción 1)",
    "Objeción 2",
    "Objeción 3"
  ],
  "nivel_conciencia": "no_sabe_problema | sabe_problema | busca_solucion | compara_opciones"
}
```

### SECCIÓN D — Identidad de marca
```json
{
  "tono": "profesional | casual | motivacional | educativo | combinación",
  "colores_hex": ["#000000", "#FFFFFF"],
  "estilo_visual": "Descripción del estilo de imágenes que prefieren",
  "tres_palabras_marca": ["Palabra1", "Palabra2", "Palabra3"],
  "evitar": "Qué temas, palabras o estilos NO quieren usar nunca"
}
```

### SECCIÓN E — Contenido y credibilidad
```json
{
  "credenciales": "Números y datos de credibilidad (años, clientes, resultados)",
  "testimonios": [
    "Nombre, cargo: 'Testimonio textual'",
    "Nombre, cargo: 'Testimonio textual'"
  ],
  "casos_exito": "Descripción de casos de éxito relevantes",
  "temas_que_funcionan": ["Tema que ya saben que engancha con su audiencia"],
  "temas_a_evitar": ["Tema que no quieren tocar"],
  "competidores": ["Competidor 1", "Competidor 2"]
}
```

### SECCIÓN F — Configuración del mes
```json
{
  "mes": "Julio 2026",
  "frecuencia_semanal": 5,
  "plataformas": ["Instagram", "LinkedIn", "Facebook", "TikTok"],
  "objetivo_mes": "awareness | leads | ventas | comunidad",
  "descripcion_objetivo": "Detalle del objetivo principal este mes",
  "evento_especial": "Lanzamiento, promoción, fecha importante (si aplica)",
  "tema_semana_1": "Tema de la primera semana",
  "tema_semana_2": "Tema de la segunda semana",
  "tema_semana_3": "Tema de la tercera semana",
  "tema_semana_4": "Tema de la cuarta semana"
}
```

---
## EJEMPLO DE BRIEF COMPLETADO — CASO CILI JULIO 2026

```json
{
  "empresa": "CiLi — Continuous Improvement & Leadership Institute",
  "industria": "Consultoría y capacitación empresarial — Lean Six Sigma",
  "ciudad": "Guadalajara, Jalisco, México",
  "anos_mercado": 15,
  "web": "cili.org.mx",
  "redes_sociales": {
    "instagram": "@cili.institute",
    "linkedin": "linkedin.com/company/cili",
    "facebook": "facebook.com/CILI.Institute",
    "tiktok": "@cili.institute"
  },
  "descripcion": "Instituto especializado en Lean Six Sigma, Mejora Continua y Liderazgo. Certificamos profesionales y transformamos organizaciones con nuestro modelo PMS IA — la evolución de la mejora continua integrada con Inteligencia Artificial.",
  "servicio_principal": "Implementaciones PMS IA — transformación de procesos empresariales con IA integrada. Arquitecturas de agentes inteligentes, copilotos operativos y automatización con base en mejora continua.",
  "servicio_secundario": "Certificaciones Lean Six Sigma con validez internacional: Yellow Belt, Green Belt, Black Belt, Master Black Belt. Certificados por CSSC, LATAMPC y STPS.",
  "precio_rango": "Consultar según alcance del proyecto",
  "que_incluye": [
    "Diagnóstico inicial del proceso",
    "Diseño del sistema PMS IA personalizado",
    "Implementación con acompañamiento",
    "Capacitación del equipo",
    "Seguimiento post-implementación"
  ],
  "duracion_o_entrega": "Depende del alcance: desde 4 semanas hasta 6 meses",
  "diferenciadores": [
    "Modelo PMS propio — no herramientas genéricas de terceros",
    "Instructores activos en la industria, no solo académicos",
    "15 años de resultados documentados: +$121 MDD en ahorros y productividad",
    "Único instituto que integra Lean Six Sigma con IA de forma estructurada",
    "Modelo implementado en Philip Morris, Bimbo, Alpura, GE, Lear Corporation"
  ],
  "resultado_tipico": "Reducción de desperdicios y errores del 30-70%, implementación de IA en procesos clave, equipo certificado con metodología aplicada",
  "perfil_demografico": "Gerentes de operaciones, directores de manufactura, directores de calidad y mejora continua. Empresas medianas y grandes en México y Latinoamérica. También profesionales individuales 28-50 años que buscan certificación para crecer.",
  "dolores": [
    "Procesos con errores que se repiten mes a mes sin solución definitiva",
    "Quieren implementar IA en su empresa pero no saben cómo ni por dónde empezar sin arriesgarse",
    "Equipos sin cultura de mejora continua — todo depende de una sola persona clave"
  ],
  "deseos": [
    "Reducir costos operativos y desperdicios con una metodología probada y medible",
    "Tener un sistema de gestión sólido que soporte la implementación de IA de forma ordenada",
    "Certificar a su equipo con validez internacional y aplicación real, no solo teoría"
  ],
  "objeciones": [
    "Ya intenté mejora continua antes y no funcionó — no confío en que esta vez sea diferente",
    "No tengo tiempo ni presupuesto para capacitar a mi equipo ahora mismo",
    "La IA es demasiado cara o técnicamente complicada para mi empresa"
  ],
  "nivel_conciencia": "sabe_problema",
  "tono": "Profesional pero accesible. Basado en resultados y datos reales. Educativo — cada post enseña algo concreto. Motivacional sin ser superficial ni genérico.",
  "colores_hex": ["#0B1120", "#FFFFFF", "#22D3EE"],
  "estilo_visual": "Corporativo premium oscuro. Tipografía bold y limpia. Gráficas y datos visualizados. Sin fotos de stock genéricas — preferir diseño tipográfico, diagramas e infografías.",
  "tres_palabras_marca": ["Confiable", "Experto", "Transformador"],
  "evitar": "Promesas vacías sin datos que las respalden. Lenguaje técnico sin explicación. Contenido motivacional genérico tipo frase del día. Imágenes de personas sonriendo en oficina (stock photo obvio).",
  "credenciales": "+2,000 personas certificadas en 13 países, +$121 MDD en ahorros y productividad generados, desde 2010, modelo implementado en Philip Morris México (toda LATAM y Canadá), Bimbo, Alpura, Grupo Gondi, Lear Corporation, General Electric, Daimler Chrysler.",
  "testimonios": [
    "Gabriel Arana, Master Black Belt: 'No he conocido ninguna organización como CiLi que no se enfoca en enseñarte solo herramientas, sino que te enseña a aplicar la mejora continua donde te desarrolles.'",
    "Sebastián León, Black Belt: 'Los casos reales expuestos por los instructores me dieron una clara visión de cómo la mejora continua debe ser base de la cultura organizacional en la gestión de operaciones exitosas.'"
  ],
  "casos_exito": "2010: Philip Morris México — implementación del modelo PMS durante consolidación de operaciones. Resultado tan exitoso que fue adoptado por toda LATAM y Canadá dentro de la misma organización.",
  "temas_que_funcionan": [
    "Los 8 desperdicios de Lean — siempre genera engagement",
    "Datos de ahorro concretos y casos reales",
    "Diferencia entre hacer mejora continua bien vs mal",
    "Testimonios de certificados contando su transformación"
  ],
  "temas_a_evitar": [
    "Política o temas sociales controversiales",
    "Críticas directas a competidores por nombre"
  ],
  "competidores": [
    "CI Academy",
    "Otras consultoras de Lean Six Sigma en México"
  ],
  "mes": "Julio 2026",
  "frecuencia_semanal": 5,
  "plataformas": ["Instagram", "LinkedIn", "Facebook", "TikTok"],
  "objetivo_mes": "leads",
  "descripcion_objetivo": "Posicionar PMS IA como la solución diferenciada para empresas que quieren implementar IA con orden, Y convertir leads calientes para las certificaciones de julio.",
  "evento_especial": "Nueva generación de certificaciones Yellow, Green y Black Belt arranca julio 2026. Lugares limitados.",
  "tema_semana_1": "Introducción — desperdicios, métricas y resultados de CiLi",
  "tema_semana_2": "PMS IA — el sistema de gestión del futuro con IA integrada",
  "tema_semana_3": "Certificaciones — guía para elegir la correcta y por qué vale la pena",
  "tema_semana_4": "Casos de éxito y credibilidad — cierre y CTA final"
}
```

---
## PROMPTS DEL SISTEMA

### strategy_prompt.txt
```
Eres un estratega de marketing de contenido especializado en B2B latinoamericano.

Recibirás el brief de un cliente en JSON. Con base en ese brief, genera una estrategia de contenido orgánico para el mes indicado.

La estrategia debe incluir:
1. Distribución de posts por semana y plataforma (respetando la frecuencia indicada)
2. Tipo de contenido por post: imagen_sola | carrusel | reel | historia | video_corto
3. Objetivo de cada post: awareness | educacion | credibilidad | conversion | comunidad
4. Gancho o ángulo principal de cada post (una línea que captura la esencia)
5. A qué dolor u objeción del cliente ideal apunta cada post

Reglas:
- El 40% del contenido debe ser educativo (aportar valor sin vender)
- El 30% orientado a conversión (CTA directo)
- El 20% de credibilidad (casos, datos, testimonios)
- El 10% de comunidad (preguntas, encuestas, conversación)
- Distribuir plataformas equilibradamente
- El mismo post puede adaptarse a 2-3 plataformas con ajustes

Responde SOLO en JSON con la estructura definida. Sin texto adicional.
```

### copy_prompt.txt
```
Eres un copywriter experto en marketing B2B para mercado mexicano y latinoamericano.

Recibirás la estrategia del mes y el brief completo del cliente. Genera el copy completo para cada post.

Por cada post genera:
- gancho: primera línea que detiene el scroll (máximo 12 palabras, sin punto final)
- cuerpo: desarrollo del mensaje con el valor o dato principal
- cta: llamada a la acción específica y concreta
- hashtags: lista de hashtags apropiados para la plataforma
- copy_completo: el texto final listo para publicar (gancho + cuerpo + cta + hashtags)
- si es reel o tiktok: script_video con indicaciones de tiempo [0-3s], [3-10s], etc.

Reglas por plataforma:
- Instagram: máximo 300 palabras en el cuerpo, emojis moderados, saltos de línea frecuentes
- LinkedIn: tono más profesional y reflexivo, 400-700 palabras, pocos emojis (solo para organizar)
- Facebook: tono conversacional, 100-300 palabras, pregunta al final para generar comentarios
- TikTok: caption corto (máximo 150 caracteres + hashtags), script del video es lo importante

El copy debe sonar auténtico a la marca — NO genérico. Usa los datos, testimonios y diferenciadores del brief siempre que sea relevante.

Responde SOLO en JSON. Sin texto adicional.
```

### image_prompt.txt
```
Eres un director de arte especializado en contenido para redes sociales B2B.

Recibirás el copy de cada post y el brief de la marca. Genera un prompt detallado para DALL-E 3 que produzca una imagen profesional y alineada a la marca.

Por cada post incluye:
- prompt_dalle: descripción completa en inglés para DALL-E (colores, estilo, elementos, texto si aplica, mood)
- dimensiones: el tamaño correcto según la plataforma
- estilo: tipographic | infographic | abstract | diagram | dark_corporate
- elementos_evitar: qué no debe aparecer en la imagen

Reglas:
- Priorizar diseño tipográfico y gráfico sobre fotografía de personas
- Los colores deben respetar el hex del brief
- Si el post lleva datos o números, incluirlos en la imagen
- Sin watermarks, sin texto genérico, sin personas de stock obvias
- Las imágenes deben verse premium y diferenciadas

Formatos por plataforma:
- Instagram post: 1080x1350px
- Instagram reel cover: 1080x1920px
- LinkedIn: 1200x627px
- Facebook: 1200x630px
- TikTok cover: 1080x1920px

Responde SOLO en JSON. Sin texto adicional.
```

---
## ARCHIVOS A CONSTRUIR — ESPECIFICACIONES

### `pipeline/brief_schema.py`
- Clase Pydantic `ClientBrief` con todos los campos del brief
- Campos requeridos vs opcionales claramente marcados
- Validaciones: plataformas válidas, nivel_conciencia válido, frecuencia entre 1-7
- Método `from_json(path)` para cargar desde archivo
- Método `validate_and_report()` que muestra exactamente qué falta

### `pipeline/strategy_generator.py`
- Función `generate_strategy(brief: ClientBrief) -> dict`
- Llama a Claude API con strategy_prompt.txt
- Retorna JSON estructurado con todos los posts del mes
- Incluye retry logic (3 intentos con backoff exponencial)
- Guarda strategy.json en /output/{cliente}/{mes}/

### `pipeline/copy_generator.py`
- Función `generate_copies(strategy: dict, brief: ClientBrief) -> dict`
- Llama a Claude API con copy_prompt.txt
- Genera copy para CADA post de la estrategia
- Adapta automáticamente según la plataforma del post
- Incluye retry logic
- Guarda copies.json en /output/{cliente}/{mes}/

### `pipeline/image_prompt_generator.py`
- Función `generate_image_prompts(copies: dict, brief: ClientBrief) -> dict`
- Llama a Claude API con image_prompt.txt
- Genera prompt DALL-E + especificaciones por post
- Guarda image_prompts.json en /output/{cliente}/{mes}/

### `pipeline/image_generator.py`
- Función `generate_images(image_prompts: dict, output_dir: str) -> dict`
- Llama a DALL-E 3 API por cada post
- Guarda imagen en /output/{cliente}/{mes}/imagenes/post_{N}_{plataforma}_{fecha}/
- Guarda copy.txt junto a cada imagen
- Si falla: reintenta 2 veces → guarda placeholder → continúa → loguea error
- Retorna dict con rutas de imágenes y estado de cada una

### `pipeline/output_formatter.py`
- Función `generate_output(strategy, copies, image_results, brief) -> str`
- Genera resumen_calendario.xlsx con columnas:
  No. | Fecha | Plataforma | Tipo | Objetivo | Gancho | Copy completo | Hashtags | CTA | Ruta imagen | Estado
- Genera resumen_calendario.md (versión texto plano)
- Genera checklist_publicacion.md con pasos para cada post
- Retorna path de los archivos generados

### `pipeline/pipeline.py`
- Función principal `run_pipeline(brief_path: str)`
- Carga y valida el brief
- Corre cada paso en orden
- Si un paso falla completamente: detiene y muestra error claro
- Muestra progreso en consola: "✅ Estrategia generada | ✅ Copies: 20/20 | ⚠️ Imágenes: 18/20"
- Al final muestra resumen: tiempo total, posts generados, errores

**Uso desde línea de comandos:**
```bash
python -m pipeline.pipeline --brief briefs/cili_julio_2026.json
```

---
## DECISIONES TÉCNICAS TOMADAS

| Decisión | Elegida | Razón |
|----------|---------|-------|
| Lenguaje | Python 3.11+ | Dominio del equipo + ecosistema IA |
| Generación de texto | Claude API (claude-sonnet-4-6) | Mejor calidad en español |
| Generación de imágenes | DALL-E 3 vía OpenAI | Disponible via OpenClaw |
| Generación de video | FFmpeg — fase 2 | Gratis, suficiente para empezar |
| Publicación | Manual por ahora | Prioridad es calidad del contenido |
| Storage | Carpetas locales organizadas | Simple para MVP, escala a Drive después |
| Orquestación futura | n8n | Ya instalado en n8n.biodentistclinic.mx |
| Validación del brief | Pydantic | Errores claros antes de gastar tokens de API |
| Output final | Excel + Markdown | Excel para el equipo, MD para Claude/agentes |

---
## PRÓXIMOS PASOS DESPUÉS DEL MVP

**Fase 2 — Automatización:**
- Conectar pipeline a n8n para que corra automáticamente el día 1 de cada mes
- Agregar generación de videos cortos con FFmpeg (slideshow + texto animado + música)
- Notificación por WhatsApp cuando el contenido esté listo para revisar

**Fase 3 — Producto:**
- Formulario web de onboarding de cliente (React + Supabase)
- Dashboard para que el cliente vea y apruebe contenido antes de publicar
- Integración con PostPeer API para publicación automática programada

**Fase 4 — Escala:**
- Multi-tenant: múltiples clientes con sus propios briefs y outputs aislados
- Historial de contenido publicado para no repetirse
- Análisis de qué posts funcionaron mejor para mejorar la estrategia del siguiente mes

---
## NOTAS IMPORTANTES PARA CLAUDE CODE

- El sistema debe funcionar para CUALQUIER cliente, no solo CiLi
- El brief.json es el ÚNICO input — todo lo demás se genera automáticamente
- Priorizar calidad del copy sobre velocidad — mejor 1 post excelente que 20 genéricos
- Los prompts están en /prompts/ como archivos de texto para que el equipo pueda editarlos sin tocar código
- Manejar rate limits de las APIs con gracia — nunca crashear por un 429
- El pipeline debe poder reanudarse si se interrumpe — no re-generar lo que ya existe
- Comentar el código en español — el equipo es mexicano
- Cada función debe tener docstring claro con parámetros, retorno y posibles errores
- Escribir al menos un test básico por módulo en /tests/
