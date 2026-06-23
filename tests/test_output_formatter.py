from pipeline.brief_schema import ClientBrief
from pipeline.output_formatter import generate_output
from pathlib import Path

BRIEF_VALIDO = Path(__file__).parent.parent / "briefs" / "cili_julio_2026.json"

CONTENIDO = {
    "posts": [
        {
            "fecha": "2026-07-01",
            "plataforma": "Instagram",
            "tipo": "imagen_sola",
            "objetivo": "educacion",
            "gancho": "Gancho de prueba",
            "copy_completo": "Texto completo",
            "hashtags": ["#lean"],
            "cta": "Agenda tu diagnóstico",
        }
    ]
}
IMAGE_RESULTS = {"posts": [{"post": "post_01_instagram_2026-07-01", "ruta_imagen": "imagenes/post_01/imagen.png", "estado": "GENERADO"}]}


def test_generate_output_crea_archivos(tmp_path):
    brief = ClientBrief.from_json(BRIEF_VALIDO)
    salidas = generate_output(CONTENIDO, IMAGE_RESULTS, brief, tmp_path)

    assert Path(salidas["xlsx"]).exists()
    assert Path(salidas["md"]).exists()
    assert Path(salidas["checklist"]).exists()

    contenido_md = Path(salidas["md"]).read_text(encoding="utf-8")
    assert "Gancho de prueba" in contenido_md
    assert "GENERADO" in contenido_md
