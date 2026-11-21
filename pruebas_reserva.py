"""Prueba manual del menú de reservas con clientes y servicios reales.
Ejecutar desde la raíz del proyecto:  python pruebas_reserva.py"""
from entidades.cliente import Cliente
from entidades.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from entidades.gestor_reservas import GestorReservas
from flujo_reservas import menu_reservas

clientes = {
    "CLI-001": Cliente("CLI-001", "Claudia Trujillo", "claudia@unad.edu.co", "3154445566"),
}
servicios = {
    "SRV-001": ReservaSala("SRV-001", "Sala Ejecutiva", 50000, 10),
    "SRV-002": AlquilerEquipo("SRV-002", "Portátil", 30000),
    "SRV-003": AsesoriaEspecializada("SRV-003", "Asesoría en Seguridad", 80000),
}

print("Clientes disponibles:", ", ".join(clientes))
print("Servicios disponibles:", ", ".join(servicios))
menu_reservas(GestorReservas(), clientes, servicios)
