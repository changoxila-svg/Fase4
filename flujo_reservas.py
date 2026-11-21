"""
==============================================================================
MÓDULO: flujo_reservas.py
AUTOR: Daniel David Escobar Reina (Rol: Manejo de excepciones)
DESCRIPCIÓN: Menú interactivo de reservas protegido con try / except / else /
             finally y excepciones encadenadas. Registra eventos y errores
             con el logger de Alejandro Gómez.
==============================================================================
"""
from entidades.reserva import Reserva
from utils.excepciones import ErrorReservaInvalida, ErrorReservaNoEncontrada

# El logger de Alejo puede quedar en utils/logger.py o en entidades/log.py
try:
    from utils.logger import obtener_logger
except ImportError:
    from entidades.log import obtener_logger

log = obtener_logger()


def _pedir_de_diccionario(diccionario: dict, etiqueta: str):
    clave = input(f"ID de {etiqueta}: ").strip()
    try:
        return diccionario[clave]
    except KeyError as err:
        raise ErrorReservaInvalida(f"No existe {etiqueta} con ID '{clave}'.") from err


def menu_reservas(gestor, clientes: dict, servicios: dict):
    """clientes y servicios son diccionarios {id: objeto}."""
    log.evento("Módulo de reservas iniciado", origen="Reserva")

    while True:
        print("\n===== MENÚ DE RESERVAS =====")
        print("1. Crear reserva")
        print("2. Confirmar reserva")
        print("3. Cancelar reserva")
        print("4. Listar reservas")
        print("5. Calcular total de una reserva")
        print("6. Salir")
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                id_reserva = input("ID de la nueva reserva: ").strip()
                cliente = _pedir_de_diccionario(clientes, "cliente")
                servicio = _pedir_de_diccionario(servicios, "servicio")
                duracion = input("Duración (horas, días o sesiones según el servicio): ")
                reserva = Reserva(id_reserva, cliente, servicio, duracion)
                gestor.agregar(reserva)
                log.evento(f"Reserva creada: {reserva}", origen="Reserva")
            elif opcion == "2":
                reserva = gestor.buscar(input("ID de la reserva: ").strip())
                reserva.confirmar()
                log.evento(f"Reserva confirmada: {reserva.id_reserva}", origen="Reserva")
            elif opcion == "3":
                reserva = gestor.buscar(input("ID de la reserva: ").strip())
                reserva.cancelar()
                log.evento(f"Reserva cancelada: {reserva.id_reserva}", origen="Reserva")
            elif opcion == "4":
                reservas = gestor.listar()
                if not reservas:
                    print("  (no hay reservas registradas)")
                for r in reservas:
                    print(" ", r)
            elif opcion == "5":
                reserva = gestor.buscar(input("ID de la reserva: ").strip())
                print(f"  Total a pagar: ${reserva.calcular_total():,.2f}")
            elif opcion == "6":
                print("Saliendo del módulo de reservas...")
                break
            else:
                raise ErrorReservaInvalida(f"Opción '{opcion}' no válida.")
        except (ErrorReservaInvalida, ErrorReservaNoEncontrada) as err:
            print(f"  ✘ [ERROR]: {err}")
            if err.__cause__ is not None:
                print(f"    Causa original: {err.__cause__!r}")
            log.error("Operación de reserva fallida", excepcion=err, origen="Reserva")
        except Exception as err:  # noqa: BLE001 - error imprevisto: el menú no se cae
            print(f"  ✘ [ERROR INESPERADO]: {err}")
            log.critico("Error inesperado en el menú de reservas", excepcion=err, origen="Reserva")
        else:
            print("  ✔ Operación completada.")
        finally:
            print("-" * 40)
