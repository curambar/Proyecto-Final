import json

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

def establecer_formato_prolog(partidos_data):
    partidos = []
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
        partidos.append(hecho)
        
    return partidos
