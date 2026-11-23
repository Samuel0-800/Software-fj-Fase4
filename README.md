# Software FJ - Gestion de clientes, servicios y reservas

Fase 4 del curso Programacion (213023), UNAD.

Sistema en Python orientado a objetos, sin base de datos. Los clientes, servicios y reservas se guardan en listas y los eventos y errores quedan en el archivo `registro_eventos.log`.

## Como ejecutarlo

Se necesita Python 3. Desde la carpeta del proyecto:

```
python main.py
```

El programa corre 16 operaciones seguidas, unas correctas y otras con errores a proposito, y al final muestra un resumen.

## Archivos

- `main.py`: la simulacion de las operaciones
- `sistema.py`: clase que maneja las listas
- `entidad.py`: clase abstracta base
- `cliente.py`: clase Cliente con validaciones
- `servicios.py`: clase abstracta Servicio y los servicios ReservaSala, AlquilerEquipo y Asesoria
- `reserva.py`: clase Reserva
- `excepciones.py`: excepciones personalizadas
- `logs.py`: escritura del archivo de logs

## Integrantes

- NOMBRE COMPLETO
