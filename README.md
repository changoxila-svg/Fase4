# Fase4
Gestion de clientes, servicios y reservas
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
=============================================================================
