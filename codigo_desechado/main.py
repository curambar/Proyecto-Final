import json
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_partidos
import codigo_desechado.consultas as consultas

if __name__ == "__main__":
    # Cargar datos
    archivo = 'primera2021.json'
    partidos_data = procesar_partidos(archivo)

    # Formatear datos para prolog
    lista_prolog = establecer_formato_partidos(partidos_data)

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
    # print('--- Consultas ---')
    # consultas.consultar(motor)
    