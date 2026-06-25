import json
import time
import uuid
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from prolog_interface import PrologInterface

app = Flask(__name__)
CORS(app)

prolog = PrologInterface()

# ---------------------------------------------------------------------------
# Estado global de la simulacion
# ---------------------------------------------------------------------------

estado_simulacion = {}
historial_simulaciones = []


def estado_inicial():
    paquetes_prolog = prolog.obtener_todos_los_paquetes()
    obstaculos = prolog.obtener_obstaculos()
    zonas = prolog.obtener_zonas_entrega()
    dimension = prolog.obtener_dimension()

    robots = [
        {
            'id': 'r1',
            'fila': 1,
            'columna': 1,
            'lleva_paquete': False,
            'paquete_id': None
        }
    ]

    paquetes = [
        {
            'id': p['id'],
            'fila': p['fila'],
            'columna': p['columna'],
            'zona': p['zona'],
            'entregado': False,
            'recogido': False
        }
        for p in paquetes_prolog
    ]

    return {
        'simulacion_id': str(uuid.uuid4()),
        'activa': False,
        'pausada': False,
        'completada': False,
        'inicio': None,
        'robots': robots,
        'paquetes': paquetes,
        'obstaculos': obstaculos,
        'zonas_entrega': zonas,
        'dimension': dimension,
        'movimientos': 0,
        'entregas': 0,
        'acciones_log': []
    }


def calcular_destino(robot: dict, paquetes: list, zonas: list) -> tuple[int, int]:
    if robot['lleva_paquete'] and robot['paquete_id']:
        zona_info = prolog.zona_de_paquete(robot['paquete_id'])
        if zona_info:
            return zona_info['fila'], zona_info['columna']
        return 1, 1

    pendientes = [p for p in paquetes if not p['entregado'] and not p['recogido']]
    if pendientes:
        p = pendientes[0]
        return p['fila'], p['columna']

    return robot['fila'], robot['columna']


def aplicar_accion(robot: dict, accion: str, paquetes: list) -> dict:
    log = {'robot': robot['id'], 'accion': accion, 'resultado': 'ok'}

    if accion == 'mover_arriba':
        robot['fila'] -= 1

    elif accion == 'mover_abajo':
        robot['fila'] += 1

    elif accion == 'mover_izquierda':
        robot['columna'] -= 1

    elif accion == 'mover_derecha':
        robot['columna'] += 1

    elif accion == 'recoger_paquete':
        for p in paquetes:
            if (p['fila'] == robot['fila'] and p['columna'] == robot['columna']
                    and not p['recogido'] and not p['entregado']):
                p['recogido'] = True
                robot['lleva_paquete'] = True
                robot['paquete_id'] = p['id']
                log['paquete'] = p['id']
                break

    elif accion == 'entregar_paquete':
        if robot['lleva_paquete'] and robot['paquete_id']:
            for p in paquetes:
                if p['id'] == robot['paquete_id']:
                    p['entregado'] = True
                    p['recogido'] = False
                    log['paquete'] = p['id']
                    break
            robot['lleva_paquete'] = False
            robot['paquete_id'] = None

    elif accion == 'esperar':
        log['resultado'] = 'espera'

    return log


# ---------------------------------------------------------------------------
# ENDPOINTS
# ---------------------------------------------------------------------------

@app.route('/api/simulacion/iniciar', methods=['POST'])
def iniciar_simulacion():
    global estado_simulacion

    estado_simulacion = estado_inicial()
    estado_simulacion['activa'] = True
    estado_simulacion['inicio'] = time.time()

    return jsonify({
        'simulacion_id': estado_simulacion['simulacion_id'],
        'estado': _estado_publico()
    })


@app.route('/api/simulacion/paso', methods=['GET'])
def ejecutar_paso():
    global estado_simulacion

    if not estado_simulacion:
        return jsonify({'error': 'No hay simulacion activa'}), 400

    if estado_simulacion.get('pausada') or estado_simulacion.get('completada'):
        return jsonify({'estado': _estado_publico(), 'completado': estado_simulacion.get('completada', False)})

    acciones_ejecutadas = []

    for robot in estado_simulacion['robots']:
        dest_f, dest_c = calcular_destino(robot, estado_simulacion['paquetes'], estado_simulacion['zonas_entrega'])

        lleva = 'si' if robot['lleva_paquete'] else 'no'
        pid = robot['paquete_id'] if robot['paquete_id'] else 'ninguno'

        accion = prolog.decidir_accion(
            robot['fila'], robot['columna'],
            lleva, pid,
            dest_f, dest_c
        )

        # Prolog usa hechos estaticos para recoger_paquete; verificar contra estado real
        if accion == 'recoger_paquete':
            paquete_disponible = any(
                p['fila'] == robot['fila'] and p['columna'] == robot['columna']
                and not p['recogido'] and not p['entregado']
                for p in estado_simulacion['paquetes']
            )
            if not paquete_disponible:
                accion = prolog.siguiente_movimiento(
                    robot['fila'], robot['columna'], dest_f, dest_c
                )

        log = aplicar_accion(robot, accion, estado_simulacion['paquetes'])
        acciones_ejecutadas.append(log)
        estado_simulacion['acciones_log'].append(log)

        if accion not in ('esperar',):
            estado_simulacion['movimientos'] += 1

        if accion == 'entregar_paquete':
            estado_simulacion['entregas'] += 1

    pendientes = [p for p in estado_simulacion['paquetes'] if not p['entregado']]
    if not pendientes:
        estado_simulacion['completada'] = True
        estado_simulacion['activa'] = False
        _guardar_en_historial('completada')

    return jsonify({
        'acciones': acciones_ejecutadas,
        'estado': _estado_publico(),
        'completado': estado_simulacion.get('completada', False)
    })


@app.route('/api/simulacion/pausar', methods=['POST'])
def pausar_simulacion():
    if not estado_simulacion:
        return jsonify({'error': 'No hay simulacion activa'}), 400

    estado_simulacion['pausada'] = not estado_simulacion.get('pausada', False)
    return jsonify({'pausado': estado_simulacion['pausada']})


@app.route('/api/simulacion/reiniciar', methods=['POST'])
def reiniciar_simulacion():
    global estado_simulacion

    if estado_simulacion and estado_simulacion.get('activa'):
        _guardar_en_historial('cancelada')

    estado_simulacion = estado_inicial()
    estado_simulacion['activa'] = True
    estado_simulacion['inicio'] = time.time()

    return jsonify({'estado': _estado_publico()})


@app.route('/api/estadisticas', methods=['GET'])
def obtener_estadisticas():
    if not estado_simulacion:
        return jsonify({'movimientos': 0, 'entregas': 0, 'pendientes': 0,
                        'tiempo_segundos': 0, 'eficiencia': 0})

    inicio = estado_simulacion.get('inicio')
    tiempo = round(time.time() - inicio, 1) if inicio else 0
    movimientos = estado_simulacion.get('movimientos', 0)
    entregas = estado_simulacion.get('entregas', 0)
    total_paquetes = len(estado_simulacion.get('paquetes', []))
    pendientes = total_paquetes - entregas

    eficiencia = 0
    if movimientos > 0:
        eficiencia = round((entregas / movimientos) * 100, 2)

    return jsonify({
        'movimientos': movimientos,
        'entregas': entregas,
        'pendientes': pendientes,
        'tiempo_segundos': tiempo,
        'eficiencia': eficiencia
    })


@app.route('/api/historial', methods=['GET'])
def obtener_historial():
    return jsonify(historial_simulaciones)


@app.route('/api/mapa/inicial', methods=['GET'])
def obtener_mapa_inicial():
    data = {
        'dimension': prolog.obtener_dimension(),
        'obstaculos': prolog.obtener_obstaculos(),
        'paquetes': prolog.obtener_todos_los_paquetes(),
        'zonas_entrega': prolog.obtener_zonas_entrega(),
        'robots': [{'id': 'r1', 'fila': 1, 'columna': 1}]
    }
    return jsonify(data)


# ---------------------------------------------------------------------------
# FUNCIONES INTERNAS
# ---------------------------------------------------------------------------

def _estado_publico() -> dict:
    return {
        'simulacion_id': estado_simulacion.get('simulacion_id'),
        'activa': estado_simulacion.get('activa'),
        'pausada': estado_simulacion.get('pausada'),
        'completada': estado_simulacion.get('completada'),
        'robots': estado_simulacion.get('robots', []),
        'paquetes': estado_simulacion.get('paquetes', []),
        'obstaculos': estado_simulacion.get('obstaculos', []),
        'zonas_entrega': estado_simulacion.get('zonas_entrega', []),
        'dimension': estado_simulacion.get('dimension', {}),
        'movimientos': estado_simulacion.get('movimientos', 0),
        'entregas': estado_simulacion.get('entregas', 0)
    }


def _guardar_en_historial(resultado: str):
    inicio = estado_simulacion.get('inicio')
    tiempo = round(time.time() - inicio, 1) if inicio else 0
    historial_simulaciones.append({
        'id': estado_simulacion.get('simulacion_id', ''),
        'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'movimientos': estado_simulacion.get('movimientos', 0),
        'entregas': estado_simulacion.get('entregas', 0),
        'tiempo_segundos': tiempo,
        'resultado': resultado
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)