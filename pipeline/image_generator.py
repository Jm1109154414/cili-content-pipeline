"""Genera las imágenes finales con DALL-E 3 y guarda copy.txt junto a cada una."""
import os
from pathlib import Path

import requests
from openai import OpenAI
from PIL import Image, ImageDraw

from .utils import con_reintentos, guardar_json, slug

MODELO_IMAGEN = "dall-e-3"


def _cliente() -> OpenAI:
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def _generar_placeholder(path_destino: Path, texto: str, ancho: int, alto: int) -> None:
    """Crea una imagen placeholder simple cuando DALL-E falla."""
    img = Image.new("RGB", (ancho, alto), color="#0B1120")
    draw = ImageDraw.Draw(img)
    mensaje = f"IMAGEN PENDIENTE\n{texto[:80]}"
    draw.multiline_text((40, alto // 2 - 40), mensaje, fill="#FFFFFF")
    img.save(path_destino)


def _descargar_imagen(url: str, path_destino: Path) -> None:
    respuesta = requests.get(url, timeout=60)
    respuesta.raise_for_status()
    path_destino.write_bytes(respuesta.content)


def generate_images(image_prompts: dict, copies: dict, output_dir: str | Path) -> dict:
    """
    Genera una imagen por post usando DALL-E 3.
    image_prompts y copies deben tener la misma lista de posts (mismo orden/índice o id de post).
    Retorna dict con el estado y la ruta de cada post.
    """
    output_dir = Path(output_dir)
    imagenes_dir = output_dir / "imagenes"
    imagenes_dir.mkdir(parents=True, exist_ok=True)
    errores_path = output_dir / "errores.log"

    posts_prompts = image_prompts.get("posts", [])
    posts_copies = copies.get("posts", [])

    resultados: dict = {"posts": []}

    for i, post_prompt in enumerate(posts_prompts):
        post_copy = posts_copies[i] if i < len(posts_copies) else {}
        plataforma = post_prompt.get("plataforma", "general")
        fecha = post_prompt.get("fecha", f"post{i + 1}")
        nombre_carpeta = f"post_{i + 1:02d}_{slug(plataforma)}_{slug(fecha)}"
        post_dir = imagenes_dir / nombre_carpeta
        post_dir.mkdir(parents=True, exist_ok=True)

        imagen_path = post_dir / "imagen.png"
        copy_path = post_dir / "copy.txt"
        copy_path.write_text(post_copy.get("copy_completo", ""), encoding="utf-8")

        dims = post_prompt.get("dimensiones", "1080x1350")
        ancho, alto = (int(x) for x in dims.lower().split("x"))
        dalle_size = "1024x1792" if alto > ancho else "1792x1024" if ancho > alto else "1024x1024"

        estado = "GENERADO"
        try:
            def llamar() -> str:
                resp = _cliente().images.generate(
                    model=MODELO_IMAGEN,
                    prompt=post_prompt.get("prompt_dalle", ""),
                    size=dalle_size,
                    n=1,
                )
                return resp.data[0].url

            url = con_reintentos(llamar, intentos=2)
            _descargar_imagen(url, imagen_path)
        except Exception as e:
            _generar_placeholder(imagen_path, post_copy.get("gancho", ""), ancho, alto)
            estado = "IMAGEN_PENDIENTE"
            with open(errores_path, "a", encoding="utf-8") as log:
                import datetime

                log.write(
                    f"{datetime.datetime.now().isoformat()} | DALLE_ERROR | {nombre_carpeta} | {e}\n"
                )

        resultados["posts"].append(
            {
                "post": nombre_carpeta,
                "ruta_imagen": str(imagen_path),
                "ruta_copy": str(copy_path),
                "estado": estado,
            }
        )

    guardar_json(resultados, output_dir / "image_results.json")
    return resultados
