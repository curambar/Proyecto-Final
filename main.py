import json
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_prolog
import consultas

if __name__ == "__main__":
    # Cargar datos
    print('Extrayendo datos del JSON... ')
    archivo = 'primera2021.json'
    partidos_data = procesar_partidos(archivo)
    print(f'Procesado {archivo}\n')

    # Formatear datos para prolog
    print('Formateando datos para el motor logico... ')
    lista_prolog = establecer_formato_prolog(partidos_data)
    print('Formateo listo\n')

    # Cargar hechos
    print('Cargando hechos... ')
    motor = MotorLogico(comentarios=False)
    motor.generar_hechos('partido',lista_prolog)
    print(f'Cargados {len(lista_prolog)} hechos de tipo "partido/9"\n')

    # Cargar reglas
    print('Cargando reglas... ')
    REGLAS_PROLOG = json.load(open('REGLAS.json'))['REGLAS_PROLOG']
    directiva = REGLAS_PROLOG[0].replace(':- ', '').replace('.', '')
    # La primera línea es una directiva de consulta inicial

    print(f'Ejecutando directiva: {directiva}')
    list(motor.consultar(directiva))

    # Se cargan las demás reglas
    for regla in REGLAS_PROLOG[1:]:
        motor.agregar_regla(regla)
    print('Reglas cargadas\n')

    # Ejemplo consultas
    print('--- Consultas ---')
    consultas.consultar(motor)
    
    print("Las remontadas ganadas por Quilmes: " + consultas.remontadas_ganadas(motor, 'tu vieja').__str__())

    tabla_equipo = consultas.tabla_equipo(motor, 'quilmes')
    print(json.dumps(tabla_equipo[0], indent=2))

