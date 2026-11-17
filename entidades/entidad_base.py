

"""
------------------------------------------------------------------------------
MÓDULO: entidad_base.py
AUTORA: Claudia Trujillo (Rol: EntidadAbstracta)
------------------------------------------------------------------------------
"""
from abc import ABC


class EntidadBase(ABC):
    """
    CLASE ABSTRACTA BASE - Desarrollo de Claudia Trujillo.
    Es la raíz de todas las entidades del sistema Software C.A.D.E.
    """
    def __init__(self, id_entidad: str):
        if not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ValueError("El identificador de la entidad no puede estar vacío.")
        self._id_entidad = id_entidad.strip()

    @property
    def id_cliente(self) -> str:
        """Retorna el identificador de la entidad."""
        return self._id_entidad