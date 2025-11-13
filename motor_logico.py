from pyswip import Prolog


class MotorLogico:
    """
        Motor lógico se cominuca con prolog, utilizando métodos para generar hechos mediante una lista
    """
    
    
    def __init__(self, comentarios=True):
        # Este método se ejecuta automáticamente al crear el objeto
        self.prolog = Prolog()
        self.comentarios = comentarios
        #Se inicializa el motor Prolog, el cual permite llemar a MotorLogico.prolog.funcion() para ejecutar el prolog del popio objeto

    def generar_hechos(self, tipo, lista_objetos):
        """
        Genera "tipo" de hechos Prolog a partir de una lista de diccionarios.
        tipo: nombre del predicado (por ej. 'persona' o 'curso')
        lista_objetos: lista de diccionarios con atributos
        """
        print('Cargando hechos...')
        
        for obj in lista_objetos:
            argumentos = ",".join(str(v).lower() for v in obj.values())
            #Se genera una cadena de argumentos que esté separados por comas, convirtiendo cada valor a minúsculas
            
            hecho = f"{tipo}({argumentos})"
            #Se crea el hecho en formato Prolog, con el tipo y los argumentos
            
            self.prolog.assertz(hecho)
            #Se agrega el hecho al motor Prolog del propio objeto
            if self.comentarios is True:
                print(f"[✔] Hecho cargado: {hecho}")
            
        print(f'Cargados {len(lista_objetos)} hechos de tipo "{tipo}/{len(obj.keys())}"\n\n')


    def agregar_regla(self, regla):
        """Genera una nueva regla mediante el formato de <regla :- condición>.<p> 
        Ejemplo: "elite(Jugador) :- PRC(Jugador, Puntaje), Puntaje > promedio."

        Args:
            regla (_type_): un string con la regla en formato Prolog
        """
        self.prolog.assertz(regla)


    def consultar(self, consulta):
        """Genera una consulta y devulve la lista de hechos. <p>
        Ejemplo: "vive_en_rosario(X)"

        Args:
            consulta (_type_): un string con la consulta en formato Prolog
        Returns:
            List: lista de hechos que cumplen la consulta 
        """
        return list(self.prolog.query(consulta))


    def listar_hechos(self, tipo, aridad):
        """Lista todos los hechos de un tipo y su aridad determinados.

        Args:
            tipo (string): un tipo de hecho (predicado) existente
            aridad (int): la cantidad de argumentos del hecho
            
        Cautions: la aridad es la cantidad de argumentos que tiene el hecho.<p> 
        Por ejemplo, persona(Nombre, Edad, Ciudad) tiene aridad 3.


        Returns:
            List: lista de hechos con {X(1): valor1, X(2): valor2, ...} 
        """
        consulta = ",".join([f"X{i}" for i in range(1, aridad + 1)])
        return list(self.prolog.query(f"{tipo}({consulta})"))
