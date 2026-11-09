

"""
==============================================================================
MÓDULO: entidad_base.py
AUTORA: Claudia Trujillo (Rol: EntidadAbstracta)
==============================================================================
"""
from abc import ABC, abstractmethod

class EntidadBase(ABC):
    """
    CLASE ABSTRACTA BASE - Desarrollo de Claudia Trujillo.
    Es la raíz de todas las entidades del sistema Software FJ.
    """
    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_cliente(self) -> str:
        """Retorna el identificador de la entidad."""
        return self._id_entidad