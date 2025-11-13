import json

def tabla_equipo(motor, equipo_nombre):
    consulta = f"tabla_equipo('{equipo_nombre}', PJ, PG, PE, PP, GF, GC, DG, Puntos)."
    resultados = motor.consultar(consulta)
    return resultados

def equipos_participantes(motor):
    consulta_equipos = "setof(Equipo, partido_jugado(Equipo), Equipos)."
    resultado_equipos = motor.consultar(consulta_equipos)
    lista_de_equipos = resultado_equipos[0]['Equipos']
    return lista_de_equipos

def remontadas_ganadas(motor, equipo_nombre):
    resultado_remontada = motor.consultar(f"total_remontadas_ganadas('{equipo_nombre}', N).")
    if resultado_remontada:
        return resultado_remontada[0]['N']
    return 0
    
def consultar(motor):
    """Consultas generales preprogramadas

    Args:
        motor (MotorLogico): el motor lógico con los hechos y reglas cargadas
    """
    
    print('\n[Consulta 1] Estadisticas de Tigre:')
    resultado_tigre = tabla_equipo(motor, 'tigre')
    if resultado_tigre:
        print(json.dumps(resultado_tigre[0], indent=2))
    else:
        print('No se encontro Tigre')

    # ------------- Otras consultas de ejemplo -------------

    print("\n[Consulta 2] Total de victorias locales:")
    resultado_locales = motor.consultar("total_victorias_locales(N).")
    if resultado_locales:
        print(f"Hubo {resultado_locales[0]['N']} victorias locales.")
        
    # -----------------------------------------------------
    lista_de_equipos = equipos_participantes(motor)

    for equipo in lista_de_equipos:
        print(f"\n[Consulta 3] Remontadas de {equipo.title()}:")
        print(f"{equipo.title()} logró {remontadas_ganadas(motor, equipo)} remontadas.")

    # -----------------------------------------------------

    print("\n[Consulta 4] Lista de todos los equipos participantes:")
    if len(lista_de_equipos) > 0:
        print(f"Se encontraron {len(lista_de_equipos)} equipos:")
        for equipo in lista_de_equipos:
            print(equipo)
    else:
        print("No se pudieron encontrar equipos.")