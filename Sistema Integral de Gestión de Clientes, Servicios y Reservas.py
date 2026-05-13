# CODIGO PRINCIPAL
# Cualquier cambio de cada integrante se pondra primero en las ramas de github, si esta correcto se hara un merge a la rama principal,
# y luego se subira a github, para que asi cada integrante pueda tener el codigo actualizado
import tkinter as tk
from tkinter import messagebox
#Excepciones
class ReservaError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass
# Clase abstracta que represente las entidades generales del sistema
class Entidad:


# Clase cliente con validacion robusta y encapsulacion de datos personales
class Cliente(Entidad):


# Clase abstracta al servicio, y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar parámetros.
class Servicio(Entidad):
# Clase asbtracta del servicio
    
    def __init__(self, id_servicio: str, nombre: str, precio_base: float):
        if not id_servicio or not nombre or precio_base <= 0:
            raise ValueError("ID, nombre y precio_base > 0 son obligatorios")
        
        self._id = id_servicio
        self._nombre = nombre
        self._precio_base = precio_base

    def calcular_costo(self, duracion):
        raise NotImplementedError("Método abstracto: implementar en clase hija")

    def describir(self):
        raise NotImplementedError("Método abstracto: implementar en clase hija")

    def validar_parametros(self, duracion):
        raise NotImplementedError("Método abstracto: implementar en clase hija")

# 3 SERVICIOS

class ServicioSala(Servicio):
    
    def __init__(self, id_servicio, nombre, precio_base, capacidad: int):
        super().__init__(id_servicio, nombre, precio_base)
        self.capacidad = capacidad

    def validar_parametros(self, horas: float):
        if horas <= 0 or horas > 24:
            raise ValueError("La duración debe estar entre 0 y 24 horas")
        return True

    def calcular_costo(self, horas: float):
        self.validar_parametros(horas)
        costo = self._precio_base * horas
        if horas > 8:                    # Descuento por día completo
            costo *= 0.9
        return round(costo, 2)

    def describir(self):
        return f"SALA: {self._nombre.upper()} - ${self._precio_base:,}/hora (Cap: {self.capacidad} personas)"

class ServicioAlquilerEquipo(Servicio):
    
    def __init__(self, id_servicio, nombre, precio_base, precio_por_dia_extra: float = 0):
        super().__init__(id_servicio, nombre, precio_base)
        self.precio_por_dia_extra = precio_por_dia_extra

    def validar_parametros(self, dias: int):
        if dias < 1:
            raise ValueError("El alquiler debe ser de al menos 1 día")
        return True

    def calcular_costo(self, dias: int):
        self.validar_parametros(dias)
        costo = self._precio_base + (max(0, dias - 1) * self.precio_por_dia_extra)
        return round(costo, 2)

    def describir(self):
        return f"ALQUILER: {self._nombre.upper()} - ${self._precio_base:,} (primer día) + ${self.precio_por_dia_extra:,}/día extra"


class ServicioAsesoria(Servicio):
    
    def __init__(self, id_servicio, nombre, precio_base, tarifa_hora_experto: float):
        super().__init__(id_servicio, nombre, precio_base)
        self.tarifa_hora_experto = tarifa_hora_experto

    def validar_parametros(self, horas: float):
        if horas < 1 or horas > 12:
            raise ValueError("La asesoría debe durar entre 1 y 12 horas")
        return True

    def calcular_costo(self, horas: float):
        self.validar_parametros(horas)
        costo = (self._precio_base * horas) + (horas * self.tarifa_hora_experto)
        return round(costo, 2)

    def describir(self):
        return f"ASESORÍA: {self._nombre.upper()} - Base ${self._precio_base:,} + tarifa experto"


# Una clase Reserva que integre cliente, servicio, duración y estado, e implemente confirmación, cancelación y procesamiento con manejo de excepciones.
class Reserva(Entidad, Servicio):

# Métodos sobrecargados (por ejemplo, diferentes variantes del cálculo de costos con impuestos, descuentos o parámetros opcionales).

# Un archivo de logs donde se registren todos los errores y eventos relevantes.
# Logs y pruebas
# LOGS
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
# PRUEBAS
def pruebas_sistema():
    print("INICIANDO PRUEBAS DEL SISTEMA\n")
    log_event("Iniciando pruebas del sistema")
    
    try:
        c1 = Cliente("C001", "Jimmy Avella", "jimmy@unad.edu.co")
        c2 = Cliente("C002", "Diana Marcela", "diana@unad.edu.co")
        
        s1 = ServicioSala("S01", "Auditorio", 80000, 50)
        s2 = ServicioAlquilerEquipo("E01", "Laptop", 25000, 8000)
        s3 = ServicioAsesoria("A01", "Python", 120000, 45000)
        
        # Reservas exitosas
        r1 = Reserva("R001", c1, s1, 10)
        r1.procesar_reserva()
        r1.confirmar()
        
        r2 = Reserva("R002", c2, s2, 3)
        r2.procesar_reserva()
        r2.confirmar()
        
        # Prueba con error (para demostrar manejo de excepciones)
        try:
            r3 = Reserva("R003", c1, s3, 0)   # duración inválida
            r3.procesar_reserva()
        except Exception as e:
            print(f"Error controlado correctamente: {e}")
        
        print("Pruebas completadas. Sistema estable.")
        
    except Exception as e:
        log_error(e, "Pruebas del sistema")

# Interfaz con tkinter y main() 

if __name__ == "__main__":
    app = SistemaReservasGUI()
    app.run()
