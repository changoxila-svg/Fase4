"""
==============================================================================
MÓDULO: reserva.py
AUTOR: Daniel David Escobar Reina (Rol: Clase Reserva)
DESCRIPCIÓN: Integra un cliente, un servicio y una duración, y controla el
             estado de la reserva (PENDIENTE, CONFIRMADA, CANCELADA).
             La duración se mide en la unidad del servicio: horas (sala),
             días (equipo) o sesiones (asesoría).
==============================================================================
"""
import math

from entidades.entidad_base import EntidadBase
from utils.excepciones import (
    ErrorReservaInvalida,
    ErrorEstadoReserva,
    ErrorServicioNoDisponible,
)


class Reserva(EntidadBase):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(self, id_reserva: str, cliente, servicio, duracion):
        # EntidadBase lanza ValueError si el ID está vacío: se encadena
        try:
            super().__init__(id_reserva)
        except ValueError as err:
            raise ErrorReservaInvalida("El ID de la reserva no es válido o está vacío.") from err

        if cliente is None or servicio is None:
            raise ErrorReservaInvalida("La reserva necesita un cliente y un servicio.")

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = None
        self.__estado = Reserva.PENDIENTE

        self._verificar_disponibilidad()
        self.duracion = duracion  # pasa por el setter con validación

    # --- Propiedades ---------------------------------------------------------
    @property
    def id_reserva(self) -> str:
        return self._id_entidad

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def duracion(self) -> float:
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        # Excepción encadenada: el error original queda como causa (__cause__)
        try:
            cantidad = float(valor)
        except (ValueError, TypeError) as err:
            raise ErrorReservaInvalida(f"La duración '{valor}' no es un número válido.") from err

        if not math.isfinite(cantidad) or cantidad <= 0:
            raise ErrorReservaInvalida("La duración debe ser un número mayor que 0.")

        # Cada servicio (de Erick) valida sus propios límites y lanza ValueError
        try:
            self.__servicio.validar_parametros(cantidad)
        except ValueError as err:
            raise ErrorReservaInvalida(f"Duración no permitida para este servicio: {err}") from err

        self.__duracion = cantidad

    # --- Reglas de negocio ---------------------------------------------------
    def _verificar_disponibilidad(self):
        try:
            self.__servicio.validar_disponibilidad()
        except ErrorServicioNoDisponible as err:
            raise ErrorReservaInvalida(f"No se puede reservar: {err}") from err

    def calcular_total(self) -> float:
        """Pide el costo al servicio (polimorfismo: cada servicio calcula distinto)."""
        try:
            return self.__servicio.calcular_costo(self.__duracion)
        except (ValueError, ErrorServicioNoDisponible) as err:
            raise ErrorReservaInvalida(f"No se pudo calcular el total: {err}") from err

    # --- Control de estados --------------------------------------------------
    def confirmar(self):
        if self.__estado != Reserva.PENDIENTE:
            raise ErrorEstadoReserva(
                f"Solo se puede confirmar una reserva PENDIENTE (estado actual: {self.__estado})."
            )
        self._verificar_disponibilidad()
        self.__estado = Reserva.CONFIRMADA

    def cancelar(self):
        if self.__estado == Reserva.CANCELADA:
            raise ErrorEstadoReserva("La reserva ya estaba cancelada.")
        self.__estado = Reserva.CANCELADA

    # --- Presentación --------------------------------------------------------
    def resumen(self) -> str:
        return (f"[{self.id_reserva}] Cliente: {self.__cliente.nombre} | "
                f"Servicio: {self.__servicio.nombre} | "
                f"Duración: {self.__duracion:g} | Estado: {self.__estado}")

    def __str__(self):
        return self.resumen()
