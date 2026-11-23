# entidad.py
# Clase abstracta que representa cualquier cosa del sistema (cliente, servicio, reserva)

from abc import ABC, abstractmethod  # ABC permite hacer clases abstractas en Python


class Entidad(ABC):  # no se puede crear un objeto Entidad directamente
    """Entidad general del sistema, todas tienen un id."""

    contador = 0  # atributo de clase, se comparte entre todos los objetos

    def __init__(self):  # constructor comun para todas las entidades
        Entidad.contador += 1  # cada vez que se crea algo sube el contador
        self._id = Entidad.contador  # el id queda protegido con guion bajo

    @property
    def id(self):  # solo lectura, el id no se deberia cambiar
        return self._id  # devuelvo el id

    @abstractmethod
    def describir(self):  # cada clase hija tiene que decir como se describe
        pass  # aqui no va codigo, lo hacen las hijas
