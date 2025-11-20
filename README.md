# Proyecto Final - Programación 3 (UNRN)
## Sistema de Estadísticas Deportivas Multi-Paradigma (Python + Prolog)

Este repositorio contiene el trabajo final grupal para la materia **Programación 3** de la Universidad Nacional de Río Negro (UNRN).

El objetivo principal del proyecto es aplicar un enfoque **multi-paradigma** para construir un sistema de consulta de estadísticas deportivas. Para esto, se combinan:

* **Programación Orientada a Objetos y Scripting (Python):** Utilizado para leer, procesar y limpiar la fuente de datos (un archivo JSON).
* **Programación Lógica (Prolog):** Utilizado como motor de base de conocimiento para definir reglas complejas (ej: qué constituye una "remontada" o cómo calcular una tabla de posiciones) y permitir consultas sobre los datos cargados.
* **API REST (Flask):** Para exponer las funcionalidades del sistema a través de endpoints web.

### Componentes del Proyecto

1.  **`main.py` (API Flask - Python)**
    * Es el punto de entrada principal del programa.
    * Inicializa el servidor Flask con CORS habilitado.
    * Configura los endpoints REST para consultar estadísticas.
    * Orquesta la inicialización del sistema completo.

2.  **`setup.py` (Configuración del Sistema - Lectura de datos - Carga de Hechos)**
    * Clase principal que coordina la inicialización del sistema.
    * Procesa los datos del archivo JSON de partidos.
    * Inicializa el `MotorLogico` y carga todos los hechos de partidos.
    * Carga todas las **reglas** de estadísticas (definidas en `REGLAS_PROLOG`).
    * Proporciona acceso a las consultas a través de `ConsultasLiga`.

3.  **`motor_logico.py` (El Motor - Python/Prolog)**
    * Una clase de Python que actúa como interfaz con un motor de Prolog, utilizando la biblioteca `pyswip`.
    * Provee métodos para `generar_hechos`, `agregar_regla` y `consultar` a la interfaz generada del Prolog.

4.  **`consultas.py` (Consultas Especializadas)**
    * Clase `ConsultasLiga` que encapsula todas las consultas disponibles.
    * Proporciona métodos para obtener estadísticas específicas como tabla de posiciones, remontadas, vallas invictas, etc.
    * Formatea los resultados en JSON para consumo de la API.

5.  **`procesador.py` (Procesamiento de Datos)**
    * Lee y procesa un archivo `.json` obteniendo sus datos.
    * Formatea los datos para generar hechos de prolog de **partidos**, formato simple para Prolog: <p> `partido(ID, Ronda, Fecha, Local, GolesET_L, Goles_L, Visitante, GolesET_V, Goles_V)`
    * Maneja errores y validaciones de datos.

6.  **`REGLAS.json` (Reglas de Negocio - Prolog)**
    * Contiene todas las reglas lógicas definidas en Prolog para calcular estadísticas.
    * Define predicados como `tabla_equipo`, `total_remontadas_ganadas`, `valla_invicta`, etc.

7.  **`primera2021.json` (Los Datos)**
    * Archivo JSON que contiene todos los datos de los partidos de la temporada 2021 de la Primera Nacional, usados como fuente de datos para el motor lógico.

### Funcionamiento

El flujo del programa es el siguiente:

1.  `main.py` se ejecuta e inicia el servidor Flask.
2.  Se crea una instancia de `SetUp` que procesa el JSON y extrae los datos de cientos de partidos.
3.  Inicia `MotorLogico`, que abre una instancia de Prolog.
4.  El procesador itera sobre los partidos y los agrega como hechos en Prolog usando la estructura `partido_simple`.
5.  Una vez cargados los hechos, carga la lista de `REGLAS_PROLOG`. Estas reglas definen la lógica para calcular estadísticas complejas, como:
    * `tabla_equipo(Equipo, PJ, PG, PE, PP, GF, GC, DG, Puntos)`: Calcula la fila completa de la tabla de posiciones para un equipo.
    * `total_victorias_locales(N)`: Cuenta cuántos partidos ganaron los locales.
    * `total_remontadas_ganadas(Equipo, N)`: Cuenta las victorias donde se empezó perdiendo en el entretiempo.
    * `valla_invicta(Equipo)`: Identifica partidos donde un equipo no recibió goles.
6.  La API Flask queda disponible con endpoints para consultar estas estadísticas.

### Endpoints de la API

La API expone los siguientes endpoints:

- `GET /` - Página de inicio para verificar que el API está funcionando
- `GET /api/tabla-posiciones` - Retorna la tabla de posiciones completa
- `GET /api/estadisticas-generales` - Retorna estadísticas generales de la liga
- `GET /api/equipo/<nombre_equipo>` - Retorna el resumen completo de un equipo específico
- `GET /api/vallas-invictas` - Retorna la lista de equipos con al menos una valla invicta

### Futuro del Proyecto

Este proyecto es un prototipo funcional que demuestra la integración exitosa de múltiples paradigmas de programación. El siguiente paso ideal sería:

* Desarrollar un frontend web que consuma la API para una experiencia de usuario más amigable.
* Agregar más endpoints para consultas específicas.
* Implementar caching para mejorar el rendimiento.
* Extender el sistema para soportar múltiples temporadas y competiciones.

### Autores

* **[Leandro Suarez/([curambar](https://github.com/curambar))]** - 
* **[Felipe Outeiral/([Blizard32](https://github.com/Blizard32))]** - 
* **[Santiago Gaiero /([SGaiero](https://github.com/SGaiero))]**
