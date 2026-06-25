import os
from pyswip import Prolog, Atom

# ---------------------------------------------------------------------------
# Configuraciones de mapa por nivel de dificultad
# ---------------------------------------------------------------------------

DIFICULTADES = {
    'facil': {
        'dimension': (8, 8),
        'obstaculos': [
            (2, 3), (3, 6), (4, 2), (5, 5), (6, 7), (7, 4)
        ],
        'paquetes': [
            ('p1', 1, 4, 'zona1'),
            ('p2', 4, 7, 'zona2'),
            ('p3', 7, 2, 'zona1'),
        ],
        'zonas': [
            ('zona1', 1, 8),
            ('zona2', 8, 8),
        ],
        'robots': [('r1', 1, 1)],
    },
    'medio': {
        'dimension': (10, 10),
        'obstaculos': [
            (2, 2), (2, 3), (3, 6), (4, 4), (5, 8),
            (6, 2), (7, 5), (8, 3), (9, 7)
        ],
        'paquetes': [
            ('p1', 1, 4, 'zona1'),
            ('p2', 3, 8, 'zona2'),
            ('p3', 5, 2, 'zona1'),
            ('p4', 7, 9, 'zona2'),
            ('p5', 9, 1, 'zona1'),
        ],
        'zonas': [
            ('zona1', 1, 10),
            ('zona2', 10, 10),
        ],
        'robots': [('r1', 1, 1)],
    },
    'dificil': {
        'dimension': (12, 12),
        'obstaculos': [
            (2, 4), (2, 9), (3, 2), (3, 7), (4, 5),
            (4, 11), (5, 3), (5, 9), (6, 6), (7, 4),
            (7, 10), (8, 2), (8, 8), (9, 5), (10, 3)
        ],
        'paquetes': [
            ('p1', 1, 3,  'zona1'),
            ('p2', 3, 11, 'zona2'),
            ('p3', 6, 8,  'zona3'),
            ('p4', 8, 1,  'zona1'),
            ('p5', 10, 11, 'zona2'),
            ('p6', 12, 5, 'zona3'),
            ('p7', 5, 6,  'zona2'),
        ],
        'zonas': [
            ('zona1', 1,  12),
            ('zona2', 12, 12),
            ('zona3', 12, 1),
        ],
        'robots': [('r1', 1, 1)],
    },
}


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

    def siguiente_movimiento(self, robot_f: int, robot_c: int,
                             dest_f: int, dest_c: int) -> str:
        """Consulta directamente el BFS de Prolog para navegar sin recoger."""
        query = f"siguiente_movimiento({robot_f}, {robot_c}, {dest_f}, {dest_c}, Accion)"
        resultados = self.consultar(query)
        if resultados:
            accion = resultados[0].get('Accion', 'esperar')
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

    def cargar_dificultad(self, nivel: str) -> bool:
        """Reemplaza los hechos del mapa en Prolog segun el nivel de dificultad."""
        config = DIFICULTADES.get(nivel)
        if not config:
            return False

        # Borrar hechos existentes del mapa
        self.prolog.retractall('dimension(_, _)')
        self.prolog.retractall('obstaculo(_, _)')
        self.prolog.retractall('paquete(_, _, _, _)')
        self.prolog.retractall('zona_entrega(_, _, _)')
        self.prolog.retractall('robot(_, _, _)')

        # Cargar nuevos hechos
        filas, cols = config['dimension']
        self.prolog.assertz(f'dimension({filas}, {cols})')

        for (f, c) in config['obstaculos']:
            self.prolog.assertz(f'obstaculo({f}, {c})')

        for (pid, f, c, zona) in config['paquetes']:
            self.prolog.assertz(f'paquete({pid}, {f}, {c}, {zona})')

        for (zid, f, c) in config['zonas']:
            self.prolog.assertz(f'zona_entrega({zid}, {f}, {c})')

        for (rid, f, c) in config['robots']:
            self.prolog.assertz(f'robot({rid}, {f}, {c})')

        return True

    def obtener_dificultades(self) -> list:
        return list(DIFICULTADES.keys())