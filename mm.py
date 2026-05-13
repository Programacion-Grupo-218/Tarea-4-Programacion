
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

    # =========================
    # SETTERS CON VALIDACIONES
    # =========================

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

    # =========================
    # MÉTODOS
    # =========================

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


# =========================
# PRUEBA DEL SISTEMA
# =========================

try:

    cliente1 = Cliente(
        "C001",
        "Alejandro",
        "alejandro@gmail.com",
        "3214567890"
    )

    cliente1.mostrar_cliente()

    print("\nResumen:")
    print(cliente1.obtener_resumen())

except ClienteError as e:

    print("Error en cliente:", e)

finally:

    print("\nProceso finalizado")