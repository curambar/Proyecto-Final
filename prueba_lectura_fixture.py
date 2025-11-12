import json
from motor_logico import MotorLogico

motor = MotorLogico()

def generar_hechos_fixtures():
    # Leer el archivo JSON
    try:
        with open('primera2021.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            
        # Acceder a la lista de fixtures en 'response'
        fixtures = data.get('response', [])
        
        # Crear instancia del motor lógico
        ids = []
        
        # Generar hechos para cada fixture
        for item in fixtures:
            if 'fixture' in item and 'id' in item['fixture']:
                fixture_id = item['fixture']['id']
                # Crear hecho en formato: fixture(ID).
                ids.append(fixture_id)
        
        motor.generar_hechos("fixture", [{"id": id} for id in ids])
        print("Hechos generados exitosamente")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo primera2021.json")
    except json.JSONDecodeError:
        print("Error: El archivo JSON no tiene un formato válido")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    generar_hechos_fixtures()
    fixtures = motor.consultar("fixture(X)")
    print(fixtures)