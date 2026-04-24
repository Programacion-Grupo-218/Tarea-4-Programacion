# CODIGO PRINCIPAL
# Cualquier cambio de cada integrante se pondra primero en las ramas de github, si esta correcto se hara un merge a la rama principal,
# y luego se subira a github, para que asi cada integrante pueda tener el codigo actualizado
import tkinter as tk
from tkinter import messagebox

# Clase abstracta que represente las entidades generales del sistema
class Entidad:


# Clase cliente con validacion robusta y encapsulacion de datos personales
class Cliente(Entidad):


# Clase abstracta al servicio, y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar parámetros.
class Servicio(Entidad):


# Una clase Reserva que integre cliente, servicio, duración y estado, e implemente confirmación, cancelación y procesamiento con manejo de excepciones.
class Reserva:

# Métodos sobrecargados (por ejemplo, diferentes variantes del cálculo de costos con impuestos, descuentos o parámetros opcionales).

# Logs y pruebas
# Interfaz con tkinter y main() 