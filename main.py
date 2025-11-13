import json
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_partidos
from consultas import ConsultasLiga  # Cambiar esta importación

def cargar_reglas(archivo_reglas, motor):
    """ Se cargan las reglas de un archivo en concreto, se genera en una 
        funcion aparte del main ya que estas reglas pueden cambiarse o haber más archivos de reglas
    """
    print('Cargando reglas... ')
    REGLAS_PROLOG = json.load(open(archivo_reglas))['REGLAS_PROLOG']
    directiva = REGLAS_PROLOG[0].replace(':- ', '').replace('.', '')
    # La primera línea es una directiva de consulta inicial

    print(f'Ejecutando directiva: {directiva}')
    list(motor.consultar(directiva))

    # Se cargan las demás reglas
    for regla in REGLAS_PROLOG[1:]:
        motor.agregar_regla(regla)
    print('Reglas cargadas\n')
    
# ------------------------------------------------------

if __name__ == "__main__":
    # Cargar datos
    archivo = 'data/primera2021.json'
    partidos_data = procesar_partidos(archivo)

    # Formatear datos para prolog
    lista_prolog = establecer_formato_partidos(partidos_data)

    # Cargar hechos
    motor = MotorLogico(comentarios=False)
    motor.generar_hechos('partido',lista_prolog)

    # Cargar reglas
    cargar_reglas('data/REGLAS.json', motor)

    # ------------------------------------------------------------
    #                    Seccion de consultas
    # ------------------------------------------------------------

    # Crear instancia de ConsultasLiga
    consultas = ConsultasLiga(motor)

    # Ejemplo de uso de las nuevas consultas
    print('--- Ejemplo de Consultas ---')
    
    # Tabla completa
    tabla = consultas.tabla_completa()
    print("Tabla de Posiciones:")
    for i, equipo in enumerate(tabla):  # Mostrar solo top 5
        print(f"{i}. {equipo['equipo']}: {equipo['Puntos']} pts")
    
    # Estadísticas generales
    stats = consultas.estadisticas_generales()
    print(f"\nEstadísticas Generales:")
    print(f"Victorias locales: {stats['victorias_locales']}")
    print(f"Victorias visitantes: {stats['victorias_visitantes']}")
    print(f"Empates: {stats['empates']}")
    
    # Equipos con valla invicta
    equipos_valla = consultas.equipos_con_valla_invicta()
    print(f"\nEquipos con al menos una valla invicta: {len(equipos_valla)}")
    
    # -----------------------------------------------------------------------------------
    # Probando cada una de las consultas de un equipo para verificar que funcionan
    # -----------------------------------------------------------------------------------
    
    equipo = 'quilmes'
    print(f"Partidos jugados de {equipo}: {consultas.partidos_jugados_por_equipo(equipo)}")
    print(f"victorias de {equipo}: {consultas.victorias_equipo(equipo)}")
    print(f"Derrotas de {equipo}: {consultas.derrotas_equipo(equipo)}")
    print(f"Empates de {equipo}: {consultas.empates_equipo(equipo)}")
    print(f"Goles a favor de {equipo}: {consultas.goles_favor_equipo(equipo)}")
    print(f"Goles en contra de {equipo}: {consultas.goles_contra_equipo(equipo)}")
    print(f"Diferencia de goles de {equipo}: {consultas.diferencia_goles_equipo(equipo)}")
    print(f"Puntos totales de {equipo}: {consultas.puntos_equipo(equipo)}")
    print(f"Vallas invictas de {equipo}: {consultas.vallas_invictas_equipo(equipo)}")
    print(f"Resumen de equipo {equipo}: {consultas.formato_json(consultas.resumen_equipo(equipo))}")
    
    print("Partido 684437:", consultas.buscar_partido_por_id(684437))
    
    
    
    
    
    
    # Se realizan las consultas cargadas por defecto
    # consultas.consultar()