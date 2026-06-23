"""Genera prompts de DALL-E por post a partir de los copies, vía Claude API."""
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


def generate_image_prompts(
    copies: dict, brief: ClientBrief, output_root: str | Path = "./output"
) -> dict:
    """Genera (o reutiliza si ya existe) image_prompts.json para los copies y brief dados."""
    out_dir = output_dir_mes(output_root, brief.empresa, brief.mes)
    prompts_path = out_dir / "image_prompts.json"

    existente = cargar_json_si_existe(prompts_path)
    if existente is not None:
        return existente

    prompt_sistema = (PROMPTS_DIR / "image_prompt.txt").read_text(encoding="utf-8")
    contenido_usuario = json.dumps(
        {"brief": brief.model_dump(), "copies": copies}, ensure_ascii=False
    )

    def llamar() -> dict:
        respuesta = _cliente().messages.create(
            model=MODELO,
            max_tokens=8000,
            system=prompt_sistema,
            messages=[{"role": "user", "content": contenido_usuario}],
        )
        texto = respuesta.content[0].text
        return json.loads(texto)

    image_prompts = con_reintentos(llamar, intentos=3)
    guardar_json(image_prompts, prompts_path)
    return image_prompts
