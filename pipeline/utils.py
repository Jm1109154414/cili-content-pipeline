"""Utilidades compartidas: paths de output y retry con backoff exponencial."""
import json
import re
import time
from pathlib import Path
from typing import Callable, TypeVar

T = TypeVar("T")


def slug(texto: str) -> str:
    """Convierte texto a slug seguro para nombres de carpeta."""
    texto = texto.strip().lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    return re.sub(r"[\s_]+", "_", texto)


def output_dir_mes(output_root: str | Path, empresa: str, mes: str) -> Path:
    path = Path(output_root) / slug(empresa) / slug(mes)
    path.mkdir(parents=True, exist_ok=True)
    return path


def guardar_json(data: dict, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def cargar_json_si_existe(path: str | Path) -> dict | None:
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def con_reintentos(func: Callable[[], T], intentos: int = 3, espera_base: float = 2.0) -> T:
    """Ejecuta func con reintentos y backoff exponencial. Re-lanza la última excepción si todos fallan."""
    ultimo_error: Exception | None = None
    for intento in range(intentos):
        try:
            return func()
        except Exception as e:
            ultimo_error = e
            if intento < intentos - 1:
                time.sleep(espera_base * (2**intento))
    assert ultimo_error is not None
    raise ultimo_error
