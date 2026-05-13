# CODIGO PRINCIPAL
# Cualquier cambio de cada integrante se pondra primero en las ramas de github, si esta correcto se hara un merge a la rama principal, y luego se subira a github, para que asi cada integrante pueda tener el codigo actualizado
# Importaciones necesarias para la interfaz gráfica y manejo de mensajes
import tkinter as tk
from tkinter import ttk, messagebox 
#Excepciones
class ReservaError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass
# Clase abstracta que represente las entidades generales del sistema
class Entidad:
    def __init__(self, id_sistema: str):
        if not id_sistema or not str(id_sistema).strip():
            raise ValueError("El ID es obligatorio para crear una entidad")
        self._id_sistema = str(id_sistema).strip()

    @property
    def id_sistema(self):
        return self._id_sistema

    def obtener_resumen(self):
        raise NotImplementedError("Método abstracto: implementar en subclase")


# Clase cliente con validacion robusta y encapsulacion de datos personales
class ClienteError(Exception):
    pass


class NombreInvalidoError(ClienteError):
    pass


class CorreoInvalidoError(ClienteError):
    pass


class TelefonoInvalidoError(ClienteError):
    pass

class Entidad:

    def __init__(self, id_sistema: str):

        if not id_sistema or not str(id_sistema).strip():
            raise ValueError(
                "El ID es obligatorio"
            )

        self._id_sistema = str(id_sistema).strip()

    @property
    def id_sistema(self):
        return self._id_sistema

    def obtener_resumen(self):
        raise NotImplementedError(
            "Debe implementarse en la subclase"
        )

class Cliente(Entidad):

    def __init__(
        self,
        id_cliente,
        nombre,
        correo,
        telefono=""
    ):

        # Herencia
        super().__init__(id_cliente)

        # Encapsulación
        self._nombre = None
        self._correo = None
        self._telefono = None

        self._reservas = []

        # Validaciones usando setters
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    @property
    def nombre(self):
        return self._nombre

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def set_nombre(self, nombre):

        try:

            if not nombre.strip():
                raise NombreInvalidoError(
                    "El nombre no puede estar vacío"
                )

            if len(nombre.strip()) < 3:
                raise NombreInvalidoError(
                    "El nombre debe tener mínimo 3 caracteres"
                )

            self._nombre = nombre.strip()

        except NombreInvalidoError as e:
            self.registrar_error(e)
            raise

    def set_correo(self, correo):

        try:

            if "@" not in correo or "." not in correo:
                raise CorreoInvalidoError(
                    "Correo electrónico inválido"
                )

            self._correo = correo.strip()

        except CorreoInvalidoError as e:
            self.registrar_error(e)
            raise

    def set_telefono(self, telefono):

        try:

            if telefono != "":

                if not telefono.isdigit():
                    raise TelefonoInvalidoError(
                        "El teléfono solo debe contener números"
                    )

                if len(telefono) < 7:
                    raise TelefonoInvalidoError(
                        "Número telefónico demasiado corto"
                    )

            self._telefono = telefono.strip()

        except TelefonoInvalidoError as e:
            self.registrar_error(e)
            raise
        
    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)

    def obtener_resumen(self):

        return (
            f"Cliente: {self._nombre} | "
            f"Correo: {self._correo} | "
            f"Reservas: {len(self._reservas)}"
        )

    def mostrar_cliente(self):

        print("===== CLIENTE =====")
        print(f"ID: {self.id_sistema}")
        print(f"Nombre: {self._nombre}")
        print(f"Correo: {self._correo}")
        print(f"Teléfono: {self._telefono}")

    def registrar_error(self, error):

        try:

            with open(
                "logs.txt",
                "a",
                encoding="utf-8"
            ) as archivo:

                archivo.write(
                    f"ERROR: {error}\n"
                )

        except Exception as e:
            print(
                "No se pudo registrar el error:",
                e
            )

try:

    cliente1 = Cliente() 
  

    cliente1.mostrar_cliente()

    print("\nResumen:")
    print(cliente1.obtener_resumen())
except Exception as e:
    print("Error en cliente:", e)

print("\nProceso finalizado")
    
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

class Reserva(Entidad):
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion):
        super().__init__(id_reserva)
        if not cliente or not servicio:
            raise ValueError("Cliente y servicio son obligatorios")
        
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
            log_event(f"Procesando reserva {self.id_sistema} - {self.cliente.nombre}")
            self.servicio.validar_parametros(self.duracion)
            self._costo_total = self.servicio.calcular_costo(self.duracion)
            log_event(f"Reserva procesada correctamente. Costo base: ${self._costo_total}")
        except Exception as e:
            log_error(e, f"Procesando reserva {self.id_sistema}")
            raise

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise ReservaError("Solo reservas en estado PENDIENTE pueden confirmarse")
        self._estado = "CONFIRMADA"
        log_event(f"Reserva {self.id_sistema} CONFIRMADA")

    def cancelar(self):
        self._estado = "CANCELADA"
        log_event(f"Reserva {self.id_sistema} CANCELADA")

    # MÉTODO SOBRECARGADO (movido dentro de la clase)
    def calcular_total(self, impuesto: float = 0.0, descuento: float = 0.0):
        total = self._costo_total
        if impuesto > 0:
            total += (total * impuesto)
        if descuento > 0:
            total -= descuento
        return round(total, 2)

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
# Interfaz con tkinter
class SistemaReservasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Software FJ - Sistema Integral de Reservas")
        self.root.geometry("720x780")
        self.root.configure(bg="#f0f0f0")

        self.reservas = []
        self.clientes = []

        self.servicios = [
            ServicioSala("S-001", "Auditorio Principal", 95000, 80),
            ServicioAlquilerEquipo("E-045", "Laptop Dell XPS", 45000, 12000),
            ServicioAsesoria("A-078", "Inteligencia Artificial", 180000, 65000),
        ]
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="SOFTWARE FJ - GESTIÓN INTEGRAL", 
                 font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)

        frame = tk.LabelFrame(self.root, text="Nueva Reserva", padx=20, pady=15, bg="#f0f0f0")
        frame.pack(padx=30, pady=10, fill="x")

        tk.Label(frame, text="Nombre Cliente:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=8)
        self.ent_nombre = tk.Entry(frame, width=45)
        self.ent_nombre.grid(row=0, column=1, pady=8, padx=10)

        tk.Label(frame, text="ID Cliente:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=8)
        self.ent_id = tk.Entry(frame, width=45)
        self.ent_id.grid(row=1, column=1, pady=8, padx=10)

        tk.Label(frame, text="Servicio:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=8)
        self.combo = ttk.Combobox(frame, values=[s.describir() for s in self.servicios], 
                                  state="readonly", width=60)
        self.combo.grid(row=2, column=1, pady=8, padx=10)
        self.combo.bind("<<ComboboxSelected>>", self.actualizar_unidad_duracion)

        tk.Label(frame, text="Duración:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=8)
        dur_frame = tk.Frame(frame, bg="#f0f0f0")
        dur_frame.grid(row=3, column=1, sticky="w", pady=8, padx=10)
        
        self.ent_dur = tk.Entry(dur_frame, width=15)
        self.ent_dur.pack(side="left")
        
        self.lbl_unidad = tk.Label(dur_frame, text=" horas", bg="#f0f0f0", fg="blue", font=("Arial", 10))
        self.lbl_unidad.pack(side="left", padx=8)

        tk.Button(self.root, text="REGISTRAR RESERVA", bg="#28a745", fg="white",
                  font=("Arial", 12, "bold"), command=self.registrar, height=2).pack(pady=20)

        tk.Label(self.root, text="Historial de Reservas", bg="#f0f0f0", 
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=30, pady=(10,5))
        
        self.monitor = tk.Text(self.root, height=18, font=("Consolas", 10))
        self.monitor.pack(padx=30, pady=5, fill="both", expand=True)

        tk.Button(self.root, text="Probar Error (Duración Inválida)", 
                  command=self.probar_error).pack(pady=8)
# Actualiza la unidad de duración según el servicio seleccionado
    def actualizar_unidad_duracion(self, event=None):
        try:
            indice = self.combo.current()
            if indice == -1:
                return
            servicio = self.servicios[indice]
            if isinstance(servicio, ServicioAlquilerEquipo):
                self.lbl_unidad.config(text=" días", fg="blue")
            else:
                self.lbl_unidad.config(text=" horas", fg="blue")
        except:
            self.lbl_unidad.config(text=" horas", fg="blue")
# Registra la reserva con validación y manejo de excepciones, mostrando el resultado en el monitor y con mensajes emergentes.
    def registrar(self):
        try:
            nombre = self.ent_nombre.get().strip()
            id_cliente = self.ent_id.get().strip()

            # Validar caracteres en el nombre y ID
            if not nombre:
                raise ValueError("El nombre del cliente es obligatorio")
            
            # Solo letras y espacios en el nombre
            if not nombre.replace(" ", "").isalpha():
                raise ValueError("El nombre solo puede contener letras y espacios")

            # ID Cliente: Solo números
            if not id_cliente:
                raise ValueError("El ID del cliente es obligatorio")
            if not id_cliente.isdigit():
                raise ValueError("El ID del cliente solo puede contener números")
            if len(id_cliente) < 5:
                raise ValueError("El ID debe tener al menos 5 dígitos")

            if self.combo.current() == -1:
                raise ValueError("Debe seleccionar un servicio")

            # Crear cliente
            cliente = Cliente(id_cliente, nombre, "cliente@unad.edu.co")
            self.clientes.append(cliente)

            # Obtener servicio y duración
            servicio = self.servicios[self.combo.current()]
            duracion = float(self.ent_dur.get())

            # Crear reserva
            id_reserva = f"R-{len(self.reservas)+1001}"
            res = Reserva(id_reserva, cliente, servicio, duracion)
            
            res.procesar_reserva()
            res.confirmar()

            total = res.calcular_total(impuesto=0.19)
            self.reservas.append(res)

            # Mostrar en el monitor
            info = f"✅ RESERVA EXITOSA #{res.id_sistema}\n"
            info += f"Cliente : {cliente.nombre}\n"
            info += f"ID      : {id_cliente}\n"
            info += f"Servicio: {servicio._nombre}\n"
            info += f"Duración: {duracion} {'días' if isinstance(servicio, ServicioAlquilerEquipo) else 'horas'}\n"
            info += f"Total   : ${total:,.0f}\n"
            info += f"Estado  : {res.estado}\n"
            info += "-"*60 + "\n\n"

            self.monitor.insert(tk.END, info)
            self.monitor.see(tk.END)

            messagebox.showinfo("Éxito", "Reserva registrada correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}")
# Método para probar el manejo de errores al procesar una reserva con parámetros inválidos.
    def probar_error(self):
        try:
            cliente = Cliente("C-999", "Test Error", "test@unad.edu.co")
            servicio = self.servicios[0]
            res = Reserva("R-ERROR", cliente, servicio, -5)
            res.procesar_reserva()
        except Exception as e:
            messagebox.showerror("Error Controlado", f"Excepción capturada correctamente:\n{str(e)}")
# Método para iniciar el loop de la interfaz gráfica.
    def run(self):
        self.root.mainloop()


# Ejecución del programa
if __name__ == "__main__":
    pruebas_sistema()
    app = SistemaReservasGUI()
    app.run()