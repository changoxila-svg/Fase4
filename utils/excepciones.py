class ErrorClienteInvalido(Exception):
    """Excepción lanzada cuando los datos de un cliente son inválidos."""
    pass


class ErrorServicioNoDisponible(Exception):
    """Excepción lanzada cuando se intenta solicitar o calcular costo de un servicio inactivo o no disponible."""
    pass


class ErrorReservaInvalida(Exception):
    """Excepción lanzada cuando los datos o la operación de una reserva son inválidos."""
    pass


class ErrorEstadoReserva(ErrorReservaInvalida):
    """Excepción lanzada ante un cambio de estado no permitido (ej: confirmar dos veces)."""
    pass


class ErrorReservaNoEncontrada(Exception):
    """Excepción lanzada cuando se busca una reserva que no existe."""
    pass


class ErrorCalculoCosto(Exception):
    """Excepción personalizada para cálculos de costos inconsistentes o parámetros inválidos."""
    pass
