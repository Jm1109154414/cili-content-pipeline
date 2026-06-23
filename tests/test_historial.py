import json
from pathlib import Path

from pipeline.historial import cargar_temas_anteriores, guardar_contenido_final


def test_guardar_contenido_final_crea_archivo(tmp_path):
    contenido = {"posts": [{"post_id": "post_01", "tema": "SIPOC"}]}
    path = guardar_contenido_final(contenido, tmp_path)

    assert path.exists()
    assert path.name == "contenido_final.json"
    assert json.loads(path.read_text(encoding="utf-8")) == contenido


def test_guardar_contenido_final_crea_directorio_si_no_existe(tmp_path):
    contenido = {"posts": []}
    output_dir = tmp_path / "no_existe_todavia"

    guardar_contenido_final(contenido, output_dir)

    assert output_dir.exists()


def test_cargar_temas_anteriores_sin_historial_devuelve_lista_vacia(tmp_path):
    temas = cargar_temas_anteriores("cliente_inexistente", tmp_path)
    assert temas == []


def test_cargar_temas_anteriores_junta_varios_meses(tmp_path):
    cliente_dir = tmp_path / "cili"
    guardar_contenido_final(
        {"posts": [{"post_id": "post_01", "tema": "SIPOC"}, {"post_id": "post_02", "tema": "5 S's"}]},
        cliente_dir / "julio_2026",
    )
    guardar_contenido_final(
        {"posts": [{"post_id": "post_01", "tema": "Andon"}]},
        cliente_dir / "agosto_2026",
    )

    temas = cargar_temas_anteriores("cili", tmp_path)

    assert set(temas) == {"SIPOC", "5 S's", "Andon"}


def test_cargar_temas_anteriores_ignora_posts_sin_tema(tmp_path):
    guardar_contenido_final(
        {"posts": [{"post_id": "post_01"}]},
        tmp_path / "cili" / "julio_2026",
    )

    temas = cargar_temas_anteriores("cili", tmp_path)

    assert temas == []


def test_cargar_temas_anteriores_ignora_json_corrupto(tmp_path):
    mes_dir = tmp_path / "cili" / "julio_2026"
    mes_dir.mkdir(parents=True)
    (mes_dir / "contenido_final.json").write_text("{esto no es json valido", encoding="utf-8")

    temas = cargar_temas_anteriores("cili", tmp_path)

    assert temas == []
