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
class Servicio:
    """Clase abstracta Servicio"""
    
    def __init__(self, id_servicio, nombre, precio_base):
        if not id_servicio or not nombre or precio_base <= 0:
            raise ValidacionError("ID, nombre y precio_base > 0 son obligatorios")
        self._id = id_servicio
        self._nombre = nombre
        self._precio_base = precio_base
        self._disponible = True

    @property
    def id(self): return self._id
    @property
    def nombre(self): return self._nombre

    def calcular_costo(self, duracion):
        raise NotImplementedError("Método abstracto: implementar en clase hija")

    def describir(self):
        raise NotImplementedError("Método abstracto: implementar en clase hija")

    def validar_parametros(self, duracion):
        raise NotImplementedError("Método abstracto: implementar en clase hija")


# Una clase Reserva que integre cliente, servicio, duración y estado, e implemente confirmación, cancelación y procesamiento con manejo de excepciones.
class Reserva(Entidad, Servicio):

# Métodos sobrecargados (por ejemplo, diferentes variantes del cálculo de costos con impuestos, descuentos o parámetros opcionales).

# Un archivo de logs donde se registren todos los errores y eventos relevantes.
contador_logs = 0
LOG_FILE = "sistema_reservas.log"

def log_event(message, level="INFO"):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{level}] {message}\n")
    except:
        pass

def log_error(error, context=""):
    try:
        log_event(f"ERROR - {context}: {type(error).__name__} - {str(error)}", "ERROR")
    except:
        pass

# Interfaz con tkinter y main() 

if __name__ == "__main__":
    app = SistemaReservasGUI()
    app.run()