import json
from motor_logico import MotorLogico
from procesador import procesar_partidos, establecer_formato_partidos
from consultas import ConsultasLiga

class SetUp:  
            
    def __init__(self, archivo):
        partidos_data = procesar_partidos(archivo)
        if partidos_data is None:
            print(f"ERROR: No se pudo cargar la data desde '{archivo}'. Abortando inicialización.")
            return
        
        # Formatear datos para prolog
        lista_prolog = establecer_formato_partidos(partidos_data)

        # Cargar hechos
        self.motor = MotorLogico(comentarios=False)
        self.motor.generar_hechos('partido',lista_prolog)
        
        archivo_reglas = 'json/REGLAS.json'
        try:
            with open(archivo_reglas, 'r') as f:
                REGLAS_PROLOG = json.load(f)['REGLAS_PROLOG']
        except FileNotFoundError:
            print(f"ERROR: Archivo de reglas '{archivo_reglas}' no encontrado.")
            return 
        
        directiva = REGLAS_PROLOG[0].replace(':- ', '').replace('.', '')
        # La primera línea es una directiva de consulta inicial

        print(f'Ejecutando directiva: {directiva}')
        list(self.motor.consultar(directiva))

        # Se cargan las demás reglas
        for regla in REGLAS_PROLOG[1:]:
            self.motor.agregar_regla(regla)
        print('Reglas cargadas\n')
        
    def obtener_acceso_consultas(self):
        return ConsultasLiga(self.motor)
