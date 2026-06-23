from pathlib import Path

from pipeline.brief_schema import ClientBrief, validate_and_report

BRIEF_VALIDO = Path(__file__).parent.parent / "briefs" / "cili_julio_2026.json"


def test_carga_brief_valido():
    brief = ClientBrief.from_json(BRIEF_VALIDO)
    assert brief.empresa.startswith("CiLi")
    assert brief.frecuencia_semanal == 5


def test_validate_and_report_brief_valido():
    es_valido, mensaje = validate_and_report(BRIEF_VALIDO)
    assert es_valido
    assert "válido" in mensaje


def test_plataforma_invalida_falla(tmp_path):
    import json

    data = json.loads(BRIEF_VALIDO.read_text(encoding="utf-8"))
    data["plataformas"] = ["Twitter"]
    archivo = tmp_path / "brief_malo.json"
    archivo.write_text(json.dumps(data), encoding="utf-8")

    es_valido, mensaje = validate_and_report(archivo)
    assert not es_valido
    assert "Plataformas inválidas" in mensaje


def test_frecuencia_fuera_de_rango_falla(tmp_path):
    import json

    data = json.loads(BRIEF_VALIDO.read_text(encoding="utf-8"))
    data["frecuencia_semanal"] = 10
    archivo = tmp_path / "brief_malo.json"
    archivo.write_text(json.dumps(data), encoding="utf-8")

    es_valido, _ = validate_and_report(archivo)
    assert not es_valido


def test_archivo_inexistente():
    es_valido, mensaje = validate_and_report("no_existe.json")
    assert not es_valido
    assert "No se encontró" in mensaje


def test_campo_obligatorio_vacio_falla(tmp_path):
    import json

    data = json.loads(BRIEF_VALIDO.read_text(encoding="utf-8"))
    data["empresa"] = ""
    archivo = tmp_path / "brief_malo.json"
    archivo.write_text(json.dumps(data), encoding="utf-8")

    es_valido, mensaje = validate_and_report(archivo)
    assert not es_valido
    assert "empresa" in mensaje


def test_objetivo_mes_invalido_falla(tmp_path):
    import json

    data = json.loads(BRIEF_VALIDO.read_text(encoding="utf-8"))
    data["objetivo_mes"] = "branding"
    archivo = tmp_path / "brief_malo.json"
    archivo.write_text(json.dumps(data), encoding="utf-8")

    es_valido, mensaje = validate_and_report(archivo)
    assert not es_valido
    assert "objetivo_mes inválido" in mensaje


def test_template_vacio_es_rechazado():
    template = Path(__file__).parent.parent / "briefs" / "_template_brief.json"
    es_valido, _ = validate_and_report(template)
    assert not es_valido
