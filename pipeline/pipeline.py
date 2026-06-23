"""Orquestador principal del pipeline de contenido orgánico.

Uso:
    python -m pipeline.pipeline --brief briefs/cili_julio_2026.json
"""
import argparse
import os
import time

from dotenv import load_dotenv

from .brief_schema import ClientBrief, validate_and_report
from .copy_generator import generate_copies
from .image_generator import generate_images
from .image_prompt_generator import generate_image_prompts
from .output_formatter import generate_output
from .strategy_generator import generate_strategy
from .utils import output_dir_mes


def run_pipeline(brief_path: str) -> None:
    load_dotenv()
    output_root = os.environ.get("OUTPUT_DIR", "./output")

    es_valido, mensaje = validate_and_report(brief_path)
    print(mensaje)
    if not es_valido:
        return

    brief = ClientBrief.from_json(brief_path)
    out_dir = output_dir_mes(output_root, brief.empresa, brief.mes)

    inicio = time.time()

    print("⏳ Generando estrategia...")
    strategy = generate_strategy(brief, output_root)
    print(f"✅ Estrategia generada ({len(strategy.get('posts', []))} posts)")

    print("⏳ Generando copies...")
    copies = generate_copies(strategy, brief, output_root)
    print(f"✅ Copies generados: {len(copies.get('posts', []))}/{len(strategy.get('posts', []))}")

    print("⏳ Generando prompts de imagen...")
    image_prompts = generate_image_prompts(copies, brief, output_root)
    print(f"✅ Prompts de imagen generados: {len(image_prompts.get('posts', []))}")

    print("⏳ Generando imágenes...")
    image_results = generate_images(image_prompts, copies, out_dir)
    exitosas = sum(1 for p in image_results["posts"] if p["estado"] == "GENERADO")
    total = len(image_results["posts"])
    icono = "✅" if exitosas == total else "⚠️"
    print(f"{icono} Imágenes: {exitosas}/{total}")

    print("⏳ Generando archivos de salida...")
    salidas = generate_output(strategy, copies, image_results, brief, out_dir)
    print(f"✅ Resumen generado: {salidas['xlsx']}")

    duracion = time.time() - inicio
    errores = total - exitosas
    print("\n--- RESUMEN ---")
    print(f"Tiempo total: {duracion:.1f}s")
    print(f"Posts generados: {total}")
    print(f"Errores de imagen: {errores}")
    print(f"Carpeta de salida: {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline de contenido orgánico automatizado")
    parser.add_argument("--brief", required=True, help="Ruta al archivo JSON del brief")
    args = parser.parse_args()
    run_pipeline(args.brief)


if __name__ == "__main__":
    main()
