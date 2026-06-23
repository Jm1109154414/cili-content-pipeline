"""Genera el copy completo de cada post a partir de la estrategia, vía Claude API."""
import json
import os
from pathlib import Path

from anthropic import Anthropic

from .brief_schema import ClientBrief
from .utils import cargar_json_si_existe, con_reintentos, guardar_json, output_dir_mes

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
MODELO = "claude-sonnet-4-6"


def _cliente() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def generate_copies(
    strategy: dict, brief: ClientBrief, output_root: str | Path = "./output"
) -> dict:
    """Genera (o reutiliza si ya existe) copies.json para la estrategia y brief dados."""
    out_dir = output_dir_mes(output_root, brief.empresa, brief.mes)
    copies_path = out_dir / "copies.json"

    existente = cargar_json_si_existe(copies_path)
    if existente is not None:
        return existente

    prompt_sistema = (PROMPTS_DIR / "copy_prompt.txt").read_text(encoding="utf-8")
    contenido_usuario = json.dumps(
        {"brief": brief.model_dump(), "estrategia": strategy}, ensure_ascii=False
    )

    def llamar() -> dict:
        respuesta = _cliente().messages.create(
            model=MODELO,
            max_tokens=16000,
            system=prompt_sistema,
            messages=[{"role": "user", "content": contenido_usuario}],
        )
        texto = respuesta.content[0].text
        return json.loads(texto)

    copies = con_reintentos(llamar, intentos=3)
    guardar_json(copies, copies_path)
    return copies
