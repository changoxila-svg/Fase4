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
from utils.calculo_costos import ErrorCalculoCosto
from utils.logger import obtener_logger
from utils.excepciones import (
    ErrorReservaInvalida,
    ErrorEstadoReserva,
    ErrorServicioNoDisponible,
)

log = obtener_logger()


class Reserva(EntidadBase):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def _init_(self, id_reserva: str, cliente, servicio, duracion):
        try:
            super()._init_(id_reserva)
        except ValueError as err:
            raise ErrorReservaInvalida("El ID de la reserva no es válido o está vacío.") from err

        if cliente is None or servicio is None:
            raise ErrorReservaInvalida("La reserva necesita un cliente y un servicio.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = None
        self._estado = Reserva.PENDIENTE

        self._verificar_disponibilidad()
        self.duracion = duracion
        log.evento(f"Reserva creada: {self.resumen()}", origen="Reserva")

    @property
    def id_reserva(self) -> str:
        return self._id_entidad

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def duracion(self) -> float:
        return self._duracion

    @duracion.setter
    def duracion(self, valor):
        try:
            cantidad = float(valor)
        except (ValueError, TypeError) as err:
            raise ErrorReservaInvalida(f"La duración '{valor}' no es un número válido.") from err

        if not math.isfinite(cantidad) or cantidad <= 0:
            raise ErrorReservaInvalida("La duración debe ser un número mayor que 0.")

        try:
            self._servicio.validar_parametros(cantidad)
        except ValueError as err:
            raise ErrorReservaInvalida(f"Duración no permitida para este servicio: {err}") from err

        self._duracion = cantidad

    def _verificar_disponibilidad(self):
        try:
            self._servicio.validar_disponibilidad()
        except ErrorServicioNoDisponible as err:
            raise ErrorReservaInvalida(f"No se puede reservar: {err}") from err

    def calcular_total(self, iva=None, descuento=None) -> float:
        try:
            return self._servicio.calcular_costo(self._duracion, iva=iva, descuento=descuento)
        except (ValueError, ErrorServicioNoDisponible, ErrorCalculoCosto) as err:
            log.error(f"Error calculando total de reserva [{self.id_reserva}]", excepcion=err, origen="Reserva")
            raise ErrorReservaInvalida(f"No se pudo calcular el total: {err}") from err

    def confirmar(self):
        if self._estado != Reserva.PENDIENTE:
            err = ErrorEstadoReserva(
                f"Solo se puede confirmar una reserva PENDIENTE (estado actual: {self._estado})."
            )
            log.error(f"Cambio de estado inválido en [{self.id_reserva}]", excepcion=err, origen="Reserva")
            raise err
        self._verificar_disponibilidad()
        self._estado = Reserva.CONFIRMADA
        log.evento(f"Reserva [{self.id_reserva}] CONFIRMADA", origen="Reserva")

    def cancelar(self):
        if self._estado == Reserva.CANCELADA:
            err = ErrorEstadoReserva("La reserva ya estaba cancelada.")
            log.error(f"Intento de cancelar dos veces [{self.id_reserva}]", excepcion=err, origen="Reserva")
            raise err
        self._estado = Reserva.CANCELADA
        log.evento(f"Reserva [{self.id_reserva}] CANCELADA", origen="Reserva")

    def resumen(self) -> str:
        return (f"[{self.id_reserva}] Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | "
                f"Duración: {self._duracion:g} | Estado: {self._estado}")
