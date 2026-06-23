from pipeline.utils import cargar_json_si_existe, con_reintentos, guardar_json, slug


def test_slug_normaliza_texto():
    assert slug("CiLi — Institute") == "cili_institute"
    assert slug("Julio 2026") == "julio_2026"


def test_guardar_y_cargar_json(tmp_path):
    path = tmp_path / "datos.json"
    guardar_json({"a": 1}, path)
    assert cargar_json_si_existe(path) == {"a": 1}


def test_cargar_json_inexistente(tmp_path):
    assert cargar_json_si_existe(tmp_path / "no_existe.json") is None


def test_con_reintentos_exitoso_al_segundo_intento():
    intentos = {"n": 0}

    def func():
        intentos["n"] += 1
        if intentos["n"] < 2:
            raise ValueError("falla simulada")
        return "ok"

    resultado = con_reintentos(func, intentos=3, espera_base=0)
    assert resultado == "ok"
    assert intentos["n"] == 2


def test_con_reintentos_falla_tras_agotar_intentos():
    import pytest

    def func():
        raise ValueError("siempre falla")

    with pytest.raises(ValueError):
        con_reintentos(func, intentos=2, espera_base=0)
