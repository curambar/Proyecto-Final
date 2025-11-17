import json
import threading

class ConsultasLiga:
    """Clase para realizar consultas sobre los partidos de la liga usando el motor lógico"""
    
    def __init__(self, motor):
        """
        Inicializa la clase con el motor lógico cargado
        
        Args:
            motor (MotorLogico): el motor lógico con hechos y reglas cargadas
        """
        self.motor = motor
        # Lock para serializar acceso al motor Prolog (no thread-safe)
        self._lock = threading.Lock()
    
    def _safe_consultar(self, consulta):
        """Wrapper que serializa las consultas al motor Prolog."""
        with self._lock:
            return self.motor.consultar(consulta)
    
    def tabla_equipo(self, equipo_nombre):
        """
        Obtiene las estadísticas completas de un equipo en la tabla
        
        Args:
            equipo_nombre (string): nombre del equipo a consultar
            
        Returns:
            dict: estadísticas del equipo o None si no existe
        """
        consulta = f"tabla_equipo('{equipo_nombre}', PJ, PG, PE, PP, GF, GC, DG, Puntos)."
        resultados = self._safe_consultar(consulta)
        return resultados[0] if resultados else None

    def equipos_participantes(self):
        """ 
        Devuelve una lista con los nombres de todos los equipos que participaron en la liga.
        
        Returns:
            list: lista de nombres de equipos
        """
        consulta_equipos = "setof(Equipo, partido_jugado(Equipo), Equipos)."
        resultado_equipos = self._safe_consultar(consulta_equipos)
        return resultado_equipos[0]['Equipos'] if resultado_equipos else []

    def remontadas_ganadas(self, equipo_nombre):
        """
        Devuelve cantidad de remontadas realizadas por un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo a consultar

        Returns:
            int: cantidad de remontadas ganadas por el equipo
        """
        resultado_remontada = self._safe_consultar(f"total_remontadas_ganadas('{equipo_nombre}', N).")
        return resultado_remontada[0]['N'] if resultado_remontada else 0

    def tabla_completa(self):
        """
        Obtiene la tabla completa de posiciones de la liga
        
        Returns:
            list: lista de diccionarios con estadísticas de todos los equipos
        """
        equipos = self.equipos_participantes()
        tabla = []
        
        for equipo in equipos:
            stats = self.tabla_equipo(equipo)
            if stats:
                stats['equipo'] = equipo
                tabla.append(stats)
        
        # Ordenar por puntos (descendente) y diferencia de goles (descendente)
        tabla_ordenada = sorted(tabla, key=lambda x: (x['Puntos'], x['DG']), reverse=True)
        return tabla_ordenada

    def partidos_jugados_por_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de partidos jugados por un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de partidos jugados
        """
        consulta = f"partidos_jugados('{equipo_nombre}', PJ)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['PJ'] if resultado else 0

    def victorias_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de victorias de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de victorias
        """
        consulta = f"total_ganados('{equipo_nombre}', PG)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['PG'] if resultado else 0

    def empates_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de empates de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de empates
        """
        consulta = f"total_empatados('{equipo_nombre}', PE)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['PE'] if resultado else 0

    def derrotas_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de derrotas de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de derrotas
        """
        consulta = f"total_perdidos('{equipo_nombre}', PP)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['PP'] if resultado else 0

    def goles_favor_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de goles a favor de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de goles a favor
        """
        consulta = f"total_gf('{equipo_nombre}', GF)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['GF'] if resultado else 0

    def goles_contra_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de goles en contra de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de goles en contra
        """
        consulta = f"total_gc('{equipo_nombre}', GC)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['GC'] if resultado else 0

    def diferencia_goles_equipo(self, equipo_nombre):
        """
        Devuelve la diferencia de goles de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: diferencia de goles (GF - GC)
        """
        consulta = f"diferencia_goles('{equipo_nombre}', DG)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['DG'] if resultado else 0

    def puntos_equipo(self, equipo_nombre):
        """
        Devuelve los puntos totales de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: puntos totales
        """
        consulta = f"total_puntos('{equipo_nombre}', Puntos)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['Puntos'] if resultado else 0

    def estadisticas_generales(self):
        """
        Devuelve estadísticas generales de toda la liga
        
        Returns:
            dict: estadísticas generales (victorias locales, visitantes, empates)
        """
        victorias_locales = self.motor.consultar("total_victorias_locales(N).")
        victorias_visitantes = self.motor.consultar("total_victorias_visitantes(N).")
        empates = self.motor.consultar("total_empates(N).")
        
        return {
            'victorias_locales': victorias_locales[0]['N'] if victorias_locales else 0,
            'victorias_visitantes': victorias_visitantes[0]['N'] if victorias_visitantes else 0,
            'empates': empates[0]['N'] if empates else 0,
            'total_partidos': (victorias_locales[0]['N'] if victorias_locales else 0) + 
                             (victorias_visitantes[0]['N'] if victorias_visitantes else 0) + 
                             (empates[0]['N'] if empates else 0)
        }

    def vallas_invictas_equipo(self, equipo_nombre):
        """
        Devuelve la cantidad de vallas invictas de un equipo
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            int: cantidad de vallas invictas
        """
        consulta = f"total_vallas_invictas('{equipo_nombre}', N)."
        resultado = self._safe_consultar(consulta)
        return resultado[0]['N'] if resultado else 0

    def equipos_con_valla_invicta(self):
        """
        Devuelve los equipos que tienen al menos una valla invicta
        
        Returns:
            list: lista de equipos con valla invicta
        """
        # Consulta para encontrar equipos únicos con valla invicta
        equipos_valla = set()
        
        # Buscar en partidos como local
        consulta_local = "partido(_, _, _, Equipo, _, _, _, _, 0)."
        resultados_local = self.motor.consultar(consulta_local)
        for resultado in resultados_local:
            equipos_valla.add(resultado['Equipo'])
        
        # Buscar en partidos como visitante
        consulta_visitante = "partido(_, _, _, _, _, _, Equipo, _, 0)."
        resultados_visitante = self.motor.consultar(consulta_visitante)
        for resultado in resultados_visitante:
            equipos_valla.add(resultado['Equipo'])
        
        return list(equipos_valla)

    def partidos_por_ronda(self, ronda):
        """
        Devuelve los partidos de una ronda específica
        
        Args:
            ronda (string): nombre de la ronda (ej: 'Regular Season - 1')
            
        Returns:
            list: lista de partidos de esa ronda
        """
        consulta = f"partido(Id, '{ronda}', Fecha, Local, GL_HT, GL_FT, Visitante, GV_HT, GV_FT)."
        return self.motor.consultar(consulta)

    def buscar_partido_por_id(self, partido_id):
        """
        Busca un partido por su ID y retorna su informacion en formato lista 
        (se recomienda pasar a formato JSON)
        
        Args:
            partido_id (int): ID del partido
            
        Returns:
            dict: información del partido o None si no existe
        """
        consulta = f"partido({partido_id}, Ronda, Fecha, Local, GL_HT, GL_FT, Visitante, GV_HT, GV_FT)."
        resultados = self.motor.consultar(consulta)
        return resultados[0] if resultados else None

    def resumen_equipo(self, equipo_nombre):
        """
        Devuelve un resumen completo de las estadísticas de un equipo retorna su informacion en formato lista 
        (se recomienda pasar a formato JSON)
        
        Args:
            equipo_nombre (string): nombre del equipo
            
        Returns:
            dict: resumen completo del equipo
        """
        return {
            'equipo': equipo_nombre,
            'partidos_jugados': self.partidos_jugados_por_equipo(equipo_nombre),
            'victorias': self.victorias_equipo(equipo_nombre),
            'empates': self.empates_equipo(equipo_nombre),
            'derrotas': self.derrotas_equipo(equipo_nombre),
            'goles_favor': self.goles_favor_equipo(equipo_nombre),
            'goles_contra': self.goles_contra_equipo(equipo_nombre),
            'diferencia_goles': self.diferencia_goles_equipo(equipo_nombre),
            'puntos': self.puntos_equipo(equipo_nombre),
            'remontadas_ganadas': self.remontadas_ganadas(equipo_nombre),
            'vallas_invictas': self.vallas_invictas_equipo(equipo_nombre)
        }
        
        
    def formato_json(self, datos):
        """
        Convierte una lista de diccionarios al formato JSON formateado
        
        Args:
            datos (list): lista de diccionarios
            
        Returns:
            str: representación JSON formateada
        """
        return json.dumps(datos, indent=2)
    
    
    def consultar(self):
        """Consultas generales preprogramadas
        """
        
        print('\n[Consulta 1] Estadisticas de Tigre:')
        resultado_tigre = self.tabla_equipo(self.motor, 'tigre')
        if resultado_tigre:
            print(self.formato_json([resultado_tigre]))
        else:
            print('No se encontro Tigre')

        # ------------- Otras consultas de ejemplo -------------

        print("\n[Consulta 2] Total de victorias locales:")
        resultado_locales = self.motor.consultar("total_victorias_locales(N).")
        if resultado_locales:
            print(f"Hubo {resultado_locales[0]['N']} victorias locales.")
            
        # -----------------------------------------------------
        lista_de_equipos = self.equipos_participantes()

        for equipo in lista_de_equipos:
            print(f"\n[Consulta 3] Remontadas de {equipo.title()}:")
            print(f"{equipo.title()} logró {self.remontadas_ganadas(equipo)} remontadas.")

        # -----------------------------------------------------

        print("\n[Consulta 4] Lista de todos los equipos participantes:")
        if len(lista_de_equipos) > 0:
            print(f"Se encontraron {len(lista_de_equipos)} equipos:")
            for equipo in lista_de_equipos:
                print(equipo)
        else:
            print("No se pudieron encontrar equipos.")