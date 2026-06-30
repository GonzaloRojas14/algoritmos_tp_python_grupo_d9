# Sistema de Gestión de Hotel

## Integrantes del grupo

| Nombre | Rol |
| :--- | :--- |
| (Completar) | (Completar) |
| (Completar) | (Completar) |
| (Completar) | (Completar) |

## Comisión

(Completar con el número de comisión)

## Descripción general del sistema

Sistema de gestión hotelera desarrollado en Python que se ejecuta por consola. Permite administrar las operaciones diarias de un hotel:

- **Registro de huéspedes:** Alta, consulta, búsqueda por DNI y baja de huéspedes.
- **Gestión de habitaciones:** Visualización del estado de las 13 habitaciones del hotel (5 simples, 5 dobles, 3 suites), cambio de estado a mantenimiento.
- **Check-in:** Asignación de habitaciones a huéspedes registrados, selección de tipo de habitación y cantidad de noches.
- **Check-out:** Finalización de estadías con emisión de factura, cálculo automático del monto total y liberación de la habitación.
- **Estadísticas:** Reportes de ocupación general, ocupación por tipo de habitación, ingresos totales y huésped con más noches acumuladas.
- **Persistencia:** Los datos se guardan automáticamente en archivos `.txt` al cerrar el programa y se cargan al iniciar.

### Estructura del proyecto

```
gestion_hotel/
├── main.py              # Punto de entrada y menú principal
├── habitaciones.py      # Gestión de habitaciones
├── huespedes.py         # Gestión de huéspedes
├── reservas.py          # Check-in y check-out
├── estadisticas.py      # Reportes y estadísticas
├── validaciones.py      # Validación de entradas
├── datos.py             # Persistencia en archivos .txt
├── README.md            # Este archivo
└── datos/               # Carpeta de datos generados
    ├── huespedes.txt
    ├── habitaciones.txt
    └── reservas.txt
```

### Conceptos aplicados

- Estructuras condicionales (`if`, `elif`, `else`)
- Estructuras repetitivas (`while`, `for`)
- Funciones con y sin retorno
- Validaciones de entrada con bucles
- Contadores y acumuladores
- Banderas (variables booleanas)
- Modularización en múltiples archivos
- Manejo de archivos `.txt` con `with open`
- Manejo de excepciones con `try/except`
- Convenciones PEP8

## Instrucciones de ejecución

### Requisitos previos

- Python 3.x instalado en el sistema.
- No se requieren bibliotecas externas.

### Cómo ejecutar

1. Abrir una terminal o consola.
2. Navegar a la carpeta del proyecto:
   ```bash
   cd ruta/a/gestion_hotel
   ```
3. Ejecutar el programa:
   ```bash
   python main.py
   ```
4. Seguir las instrucciones del menú en pantalla.

### Notas

- En la primera ejecución, el sistema inicializa automáticamente las habitaciones del hotel.
- Los datos se guardan al seleccionar la opción "Guardar y salir" del menú principal.
- Los archivos de datos se almacenan en la carpeta `datos/`.

## Uso de Inteligencia Artificial

| Herramienta | Para qué se utilizó | Cómo se utilizó |
| :--- | :--- | :--- |
| (Completar, ej: Google Gemini) | (Completar, ej: generar estructura inicial del proyecto) | (Completar, ej: se le proporcionó la consigna y los apuntes de la materia como contexto. Se revisó y adaptó cada módulo generado para asegurar que cumpla con los lineamientos de la cátedra) |

> **Nota:** Todas las soluciones propuestas por la IA fueron revisadas, comprendidas y adaptadas por los integrantes del grupo. Se verificó que el código cumpla con los paradigmas y estructuras enseñadas en la asignatura.
