import json
from motor_logico import MotorLogico

# 1️⃣ Crear motor Prolog
motor = MotorLogico()

# 2️⃣ Leer datos desde JSON
with open("datos.json", encoding="utf-8") as f:
    datos = json.load(f)

# 3️⃣ Generar hechos dinámicos
motor.generar_hechos("persona", datos["personas"])
motor.generar_hechos("curso", datos["cursos"])

# 4️⃣ Agregar reglas lógicas (estadísticas o inferencias)
motor.agregar_regla("vive_en_rosario(X) :- persona(X, _, rosario)")
motor.agregar_regla("curso_grande(C) :- curso(C, N), N > 40")

# 5️⃣ Consultar estadísticas
print("\n=== Personas que viven en Rosario ===")
for r in motor.consultar("vive_en_rosario(X)"):
    print(" →", r["X"])

print("\n=== Cursos grandes (más de 40 alumnos) ===")
for r in motor.consultar("curso_grande(C)"):
    print(" →", r["C"])

# 6️⃣ Ejemplo de consulta agregada (contar cuántos hechos hay)
personas = motor.listar_hechos("pepes", 3)
cantidad = len(personas)
print(f"\nTotal de personas cargadas: {cantidad}")
print(personas)
