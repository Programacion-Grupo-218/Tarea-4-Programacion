# CODIGO PRINCIPAL
# Cualquier cambio de cada integrante se pondra primero en las ramas de github, si esta correcto se hara un merge a la rama principal,
# y luego se subira a github, para que asi cada integrante pueda tener el codigo actualizado
import tkinter as tk
from tkinter import messagebox

# Clase abstracta que represente las entidades generales del sistema
class Entidad:
#Clase abstracta del sistema

    def __init__(self, id_sistema: str):
        # Validación de parámetros: Asegura que la entidad no se cree sin un ID
        if not id_sistema:
            raise ValueError("El ID del sistema es obligatorio para crear una entidad")
        self._id_sistema = id_sistema

    @property
    def id_sistema(self):
    #Para obtener el Id de forma controlada
        return self._id_sistema

    def obtener_resumen(self):
    #Método para implementar el poliformismo
        raise NotImplementedError("Error: El método 'obtener_resumen' debe ser implementado por la clase hija.")



# Clase cliente con validacion robusta y encapsulacion de datos personales
class Cliente(Entidad):


# Clase abstracta al servicio, y al menos tres servicios especializados que hereden de ella, implementando polimorfismo y métodos sobrescritos para calcular costos, describir servicios y validar parámetros.
class Servicio:
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
        return f"Sala '{self._nombre}' - ${self._precio_base}/hora (Cap: {self.capacidad} personas)"


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
        return f"{self._nombre} - ${self._precio_base} (primer día) + ${self.precio_por_dia_extra}/día extra"


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
        return f"Asesoría '{self._nombre}' - Base ${self._precio_base} + tarifa experto"

 
#Clase Reserva 
class Reserva(Entidad, Servicio):     #para los fallos en el módulo de reservas 
    pass 

class Reserva(Entidad):
    def __init__(self,cliente, servicio, duracion):
        if not cliente or not servicio:
            raise ValueError("Se requiere un cliente y un servicio para la reserva.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

@property
def estado(self):
    return self._estado

def procesar_reserva(self):
    try:
        log_event(f"Procesando reserva: Cliente {self.cliente}")
        
        self.servicio.validar_parametros(self.duracion)
        self._costo_total = self.servicio.calcular_costo(self.duracion)

        log_event(f"Reserva procesada. Costo base: ${self._costo_total}")
    except (ValueError, TypeError) as e:
        log_error(e, "Error de validacion en reserva")
        raise ReservaError(f"Datos de reserva invalidos: {e}")
    except Exception as e:
        log_error(e, "Error critico no identificado")
        raise

def confirmar(self):
    if self._estado == "PENDIENTE"
        self._estado = "CONFIRMADA"
        log_event( "Reserva confirmada exitosamente")
    else:
        log_error("No se pudo confirmar: La reserva no esta pendiente")

def cancelar(self):
    try:
        self._estado = "CANCELADA"
        log_event("Reserva cancelada")
    finally:
        print(f"Log: Finalizado proceso de cancelacion para {self.cliente}")

#métodos sobrecargados 
def calcular_total(self, impuesto: float = 0.0, descuento : float = 0.0):
    total = self._costo_total
    if impuesto > 0:
        total += (total * impuesto)
    if descuento > 0:
        total -=descuento
    return round(total, 2)
    
            
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
