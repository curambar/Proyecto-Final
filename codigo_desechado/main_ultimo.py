import json
from setup import SetUp
from procesador import procesar_partidos, establecer_formato_partidos

if __name__ == "__main__":
    # Cargar datos
    archivo = 'json/primera2021.json'
    setup = SetUp(archivo)
    consultas = setup.obtener_acceso_consultas()
    
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
    
    print("Partido 684437:", consultas.formato_json(consultas.buscar_partido_por_id(684437)))
    
    # Se realizan las consultas cargadas por defecto
    # consultas.consultar()