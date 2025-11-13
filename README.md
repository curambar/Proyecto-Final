# Proyecto Final - Programación 3 (UNRN)
## Sistema de Estadísticas Deportivas Multi-Paradigma (Python + Prolog)

Este repositorio contiene el trabajo final grupal para la materia **Programación 3** de la Universidad Nacional de Río Negro (UNRN).

El objetivo principal del proyecto es aplicar un enfoque **multi-paradigma** para construir un sistema de consulta de estadísticas deportivas. Para esto, se combinan:

* **Programación Orientada a Objetos y Scripting (Python):** Utilizado para leer, procesar y limpiar la fuente de datos (un archivo JSON).
* **Programación Lógica (Prolog):** Utilizado como motor de base de conocimiento para definir reglas complejas (ej: qué constituye una "remontada" o cómo calcular una tabla de posiciones) y permitir consultas sobre los datos cargados.

### 🛠️ Componentes del Proyecto

1.  **`procesador.py` (El Orquestador - Python)**
    * Es el punto de entrada principal del programa.
    * Lee y procesa el archivo `primera2021.json`.
    * Formatea los datos de los partidos en un formato simple.
    * Inicializa el `MotorLogico`.
    * Carga todos los partidos como **hechos** en Prolog.
    * Carga todas las **reglas** de estadísticas (definidas en `REGLAS_PROLOG`).
    * Ejecuta las consultas de ejemplo y muestra los resultados en la consola.

2.  **`motor_logico.py` (El Motor - Python/Prolog)**
    * Una clase de Python que actúa como interfaz con un motor de Prolog, utilizando la biblioteca `pyswip`.
    * Provee métodos para `generar_hechos`, `agregar_regla` y `consultar` la base de conocimiento.

3.  **`primera2021.json` (Los Datos)**
    * Archivo JSON que contiene todos los datos de los partidos de la temporada 2021 de la Primera Nacional, usados como fuente de datos para el motor lógico.

### 📖 Funcionamiento

El flujo del programa es el siguiente:

1.  `procesador.py` se ejecuta.
2.  Lee el JSON y extrae los datos de cientos de partidos.
3.  Inicia `MotorLogico`, que abre una instancia de Prolog.
4.  El procesador itera sobre los partidos y los "afirma" (agrega) como hechos en Prolog usando la estructura:
    `partido(ID, Ronda, Fecha, Local, GolesET_L, Goles_L, Visitante, GolesET_V, Goles_V)`.
5.  Una vez cargados los hechos, carga la lista de `REGLAS_PROLOG`. Estas reglas definen la lógica para calcular estadísticas complejas, como:
    * `tabla_equipo(Equipo, PJ, PG, PE, PP, GF, GC, DG, Puntos)`: Calcula la fila completa de la tabla de posiciones para un equipo.
    * `total_victorias_locales(N)`: Cuenta cuántos partidos ganaron los locales.
    * `total_remontadas_ganadas(Equipo, N)`: Cuenta las victorias donde se empezó perdiendo en el entretiempo.
6.  Finalmente, el script ejecuta y muestra los resultados de las consultas de ejemplo definidas al final del archivo.

### 🚀 Instalación y Ejecución

Este proyecto depende de Python y de un motor de Prolog funcional.

#### 1. Prerrequisitos

* **Python 3:** Asegúrate de tener Python 3 instalado.
* **SWI-Prolog:** La biblioteca `pyswip` es una interfaz y requiere una instalación funcional de SWI-Prolog en tu sistema.
    * **Windows/macOS:** Descargar el instalador desde [swi-prolog.org](https://www.swi-prolog.org/download/stable)
    * **Linux (Ubuntu/Debian):** `sudo apt-get install swi-prolog`
* **Biblioteca `pyswip`:** Instalar la dependencia de Python.
    ```bash
    pip install pyswip
    ```

#### 2. Ejecución

Una vez instaladas las dependencias, clona el repositorio y ejecuta el `procesador.py`:

```bash
git clone [https://github.com/curambar/Proyecto-Final.git](https://github.com/curambar/Proyecto-Final.git)
cd Proyecto-Final
python procesador.py
```

Esto cargará los datos del JSON, compilará las reglas y mostrará en la consola los resultados de las consultas de ejemplo:

```
Extrayendo datos del JSON...
Procesado primera2021.json

Formateando datos para el motor logico...
Formateo listo

Cargando hechos...
[✔] Hecho cargado: partido(684437,'regular season - 1','2021-03-12','san martin s.j.',2,4,'atletico de rafaela',2,2)
[✔] Hecho cargado: partido(684438,'regular season - 1','2021-03-12','nueva chicago',1,1,'atletico mitre',1,2)
...
Cargados 590 hechos de tipo "partido/9"

Cargando reglas...
Ejecutando directiva: dynamic(partido/9)
Reglas cargadas

--- Consultas ---

[Consulta 1] Estadisticas de Tigre:
{
  "Equipo": "tigre",
  "PJ": 32,
  "PG": 17,
  "PE": 7,
  "PP": 8,
  "GF": 48,
  "GC": 28,
  "DG": 20,
  "Puntos": 58
}

[Consulta 2] Total de victorias locales:
Hubo 196 victorias locales.

[Consulta 3] Remontadas de 'san martin tucuman':
San Martin de Tucumán logró 2 remontadas.

[Consulta 4] Lista de todos los equipos participantes:
...
```

### 🔮 Futuro del Proyecto

Este proyecto es un prototipo funcional. El siguiente paso ideal sería desacoplar la lógica de la presentación, desarrollando una API (por ejemplo, con Flask o FastAPI) que exponga el motor de consultas, y una interfaz web (frontend) que permita a los usuarios realizar estas consultas de forma gráfica.

### 🧑‍💻 Autores

* **[Tu Nombre/Usuario]** - ([curambar](https://github.com/curambar))
* **[Felipe Outeiral/Blizard32]** - 
* **[Nombre Alumno 3]**
