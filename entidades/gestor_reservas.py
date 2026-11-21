"""
==============================================================================
MÓDULO: gestor_reservas.py
AUTOR: Daniel David Escobar Reina (Rol: Capa de Persistencia)
DESCRIPCIÓN: Repositorio en memoria local (un diccionario). Sin base de datos.
==============================================================================
"""
from utils.excepciones import ErrorReservaInvalida, ErrorReservaNoEncontrada


class GestorReservas:
    def __init__(self):
        self.__reservas = {}

    def agregar(self, reserva):
        if reserva.id_reserva in self.__reservas:
            raise ErrorReservaInvalida(f"Ya existe una reserva con el ID '{reserva.id_reserva}'.")
        self.__reservas[reserva.id_reserva] = reserva

    def buscar(self, id_reserva: str):
        try:
            return self.__reservas[id_reserva]
        except KeyError as err:
            raise ErrorReservaNoEncontrada(f"No existe la reserva '{id_reserva}'.") from err

    def listar(self) -> list:
        return list(self.__reservas.values())

    def eliminar(self, id_reserva: str):
        self.buscar(id_reserva)  # lanza ErrorReservaNoEncontrada si no existe
        del self.__reservas[id_reserva]
