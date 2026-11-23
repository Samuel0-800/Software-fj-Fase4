# main.py
# Simulacion de operaciones del sistema de Software FJ
# Se mezclan casos buenos y malos para ver que el programa sigue funcionando aunque haya errores

from sistema import SistemaSoftwareFJ  # clase que maneja las listas
from servicios import ReservaSala, AlquilerEquipo, Asesoria  # los tres servicios
from excepciones import ErrorSoftwareFJ  # excepcion base
from logs import registrar_log  # para el log

sistema = SistemaSoftwareFJ()  # creo el sistema vacio
registrar_log("INFO", "---- Inicio de la simulacion ----")  # marca de inicio en el log

# Operacion 1: cliente con datos correctos
print("Operacion 1: registrar cliente valido")  # titulo de la operacion
ana = sistema.registrar_cliente("Ana Torres", "1023456789", "ana.torres@gmail.com", "3104567890")  # deberia funcionar

# Operacion 2: cliente con correo sin @
print("\nOperacion 2: registrar cliente con correo invalido")  # caso de error
sistema.registrar_cliente("Pedro Ruiz", "79876543", "pedro.ruizgmail.com", "3001234567")  # falla por el correo

# Operacion 3: documento con letras
print("\nOperacion 3: registrar cliente con documento invalido")  # otro error
sistema.registrar_cliente("Luis Gomez", "10AB345", "luis@hotmail.com", "3157778899")  # falla por el documento

# Operacion 4: segundo cliente valido
print("\nOperacion 4: registrar otro cliente valido")  # caso bueno
carlos = sistema.registrar_cliente("Carlos Mejia", 1098765432, "Carlos.Mejia@outlook.com", 3209991122)  # llega como numero y igual se valida

# Operacion 5: crear los servicios correctos
print("\nOperacion 5: crear servicios validos")  # tres servicios distintos
sala = sistema.agregar_servicio(ReservaSala, "Sala de juntas", 50000, 12)  # sala para 12 personas
equipos = sistema.agregar_servicio(AlquilerEquipo, "Portatil", 15000, 3)  # 3 portatiles
asesoria = sistema.agregar_servicio(Asesoria, "Ciberseguridad", 80000, "avanzado")  # asesoria avanzada

# Operacion 6: servicios mal creados
print("\nOperacion 6: crear servicios invalidos")  # errores al crear
sistema.agregar_servicio(ReservaSala, "Auditorio", -20000, 100)  # precio negativo
sistema.agregar_servicio(Asesoria, "Bases de datos", 60000, "experto")  # nivel que no existe
sistema.agregar_servicio(AlquilerEquipo, "Video beam", 20000, 15)  # mas equipos de los permitidos

# Operacion 7: reserva completa que sale bien (crear, confirmar y procesar con IVA)
print("\nOperacion 7: reserva exitosa con IVA del 19%")  # flujo completo
r1 = sistema.crear_reserva(ana, sala, 3)  # 3 horas de sala
try:  # confirmar y procesar pueden fallar
    r1.confirmar()  # pendiente -> confirmada
    total = r1.procesar(0.19)  # solo impuesto, sin descuento
except ErrorSoftwareFJ as e:  # si algo falla lo registro
    registrar_log("ERROR", "Fallo en la operacion 7: " + str(e))  # log
    print("  Error:", e)  # consola
else:  # si todo salio bien
    print("  Total cobrado: $" + str(total))  # muestro el valor

# Operacion 8: reserva con horas fuera de rango (la asesoria es maximo de 4 horas)
print("\nOperacion 8: reserva con duracion no permitida")  # error encadenado
sistema.crear_reserva(carlos, asesoria, 6)  # 6 horas no se puede

# Operacion 9: reserva con horas en texto
print("\nOperacion 9: reserva con horas escritas como texto")  # TypeError encadenado
sistema.crear_reserva(carlos, equipos, "tres")  # deberia ser un numero

# Operacion 10: reserva sin cliente (parametro faltante)
print("\nOperacion 10: reserva sin cliente")  # falta un dato
sistema.crear_reserva(None, sala, 2)  # el cliente llega vacio

# Operacion 11: servicio que no esta disponible
print("\nOperacion 11: confirmar reserva de un servicio no disponible")  # servicio ocupado
r2 = sistema.crear_reserva(carlos, equipos, 5)  # la reserva se crea bien
equipos.cambiar_disponibilidad(False)  # simulo que los portatiles ya estan alquilados
try:  # al confirmar deberia fallar
    r2.confirmar()  # lanza ServicioNoDisponibleError
except ErrorSoftwareFJ as e:  # lo capturo
    registrar_log("ERROR", "Fallo en la operacion 11: " + str(e))  # log
    print("  Error:", e)  # consola
finally:  # pase lo que pase vuelvo a dejar el servicio disponible
    equipos.cambiar_disponibilidad(True)  # para las siguientes pruebas
    print("  Servicio de equipos disponible otra vez")  # aviso

# Operacion 12: procesar con un descuento que no tiene sentido
print("\nOperacion 12: procesar reserva con descuento invalido")  # calculo inconsistente
r3 = sistema.crear_reserva(carlos, asesoria, 2)  # 2 horas de asesoria
try:  # confirmo y proceso
    r3.confirmar()  # queda confirmada
    r3.procesar(0.19, 0.8)  # 80% de descuento no esta permitido
except ErrorSoftwareFJ as e:  # aqui llega la ReservaInvalidaError encadenada
    registrar_log("ERROR", "Fallo en la operacion 12: " + str(e) + " | causa: " + str(e.__cause__))  # guardo tambien la causa
    print("  Error:", e, "| causa:", e.__cause__)  # muestro las dos
print("  Estado de la reserva despues del error:", r3.estado)  # sigue confirmada, no se perdio

# Operacion 13: ahora si se procesa con un descuento valido
print("\nOperacion 13: procesar la misma reserva con descuento del 10%")  # se corrige y se intenta otra vez
try:  # puede fallar igual
    total = r3.procesar(0.19, 0.10)  # impuesto y descuento
    print("  Total cobrado: $" + str(total))  # resultado
except ErrorSoftwareFJ as e:  # por si acaso
    registrar_log("ERROR", "Fallo en la operacion 13: " + str(e))  # log
    print("  Error:", e)  # consola

# Operacion 14: cancelar una reserva que ya se proceso
print("\nOperacion 14: cancelar una reserva ya procesada")  # operacion no permitida
try:  # cancelar
    r1.cancelar()  # r1 ya se proceso en la operacion 7
except ErrorSoftwareFJ as e:  # OperacionNoPermitidaError
    registrar_log("ERROR", "Fallo en la operacion 14: " + str(e))  # log
    print("  Error:", e)  # consola

# Operacion 15: cancelar una reserva pendiente (si se puede)
print("\nOperacion 15: cancelar una reserva pendiente")  # caso bueno
try:  # r2 quedo pendiente porque no se pudo confirmar
    r2.cancelar()  # pasa a cancelada
    print("  Reserva", r2.id, "cancelada")  # aviso
except ErrorSoftwareFJ as e:  # no deberia pasar
    registrar_log("ERROR", "Fallo en la operacion 15: " + str(e))  # log
    print("  Error:", e)  # consola

# Operacion 16: las tres formas de llamar calcular_costo (sobrecarga con parametros opcionales)
print("\nOperacion 16: variantes del calculo de costo")  # mismo metodo, distintos parametros
try:  # calculos de prueba sin crear reservas
    print("  Sala 2 h sin nada: $" + str(sala.calcular_costo(2)))  # solo horas
    print("  Sala 2 h con IVA: $" + str(sala.calcular_costo(2, 0.19)))  # horas e impuesto
    print("  Sala 2 h con IVA y 10% desc: $" + str(sala.calcular_costo(2, 0.19, 0.10)))  # todo
    print("  Asesoria 2 h con IVA: $" + str(asesoria.calcular_costo(2, impuesto=0.19)))  # polimorfismo, otra formula
    print("  Equipos 4 h sin nada: $" + str(equipos.calcular_costo(4)))  # otra formula mas
except ErrorSoftwareFJ as e:  # si algun calculo falla
    registrar_log("ERROR", "Fallo en la operacion 16: " + str(e))  # log
    print("  Error:", e)  # consola

# Al final se muestra lo que quedo guardado en las listas
print("\nResumen final")  # el programa llego al final sin detenerse
sistema.resumen()  # conteo de clientes, servicios y reservas
registrar_log("INFO", "---- Fin de la simulacion ----")  # marca de fin
print("\nRevise el archivo registro_eventos.log para ver los eventos y errores")  # recordatorio
