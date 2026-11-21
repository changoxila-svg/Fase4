from abc import ABC, abstractmethod


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
    def id_entidad(self) -> str:
        """Retorna el identificador general de la entidad."""
        return self._id_entidad

    @property
    def id_cliente(self) -> str:
        """Alias para compatibilidad con la clase Cliente."""
        return self._id_entidad

    def resumen(self) -> str:
        """Retorna una descripción resumida de la entidad."""
        return f"Entidad [{self._id_entidad}]"

    @abstractmethod
    def resumen(self) -> str:
        """Cada entidad concreta debe implementar su resumen."""
        raise NotImplementedError