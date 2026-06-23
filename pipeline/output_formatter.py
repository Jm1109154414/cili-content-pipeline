"""Genera el resumen final del mes: Excel, Markdown y checklist de publicación."""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from .brief_schema import ClientBrief

COLUMNAS = [
    "No.", "Fecha", "Plataforma", "Tipo", "Objetivo", "Gancho",
    "Copy completo", "Hashtags", "CTA", "Ruta imagen", "Estado",
]


def _filas(contenido: dict, image_results: dict) -> list[dict]:
    """contenido viene de chequeo-marca (que ya consolidó el "estado" final
    de estrategia-copy + imagenes, ver vocabulario único en PLAN_MAESTRO.md):
    {"posts": [{fecha, plataforma, tipo, objetivo, gancho, copy_completo,
    hashtags, cta, estado, ...}]}. El fallback a imagen_post.get("estado")
    solo aplica si "contenido" viniera directo de estrategia-copy sin pasar
    por chequeo-marca."""
    posts_contenido = contenido.get("posts", [])
    imagenes_lista = image_results.get("posts", [])

    filas = []
    for i, post in enumerate(posts_contenido):
        imagen_post = imagenes_lista[i] if i < len(imagenes_lista) else {}
        filas.append(
            {
                "No.": i + 1,
                "Fecha": post.get("fecha", ""),
                "Plataforma": post.get("plataforma", ""),
                "Tipo": post.get("tipo", ""),
                "Objetivo": post.get("objetivo", ""),
                "Gancho": post.get("gancho", ""),
                "Copy completo": post.get("copy_completo", ""),
                "Hashtags": ", ".join(post.get("hashtags", [])),
                "CTA": post.get("cta", ""),
                "Ruta imagen": imagen_post.get("ruta_imagen", ""),
                "Estado": post.get("estado") or imagen_post.get("estado", "GENERADO"),
            }
        )
    return filas


def _generar_xlsx(filas: list[dict], path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Calendario"
    ws.append(COLUMNAS)
    for fila in filas:
        ws.append([fila[c] for c in COLUMNAS])
    for idx, columna in enumerate(COLUMNAS, start=1):
        ws.column_dimensions[get_column_letter(idx)].width = max(15, len(columna) + 5)
    wb.save(path)


def _generar_md(filas: list[dict], brief: ClientBrief, path: Path) -> None:
    lineas = [f"# Calendario de contenido — {brief.empresa} — {brief.mes}", ""]
    for fila in filas:
        lineas.append(f"## Post {fila['No.']} — {fila['Plataforma']} ({fila['Fecha']})")
        lineas.append(f"- **Tipo:** {fila['Tipo']}")
        lineas.append(f"- **Objetivo:** {fila['Objetivo']}")
        lineas.append(f"- **Gancho:** {fila['Gancho']}")
        lineas.append(f"- **Copy completo:**\n\n{fila['Copy completo']}\n")
        lineas.append(f"- **Hashtags:** {fila['Hashtags']}")
        lineas.append(f"- **CTA:** {fila['CTA']}")
        lineas.append(f"- **Imagen:** {fila['Ruta imagen']}")
        lineas.append(f"- **Estado:** {fila['Estado']}")
        lineas.append("")
    path.write_text("\n".join(lineas), encoding="utf-8")


def _generar_checklist(filas: list[dict], path: Path) -> None:
    lineas = ["# Checklist de publicación", ""]
    for fila in filas:
        lineas.append(f"- [ ] Post {fila['No.']} — {fila['Plataforma']} ({fila['Fecha']}) — {fila['Estado']}")
    path.write_text("\n".join(lineas), encoding="utf-8")


def generate_output(
    contenido: dict, image_results: dict, brief: ClientBrief, output_dir: str | Path
) -> dict:
    """Genera resumen_calendario.xlsx, resumen_calendario.md y checklist_publicacion.md.

    contenido: salida del skill estrategia-copy (un solo dict con estrategia+copy fusionados).
    image_results: salida del skill/paso de imágenes.
    """
    output_dir = Path(output_dir)
    filas = _filas(contenido, image_results)

    xlsx_path = output_dir / "resumen_calendario.xlsx"
    md_path = output_dir / "resumen_calendario.md"
    checklist_path = output_dir / "checklist_publicacion.md"

    _generar_xlsx(filas, xlsx_path)
    _generar_md(filas, brief, md_path)
    _generar_checklist(filas, checklist_path)

    return {"xlsx": str(xlsx_path), "md": str(md_path), "checklist": str(checklist_path)}
