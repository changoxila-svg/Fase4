class ErrorClienteInvalido(Exception):
    """Excepción lanzada cuando los datos de un cliente son inválidos."""
    pass


class ErrorServicioNoDisponible(Exception):
    """Excepción lanzada cuando se intenta solicitar o calcular costo de un servicio inactivo o no disponible."""
    pass
