"""Schema y validación del brief del cliente."""
import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

PLATAFORMAS_VALIDAS = {"Instagram", "LinkedIn", "Facebook", "TikTok"}
NIVELES_CONCIENCIA_VALIDOS = {
    "no_sabe_problema",
    "sabe_problema",
    "busca_solucion",
    "compara_opciones",
}
OBJETIVOS_MES_VALIDOS = {"awareness", "leads", "ventas", "comunidad"}


class RedesSociales(BaseModel):
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    facebook: Optional[str] = None
    tiktok: Optional[str] = None


class ClientBrief(BaseModel):
    # SECCIÓN A — Identidad del negocio
    empresa: str = Field(min_length=1)
    industria: str = Field(min_length=1)
    ciudad: str = Field(min_length=1)
    anos_mercado: int
    web: str = Field(min_length=1)
    redes_sociales: RedesSociales
    descripcion: str = Field(min_length=1)

    # SECCIÓN B — Oferta y servicios
    servicio_principal: str = Field(min_length=1)
    servicio_secundario: Optional[str] = None
    precio_rango: Optional[str] = None
    que_incluye: list[str] = Field(default_factory=list)
    duracion_o_entrega: Optional[str] = None
    diferenciadores: list[str] = Field(default_factory=list)
    resultado_tipico: Optional[str] = None

    # SECCIÓN C — Cliente ideal
    perfil_demografico: str = Field(min_length=1)
    dolores: list[str] = Field(min_length=1)
    deseos: list[str] = Field(min_length=1)
    objeciones: list[str] = Field(min_length=1)
    nivel_conciencia: str

    # SECCIÓN D — Identidad de marca
    tono: str = Field(min_length=1)
    colores_hex: list[str] = Field(min_length=1)
    estilo_visual: str = Field(min_length=1)
    tres_palabras_marca: list[str] = Field(min_length=1)
    evitar: Optional[str] = None

    # SECCIÓN E — Contenido y credibilidad
    credenciales: Optional[str] = None
    testimonios: list[str] = Field(default_factory=list)
    casos_exito: Optional[str] = None
    temas_que_funcionan: list[str] = Field(default_factory=list)
    temas_a_evitar: list[str] = Field(default_factory=list)
    competidores: list[str] = Field(default_factory=list)

    # SECCIÓN F — Configuración del mes
    mes: str = Field(min_length=1)
    frecuencia_semanal: int
    plataformas: list[str] = Field(min_length=1)
    objetivo_mes: str = Field(min_length=1)
    descripcion_objetivo: Optional[str] = None
    evento_especial: Optional[str] = None
    tema_semana_1: Optional[str] = None
    tema_semana_2: Optional[str] = None
    tema_semana_3: Optional[str] = None
    tema_semana_4: Optional[str] = None

    @field_validator("plataformas")
    @classmethod
    def validar_plataformas(cls, v: list[str]) -> list[str]:
        invalidas = set(v) - PLATAFORMAS_VALIDAS
        if invalidas:
            raise ValueError(
                f"Plataformas inválidas: {invalidas}. Válidas: {PLATAFORMAS_VALIDAS}"
            )
        return v

    @field_validator("nivel_conciencia")
    @classmethod
    def validar_nivel_conciencia(cls, v: str) -> str:
        if v not in NIVELES_CONCIENCIA_VALIDOS:
            raise ValueError(
                f"nivel_conciencia inválido: '{v}'. Válidos: {NIVELES_CONCIENCIA_VALIDOS}"
            )
        return v

    @field_validator("frecuencia_semanal")
    @classmethod
    def validar_frecuencia(cls, v: int) -> int:
        if not 1 <= v <= 7:
            raise ValueError(f"frecuencia_semanal debe estar entre 1 y 7, recibido: {v}")
        return v

    @field_validator("objetivo_mes")
    @classmethod
    def validar_objetivo_mes(cls, v: str) -> str:
        if v not in OBJETIVOS_MES_VALIDOS:
            raise ValueError(
                f"objetivo_mes inválido: '{v}'. Válidos: {OBJETIVOS_MES_VALIDOS}"
            )
        return v

    @classmethod
    def from_json(cls, path: str | Path) -> "ClientBrief":
        """Carga y valida un brief desde un archivo JSON."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.model_validate(data)


def validate_and_report(path: str | Path) -> tuple[bool, str]:
    """Valida un brief y retorna (es_valido, mensaje_legible)."""
    try:
        ClientBrief.from_json(path)
        return True, f"✅ Brief válido: {path}"
    except ValidationError as e:
        lineas = ["❌ Brief inválido. Campos con problema:"]
        for err in e.errors():
            campo = ".".join(str(p) for p in err["loc"])
            lineas.append(f"  - {campo}: {err['msg']}")
        return False, "\n".join(lineas)
    except json.JSONDecodeError as e:
        return False, f"❌ El archivo no es JSON válido: {e}"
    except FileNotFoundError:
        return False, f"❌ No se encontró el archivo: {path}"
