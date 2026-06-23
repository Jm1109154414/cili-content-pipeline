"""Persistencia y consulta del historial de contenido por cliente.

Permite que estrategia-copy revise qué temas ya se usaron en meses
anteriores del mismo cliente, para no repetirlos (ver PLAN_MAESTRO.md).
"""
import json
from pathlib import Path

NOMBRE_ARCHIVO_HISTORIAL = "contenido_final.json"


def guardar_contenido_final(contenido: dict, output_dir: str | Path) -> Path:
    """Guarda el JSON final consolidado (salida de chequeo-marca) en
    output_dir/contenido_final.json, para que meses futuros puedan leerlo."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / NOMBRE_ARCHIVO_HISTORIAL
    path.write_text(json.dumps(contenido, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def cargar_temas_anteriores(cliente_slug: str, output_root: str | Path = "./output") -> list[str]:
    """Recorre output/{cliente_slug}/*/contenido_final.json y devuelve la
    lista de `tema` de todos los posts ya publicados (meses anteriores),
    para que estrategia-copy evite repetirlos. Ignora meses sin historial
    guardado (no falla si la carpeta o el archivo no existen)."""
    cliente_dir = Path(output_root) / cliente_slug
    if not cliente_dir.exists():
        return []

    temas: list[str] = []
    for mes_dir in sorted(cliente_dir.iterdir()):
        archivo = mes_dir / NOMBRE_ARCHIVO_HISTORIAL
        if not archivo.exists():
            continue
        try:
            data = json.loads(archivo.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        for post in data.get("posts", []):
            tema = post.get("tema")
            if tema:
                temas.append(tema)
    return temas
