import json
from setup import SetUp
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_partidos
from consultas import ConsultasLiga 

# Importamos CORS
from flask_cors import CORS 
from flask import Flask, jsonify, request

# --- INICIALIZACIÓN DE FLASK ---
app = Flask(__name__)
# 🟢 SOLUCIÓN CORS: Habilitar CORS para permitir solicitudes desde cualquier origen (*)
CORS(app)

# Intentar inicializar el motor globalmente
archivo = 'json/primera2021.json'
setup = SetUp(archivo)
consultas_liga = setup.obtener_acceso_consultas()


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