% ============================================================
% Base de conocimiento: Rutas entre ciudades de Guatemala
% Sistema de rutas mas cortas
% ============================================================

:- dynamic conexion/3.

% ------------------------------------------------------------
% Hechos: conexion(CiudadOrigen, CiudadDestino, DistanciaKm)
% Las conexiones son unidireccionales; la simetria se
% maneja mediante la regla camino/3.
% ------------------------------------------------------------

conexion(guatemala,      escuintla,       64).
conexion(guatemala,      antigua,         45).
conexion(guatemala,      chimaltenango,   54).
conexion(guatemala,      zacapa,         148).
conexion(guatemala,      jalapa,         113).
conexion(antigua,        chimaltenango,   18).
conexion(antigua,        escuintla,       58).
conexion(escuintla,      mazatenango,     84).
conexion(chimaltenango,  quetzaltenango, 132).
conexion(chimaltenango,  coban,          175).
conexion(quetzaltenango, huehuetenango,   92).
conexion(quetzaltenango, mazatenango,     60).
conexion(coban,          flores,         264).
conexion(coban,          zacapa,         154).
conexion(zacapa,         puerto_barrios, 175).
conexion(zacapa,         jalapa,          90).
conexion(flores,         puerto_barrios, 380).
conexion(mazatenango,    huehuetenango,  200).

% ------------------------------------------------------------
% camino/3: relacion simetrica sobre conexion/3
% camino(A, B, D) es verdadero si existe conexion directa
% entre A y B con distancia D (en cualquier direccion).
% ------------------------------------------------------------

camino(X, Y, D) :- conexion(X, Y, D).
camino(X, Y, D) :- conexion(Y, X, D).

% ------------------------------------------------------------
% ruta/4: encuentra una ruta entre Origen y Destino.
% ruta(Origen, Destino, Ruta, DistanciaTotal)
% Ruta es la lista de ciudades recorridas (de origen a destino).
% Se evitan ciclos mediante la lista de ciudades Visitadas.
% ------------------------------------------------------------

ruta(Origen, Destino, Ruta, Distancia) :-
    ruta_aux(Origen, Destino, [Origen], RutaInversa, Distancia),
    reverse(RutaInversa, Ruta).

ruta_aux(Destino, Destino, Visitados, Visitados, 0).
ruta_aux(Actual, Destino, Visitados, RutaFinal, Distancia) :-
    camino(Actual, Siguiente, D),
    \+ member(Siguiente, Visitados),
    ruta_aux(Siguiente, Destino, [Siguiente|Visitados], RutaFinal, DistResto),
    Distancia is D + DistResto.

% ------------------------------------------------------------
% ruta_mas_corta/4: determina la ruta con menor distancia total.
% ruta_mas_corta(Origen, Destino, RutaOptima, DistanciaOptima)
% Reune todas las rutas posibles y selecciona la de menor costo.
% ------------------------------------------------------------

ruta_mas_corta(Origen, Destino, RutaOptima, DistanciaOptima) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    Rutas \= [],
    sort(Rutas, [DistanciaOptima-RutaOptima|_]).

% ------------------------------------------------------------
% todas_las_rutas/3: obtiene todas las rutas posibles,
% ordenadas de menor a mayor distancia.
% todas_las_rutas(Origen, Destino, RutasOrdenadas)
% Cada elemento de RutasOrdenadas tiene la forma D-R.
% ------------------------------------------------------------

todas_las_rutas(Origen, Destino, RutasOrdenadas) :-
    findall(D-R, ruta(Origen, Destino, R, D), Rutas),
    sort(Rutas, RutasOrdenadas).

% ------------------------------------------------------------
% todas_ciudades/1: lista todas las ciudades registradas,
% sin duplicados y en orden alfabetico.
% ------------------------------------------------------------

ciudad_registrada(C) :- conexion(C, _, _).
ciudad_registrada(C) :- conexion(_, C, _).

todas_ciudades(Ciudades) :-
    findall(C, ciudad_registrada(C), Lista),
    sort(Lista, Ciudades).

% ------------------------------------------------------------
% ciudad_existe/1: verifica si una ciudad esta en la base.
% ------------------------------------------------------------

ciudad_existe(Ciudad) :-
    ciudad_registrada(Ciudad).

% ------------------------------------------------------------
% agregar_conexion/3: agrega dinamicamente una nueva conexion.
% agregar_conexion(Ciudad1, Ciudad2, Distancia)
% Si la conexion ya existe, no se duplica.
% ------------------------------------------------------------

agregar_conexion(Ciudad1, Ciudad2, Distancia) :-
    ( conexion(Ciudad1, Ciudad2, _) ->
        retract(conexion(Ciudad1, Ciudad2, _))
    ; true ),
    assertz(conexion(Ciudad1, Ciudad2, Distancia)).

% ------------------------------------------------------------
% todas_conexiones/1: lista todos los hechos conexion/3.
% ------------------------------------------------------------

todas_conexiones(Conexiones) :-
    findall(O-D-Dist, conexion(O, D, Dist), Conexiones).
