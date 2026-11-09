# 🏢 SOFTWARE C.A.D.E. - SISTEMA INTEGRAL INTERACTIVO
**UNIVERSIDAD NACIONAL ABIERTA Y A DISTANCIA (UNAD)**  
**Curso:** Programación (Código 213023) - Unidad 2 - Paso 4: Laboratorio POO  

Este proyecto consiste en un software integral de gestión de clientes, servicios y reservas que opera al 100% mediante interfaz interactiva por terminal (CMD / PowerShell). Aplica principios avanzados de Programación Orientada a Objetos (POO) y un sistema robusto de control de excepciones encadenadas.

---

## 👥 Distribución Oficial de Roles y Componentes

1. **Claudia Trujillo (Autora de la Base):**
   * **Entidad Abstracta:** Modelado e implementación de `EntidadBase` en el módulo de entidades.
   * **Clase Cliente:** Aplicación de encapsulación estricta mediante atributos privados (`__`) y filtros de validación de datos personales con decoradores `@property` y `.setter` (Longitud estricta de celular para telefonía en Colombia).

2. **Erick Sánchez:**
   * **Clase Abstracta Servicio:** Diseño y estructura general del módulo de servicios.
   * **Especializaciones Polimórficas:** Implementación de las clases hijas `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
   * **Arquitectura:** Coordinación general de la estructura del sistema.

3. **Alejandro Gómez (Alejo):**
   * **Sobrecarga de Métodos:** Desarrollo de algoritmos de cálculo de costos base, adición de impuestos (IVA) y aplicación de descuentos.
   * **Sistema de Registro:** Módulo `logger.py` para el control y almacenamiento histórico de eventos y errores en un archivo de texto plano.

4. **Daniel David Escobar Reina:**
   * **Clase Reserva:** Integración y cohesión final de clientes, servicios, duraciones y control de estados.
   * **Manejo de Excepciones:** Flujo de ejecución interactivo protegido por bloques `try / except / else / finally` y excepciones encadenadas.
   * **Capa de Persistencia:** Módulo `GestorReservas` para administración de datos en memoria local.

---

## 📁 Estructura del Proyecto

*   `entidades/`: Contiene las plantillas abstractas y los modelos del negocio (`entidad_base.py`, `cliente.py`, etc.).
*   `utils/`: Módulos para herramientas de soporte, excepciones personalizadas (`excepciones.py`) y registro de logs.
*   `Proyecto C.A.D.E.PY`: Script de inicialización principal del sistema y menú de consola interactivo.

---

## 🚀 Instrucciones de Uso y Validación (Fase Inicial)

El componente desarrollado por **Claudia Trujillo** cuenta con estabilidad absoluta y pruebas automatizadas. Para validar el funcionamiento de las propiedades encapsuladas y el control de excepciones independiente, ejecute en la terminal:

```bash
python "Proyecto C.A.D.E.PY"
```
