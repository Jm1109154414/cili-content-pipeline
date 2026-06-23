"""Genera la estrategia de contenido del mes a partir del brief, vía Claude API."""
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


def generate_strategy(brief: ClientBrief, output_root: str | Path = "./output") -> dict:
    """Genera (o reutiliza si ya existe) strategy.json para el brief dado."""
    out_dir = output_dir_mes(output_root, brief.empresa, brief.mes)
    strategy_path = out_dir / "strategy.json"

    existente = cargar_json_si_existe(strategy_path)
    if existente is not None:
        return existente

    prompt_sistema = (PROMPTS_DIR / "strategy_prompt.txt").read_text(encoding="utf-8")
    brief_json = brief.model_dump_json(indent=2)

    def llamar() -> dict:
        respuesta = _cliente().messages.create(
            model=MODELO,
            max_tokens=8000,
            system=prompt_sistema,
            messages=[{"role": "user", "content": brief_json}],
        )
        texto = respuesta.content[0].text
        return json.loads(texto)

    strategy = con_reintentos(llamar, intentos=3)
    guardar_json(strategy, strategy_path)
    return strategy
