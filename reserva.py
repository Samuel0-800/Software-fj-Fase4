# reserva.py
# Clase Reserva: une un cliente, un servicio y la duracion en horas

from entidad import Entidad  # la reserva tambien hereda de Entidad
from cliente import Cliente  # para revisar que el cliente sea de verdad un Cliente
from servicios import Servicio  # lo mismo con el servicio
from excepciones import (ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError, CalculoInvalidoError)  # errores que se usan aqui
from logs import registrar_log  # para dejar registro de cada paso


class Reserva(Entidad):  # herencia de la clase abstracta
    """Reserva de un servicio. Estados: pendiente, confirmada, cancelada, procesada."""

    def __init__(self, cliente, servicio, horas):
        if not isinstance(cliente, Cliente):  # si falta el cliente o mandan otra cosa
            raise ReservaInvalidaError("La reserva necesita un cliente valido")  # no se puede crear
        if not isinstance(servicio, Servicio):  # lo mismo para el servicio
            raise ReservaInvalidaError("La reserva necesita un servicio valido")  # error
        try:  # las horas las valida cada servicio segun sus reglas
            servicio.validar_parametros(horas)  # puede lanzar ValueError o TypeError
        except (ValueError, TypeError) as e:  # capturo el error original
            raise ReservaInvalidaError("No se pudo crear la reserva: horas no validas") from e  # encadenamiento, se conserva la causa
        self.cliente = cliente  # quien reserva
        self.servicio = servicio  # que reserva
        self.horas = horas  # cuanto tiempo
        self.estado = "pendiente"  # toda reserva arranca pendiente
        self.costo = None  # el costo se calcula al procesar
        super().__init__()  # id de la reserva, solo si paso todas las validaciones

    def confirmar(self):  # pasa de pendiente a confirmada
        if self.estado != "pendiente":  # solo se confirma lo que esta pendiente
            raise OperacionNoPermitidaError("No se puede confirmar una reserva " + self.estado)  # error de estado
        if not self.servicio.disponible:  # el servicio puede estar ocupado o en mantenimiento
            raise ServicioNoDisponibleError("El servicio '" + self.servicio.nombre + "' no esta disponible")  # no se confirma
        self.estado = "confirmada"  # cambio de estado
        registrar_log("INFO", "Reserva " + str(self.id) + " confirmada")  # queda en el log

    def cancelar(self):  # cancela si todavia se puede
        if self.estado in ("cancelada", "procesada"):  # ya no tiene sentido cancelar
            raise OperacionNoPermitidaError("No se puede cancelar una reserva " + self.estado)  # operacion no permitida
        self.estado = "cancelada"  # se cancela
        registrar_log("INFO", "Reserva " + str(self.id) + " cancelada")  # registro

    def procesar(self, impuesto=None, descuento=None):  # calcula el cobro y cierra la reserva
        if self.estado != "confirmada":  # primero hay que confirmarla
            raise OperacionNoPermitidaError("Solo se procesan reservas confirmadas, esta esta " + self.estado)  # error
        try:  # el calculo puede fallar por impuesto o descuento malo
            total = self.servicio.calcular_costo(self.horas, impuesto, descuento)  # polimorfismo: cada servicio calcula distinto
        except CalculoInvalidoError as e:  # si el calculo no cuadra
            raise ReservaInvalidaError("No se pudo procesar la reserva " + str(self.id)) from e  # encadeno con la causa
        else:  # solo entra aqui si no hubo error
            self.costo = total  # guardo el costo final
            self.estado = "procesada"  # la reserva queda cerrada
            registrar_log("INFO", "Reserva " + str(self.id) + " procesada por $" + str(total))  # registro del cobro
        finally:  # esto se ejecuta siempre, salga bien o mal
            registrar_log("INFO", "Intento de procesar la reserva " + str(self.id) + " terminado")  # queda constancia del intento
        return self.costo  # devuelvo el valor cobrado

    def describir(self):  # resumen de la reserva
        return ("Reserva " + str(self.id) + ": " + self.cliente.nombre + " - " + self.servicio.nombre
                + " (" + str(self.horas) + " h) estado " + self.estado)  # texto con los datos principales
