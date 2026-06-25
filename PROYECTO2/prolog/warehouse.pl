% warehouse.pl - Base de conocimiento Smart Warehouse
% Inteligencia Artificial 1 - USAC

% ---------------------------------------------------------------------------
% Declaraciones dinamicas: los hechos del mapa se pueden modificar en tiempo
% de ejecucion (retractall/assertz) para soportar distintos niveles de dificultad
% ---------------------------------------------------------------------------

:- dynamic dimension/2.
:- dynamic obstaculo/2.
:- dynamic paquete/4.
:- dynamic zona_entrega/3.
:- dynamic robot/3.

% ---------------------------------------------------------------------------
% HECHOS INICIALES: configuracion por defecto (nivel medio, mapa 10x10)
% Estos hechos se reemplazan dinamicamente al seleccionar otro nivel.
% ---------------------------------------------------------------------------

dimension(10, 10).

% Obstaculos: obstaculo(Fila, Columna) - 9 en total
obstaculo(2, 2).
obstaculo(2, 3).
obstaculo(3, 6).
obstaculo(4, 4).
obstaculo(5, 8).
obstaculo(6, 2).
obstaculo(7, 5).
obstaculo(8, 3).
obstaculo(9, 7).

% Paquetes: paquete(ID, FilaInicial, ColumnaInicial, ZonaEntrega) - 5 en total
paquete(p1, 1, 4, zona1).
paquete(p2, 3, 8, zona2).
paquete(p3, 5, 2, zona1).
paquete(p4, 7, 9, zona2).
paquete(p5, 9, 1, zona1).

% Zonas de entrega: zona_entrega(ID, Fila, Columna) - 2 en total
zona_entrega(zona1, 1, 9).
zona_entrega(zona2, 9, 9).

% Robots: robot(ID, FilaInicial, ColumnaInicial) - 1 en total
robot(r1, 1, 1).

% ---------------------------------------------------------------------------
% REGLAS DE INFERENCIA
% ---------------------------------------------------------------------------

% Regla 1: Verificar si una casilla es valida (dentro del mapa y sin obstaculo)
casilla_valida(F, C) :-
    dimension(MaxF, MaxC),
    F > 0, F =< MaxF,
    C > 0, C =< MaxC,
    \+ obstaculo(F, C).

% Regla 2: El robot puede moverse arriba
puede_mover_arriba(F, C, NF, C) :-
    NF is F - 1,
    casilla_valida(NF, C).

% Regla 3: El robot puede moverse abajo
puede_mover_abajo(F, C, NF, C) :-
    NF is F + 1,
    casilla_valida(NF, C).

% Regla 4: El robot puede moverse a la izquierda
puede_mover_izquierda(F, C, F, NC) :-
    NC is C - 1,
    casilla_valida(F, NC).

% Regla 5: El robot puede moverse a la derecha
puede_mover_derecha(F, C, F, NC) :-
    NC is C + 1,
    casilla_valida(F, NC).

% Regla 6: El robot puede recoger un paquete si esta en la misma casilla
puede_recoger(RobotF, RobotC, PaqueteID) :-
    paquete(PaqueteID, RobotF, RobotC, _),
    !.

% Regla 7: El robot puede entregar el paquete si esta en la zona correcta
puede_entregar(RobotF, RobotC, PaqueteID) :-
    paquete(PaqueteID, _, _, ZonaID),
    zona_entrega(ZonaID, RobotF, RobotC),
    !.

% Regla 8: Verificar si una posicion es una zona de entrega
es_zona_entrega(F, C) :-
    zona_entrega(_, F, C).

% ---------------------------------------------------------------------------
% REGLA PRINCIPAL DE DECISION
% decidir_accion(RobotF, RobotC, LlevaPaquete, PaqueteID, DestF, DestC, Accion)
%   LlevaPaquete: 'si' o 'no'
%   PaqueteID:    ID del paquete que lleva (o 'ninguno')
%   DestF, DestC: coordenadas del destino calculadas por el backend
%   Accion:       accion a ejecutar (variable de salida)
% ---------------------------------------------------------------------------

% Caso 1: Lleva paquete y ya esta en la zona de entrega -> entregar
decidir_accion(RobotF, RobotC, si, PaqueteID, _, _, entregar_paquete) :-
    puede_entregar(RobotF, RobotC, PaqueteID),
    !.

% Caso 2: No lleva paquete y hay uno en su posicion -> recoger
decidir_accion(RobotF, RobotC, no, _, _, _, recoger_paquete) :-
    puede_recoger(RobotF, RobotC, _),
    !.

% Caso 3: Ya esta en el destino -> esperar
decidir_accion(F, C, _, _, F, C, esperar) :- !.

% Caso 4: Navegar hacia el destino usando BFS para evadir obstaculos
decidir_accion(RobotF, RobotC, _, _, DestF, DestC, Accion) :-
    siguiente_movimiento(RobotF, RobotC, DestF, DestC, Accion),
    !.

% Caso fallback: no hay camino posible -> esperar
decidir_accion(_, _, _, _, _, _, esperar).

% ---------------------------------------------------------------------------
% BFS: Busqueda en anchura para encontrar el camino mas corto evitando obstaculos
% siguiente_movimiento(InicioF, InicioC, DestF, DestC, Accion)
%   Retorna la primera accion del camino optimo hacia el destino.
%   Usa BFS para garantizar camino minimo y correcto manejo de obstaculos.
% ---------------------------------------------------------------------------

siguiente_movimiento(InicioF, InicioC, DestF, DestC, Accion) :-
    bfs_buscar([[InicioF, InicioC, none]], DestF, DestC, [InicioF-InicioC], Accion).

% BFS: caso base - se llego al destino con una primera accion definida
bfs_buscar([[DestF, DestC, Accion]|_], DestF, DestC, _, Accion) :-
    Accion \= none, !.

% BFS: caso recursivo - expandir el nodo actual y encolar vecinos
bfs_buscar([[F, C, PrimerAccion]|Cola], DestF, DestC, Visitados, Resultado) :-
    findall([NF, NC, PA], (
        movimiento_bfs(F, C, NF, NC, Act),
        \+ member(NF-NC, Visitados),
        (PrimerAccion = none -> PA = Act ; PA = PrimerAccion)
    ), Hijos),
    findall(NF-NC, member([NF, NC, _], Hijos), NuevosVisitados),
    append(Visitados, NuevosVisitados, TodosVisitados),
    append(Cola, Hijos, ColaNueva),
    bfs_buscar(ColaNueva, DestF, DestC, TodosVisitados, Resultado).

% Movimientos validos para la expansion BFS (usa las mismas reglas base)
movimiento_bfs(F, C, NF, C, mover_arriba)    :- puede_mover_arriba(F, C, NF, C).
movimiento_bfs(F, C, NF, C, mover_abajo)     :- puede_mover_abajo(F, C, NF, C).
movimiento_bfs(F, C, F, NC, mover_izquierda) :- puede_mover_izquierda(F, C, F, NC).
movimiento_bfs(F, C, F, NC, mover_derecha)   :- puede_mover_derecha(F, C, F, NC).

% ---------------------------------------------------------------------------
% UTILIDADES AUXILIARES
% ---------------------------------------------------------------------------

% Obtener lista de todos los paquetes definidos
todos_los_paquetes(Lista) :-
    findall(PID, paquete(PID, _, _, _), Lista).

% Obtener la zona de entrega de un paquete
zona_de_paquete(PaqueteID, ZonaID, ZonaF, ZonaC) :-
    paquete(PaqueteID, _, _, ZonaID),
    zona_entrega(ZonaID, ZonaF, ZonaC).

% Verificar si la lista de paquetes pendientes esta vacia (simulacion completa)
simulacion_completada([]) :- !.

% Obtener posicion inicial de un robot
posicion_inicial_robot(RobotID, F, C) :-
    robot(RobotID, F, C).

% Obtener posicion inicial de un paquete
posicion_inicial_paquete(PaqueteID, F, C) :-
    paquete(PaqueteID, F, C, _).