# Gestion de clientes, servicios y reservas

"""
==============================================================================
PROYECTO: SOFTWARE FJ - SISTEMA INTEGRAL INTERACTIVO POR TERMINAL
MÓDULO: main2.py (Consola Interactiva - 100% Terminal CMD / PowerShell)
CURSO: Programación (Código 213023) - Unidad 2 - Paso 4: Laboratorio POO
UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)

DISTRIBUCIÓN OFICIAL DE ROLES:
  1. Claudia Trujillo:
     • Entidad abstracta (EntidadBase)
     • Clase Cliente con encapsulación de atributos privados y validaciones robustas.
  2. Erick Sánchez:
     • Clase abstracta Servicio
     • 3 clases especializadas con polimorfismo: ReservaSala, AlquilerEquipo, AsesoriaEspecializada.
     • Coordinación y arquitectura del sistema.
  3. Alejandro Gómez (Alejo):
     • Métodos sobrecargados de cálculo de costos (base, impuestos IVA, descuentos).
     • Sistema de registro de eventos y errores en archivo de texto (logger.py).
  4. Daniel David Escobar Reina:
     • Clase Reserva (integración de cliente, servicio, duración, estados).
     • Flujo con manejo de excepciones (try / except / else / finally y encadenamiento).
     • Gestor de reservas y repositorio en memoria (GestorReservas).
==============================================================================
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from entidades.entidad_base import EntidadBase
from utils.excepciones import ErrorClienteInvalido


class Cliente(EntidadBase):
    """
    CLASE CLIENTE - DESARROLLADA POR: Claudia Trujillo
    Aplica encapsulación estricta y validación de datos personales.
    """
    def __init__(self, id_cliente: str, nombre: str, email: str, celular: str):
        # Inicializa la clase abstracta base
        super().__init__(id_cliente)

        # Atributos privados encapsulados
        self.__nombre = None
        self.__email = None
        self.__celular = None

        # Asignación pasando obligatoriamente por los filtros de validación
        self.nombre = nombre
        self.email = email
        self.celular = celular

    # --- ENCAPSULACIÓN Y VALIDACIÓN DEL NOMBRE ---
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ErrorClienteInvalido("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    # --- ENCAPSULACIÓN Y VALIDACIÓN DEL EMAIL ---
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if "@" not in valor or "." not in valor:
            raise ErrorClienteInvalido(f"El correo '{valor}' no tiene un formato válido (ej: usuario@dominio.com).")
        self.__email = valor.strip()

    # --- ENCAPSULACIÓN Y VALIDACIÓN DEL CELULAR ---
    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str):
        # Validación ajustada a la longitud estricta de telefonía celular en Colombia (10 dígitos)
        if not valor or not valor.isdigit() or len(valor) != 10:
            raise ErrorClienteInvalido(f"El número celular '{valor}' debe contener exactamente 10 dígitos numéricos.")
        self.__celular = valor


# ==============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL (Para iniciar el programa en la terminal)
# ==============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" 🏢 SOFTWARE C.A.D.E. - SISTEMA INTEGRAL INTERACTIVO ")
    print("     FASE 4: COMPONENTE PRÁCTICO (POO Y EXCEPCIONES) ")
    print("=" * 70)
    
    try:
        print("\nPrueba 1: Intentando registrar cliente válido...")
        # Intentamos crear un usuario con datos que cumplen tus reglas @property
        cliente_ok = Cliente("CLI-001", "Claudia Trujillo", "claudia@unad.edu.co", "3154445566")
        print(f"  ✔ [ÉXITO]: Cliente creado -> Nombre: {cliente_ok.nombre}, Celular: {cliente_ok.celular}")
        
        print("\nPrueba 2: Intentando forzar un error de celular (menos de 10 dígitos)...")
        # Esto disparará tu excepción personalizada ErrorClienteInvalido automáticamente
        cliente_error = Cliente("CLI-002", "Juan Pérez", "juan@correo.com", "300123")
        
    except ErrorClienteInvalido as err:
        print(f"  ✔ [EXCEPCIÓN CAPTURADA CORRECTAMENTE]: {err}")
    
    print("\n" + "=" * 70)
    print(" PROGRAMA FINALIZADO CON ESTABILIDAD ABSOLUTA ")
    print("=" * 70)