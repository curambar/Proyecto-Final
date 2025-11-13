import json
# Importamos CORS
from flask_cors import CORS 
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_partidos
from consultas import ConsultasLiga 
from flask import Flask, jsonify, request

# --- INICIALIZACIÓN DE FLASK ---
app = Flask(__name__)
# 🟢 SOLUCIÓN CORS: Habilitar CORS para permitir solicitudes desde cualquier origen (*)
CORS(app)

# Variable global para mantener la instancia de ConsultasLiga cargada
consultas_liga = None

def cargar_reglas(archivo_reglas, motor):
    """ Se cargan las reglas de un archivo en concreto. """
    print('Cargando reglas... ')
    try:
        with open(archivo_reglas, 'r') as f:
            REGLAS_PROLOG = json.load(f)['REGLAS_PROLOG']
    except FileNotFoundError:
        print(f"ERROR: Archivo de reglas '{archivo_reglas}' no encontrado.")
        return False

    directiva = REGLAS_PROLOG[0].replace(':- ', '').replace('.', '')
    # La primera línea es una directiva de consulta inicial

    print(f'Ejecutando directiva: {directiva}')
    list(motor.consultar(directiva))

    # Se cargan las demás reglas
    for regla in REGLAS_PROLOG[1:]:
        motor.agregar_regla(regla)
    print('Reglas cargadas\n')
    return True

# ------------------------------------------------------
# Lógica de Carga y Configuración (Se ejecuta una sola vez al inicio)
# ------------------------------------------------------

def inicializar_motor_logico():
    """ Carga todos los hechos y reglas en el motor lógico y retorna la instancia de ConsultasLiga. """
    print("--- INICIALIZANDO MOTOR LÓGICO Y CARGANDO DATOS ---")
    
    # Cargar datos - RUTA CORREGIDA a 'json/'
    archivo_datos = 'json/primera2021.json'
    partidos_data = procesar_partidos(archivo_datos)

    if partidos_data is None:
        print(f"ERROR: No se pudo cargar la data desde '{archivo_datos}'. Abortando inicialización.")
        return None

    # Formatear datos para prolog
    lista_prolog = establecer_formato_partidos(partidos_data)

    # Cargar hechos
    motor = MotorLogico(comentarios=False)
    motor.generar_hechos('partido', lista_prolog)

    # Cargar reglas - RUTA CORREGIDA a 'json/'
    if not cargar_reglas('json/REGLAS.json', motor):
        return None

    # Crear instancia de ConsultasLiga
    return ConsultasLiga(motor)

# Intentar inicializar el motor globalmente
consultas_liga = inicializar_motor_logico()


# ------------------------------------------------------
#                    ENDPOINTS API
# ------------------------------------------------------

def verificar_motor():
    """ Función auxiliar para chequear si el motor está listo. """
    if consultas_liga is None:
        return jsonify({"error": "Error interno: El motor lógico no pudo inicializarse. Revise los archivos JSON."}), 500
    return None

@app.route('/')
def inicio():
    """ Página de inicio simple para verificar que el API está corriendo. """
    return "API de Consultas de Liga con SWI-Prolog (pyswip) está funcionando."

@app.route('/api/tabla-posiciones', methods=['GET'])
def get_tabla_completa():
    """ Retorna la tabla de posiciones completa. """
    error_response = verificar_motor()
    if error_response:
        return error_response
    
    # Llama al método de la clase ConsultasLiga
    tabla = consultas_liga.tabla_completa()
    return jsonify(tabla)

@app.route('/api/estadisticas-generales', methods=['GET'])
def get_estadisticas_generales():
    """ Retorna el resumen de victorias/empates. """
    error_response = verificar_motor()
    if error_response:
        return error_response
    
    stats = consultas_liga.estadisticas_generales()
    return jsonify(stats)

@app.route('/api/equipo/<string:nombre_equipo>', methods=['GET'])
def get_resumen_equipo(nombre_equipo):
    """ Retorna el resumen completo de un equipo específico por su nombre. """
    error_response = verificar_motor()
    if error_response:
        return error_response
    
    # Nota: Los nombres de equipo deben pasarse en minúsculas en la URL si el Prolog usa minúsculas
    equipo = nombre_equipo.lower()
    
    # Se obtienen todos los datos en una sola consulta
    resumen_datos = consultas_liga.resumen_equipo(equipo)
    
    if not resumen_datos:
         return jsonify({"error": f"Equipo '{equipo}' no encontrado o sin datos."}), 404
         
    # La consulta ya retorna los datos formateados
    return jsonify(resumen_datos[0])

@app.route('/api/vallas-invictas', methods=['GET'])
def get_equipos_valla_invicta():
    """ Retorna la lista de equipos con al menos una valla invicta. """
    error_response = verificar_motor()
    if error_response:
        return error_response
    
    equipos = consultas_liga.equipos_con_valla_invicta()
    return jsonify(equipos)


if __name__ == "__main__":
    if consultas_liga:
        print("✅ Motor lógico inicializado correctamente.")
        print("🚀 Iniciando servidor Flask en http://127.0.0.1:5000")
        # El host '0.0.0.0' es a veces necesario para el acceso externo en contenedores/entornos específicos
        # Mantenemos 127.0.0.1 ya que es lo que el cliente espera.
        app.run(debug=True, port=5000)
    else:
        print("❌ No se pudo iniciar el servidor Flask debido a errores en la inicialización del motor lógico.")