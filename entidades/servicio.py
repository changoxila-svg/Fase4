"""
==============================================================================
MÓDULO: servicio.py
RESPONSABLE: Erick Sánchez
CURSO: Programación (Código 213023) - UNAD - Paso 4: Laboratorio POO
DESCRIPCIÓN: Define la clase abstracta Servicio y 3 clases hijas polimórficas:
               1. ReservaSala
               2. AlquilerEquipo
               3. AsesoriaEspecializada
             Implementa los métodos obligatorios:
               - calcular_costo()
               - describir_servicio()
               - validar_parametros()
==============================================================================
"""
from abc import abstractmethod
from entidades.entidad_base import EntidadBase
from utils.excepciones import ErrorClienteInvalido  # O la excepción de validación base
class Servicio(EntidadBase):
    """
    Clase abstracta que define el contrato común para todos los servicios de Software FJ.
    No puede ser instanciada directamente.
    """
    def __init__(self, id_servicio: str, nombre: str, precio_base: float):
        super().__init__(id_servicio)
        if precio_base <= 0:
            raise ValueError(f"El precio base debe ser mayor a 0. Recibido: {precio_base}")
        self._nombre = nombre
        self._precio_base = float(precio_base)
        self._disponible = True
    # ── Propiedades ───────────────────────────────────────────────────────────
    @property
    def id_servicio(self) -> str:
        return self._id_entidad
    @property
    def nombre(self) -> str:
        return self._nombre
    @property
    def precio_base(self) -> float:
        return self._precio_base
    @property
    def disponible(self) -> bool:
        return self._disponible
    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)
    # ── Métodos abstractos (Exigidos por la guía UNAD) ─────────────────────────
    @abstractmethod
    def calcular_costo(self, duracion: float) -> float:
        """Calcula el costo total según la tarifa específica del servicio."""
        pass
    @abstractmethod
    def describir_servicio(self) -> str:
        """Retorna una descripción detallada de las características del servicio."""
        pass
    @abstractmethod
    def validar_parametros(self, duracion: float) -> bool:
        """Valida las reglas de negocio (tiempos mínimos y máximos)."""
        pass
# ═════════════════════════════════════════════════════════════════════════════
# 1. ESPECIALIZACIÓN: Reserva de Salas
# ═════════════════════════════════════════════════════════════════════════════
class ReservaSala(Servicio):
    """Servicio de salas de juntas / conferencias (cobro por hora)."""
    def __init__(self, id_servicio: str, nombre: str, precio_por_hora: float, capacidad: int):
        super().__init__(id_servicio, nombre, precio_por_hora)
        if capacidad <= 0:
            raise ValueError(f"La capacidad debe ser positiva. Recibido: {capacidad}")
        self._capacidad = capacidad
    @property
    def capacidad(self) -> int:
        return self._capacidad
    def validar_parametros(self, duracion: float) -> bool:
        if not (1.0 <= duracion <= 8.0):
            raise ValueError(f"La duración en sala debe ser entre 1 y 8 horas. Recibido: {duracion}")
        return True
    def calcular_costo(self, duracion: float) -> float:
        self.validar_parametros(duracion)
        return round(self.precio_base * duracion, 2)
    def describir_servicio(self) -> str:
        return f"[SALA] {self.nombre} | Capacidad: {self.capacidad} personas | Tarifa: ${self.precio_base}/hora"
# ═════════════════════════════════════════════════════════════════════════════
# 2. ESPECIALIZACIÓN: Alquiler de Equipos
# ═════════════════════════════════════════════════════════════════════════════
class AlquilerEquipo(Servicio):
    """Alquiler de portátiles y servidores (cobro por días + seguro)."""
    def __init__(self, id_servicio: str, nombre: str, precio_por_dia: float, seguro: float = 5000.0):
        super().__init__(id_servicio, nombre, precio_por_dia)
        self._seguro = seguro
    def validar_parametros(self, duracion: float) -> bool:
        if duracion < 1:
            raise ValueError("El alquiler de equipo debe ser de al menos 1 día.")
        return True
    def calcular_costo(self, duracion: float) -> float:
        self.validar_parametros(duracion)
        # Costo = (precio por día * días) + seguro obligatorio
        return round((self.precio_base * duracion) + self._seguro, 2)
    def describir_servicio(self) -> str:
        return f"[EQUIPO] {self.nombre} | Seguro: ${self._seguro} | Tarifa: ${self.precio_base}/día"
# ═════════════════════════════════════════════════════════════════════════════
# 3. ESPECIALIZACIÓN: Asesoría Especializada
# ═════════════════════════════════════════════════════════════════════════════
class AsesoriaEspecializada(Servicio):
    """Consultoría profesional (cobro por sesión)."""
    def __init__(self, id_servicio: str, nombre: str, precio_por_sesion: float, area: str = "Ciberseguridad"):
        super().__init__(id_servicio, nombre, precio_por_sesion)
        self._area = area
    def validar_parametros(self, duracion: float) -> bool:
        if duracion <= 0:
            raise ValueError("Las sesiones de asesoría deben ser mayores a 0.")
        return True
    def calcular_costo(self, duracion: float) -> float:
        self.validar_parametros(duracion)
        return round(self.precio_base * duracion, 2)
    def describir_servicio(self) -> str:
        return f"[ASESORÍA] {self.nombre} | Área: {self._area} | Tarifa: ${self.precio_base}/sesión"
