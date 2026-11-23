# logs.py
# Funcion para guardar los eventos y errores en un archivo de texto

from datetime import datetime  # para poner la fecha y hora en cada linea

ARCHIVO_LOG = "registro_eventos.log"  # nombre del archivo donde queda todo


def registrar_log(tipo, mensaje):
    """Escribe una linea en el archivo de logs. tipo puede ser INFO o ERROR."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # fecha en formato legible
    linea = "[" + fecha + "] [" + tipo + "] " + mensaje + "\n"  # armo la linea completa
    try:  # abrir un archivo tambien puede fallar
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:  # "a" para agregar sin borrar lo anterior
            archivo.write(linea)  # guardo la linea
    except OSError as e:  # por ejemplo si no hay permisos en la carpeta
        print("No se pudo escribir en el log:", e)  # aviso por consola pero el programa sigue
