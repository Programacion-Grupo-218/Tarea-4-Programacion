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
import tkinter as tk
from tkinter import messagebox, ttk

# Clases de bases 
class Entidad:
    def __init__(self, id_entidad):
        self.id_entidad = id_entidad

class Cliente(Entidad):
    def __init__(self, id_cliente, nombre, correo):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
    
    def __str__(self):
        return f"{self.nombre} (ID: {self.id_entidad})"

class ReservaError(Exception):
    pass

# logica de servicio 
class Servicio:
    def __init__(self, id_servicio: str, nombre: str, precio_base: float):
        if not id_servicio or not nombre or precio_base <= 0:
            raise ValueError("ID, nombre y precio_base > 0 son obligatorios")
        self._id = id_servicio
        self._nombre = nombre
        self._precio_base = precio_base

    def calcular_costo(self, duracion):
        raise NotImplementedError("Implementar en clase hija")

    def describir(self):
        raise NotImplementedError("Implementar en clase hija")

    def validar_parametros(self, duracion):
        raise NotImplementedError("Implementar en clase hija")

class ServicioSala(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, capacidad: int):
        super().__init__(id_servicio, nombre, precio_base)
        self.capacidad = capacidad

    def validar_parametros(self, horas: float):
        if horas <= 0 or horas > 24:
            raise ValueError("La duración debe estar entre 0.1 y 24 horas")
        return True

    def calcular_costo(self, horas: float):
        self.validar_parametros(horas)
        costo = self._precio_base * horas
        if horas > 8: costo *= 0.9  # Descuento 10%
        return round(costo, 2)

    def describir(self):
        return f"SALA: {self._nombre} (${self._precio_base}/hr)"

class ServicioAlquilerEquipo(Servicio):
    def __init__(self, id_servicio, nombre, precio_base, precio_por_dia_extra: float = 0):
        super().__init__(id_servicio, nombre, precio_base)
        self.precio_por_dia_extra = precio_por_dia_extra

    def validar_parametros(self, dias: int):
        if dias < 1: raise ValueError("Mínimo 1 día de alquiler")
        return True

    def calcular_costo(self, dias: int):
        self.validar_parametros(dias)
        costo = self._precio_base + (max(0, int(dias) - 1) * self.precio_por_dia_extra)
        return round(costo, 2)

    def describir(self):
        return f"EQUIPO: {self._nombre} (${self._precio_base} base)"

# Clase de reserva 
class Reserva(Entidad):
    def __init__(self, cliente, servicio, duracion):
        super().__init__(id_entidad=f"RES-{cliente.id_entidad}")
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
            log_event(f"Procesando: {self.cliente.nombre}")
            self.servicio.validar_parametros(self.duracion)
            self._costo_total = self.servicio.calcular_costo(self.duracion)
        except Exception as e:
            log_error(e, "Procesamiento")
            raise ReservaError(str(e))

    def confirmar(self):
        if self._estado == "PENDIENTE":
            self._estado = "CONFIRMADA"
            log_event(f"Reserva {self.id_entidad} CONFIRMADA")

    def calcular_total(self, impuesto: float = 0.0, descuento: float = 0.0):
        total = self._costo_total
        if impuesto > 0: total += (total * impuesto)
        if descuento > 0: total -= descuento
        return round(total, 2)

# Sistema de logs 
LOG_FILE = "sistema_reservas.log"
def log_event(msg, level="INFO"):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{level}] {msg}\n")
    except: pass

def log_error(err, context=""):
    log_event(f"{context}: {type(err).__name__} - {str(err)}", "ERROR")

# Interfaz grafica 
class SistemaReservasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JimmyAvella - Gestión de Reservas UNAD")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        self.servicios = [
            ServicioSala("S01", "Auditorio Central", 80000, 50),
            ServicioAlquilerEquipo("E01", "Portátil Dell", 25000, 10000),
            ServicioSala("S02", "Sala de Cómputo", 45000, 20)
        ]
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="SISTEMA DE RESERVAS", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

        # Frame de Datos
        f = tk.Frame(self.root, bg="#f0f0f0")
        f.pack(padx=20, fill="x")

        tk.Label(f, text="Nombre del Cliente:", bg="#f0f0f0").pack(anchor="w")
        self.ent_nombre = tk.Entry(f); self.ent_nombre.pack(fill="x", pady=2)

        tk.Label(f, text="ID / Cédula:", bg="#f0f0f0").pack(anchor="w")
        self.ent_id = tk.Entry(f); self.ent_id.pack(fill="x", pady=2)

        tk.Label(f, text="Seleccione Servicio:", bg="#f0f0f0").pack(anchor="w", pady=(10,0))
        self.combo = ttk.Combobox(f, values=[s.describir() for s in self.servicios], state="readonly")
        self.combo.pack(fill="x", pady=2)

        tk.Label(f, text="Duración (Horas o Días):", bg="#f0f0f0").pack(anchor="w")
        self.ent_dur = tk.Entry(f); self.ent_dur.pack(fill="x", pady=2)

        # Botón
        tk.Button(self.root, text="REGISTRAR Y CONFIRMAR", bg="#28a745", fg="white", 
                  font=("Arial", 10, "bold"), command=self.registrar, height=2).pack(pady=20)

        # Monitor
        tk.Label(self.root, text="Historial de esta sesión:", bg="#f0f0f0").pack()
        self.monitor = tk.Text(self.root, height=12, width=55, font=("Consolas", 9))
        self.monitor.pack(padx=20, pady=5)

    def registrar(self):
        try:
            if not self.ent_nombre.get() or self.combo.current() == -1:
                raise ValueError("Faltan datos obligatorios")

            cliente = Cliente(self.ent_id.get(), self.ent_nombre.get(), "user@unad.edu.co")
            servicio = self.servicios[self.combo.current()]
            duracion = float(self.ent_dur.get())

            # Lógica de Reserva
            res = Reserva(cliente, servicio, duracion)
            res.procesar_reserva()
            res.confirmar()
            
            total_con_iva = res.calcular_total(impuesto=0.19)
            
            # Mostrar resultado
            info = f" EXITOSO: {cliente.nombre}\n   Servicio: {servicio._nombre}\n   Pago Total: ${total_con_iva}\n   Estado: {res.estado}\n"
            info += "-"*45 + "\n"
            self.monitor.insert(tk.END, info)
            self.monitor.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Verifique los datos: {e}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SistemaReservasGUI()
    app.run()