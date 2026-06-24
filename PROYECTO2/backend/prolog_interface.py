import os
from pyswip import Prolog, Atom


class PrologInterface:
    def __init__(self):
        self.prolog = Prolog()
        kb_path = os.path.join(os.path.dirname(__file__), '..', 'prolog', 'warehouse.pl')
        kb_path = os.path.abspath(kb_path).replace('\\', '/')
        self.prolog.consult(kb_path)

    def consultar(self, query: str) -> list:
        try:
            return list(self.prolog.query(query))
        except Exception as e:
            print(f"Error en consulta Prolog: {e} | Query: {query}")
            return []

    def decidir_accion(self, robot_f: int, robot_c: int, lleva_paquete: str,
                       paquete_id: str, dest_f: int, dest_c: int) -> str:
        paquete_atom = paquete_id if paquete_id != 'ninguno' else 'ninguno'
        query = (
            f"decidir_accion({robot_f}, {robot_c}, {lleva_paquete}, "
            f"{paquete_atom}, {dest_f}, {dest_c}, Accion)"
        )
        resultados = self.consultar(query)
        if resultados:
            accion = resultados[0].get('Accion', 'esperar')
            if isinstance(accion, Atom):
                return str(accion)
            return str(accion)
        return 'esperar'

    def puede_recoger(self, robot_f: int, robot_c: int) -> str | None:
        query = f"puede_recoger({robot_f}, {robot_c}, PaqueteID)"
        resultados = self.consultar(query)
        if resultados:
            pid = resultados[0].get('PaqueteID', None)
            return str(pid) if pid else None
        return None

    def puede_entregar(self, robot_f: int, robot_c: int, paquete_id: str) -> bool:
        query = f"puede_entregar({robot_f}, {robot_c}, {paquete_id})"
        return len(self.consultar(query)) > 0

    def zona_de_paquete(self, paquete_id: str) -> dict | None:
        query = f"zona_de_paquete({paquete_id}, ZonaID, ZonaF, ZonaC)"
        resultados = self.consultar(query)
        if resultados:
            r = resultados[0]
            return {
                'zona_id': str(r['ZonaID']),
                'fila': int(r['ZonaF']),
                'columna': int(r['ZonaC'])
            }
        return None

    def posicion_inicial_robot(self, robot_id: str) -> dict | None:
        query = f"posicion_inicial_robot({robot_id}, F, C)"
        resultados = self.consultar(query)
        if resultados:
            r = resultados[0]
            return {'fila': int(r['F']), 'columna': int(r['C'])}
        return None

    def posicion_inicial_paquete(self, paquete_id: str) -> dict | None:
        query = f"posicion_inicial_paquete({paquete_id}, F, C)"
        resultados = self.consultar(query)
        if resultados:
            r = resultados[0]
            return {'fila': int(r['F']), 'columna': int(r['C'])}
        return None

    def obtener_todos_los_paquetes(self) -> list:
        query = "paquete(PID, F, C, ZonaID)"
        resultados = self.consultar(query)
        return [
            {
                'id': str(r['PID']),
                'fila': int(r['F']),
                'columna': int(r['C']),
                'zona': str(r['ZonaID'])
            }
            for r in resultados
        ]

    def obtener_obstaculos(self) -> list:
        query = "obstaculo(F, C)"
        resultados = self.consultar(query)
        return [{'fila': int(r['F']), 'columna': int(r['C'])} for r in resultados]

    def obtener_zonas_entrega(self) -> list:
        query = "zona_entrega(ZID, F, C)"
        resultados = self.consultar(query)
        return [
            {'id': str(r['ZID']), 'fila': int(r['F']), 'columna': int(r['C'])}
            for r in resultados
        ]

    def obtener_dimension(self) -> dict:
        query = "dimension(MaxF, MaxC)"
        resultados = self.consultar(query)
        if resultados:
            r = resultados[0]
            return {'filas': int(r['MaxF']), 'columnas': int(r['MaxC'])}
        return {'filas': 10, 'columnas': 10}