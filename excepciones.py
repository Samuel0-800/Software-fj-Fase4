# excepciones.py
# Aqui van las excepciones propias del sistema de Software FJ

class ErrorSoftwareFJ(Exception):  # excepcion base, todas las demas heredan de esta
    """Error general del sistema."""
    pass  # no necesita nada extra, solo sirve para agruparlas


class ClienteInvalidoError(ErrorSoftwareFJ):  # para datos malos del cliente (nombre, correo, etc.)
    pass  # se usa igual que una excepcion normal


class ServicioInvalidoError(ErrorSoftwareFJ):  # cuando un servicio se crea con parametros que no sirven
    pass  # sin cuerpo, el mensaje se manda al lanzarla


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # el servicio existe pero no se puede reservar ahora
    pass  # igual que las anteriores


class ReservaInvalidaError(ErrorSoftwareFJ):  # errores al crear o procesar una reserva
    pass  # aqui tambien llegan errores encadenados con "from"


class OperacionNoPermitidaError(ErrorSoftwareFJ):  # por ejemplo cancelar algo que ya se proceso
    pass  # solo la definicion


class CalculoInvalidoError(ErrorSoftwareFJ):  # costos negativos, impuestos raros, descuentos de mas
    pass  # la usamos en los metodos de calcular_costo
