"""
==============================================================================
MÓDULO: utils/logger.py
RESPONSABLE: Alejandro Gómez
DESCRIPCIÓN:
    Sistema de registro de eventos y errores en archivo de texto.
    Cumple el requisito: "Un archivo de logs donde se registren todos los
    errores y eventos relevantes".

    - Patrón Singleton: todo el sistema escribe en el mismo archivo.
    - Registra eventos (INFO), advertencias (WARNING), errores (ERROR)
      y fallos críticos (CRITICAL).
    - Soporta ENCADENAMIENTO de excepciones: si una excepción fue lanzada
      con "raise X from Y", el log guarda toda la cadena de causas.
    - El logger NUNCA debe tumbar la aplicación: si no puede escribir el
      archivo, lo informa por consola y el sistema sigue funcionando.
==============================================================================
"""
import logging
import os

# Carpeta raíz del proyecto (un nivel arriba de /utils)
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_LOGS = os.path.join(RAIZ_PROYECTO, "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


class RegistroEventos:
    """Registrador central de eventos y errores (Singleton)."""

    _instancia = None

    def __new__(cls):
        # Si ya existe una instancia se reutiliza (Singleton)
        if cls._instancia is None:
            instancia = super().__new__(cls)
            instancia._configurar()
            cls._instancia = instancia
        return cls._instancia

    def _configurar(self):
        """Prepara el archivo de logs y el formato de cada línea."""
        self._logger = logging.getLogger("software_fj")
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False  # evita duplicar líneas en consola

        if not self._logger.handlers:
            try:
                os.makedirs(RUTA_LOGS, exist_ok=True)
                manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
                manejador.setFormatter(logging.Formatter(
                    "%(asctime)s | %(levelname)-8s | %(message)s",
                    "%Y-%m-%d %H:%M:%S",
                ))
                self._logger.addHandler(manejador)
            except OSError as err:
                # El sistema debe seguir activo aunque falle el archivo
                print(f"[AVISO] No se pudo abrir el archivo de logs: {err}")
                self._logger.addHandler(logging.NullHandler())

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------
    @staticmethod
    def _cadena_excepciones(excepcion: BaseException) -> str:
        """
        Devuelve la cadena completa de excepciones encadenadas.
        Ej: ErrorCalculoCosto('...') <- ValueError('...')
        """
        partes = []
        actual = excepcion
        vistas = set()
        while actual is not None and id(actual) not in vistas:
            vistas.add(id(actual))
            partes.append(f"{type(actual).__name__}('{actual}')")
            # __cause__ = "raise X from Y" | __context__ = error previo implícito
            actual = actual.__cause__ or actual.__context__
        return " <- ".join(partes)

    def _escribir(self, nivel: int, mensaje: str, origen: str):
        """Escribe en el log sin permitir que un fallo detenga el programa."""
        try:
            prefijo = f"[{origen}] " if origen else ""
            self._logger.log(nivel, prefijo + mensaje)
        except Exception as err:  # noqa: BLE001 - el log nunca debe romper el sistema
            print(f"[AVISO] Fallo al escribir en el log: {err}")

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------
    def evento(self, mensaje: str, origen: str = ""):
        """Registra un evento normal (cliente creado, reserva confirmada...)."""
        self._escribir(logging.INFO, mensaje, origen)

    def advertencia(self, mensaje: str, origen: str = ""):
        """Registra una situación anómala que no detiene la operación."""
        self._escribir(logging.WARNING, mensaje, origen)

    def error(self, mensaje: str, excepcion: BaseException = None, origen: str = ""):
        """Registra un error. Si se pasa la excepción, guarda su cadena de causas."""
        if excepcion is not None:
            mensaje = f"{mensaje} | Detalle: {self._cadena_excepciones(excepcion)}"
        self._escribir(logging.ERROR, mensaje, origen)

    def critico(self, mensaje: str, excepcion: BaseException = None, origen: str = ""):
        """Registra un fallo grave que compromete la operación."""
        if excepcion is not None:
            mensaje = f"{mensaje} | Detalle: {self._cadena_excepciones(excepcion)}"
        self._escribir(logging.CRITICAL, mensaje, origen)


def obtener_logger() -> RegistroEventos:
    """Acceso rápido al registrador único del sistema."""
    return RegistroEventos()


# ==============================================================================
# Prueba rápida:  python utils/logger.py
# ==============================================================================
if __name__ == "__main__":
    log = obtener_logger()
    log.evento("Sistema iniciado", origen="Main")
    log.advertencia("Servicio con poca disponibilidad", origen="Servicio")
    try:
        try:
            int("abc")
        except ValueError as causa:
            raise RuntimeError("No se pudo procesar la reserva") from causa
    except RuntimeError as err:
        log.error("Fallo en reserva", excepcion=err, origen="Reserva")
        log.critico("Fallo crítico simulado en el subsistema", excepcion=err, origen="Sistema")
    print(f"Revisa el archivo: {ARCHIVO_LOG}")
