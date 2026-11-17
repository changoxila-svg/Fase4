"""
------------------------------------------------------------------------------
MÓDULO: cliente.py
AUTORA: Claudia Trujillo (Rol: EntidadAbstracta y Cliente)
------------------------------------------------------------------------------
"""
from entidades.entidad_base import EntidadBase
from utils.excepciones import ErrorClienteInvalido


class Cliente(EntidadBase):
    """
    CLASE CLIENTE - DESARROLLADA POR: Claudia Trujillo
    Aplica encapsulación estricta y validación de datos personales.
    """
    def __init__(self, id_cliente: str, nombre: str, email: str, celular: str):
        try:
            super().__init__(id_cliente)
        except ValueError as err:
            raise ErrorClienteInvalido("El ID del cliente no es válido o está vacío.") from err

        self.__nombre = None
        self.__email = None
        self.__celular = None

        self.nombre = nombre
        self.email = email
        self.celular = celular

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorClienteInvalido("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ErrorClienteInvalido(f"El correo '{valor}' no tiene un formato válido (ej: usuario@dominio.com).")
        self.__email = valor.strip()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str):
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ErrorClienteInvalido(f"El número celular '{valor}' debe contener exactamente 10 dígitos numéricos.")
        self.__celular = valor

    def resumen(self) -> str:
        return f"Cliente [{self.id_cliente}]: {self.nombre} | Tel: {self.celular}"