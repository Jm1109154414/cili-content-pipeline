# Formulario de Onboarding — Brief de Cliente

Este formulario captura toda la información que el sistema necesita para generar el contenido del mes. Se llena **una vez** al iniciar con el cliente y se actualiza solo en la **Sección F** cada mes.

Instrucciones: llena cada campo con texto normal. Cuando termines, pásalo a `briefs/{cliente}_{mes}.json` siguiendo la plantilla en `_template_brief.json`.

---

## SECCIÓN A — Identidad del negocio

| Campo | Tu respuesta |
|---|---|
| Nombre de la empresa | |
| Industria / giro | |
| Ciudad, Estado, País | |
| Años en el mercado | |
| Sitio web | |
| Instagram (@usuario) | |
| LinkedIn (link) | |
| Facebook (link) | |
| TikTok (@usuario) | |
| Descripción del negocio (2-3 líneas: qué hacen, para quién, cómo) | |

---

## SECCIÓN B — Oferta y servicios

| Campo | Tu respuesta |
|---|---|
| Servicio principal que quieren vender este mes | |
| Servicio secundario / complementario | |
| Rango de precio | |
| Qué incluye (lista) | |
| Duración o tiempo de entrega | |
| Diferenciadores (qué los hace distintos a la competencia) | |
| Resultado típico que logra el cliente | |

---

## SECCIÓN C — Cliente ideal

| Campo | Tu respuesta |
|---|---|
| Perfil demográfico (edad, cargo, industria, tamaño de empresa) | |
| 3 dolores principales que los hacen buscar una solución | 1.<br>2.<br>3. |
| 3 deseos / metas principales | 1.<br>2.<br>3. |
| 3 objeciones (por qué NO comprarían) | 1.<br>2.<br>3. |
| Nivel de conciencia del cliente | ☐ no sabe que tiene el problema<br>☐ sabe el problema<br>☐ ya busca solución<br>☐ está comparando opciones |

---

## SECCIÓN D — Identidad de marca

| Campo | Tu respuesta |
|---|---|
| Tono de comunicación | ☐ profesional ☐ casual ☐ motivacional ☐ educativo ☐ combinación: ___ |
| Colores de marca (hex, ej. #0B1120) | |
| Estilo visual deseado | |
| 3 palabras que describen la marca | |
| Qué evitar siempre (temas, palabras, estilos) | |

---

## SECCIÓN E — Contenido y credibilidad

| Campo | Tu respuesta |
|---|---|
| Credenciales / números de respaldo (años, clientes, resultados) | |
| Testimonios (nombre, cargo, cita textual) — mínimo 2 | 1.<br>2. |
| Casos de éxito relevantes | |
| Temas que ya saben que funcionan con su audiencia | |
| Temas que prefieren NO tocar | |
| Competidores principales | |

---

## SECCIÓN F — Configuración del mes (se actualiza cada mes)

| Campo | Tu respuesta |
|---|---|
| Mes (ej. "Julio 2026") | |
| Frecuencia de posts por semana (1-7) | |
| Plataformas a usar este mes | ☐ Instagram ☐ LinkedIn ☐ Facebook ☐ TikTok |
| Objetivo del mes | ☐ awareness ☐ leads ☐ ventas ☐ comunidad |
| Detalle del objetivo | |
| Evento especial (lanzamiento, promo, fecha importante) | |
| Tema semana 1 | |
| Tema semana 2 | |
| Tema semana 3 | |
| Tema semana 4 | |
| Medio de aprobación interna (lo decide el equipo que opera la cuenta, no se le pregunta al cliente final) | ☐ WhatsApp ☐ Excel ☐ ambos (default si no se especifica) |

---

**Nota para quien pasa esto a JSON:** revisa que `plataformas` y `nivel_conciencia` usen exactamente las palabras válidas del sistema (`Instagram`, `LinkedIn`, `Facebook`, `TikTok` / `no_sabe_problema`, `sabe_problema`, `busca_solucion`, `compara_opciones`), si no, el pipeline rechaza el brief antes de generar nada.
