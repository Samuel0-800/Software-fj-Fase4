# cliente.py
# Clase Cliente con los datos personales encapsulados y validados

from entidad import Entidad  # Cliente hereda de la clase abstracta
from excepciones import ClienteInvalidoError  # error propio para datos malos


class Cliente(Entidad):  # herencia: Cliente es una Entidad
    """Cliente de Software FJ."""

    def __init__(self, nombre, documento, correo, telefono):
        self.nombre = nombre  # esto pasa por el setter y se valida
        self.documento = documento  # igual, se valida en el setter
        self.correo = correo  # validacion del correo
        self.telefono = telefono  # validacion del telefono
        super().__init__()  # el id se asigna al final, asi un cliente invalido no gasta un numero

    # ---- nombre ----
    @property
    def nombre(self):  # getter del nombre
        return self.__nombre  # atributo privado con doble guion bajo

    @nombre.setter
    def nombre(self, valor):  # setter con validacion
        if not isinstance(valor, str) or valor.strip() == "":  # vacio o que no sea texto
            raise ClienteInvalidoError("El nombre no puede estar vacio")  # lo rechazo
        if any(c.isdigit() for c in valor):  # un nombre con numeros no tiene sentido
            raise ClienteInvalidoError("El nombre no puede tener numeros: " + valor)  # error con el dato
        self.__nombre = valor.strip()  # guardo sin espacios de sobra

    # ---- documento ----
    @property
    def documento(self):  # getter del documento
        return self.__documento  # privado

    @documento.setter
    def documento(self, valor):  # el documento debe ser solo numeros
        valor = str(valor)  # por si llega como int lo paso a texto
        if not valor.isdigit() or len(valor) < 6 or len(valor) > 10:  # cedula colombiana entre 6 y 10 digitos
            raise ClienteInvalidoError("Documento invalido: " + valor)  # no cumple
        self.__documento = valor  # queda guardado

    # ---- correo ----
    @property
    def correo(self):  # getter del correo
        return self.__correo  # privado

    @correo.setter
    def correo(self, valor):  # reviso que tenga forma de correo
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:  # necesita @ y un punto despues
            raise ClienteInvalidoError("Correo invalido: " + str(valor))  # str() por si llega None
        self.__correo = valor.lower()  # lo guardo en minuscula

    # ---- telefono ----
    @property
    def telefono(self):  # getter del telefono
        return self.__telefono  # privado

    @telefono.setter
    def telefono(self, valor):  # celular de 10 digitos
        valor = str(valor)  # lo convierto a texto para revisarlo
        if not valor.isdigit() or len(valor) != 10:  # tiene que ser exactamente 10 numeros
            raise ClienteInvalidoError("Telefono invalido: " + valor)  # se lanza el error
        self.__telefono = valor  # se guarda

    def describir(self):  # implementacion del metodo abstracto
        return "Cliente " + str(self.id) + ": " + self.nombre + " (" + self.correo + ")"  # texto corto del cliente
