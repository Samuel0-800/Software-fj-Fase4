# servicios.py
# Clase abstracta Servicio y los tres servicios que ofrece Software FJ

from abc import abstractmethod  # para marcar los metodos que las hijas deben hacer
from entidad import Entidad  # Servicio tambien es una Entidad
from excepciones import ServicioInvalidoError, CalculoInvalidoError  # errores propios


class Servicio(Entidad):  # clase abstracta, no se crea directamente
    """Servicio general. Las clases hijas definen como se cobra."""

    def __init__(self, nombre, precio_hora):
        if not isinstance(nombre, str) or nombre.strip() == "":  # el servicio necesita nombre
            raise ServicioInvalidoError("El servicio necesita un nombre")  # sin nombre no se crea
        if not isinstance(precio_hora, (int, float)) or precio_hora <= 0:  # precio tiene que ser numero positivo
            raise ServicioInvalidoError("Precio por hora invalido: " + str(precio_hora))  # muestro el valor malo
        self._nombre = nombre  # protegido
        self._precio_hora = precio_hora  # protegido
        self._disponible = True  # al crearlo queda disponible
        super().__init__()  # id al final, solo si todo estaba bien

    @property
    def nombre(self):  # getter del nombre
        return self._nombre  # devuelve el nombre

    @property
    def disponible(self):  # para saber si se puede reservar
        return self._disponible  # True o False

    def cambiar_disponibilidad(self, estado):  # para simular que un servicio deja de estar disponible
        self._disponible = estado  # guardo el nuevo estado

    def _validar_horas(self, horas, maximo):  # revision comun que usan las tres clases hijas
        if not isinstance(horas, (int, float)):  # si mandan texto u otra cosa
            raise TypeError("Las horas deben ser un numero, llego: " + str(horas))  # error de tipo
        if horas <= 0 or horas > maximo:  # fuera del rango permitido
            raise ValueError("Horas fuera de rango (1 a " + str(maximo) + "): " + str(horas))  # error de valor

    def _aplicar_ajustes(self, base, impuesto, descuento):  # suma impuesto y resta descuento al valor base
        if impuesto is None:  # si no mandan impuesto queda en 0
            impuesto = 0  # sin impuesto
        if descuento is None:  # lo mismo con el descuento
            descuento = 0  # sin descuento
        if impuesto < 0 or impuesto > 0.5:  # un impuesto mayor al 50% seguro es un error de digitacion
            raise CalculoInvalidoError("Impuesto no valido: " + str(impuesto))  # lo rechazo
        if descuento < 0 or descuento > 0.5:  # tampoco dejamos descuentos de mas del 50%
            raise CalculoInvalidoError("Descuento no valido: " + str(descuento))  # error de calculo
        total = base * (1 + impuesto) * (1 - descuento)  # primero el impuesto y despues el descuento
        if total <= 0:  # por si algo raro deja el total en cero o negativo
            raise CalculoInvalidoError("El costo dio un valor inconsistente: " + str(total))  # no deberia pasar
        return round(total, 2)  # redondeo a dos decimales

    @abstractmethod
    def calcular_costo(self, horas, impuesto=None, descuento=None):  # metodo "sobrecargado" con parametros opcionales
        pass  # cada servicio lo implementa a su manera

    @abstractmethod
    def validar_parametros(self, horas):  # cada servicio tiene sus propios limites
        pass  # lo hacen las hijas

    @abstractmethod
    def describir(self):  # descripcion del servicio
        pass  # lo hacen las hijas


class ReservaSala(Servicio):  # primer servicio: alquiler de salas
    """Reserva de salas por horas."""

    def __init__(self, nombre, precio_hora, capacidad):
        if not isinstance(capacidad, int) or capacidad <= 0:  # la sala debe tener capacidad positiva
            raise ServicioInvalidoError("Capacidad de sala invalida: " + str(capacidad))  # error al crear
        self.capacidad = capacidad  # cuantas personas caben
        super().__init__(nombre, precio_hora)  # el padre valida nombre y precio

    def validar_parametros(self, horas):  # una sala se reserva maximo 8 horas
        self._validar_horas(horas, 8)  # uso la validacion del padre

    def calcular_costo(self, horas, impuesto=None, descuento=None):  # sobrescritura del metodo del padre
        self.validar_parametros(horas)  # primero reviso las horas
        base = self._precio_hora * horas  # la sala se cobra solo por hora
        return self._aplicar_ajustes(base, impuesto, descuento)  # aplico impuesto o descuento si llegan

    def describir(self):  # descripcion propia de la sala
        return "Sala '" + self.nombre + "' para " + str(self.capacidad) + " personas, $" + str(self._precio_hora) + " la hora"  # texto


class AlquilerEquipo(Servicio):  # segundo servicio: alquiler de equipos
    """Alquiler de equipos (portatiles, video beam, etc.)."""

    def __init__(self, nombre, precio_hora, cantidad):
        if not isinstance(cantidad, int) or cantidad < 1 or cantidad > 10:  # se alquilan de 1 a 10 equipos
            raise ServicioInvalidoError("Cantidad de equipos invalida: " + str(cantidad))  # fuera de rango
        self.cantidad = cantidad  # numero de equipos
        super().__init__(nombre, precio_hora)  # validacion basica en el padre

    def validar_parametros(self, horas):  # los equipos se alquilan maximo 24 horas seguidas
        self._validar_horas(horas, 24)  # validacion comun

    def calcular_costo(self, horas, impuesto=None, descuento=None):  # aqui el costo depende de la cantidad
        self.validar_parametros(horas)  # reviso horas
        base = self._precio_hora * horas * self.cantidad  # precio por hora por cada equipo
        return self._aplicar_ajustes(base, impuesto, descuento)  # ajustes opcionales

    def describir(self):  # descripcion del alquiler
        return "Alquiler de " + str(self.cantidad) + " x '" + self.nombre + "', $" + str(self._precio_hora) + " la hora cada uno"  # texto


class Asesoria(Servicio):  # tercer servicio: asesorias especializadas
    """Asesoria con un especialista. El nivel avanzado cuesta mas."""

    def __init__(self, nombre, precio_hora, nivel):
        if nivel not in ("basico", "avanzado"):  # solo hay dos niveles
            raise ServicioInvalidoError("Nivel de asesoria no existe: " + str(nivel))  # nivel desconocido
        self.nivel = nivel  # guardo el nivel
        super().__init__(nombre, precio_hora)  # el padre valida lo comun

    def validar_parametros(self, horas):  # una asesoria dura maximo 4 horas
        self._validar_horas(horas, 4)  # validacion comun

    def calcular_costo(self, horas, impuesto=None, descuento=None):  # el avanzado tiene recargo
        self.validar_parametros(horas)  # primero las horas
        recargo = 1.5 if self.nivel == "avanzado" else 1  # 50% mas si es avanzado
        base = self._precio_hora * horas * recargo  # costo base con recargo
        return self._aplicar_ajustes(base, impuesto, descuento)  # ajustes

    def describir(self):  # descripcion de la asesoria
        return "Asesoria '" + self.nombre + "' nivel " + self.nivel + ", $" + str(self._precio_hora) + " la hora"  # texto
