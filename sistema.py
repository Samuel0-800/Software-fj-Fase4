# sistema.py
# Clase que guarda todo en listas (no hay base de datos) y maneja los errores para que el programa no se caiga

from cliente import Cliente  # para crear clientes
from reserva import Reserva  # para crear reservas
from excepciones import ErrorSoftwareFJ  # la excepcion base atrapa todas las propias
from logs import registrar_log  # registro de eventos y errores


class SistemaSoftwareFJ:
    """Gestiona clientes, servicios y reservas usando listas."""

    def __init__(self):
        self.clientes = []  # lista de clientes registrados
        self.servicios = []  # lista de servicios creados
        self.reservas = []  # lista de reservas

    def registrar_cliente(self, nombre, documento, correo, telefono):
        try:  # el constructor de Cliente valida todo
            cliente = Cliente(nombre, documento, correo, telefono)  # si algo esta mal lanza ClienteInvalidoError
        except ErrorSoftwareFJ as e:  # capturo el error propio
            registrar_log("ERROR", "Registro de cliente fallido: " + str(e))  # lo guardo en el log
            print("  Error:", e)  # y lo muestro
            return None  # no se registro nada
        else:  # si no hubo error se agrega a la lista
            self.clientes.append(cliente)  # queda guardado en memoria
            registrar_log("INFO", "Cliente registrado: " + cliente.describir())  # evento en el log
            print("  Registrado:", cliente.describir())  # mensaje en consola
            return cliente  # devuelvo el objeto para usarlo despues

    def agregar_servicio(self, clase_servicio, *datos):  # recibe la clase y los datos que necesite
        try:  # crear el servicio puede fallar
            servicio = clase_servicio(*datos)  # creo el objeto de la clase que llego
        except ErrorSoftwareFJ as e:  # error de validacion del servicio
            registrar_log("ERROR", "No se creo el servicio: " + str(e))  # al log
            print("  Error:", e)  # a la consola
            return None  # no se agrego
        self.servicios.append(servicio)  # si llego aqui todo salio bien
        registrar_log("INFO", "Servicio creado: " + servicio.describir())  # registro
        print("  Creado:", servicio.describir())  # aviso
        return servicio  # lo devuelvo

    def crear_reserva(self, cliente, servicio, horas):
        try:  # la reserva valida cliente, servicio y horas
            reserva = Reserva(cliente, servicio, horas)  # puede lanzar ReservaInvalidaError
        except ErrorSoftwareFJ as e:  # error al crear la reserva
            causa = e.__cause__  # si fue encadenado aqui esta el error original
            detalle = str(e) if causa is None else str(e) + " | causa: " + str(causa)  # armo el mensaje con la causa
            registrar_log("ERROR", "Reserva fallida: " + detalle)  # al log con todo el detalle
            print("  Error:", detalle)  # tambien en pantalla
            return None  # no se creo
        self.reservas.append(reserva)  # se guarda en la lista
        registrar_log("INFO", "Reserva creada: " + reserva.describir())  # evento
        print("  Creada:", reserva.describir())  # aviso
        return reserva  # devuelvo la reserva

    def resumen(self):  # cuenta lo que quedo guardado al final
        print("Clientes registrados:", len(self.clientes))  # total de clientes
        print("Servicios creados:", len(self.servicios))  # total de servicios
        print("Reservas creadas:", len(self.reservas))  # total de reservas
        for r in self.reservas:  # recorro cada reserva
            print("  -", r.describir())  # muestro su estado final
