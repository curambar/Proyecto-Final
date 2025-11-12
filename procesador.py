import json
from motor_logico import MotorLogico

def procesar_partidos(archivo_json):
    """
    Carga un archivo JSON de partidos, extrae los datos relevantes de cada partido
    y los devuelve como una lista de diccionarios simples.
    """
    partidos_extraidos = []
    
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_json}' no fue encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"Error: No se pudo decodificar el JSON del archivo '{archivo_json}'.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al leer el archivo: {e}")
        return None

    # La lista de partidos está en el key 'response'
    lista_partidos = data.get('response', [])
    
    if not lista_partidos:
        print("No se encontraron partidos en la clave 'response' del JSON.")
        return []

    for partido in lista_partidos:
        try:
            fixture = partido.get('fixture', {})
            torneo = partido.get('league', {})
            equipos = partido.get('teams', {})
            goles = partido.get('goals', {})
            resultado = partido.get('score', {})
            entretiempo = resultado.get('halftime', {})
            
            equipo_local = equipos.get('home', {})
            equipo_visitante = equipos.get('away', {})

            # Maneja goles que podrían ser None
            total_local = goles.get('home')
            total_visitante = goles.get('away')
            entretiempo_local = entretiempo.get('home')
            entretiempo_visitante = entretiempo.get('away')

            # Crea un diccionario simple (hecho) para cada partido
            partido_simple = {
                'partido_id': fixture.get('id'),
                'fecha': fixture.get('date', '').split('T')[0], # Extraer solo la fecha
                'ronda': torneo.get('round'),
                'local': equipo_local.get('name'),
                'visitante': equipo_visitante.get('name'),
                'local_id': equipo_local.get('id'),
                'visitante_id': equipo_visitante.get('id'),
                'total_local': total_local if total_local is not None else 0,
                'total_visitante': total_visitante if total_visitante is not None else 0,
                'entretiempo_local': entretiempo_local if entretiempo_local is not None else 0,
                'entretiempo_visitante': entretiempo_visitante if entretiempo_visitante is not None else 0,
                'ganador_local': equipo_local.get('winner') # (puede ser True, False, o None para empate)
            }

            partidos_extraidos.append(partido_simple)

        except Exception as e:
            # Capturar errores si la estructura de un partido es inesperada
            print(f"Error procesando partido (ID: {fixture.get('id')}): {e}")
            continue # Saltar al siguiente partido

    return partidos_extraidos

REGLAS_PROLOG = [
    # --- Reglas de utilidad ---
    "partido_jugado(Equipo) :- partido(_, _, _, Equipo, _, _, _, _, _)",
    "partido_jugado(Equipo) :- partido(_, _, _, _, _, _, Equipo, _, _)",
    
    # --- Reglas de resultados (stats_partido) ---
    "stats_partido(Equipo, 3, GolesF, GolesC) :- partido(_, _, _, Equipo, _, GolesF, _, _, GolesC), GolesF > GolesC",
    "stats_partido(Equipo, 1, GolesF, GolesC) :- partido(_, _, _, Equipo, _, GolesF, _, _, GolesC), GolesF =:= GolesC",
    "stats_partido(Equipo, 0, GolesF, GolesC) :- partido(_, _, _, Equipo, _, GolesF, _, _, GolesC), GolesF < GolesC",
    "stats_partido(Equipo, 3, GolesF, GolesC) :- partido(_, _, _, _, _, GolesC, Equipo, _, GolesF), GolesF > GolesC",
    "stats_partido(Equipo, 1, GolesF, GolesC) :- partido(_, _, _, _, _, GolesC, Equipo, _, GolesF), GolesF =:= GolesC",
    "stats_partido(Equipo, 0, GolesF, GolesC) :- partido(_, _, _, _, _, GolesC, Equipo, _, GolesF), GolesF < GolesC",

    # --- Reglas de agregación (Totales) ---
    "partidos_jugados(Equipo, PJ) :- findall(1, stats_partido(Equipo, _, _, _), Partidos), length(Partidos, PJ)",
    "total_ganados(Equipo, PG) :- findall(1, stats_partido(Equipo, 3, _, _), Victorias), length(Victorias, PG)",
    "total_empatados(Equipo, PE) :- findall(1, stats_partido(Equipo, 1, _, _), Empates), length(Empates, PE)",
    "total_perdidos(Equipo, PP) :- findall(1, stats_partido(Equipo, 0, _, _), Derrotas), length(Derrotas, PP)",
    
    "total_puntos(Equipo, Puntos) :- total_ganados(Equipo, PG), total_empatados(Equipo, PE), Puntos is (PG * 3) + (PE * 1)",
    
    "total_gf(Equipo, GF) :- findall(G, stats_partido(Equipo, _, G, _), Goles), sum_list(Goles, GF)",
    "total_gc(Equipo, GC) :- findall(G, stats_partido(Equipo, _, _, G), Goles), sum_list(Goles, GC)",
    "diferencia_goles(Equipo, DG) :- total_gf(Equipo, GF), total_gc(Equipo, GC), DG is GF - GC",

    # --- Regla principal de la tabla ---
    "tabla_equipo(Equipo, PJ, PG, PE, PP, GF, GC, DG, Puntos) :- \
        partido_jugado(Equipo), \
        partidos_jugados(Equipo, PJ), \
        total_ganados(Equipo, PG), \
        total_empatados(Equipo, PE), \
        total_perdidos(Equipo, PP), \
        total_gf(Equipo, GF), \
        total_gc(Equipo, GC), \
        diferencia_goles(Equipo, DG), \
        total_puntos(Equipo, Puntos)",
    
    # --- Estadísticas del torneo (CORREGIDAS) ---
    "total_victorias_locales(N) :- findall(1, (partido(_, _, _, _, _, GL, _, _, GV), GL > GV), Lista), length(Lista, N)",
    "total_victorias_visitantes(N) :- findall(1, (partido(_, _, _, _, _, GL, _, _, GV), GL < GV), Lista), length(Lista, N)",
    "total_empates(N) :- findall(1, partido(_, _, _, _, _, G, _, _, G), Lista), length(Lista, N)",

    # --- Estadísticas específicas ---
    "valla_invicta(Equipo) :- partido(_, _, _, Equipo, _, _, _, _, 0)",
    "valla_invicta(Equipo) :- partido(_, _, _, _, _, _, Equipo, _, 0)",
    "total_vallas_invictas(Equipo, N) :- findall(1, valla_invicta(Equipo), Lista), length(Lista, N)",
    
    "remontada_ganada(Equipo) :- partido(_, _, _, Equipo, GL_HT, GL_FT, _, GV_HT, GV_FT), GL_HT < GV_HT, GL_FT > GV_FT",
    "remontada_ganada(Equipo) :- partido(_, _, _, _, GV_HT, GV_FT, Equipo, GL_HT, GL_FT), GL_HT < GV_HT, GL_FT > GV_FT",
    "total_remontadas_ganadas(Equipo, N) :- findall(1, remontada_ganada(Equipo), Lista), length(Lista, N)"
]

# Cargar datos
print('Extrayendo datos del JSON... ')
archivo = 'primera2021.json'
partidos_data = procesar_partidos(archivo)
print(f'Procesado {archivo}\n')

# Formatear datos para prolog
print('Formateando datos para el motor logico... ')
lista_prolog = []
for p in partidos_data:
    hecho = {
        'id': p['partido_id'],
        'ronda': f"'{p['ronda']}'",
        'fecha': f"'{p['fecha']}'",
        'local': f"'{p['local']}'",
        'entretiempo_local': p['entretiempo_local'],
        'total_local': p['total_local'],
        'visitante': f"'{p['visitante']}'",
        'entretiempo_visitante': p['entretiempo_visitante'],
        'total_visitante': p['total_visitante'],
    }
    lista_prolog.append(hecho)
print('Formateo listo\n')

# Cargar hechos
print('Cargando hechos... ')
motor = MotorLogico()
motor.comentarios = False
motor.generar_hechos('partido',lista_prolog)
motor.comentarios = True
print(f'Cargados {len(lista_prolog)} hechos de tipo "partido/9"\n')

# Cargar reglas
print('Cargando reglas... ')
directiva = "dynamic(partido/9)"
print(f'Ejecutando directiva: {directiva}')
list(motor.consultar(directiva))

for regla in REGLAS_PROLOG:
    motor.agregar_regla(regla)
print('Reglas cargadas\n')

# Ejemplo consultas
print('--- Consultas ---')

print('\n[Consulta 1] Estadisticas de Tigre:')
consulta_tigre = "tabla_equipo('tigre', PJ, PG, PE, PP, GF, GC, DG, Puntos)."
resultado_tigre = motor.consultar(consulta_tigre)
if resultado_tigre:
    print(json.dumps(resultado_tigre[0], indent=2))
else:
    print('No se encontro Tigre')

print("\n[Consulta 2] Total de victorias locales:")
resultado_locales = motor.consultar("total_victorias_locales(N).")
if resultado_locales:
    print(f"Hubo {resultado_locales[0]['N']} victorias locales.")

print("\n[Consulta 3] Remontadas de 'san martin tucuman':")
resultado_remontada = motor.consultar("total_remontadas_ganadas('san martin tucuman', N).")
if resultado_remontada:
    print(f"San Martin de Tucumán logró {resultado_remontada[0]['N']} remontadas.")

print("\n[Consulta 4] Lista de todos los equipos participantes:")
consulta_equipos = "setof(Equipo, partido_jugado(Equipo), Equipos)."
resultado_equipos = motor.consultar(consulta_equipos)
if resultado_equipos:
    lista_de_equipos = resultado_equipos[0]['Equipos']
    print(f"Se encontraron {len(lista_de_equipos)} equipos:")
    for equipo in lista_de_equipos:
        print(equipo)
else:
    print("No se pudieron encontrar equipos.")
