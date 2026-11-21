import unittest

from entidades.cliente import Cliente
from entidades.servicio import ReservaSala, AlquilerEquipo
from entidades.reserva import Reserva
from entidades.gestor_reservas import GestorReservas
from utils.excepciones import (
    ErrorReservaInvalida,
    ErrorEstadoReserva,
    ErrorReservaNoEncontrada,
    ErrorServicioNoDisponible,
)


class TestReserva(unittest.TestCase):
    def setUp(self):
        self.cliente = Cliente("CLI-001", "Claudia Trujillo", "claudia@unad.edu.co", "3154445566")
        self.sala = ReservaSala("SRV-001", "Sala Ejecutiva", 50000, 10)
        self.equipo = AlquilerEquipo("SRV-002", "Portátil", 30000)

    def test_nace_pendiente(self):
        r = Reserva("R1", self.cliente, self.sala, 2)
        self.assertEqual(r.estado, "PENDIENTE")

    def test_duracion_texto_encadena_valueerror(self):
        with self.assertRaises(ErrorReservaInvalida) as ctx:
            Reserva("R1", self.cliente, self.sala, "abc")
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_duracion_cero(self):
        with self.assertRaises(ErrorReservaInvalida):
            Reserva("R1", self.cliente, self.sala, 0)

    def test_duracion_fuera_de_rango_de_la_sala(self):
        with self.assertRaises(ErrorReservaInvalida) as ctx:
            Reserva("R1", self.cliente, self.sala, 9)  # la sala admite 1 a 8 horas
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_servicio_no_disponible(self):
        self.sala.disponible = False
        with self.assertRaises(ErrorReservaInvalida) as ctx:
            Reserva("R1", self.cliente, self.sala, 2)
        self.assertIsInstance(ctx.exception.__cause__, ErrorServicioNoDisponible)

    def test_id_vacio(self):
        with self.assertRaises(ErrorReservaInvalida) as ctx:
            Reserva("   ", self.cliente, self.sala, 2)
        self.assertIsInstance(ctx.exception.__cause__, ValueError)

    def test_confirmar_dos_veces(self):
        r = Reserva("R1", self.cliente, self.sala, 2)
        r.confirmar()
        with self.assertRaises(ErrorEstadoReserva):
            r.confirmar()

    def test_cancelar_dos_veces(self):
        r = Reserva("R1", self.cliente, self.sala, 2)
        r.cancelar()
        with self.assertRaises(ErrorEstadoReserva):
            r.cancelar()

    def test_total_sala(self):
        self.assertEqual(Reserva("R1", self.cliente, self.sala, 2).calcular_total(), 100000.0)

    def test_total_equipo_incluye_seguro(self):
        # 30000 * 3 días + 5000 de seguro
        self.assertEqual(Reserva("R1", self.cliente, self.equipo, 3).calcular_total(), 95000.0)

    def test_id_duplicado(self):
        g = GestorReservas()
        g.agregar(Reserva("R1", self.cliente, self.sala, 2))
        with self.assertRaises(ErrorReservaInvalida):
            g.agregar(Reserva("R1", self.cliente, self.sala, 3))

    def test_buscar_inexistente(self):
        with self.assertRaises(ErrorReservaNoEncontrada) as ctx:
            GestorReservas().buscar("R99")
        self.assertIsInstance(ctx.exception.__cause__, KeyError)


if __name__ == "__main__":
    unittest.main()
