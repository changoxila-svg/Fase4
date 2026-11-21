"""
==============================================================================
MÓDULO: entidades/metodos.sobrecargados.py
RESPONSABLE: Alejandro Gomez
DESCRIPCION:
    Métodos SOBRECARGADOS para el cálculo de costos (base, IVA, descuentos).

    NOTA SOBRE SOBRECARGA EN PYTHON:
    Python no permite definir dos métodos con el mismo nombre y distinta
    firma (como Java o C#). Se simula la sobrecarga con tres técnicas:
      1. Parámetros opcionales con valores por defecto  -> calcular_costo()
      2. Despacho por tipo de argumento (singledispatchmethod)
                                                         -> calcular_descuento()
      3. Métodos con nombres especializados que delegan en el principal
                                                         -> calcular_costo_con_iva(), etc.
==============================================================================
"""
from functools import singledispatchmethod

from entidades.logger import obtener_logger

log = obtener_logger()


class ErrorCalculoCosto(Exception):
    """
    Excepción personalizada para cálculos inconsistentes.
    (Si el equipo ya la define en utils/excepciones.py, se puede mover allí
    y cambiar el import.)
    """


class CalculadoraCostos:
    """Calculadora de costos con métodos sobrecargados."""

    IVA_COLOMBIA = 0.19  # IVA general en Colombia (19 %)

    # ------------------------------------------------------------------
    # Validaciones internas
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_numero_positivo(valor, nombre: str):
        """Valida que un parámetro sea numérico (no bool) y mayor que cero."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ErrorCalculoCosto(f"'{nombre}' debe ser numérico, se recibió: {valor!r}")
        if valor <= 0:
            raise ErrorCalculoCosto(f"'{nombre}' debe ser mayor que cero, se recibió: {valor}")

    # ------------------------------------------------------------------
    # SOBRECARGA POR TIPO: calcular_descuento(descuento, subtotal)
    #   float  -> fracción        (0.10  = 10 %)
    #   int    -> monto fijo      (5000  = $5.000)
    #   str    -> porcentaje texto ("15%")
    # ------------------------------------------------------------------
    @singledispatchmethod
    def calcular_descuento(self, descuento, subtotal: float) -> float:
        """Versión base: tipo de descuento no soportado."""
        raise ErrorCalculoCosto(
            f"Tipo de descuento no soportado: {type(descuento).__name__} ({descuento!r})"
        )

    @calcular_descuento.register(float)
    def _(self, descuento: float, subtotal: float) -> float:
        # Descuento como fracción del subtotal
        if not 0 <= descuento < 1:
            raise ErrorCalculoCosto(f"El descuento fraccional debe estar entre 0 y 1: {descuento}")
        return subtotal * descuento

    @calcular_descuento.register(int)
    def _(self, descuento: int, subtotal: float) -> float:
        # bool es subclase de int: se rechaza explícitamente
        if isinstance(descuento, bool):
            raise ErrorCalculoCosto("El descuento no puede ser booleano.")
        # Descuento como monto fijo en pesos
        if descuento < 0 or descuento > subtotal:
            raise ErrorCalculoCosto(
                f"El descuento fijo ({descuento}) no puede ser negativo ni superar el subtotal ({subtotal})."
            )
        return float(descuento)

    @calcular_descuento.register(str)
    def _(self, descuento: str, subtotal: float) -> float:
        # Descuento como texto, ej: "15%"
        texto = descuento.strip()
        if not texto.endswith("%"):
            raise ErrorCalculoCosto(f"El descuento en texto debe terminar en '%': {descuento!r}")
        try:
            porcentaje = float(texto[:-1].replace(",", "."))
        except ValueError as causa:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ErrorCalculoCosto(f"Porcentaje de descuento inválido: {descuento!r}") from causa
        if not 0 <= porcentaje < 100:
            raise ErrorCalculoCosto(f"El porcentaje debe estar entre 0 y 100: {porcentaje}")
        return subtotal * porcentaje / 100

    # ------------------------------------------------------------------
    # SOBRECARGA POR PARÁMETROS OPCIONALES: método principal
    #   calcular_costo(tarifa, duracion)
    #   calcular_costo(tarifa, duracion, iva=True)
    #   calcular_costo(tarifa, duracion, iva=0.05)
    #   calcular_costo(tarifa, duracion, descuento="10%")
    #   calcular_costo(tarifa, duracion, iva=True, descuento=5000)
    # ------------------------------------------------------------------
    def calcular_costo(self, tarifa: float, duracion: float, iva=None, descuento=None) -> float:
        """
        Calcula el costo total de un servicio.

        :param tarifa:    valor por unidad de tiempo (hora/día)
        :param duracion:  cantidad de unidades de tiempo
        :param iva:       None/False = sin IVA | True = 19 % | float = tasa personalizada
        :param descuento: None | float (fracción) | int (monto fijo) | str ("15%")
        :return:          costo total redondeado a 2 decimales
        :raises ErrorCalculoCosto: ante datos inválidos o resultados inconsistentes
        """
        try:
            self._validar_numero_positivo(tarifa, "tarifa")
            self._validar_numero_positivo(duracion, "duracion")

            subtotal = float(tarifa) * float(duracion)

            # 1) Descuento (se aplica antes del IVA)
            if descuento is not None:
                subtotal -= self.calcular_descuento(descuento, subtotal)

            # 2) IVA
            tasa = self._resolver_tasa_iva(iva)
            total = round(subtotal * (1 + tasa), 2)

            # 3) Verificación de consistencia
            if total < 0:
                raise ErrorCalculoCosto(f"El cálculo produjo un total negativo: {total}")

            log.evento(
                f"Costo calculado: tarifa={tarifa}, duracion={duracion}, "
                f"iva={iva}, descuento={descuento!r} -> total={total}",
                origen="CalculadoraCostos",
            )
            return total

        except ErrorCalculoCosto as err:
            log.error("Fallo en el cálculo de costo", excepcion=err, origen="CalculadoraCostos")
            raise
        except Exception as err:  # noqa: BLE001 - cualquier error imprevisto
            log.critico("Error inesperado en el cálculo de costo", excepcion=err, origen="CalculadoraCostos")
            raise ErrorCalculoCosto("Error inesperado al calcular el costo.") from err

    def _resolver_tasa_iva(self, iva) -> float:
        """Convierte el parámetro 'iva' en una tasa numérica."""
        if iva is None or iva is False:
            return 0.0
        if iva is True:
            return self.IVA_COLOMBIA
        if isinstance(iva, (int, float)) and 0 <= iva < 1:
            return float(iva)
        raise ErrorCalculoCosto(f"Tasa de IVA inválida (use True o un valor entre 0 y 1): {iva!r}")

    # ------------------------------------------------------------------
    # SOBRECARGA POR NOMBRE: variantes que delegan en calcular_costo()
    # ------------------------------------------------------------------
    def calcular_costo_base(self, tarifa: float, duracion: float) -> float:
        """Costo sin impuestos ni descuentos."""
        return self.calcular_costo(tarifa, duracion)

    def calcular_costo_con_iva(self, tarifa: float, duracion: float, tasa_iva=True) -> float:
        """Costo con IVA (19 % por defecto o tasa personalizada)."""
        return self.calcular_costo(tarifa, duracion, iva=tasa_iva)

    def calcular_costo_con_descuento(self, tarifa: float, duracion: float, descuento) -> float:
        """Costo con descuento, sin IVA."""
        return self.calcular_costo(tarifa, duracion, descuento=descuento)

    def calcular_costo_completo(self, tarifa: float, duracion: float, descuento, tasa_iva=True) -> float:
        """Costo con descuento e IVA."""
        return self.calcular_costo(tarifa, duracion, iva=tasa_iva, descuento=descuento)


# ==============================================================================
# Prueba rápida:  python -m utils.calculo_costos   (desde la raíz del proyecto)
# ==============================================================================
if __name__ == "__main__":
    calc = CalculadoraCostos()
    print("Base               :", calc.calcular_costo_base(50000, 3))
    print("Con IVA 19 %       :", calc.calcular_costo_con_iva(50000, 3))
    print("IVA personalizado  :", calc.calcular_costo(50000, 3, iva=0.05))
    print("Desc. fracción 10% :", calc.calcular_costo_con_descuento(50000, 3, 0.10))
    print("Desc. fijo $5.000  :", calc.calcular_costo_con_descuento(50000, 3, 5000))
    print("Desc. texto '15%'  :", calc.calcular_costo_con_descuento(50000, 3, "15%"))
    print("Completo           :", calc.calcular_costo_completo(50000, 3, "10%"))

    for datos in [(-1, 2), (50000, 0), (50000, 2, None, "abc%"), (50000, 2, 0.5, 1.5)]:
        try:
            calc.calcular_costo(*datos)
        except ErrorCalculoCosto as e:
            print(f"  ✔ Error controlado {datos}: {e}")
