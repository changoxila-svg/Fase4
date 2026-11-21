from entidades.entidad_base import EntidadBase
from entidades.cliente import Cliente
from entidades.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from entidades.reserva import Reserva
from entidades.gestor_reservas import GestorReservas
from utils.calculo_costos import ErrorCalculoCosto
from utils.excepciones import (
    ErrorClienteInvalido,
    ErrorServicioNoDisponible,
    ErrorReservaInvalida,
    ErrorEstadoReserva,
    ErrorReservaNoEncontrada,
)
from utils.logger import obtener_logger, ARCHIVO_LOG

log = obtener_logger()


def ejecutar_operacion(numero: int, titulo: str, accion):
    """Ejecuta una operación protegida con try / except / else / finally sin detener el sistema."""
    print(f"\n[Operación {numero:02d}] {titulo}")
    try:
        resultado = accion()
    except (
        ErrorClienteInvalido,
        ErrorServicioNoDisponible,
        ErrorReservaInvalida,
        ErrorEstadoReserva,
        ErrorReservaNoEncontrada,
        ErrorCalculoCosto,
        TypeError,
        ValueError,
    ) as err:
        print(f"  ✘ Excepción controlada ({type(err)}): {err}")
        causa = getattr(err, "_" + "cause_", None)
        if causa is not None:
            print(f"    ↳ Causa encadenada: {causa}")
        log.error(f"Operación {numero:02d} ({titulo}) controlada", excepcion=err, origen="Simulacion")
    except Exception as err:
        print(f"  ✘ Error inesperado: {err}")
        log.critico(f"Operación {numero:02d} ({titulo}) fallo crítico", excepcion=err, origen="Simulacion")
    else:
        print(f"  ✔️ Éxito: {resultado}")
        log.evento(f"Operación {numero:02d} ({titulo}) exitosa -> {resultado}", origen="Simulacion")
    finally:
        print("-" * 70)


def simular_sistema():
    print("=" * 70)
    print(" 🏢 SOFTWARE C.A.D.E. - SIMULACIÓN INTEGRAL (12 OPERACIONES) ")
    print("=" * 70)
    log.evento("=== INICIO DE SIMULACIÓN SOFTWARE C.A.D.E. ===", origen="Main")

    gestor = GestorReservas()
    contexto = {}

    def op_01():
        EntidadBase("ID-001")
    ejecutar_operacion(1, "Intento de instanciar clase abstracta EntidadBase (debe fallar)", op_01)

    def op_02():
        c1 = Cliente("CLI-001", "Claudia Trujillo", "claudia@unad.edu.co", "3154445566")
        c2 = Cliente("CLI-002", "Erick Sánchez", "erick@unad.edu.co", "3109998877")
        contexto["c1"], contexto["c2"] = c1, c2
        return f"{c1.resumen()} | {c2.resumen()}"
    ejecutar_operacion(2, "Registro de clientes válidos", op_02)

    def op_03():
        return Cliente("CLI-003", "Juan Pérez", "juan@correo.com", "300123")
    ejecutar_operacion(3, "Registro de cliente con celular inválido (debe fallar)", op_03)

    def op_04():
        sala = ReservaSala("SRV-001", "Sala Ejecutiva", 50000, capacidad=12)
        equipo = AlquilerEquipo("SRV-002", "Servidor GPU", 120000, seguro=15000)
        asesoria = AsesoriaEspecializada("SRV-003", "Consultoría Cloud", 90000, area="Arquitectura")
        contexto["sala"], contexto["equipo"], contexto["asesoria"] = sala, equipo, asesoria
        return f"{sala.resumen()} | {equipo.resumen()} | {asesoria.resumen()}"
    ejecutar_operacion(4, "Creación de 3 servicios polimórficos (Sala, Equipo, Asesoría)", op_04)

    def op_05():
        return ReservaSala("SRV-ERR", "Sala Fantasma", -10000, capacidad=5)
    ejecutar_operacion(5, "Creación de servicio con tarifa negativa (debe fallar)", op_05)

    def op_06():
        r1 = Reserva("RES-001", contexto["c1"], contexto["sala"], 4)
        r2 = Reserva("RES-002", contexto["c2"], contexto["equipo"], 2)
        r3 = Reserva("RES-003", contexto["c1"], contexto["asesoria"], 3)
        for r in (r1, r2, r3):
            gestor.agregar(r)
        contexto["r1"], contexto["r2"], contexto["r3"] = r1, r2, r3
        return f"Reservas registradas: {len(gestor.listar())}"
    ejecutar_operacion(6, "Creación y almacenamiento de 3 reservas válidas", op_06)

    def op_07():
        base = contexto["r1"].calcular_total()
        con_iva = contexto["r1"].calcular_total(iva=True)
        con_desc_txt = contexto["r2"].calcular_total(iva=True, descuento="10%")
        con_desc_fijo = contexto["r3"].calcular_total(iva=0.05, descuento=10000)
        return (
            f"RES-001 Base=${base:,.2f}, IVA=${con_iva:,.2f} | "
            f"RES-002 (IVA+Desc 10%)=${con_desc_txt:,.2f} | "
            f"RES-003 (IVA 5%+Desc $10k)=${con_desc_fijo:,.2f}"
        )
    ejecutar_operacion(7, "Cálculo de costos sobrecargados (base, IVA y descuentos)", op_07)

    def op_08():
        contexto["r1"].confirmar()
        contexto["r2"].cancelar()
        return f"RES-001={contexto['r1'].estado} | RES-002={contexto['r2'].estado}"
    ejecutar_operacion(8, "Confirmación de RES-001 y cancelación de RES-002", op_08)

    def op_09():
        contexto["r1"].confirmar()
    ejecutar_operacion(9, "Re-confirmar reserva ya confirmada (debe fallar)", op_09)

    def op_10():
        return Reserva("RES-004", contexto["c1"], contexto["sala"], 15)
    ejecutar_operacion(10, "Reserva de sala por 15 horas (máximo 8h, debe fallar)", op_10)

    def op_11():
        contexto["asesoria"].disponible = False
        return Reserva("RES-005", contexto["c2"], contexto["asesoria"], 1)
    ejecutar_operacion(11, "Reserva sobre servicio deshabilitado (debe fallar)", op_11)

    def op_12():
        return gestor.buscar("RES-999")
    ejecutar_operacion(12, "Búsqueda de reserva inexistente RES-999 (debe fallar)", op_12)

    log.evento("=== FIN DE SIMULACIÓN SOFTWARE C.A.D.E. ===", origen="Main")
    print(f"\n📄 Registro histórico guardado en: {ARCHIVO_LOG}")


simular_sistema()
