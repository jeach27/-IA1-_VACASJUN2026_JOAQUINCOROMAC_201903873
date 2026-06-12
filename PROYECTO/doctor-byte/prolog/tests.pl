% tests.pl
% Consultas de prueba para verificar el correcto funcionamiento de la base de conocimiento.
% Ejecutar desde la consola de SWI-Prolog: ?- consult('tests.pl').
% Luego correr: ?- ejecutar_todas_las_pruebas.

:- consult('knowledge_base.pl').

% ejecutar_todas_las_pruebas/0
% Corre todos los casos de prueba y reporta el resultado de cada uno.
ejecutar_todas_las_pruebas :-
    prueba_cp01,
    prueba_cp02,
    prueba_cp03,
    prueba_cp04,
    prueba_cp05,
    prueba_cp06,
    prueba_cp07,
    prueba_cp08,
    prueba_cp09,
    prueba_cp10,
    write('Todas las pruebas completadas.'), nl.

% CP-01: pantalla negra + no enciende -> falla_fuente_poder
prueba_cp01 :-
    Sintomas = [pantalla_negra, no_enciende],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_fuente_poder, Diagnosticos)
    ->  write('CP-01 PASADO: falla_fuente_poder detectada'), nl
    ;   write('CP-01 FALLIDO: no se detecto falla_fuente_poder'), nl
    ).

% CP-02: lentitud extrema + aplicaciones se cierran -> virus_malware
prueba_cp02 :-
    Sintomas = [lentitud_extrema, aplicaciones_se_cierran_solas],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(virus_malware, Diagnosticos)
    ->  write('CP-02 PASADO: virus_malware detectado'), nl
    ;   write('CP-02 FALLIDO: no se detecto virus_malware'), nl
    ).

% CP-03: sobrecalentamiento + ventilador ruidoso -> sobrecalentamiento_cpu
prueba_cp03 :-
    Sintomas = [sobrecalentamiento, ventilador_muy_ruidoso],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(sobrecalentamiento_cpu, Diagnosticos)
    ->  write('CP-03 PASADO: sobrecalentamiento_cpu detectado'), nl
    ;   write('CP-03 FALLIDO: no se detecto sobrecalentamiento_cpu'), nl
    ).

% CP-04: sonido de pitidos al arranque -> falla_ram
prueba_cp04 :-
    Sintomas = [sonido_pitidos_arranque],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_ram, Diagnosticos)
    ->  write('CP-04 PASADO: falla_ram detectada'), nl
    ;   write('CP-04 FALLIDO: no se detecto falla_ram'), nl
    ).

% CP-05: pantalla azul + reinicio inesperado -> falla_sistema_operativo
prueba_cp05 :-
    Sintomas = [pantalla_azul_muerte, reinicio_inesperado],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_sistema_operativo, Diagnosticos)
    ->  write('CP-05 PASADO: falla_sistema_operativo detectada'), nl
    ;   write('CP-05 FALLIDO: no se detecto falla_sistema_operativo'), nl
    ).

% CP-06: no reconoce disco -> falla_disco_duro
prueba_cp06 :-
    Sintomas = [no_reconoce_disco],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_disco_duro, Diagnosticos)
    ->  write('CP-06 PASADO: falla_disco_duro detectada'), nl
    ;   write('CP-06 FALLIDO: no se detecto falla_disco_duro'), nl
    ).

% CP-07: sin sonido -> falla_drivers
prueba_cp07 :-
    Sintomas = [sin_sonido],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_drivers, Diagnosticos)
    ->  write('CP-07 PASADO: falla_drivers detectada'), nl
    ;   write('CP-07 FALLIDO: no se detecto falla_drivers'), nl
    ).

% CP-08: red no conecta -> falla_drivers
prueba_cp08 :-
    Sintomas = [red_no_conecta],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_drivers, Diagnosticos)
    ->  write('CP-08 PASADO: falla_drivers detectada'), nl
    ;   write('CP-08 FALLIDO: no se detecto falla_drivers'), nl
    ).

% CP-09: bateria no carga -> falla_bateria
prueba_cp09 :-
    Sintomas = [bateria_no_carga],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   member(falla_bateria, Diagnosticos)
    ->  write('CP-09 PASADO: falla_bateria detectada'), nl
    ;   write('CP-09 FALLIDO: no se detecto falla_bateria'), nl
    ).

% CP-10: pantalla negra + sonido de pitidos -> falla_ram o falla_placa_madre
prueba_cp10 :-
    Sintomas = [pantalla_negra, sonido_pitidos_arranque],
    obtener_diagnosticos(Sintomas, Diagnosticos),
    (   (member(falla_ram, Diagnosticos) ; member(falla_placa_madre, Diagnosticos))
    ->  write('CP-10 PASADO: falla_ram o falla_placa_madre detectada'), nl
    ;   write('CP-10 FALLIDO: no se detecto falla_ram ni falla_placa_madre'), nl
    ).
