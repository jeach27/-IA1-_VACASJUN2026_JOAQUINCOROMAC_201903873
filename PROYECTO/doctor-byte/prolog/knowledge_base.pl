% knowledge_base.pl
% Base de conocimiento de Doctor Byte para el diagnostico de fallas en computadoras.
% Usamos hechos, reglas, variables, listas y cortes para representar el conocimiento
% del sistema experto.

% =============================================================================
% SECCION 1: SINTOMAS DISPONIBLES (15 sintomas)
% Cada hecho sintoma/1 declara un sintoma valido que el usuario puede reportar.
% =============================================================================

sintoma(pantalla_negra).
sintoma(reinicio_inesperado).
sintoma(lentitud_extrema).
sintoma(no_enciende).
sintoma(sonido_pitidos_arranque).
sintoma(sobrecalentamiento).
sintoma(pantalla_azul_muerte).
sintoma(no_reconoce_disco).
sintoma(aplicaciones_se_cierran_solas).
sintoma(sin_sonido).
sintoma(red_no_conecta).
sintoma(teclado_no_responde).
sintoma(mouse_no_responde).
sintoma(bateria_no_carga).
sintoma(ventilador_muy_ruidoso).

% =============================================================================
% SECCION 2: FALLAS DIAGNOSTICABLES (10 fallas)
% Cada hecho falla/1 declara una falla que el sistema puede diagnosticar.
% =============================================================================

falla(falla_ram).
falla(falla_disco_duro).
falla(falla_fuente_poder).
falla(sobrecalentamiento_cpu).
falla(falla_sistema_operativo).
falla(virus_malware).
falla(falla_tarjeta_grafica).
falla(falla_placa_madre).
falla(falla_drivers).
falla(falla_bateria).

% =============================================================================
% SECCION 3: RECOMENDACIONES (10 recomendaciones)
% recomendacion(+Falla, -Texto) asocia una falla con su recomendacion de solucion.
% =============================================================================

recomendacion(falla_ram,
    'Verificar y reemplazar los modulos de RAM. Probar con un modulo a la vez para identificar el defectuoso.').
recomendacion(falla_disco_duro,
    'Respaldar datos de inmediato y reemplazar el disco duro. Ejecutar herramientas de diagnostico como CrystalDiskInfo.').
recomendacion(falla_fuente_poder,
    'Revisar conexiones de la fuente de poder y medir voltajes. Reemplazar la fuente si los valores estan fuera de rango.').
recomendacion(sobrecalentamiento_cpu,
    'Limpiar el sistema de refrigeracion, reemplazar la pasta termica del CPU y verificar que el ventilador funcione correctamente.').
recomendacion(falla_sistema_operativo,
    'Ejecutar herramientas de reparacion del sistema operativo o realizar una reinstalacion limpia conservando los datos del usuario.').
recomendacion(virus_malware,
    'Ejecutar un analisis completo con un antivirus actualizado. Si el problema persiste, reinstalar el sistema operativo.').
recomendacion(falla_tarjeta_grafica,
    'Actualizar los drivers de la tarjeta grafica. Si el problema persiste, verificar el asentamiento fisico o reemplazar la tarjeta.').
recomendacion(falla_placa_madre,
    'Revisar que todos los componentes esten correctamente conectados. Si persiste, llevar el equipo a servicio tecnico especializado.').
recomendacion(falla_drivers,
    'Actualizar o reinstalar los drivers del dispositivo afectado desde el sitio oficial del fabricante.').
recomendacion(falla_bateria,
    'Calibrar la bateria realizando ciclos de carga completos. Si persiste, reemplazar la bateria por una original del fabricante.').

% =============================================================================
% SECCION 4: REGLAS DE INFERENCIA (10+ reglas)
% diagnostico(+Sintomas, -Falla) infiere una falla a partir de una lista de sintomas.
% Usamos member/2 para verificar pertenencia en la lista de sintomas.
% Usamos cortes (!) para evitar backtracking innecesario cuando la causa es clara.
% =============================================================================

% Regla 1: La fuente de poder falla cuando el equipo no enciende y la pantalla esta negra.
% El corte evita buscar otras causas si se cumplen ambas condiciones.
diagnostico(Sintomas, falla_fuente_poder) :-
    member(pantalla_negra, Sintomas),
    member(no_enciende, Sintomas),
    !.

% Regla 2: Falla de RAM cuando hay pitidos al arranque sin falla evidente de placa madre.
% Descartamos la placa madre si los perifericos basicos responden.
diagnostico(Sintomas, falla_ram) :-
    member(sonido_pitidos_arranque, Sintomas),
    \+ member(teclado_no_responde, Sintomas),
    \+ member(mouse_no_responde, Sintomas),
    !.

% Regla 3: Falla de placa madre cuando los pitidos van acompanados de perifericos sin respuesta.
diagnostico(Sintomas, falla_placa_madre) :-
    member(sonido_pitidos_arranque, Sintomas),
    member(teclado_no_responde, Sintomas),
    !.

% Regla 4: Falla de placa madre cuando teclado y mouse dejan de responder simultaneamente.
% El corte evita buscar otras causas al confirmar ambos perifericos inactivos.
diagnostico(Sintomas, falla_placa_madre) :-
    member(teclado_no_responde, Sintomas),
    member(mouse_no_responde, Sintomas),
    !.

% Regla 5: Sobrecalentamiento del CPU cuando hay calor excesivo y el ventilador esta forzado.
diagnostico(Sintomas, sobrecalentamiento_cpu) :-
    member(sobrecalentamiento, Sintomas),
    member(ventilador_muy_ruidoso, Sintomas),
    !.

% Regla 6: Falla de tarjeta grafica cuando la pantalla se apaga por calor pero el equipo
% sigue encendido. Descartamos fuente de poder porque el equipo responde.
diagnostico(Sintomas, falla_tarjeta_grafica) :-
    member(pantalla_negra, Sintomas),
    member(sobrecalentamiento, Sintomas),
    \+ member(no_enciende, Sintomas),
    !.

% Regla 7: Falla del sistema operativo cuando hay pantalla azul con reinicios inesperados.
diagnostico(Sintomas, falla_sistema_operativo) :-
    member(pantalla_azul_muerte, Sintomas),
    member(reinicio_inesperado, Sintomas),
    !.

% Regla 8: Falla de disco duro cuando el sistema no reconoce el dispositivo de almacenamiento.
diagnostico(Sintomas, falla_disco_duro) :-
    member(no_reconoce_disco, Sintomas),
    !.

% Regla 9: Virus o malware cuando la lentitud extrema coincide con aplicaciones que se cierran.
diagnostico(Sintomas, virus_malware) :-
    member(lentitud_extrema, Sintomas),
    member(aplicaciones_se_cierran_solas, Sintomas),
    !.

% Regla 10: Falla de drivers cuando al menos uno de los sintomas tipicos de drivers esta presente.
% Usamos una lista de sintomas conocidos de drivers y la interseccion para verificar.
diagnostico(Sintomas, falla_drivers) :-
    SintomasDrivers = [sin_sonido, red_no_conecta],
    intersection(Sintomas, SintomasDrivers, Coincidencias),
    Coincidencias \= [],
    !.

% Regla 11: Falla de bateria cuando la bateria no carga.
diagnostico(Sintomas, falla_bateria) :-
    member(bateria_no_carga, Sintomas),
    !.

% =============================================================================
% SECCION 5: PREDICADOS UTILITARIOS
% Estos predicados son usados por el backend para consultar la base de conocimiento.
% =============================================================================

% listar_sintomas(-Sintomas)
% Obtiene la lista de todos los sintomas disponibles en la base de conocimiento.
listar_sintomas(Sintomas) :-
    findall(S, sintoma(S), Sintomas).

% obtener_diagnosticos(+Sintomas, -Diagnosticos)
% Dado una lista de sintomas, obtiene todas las fallas diagnosticadas sin duplicados.
obtener_diagnosticos(Sintomas, Diagnosticos) :-
    findall(F, diagnostico(Sintomas, F), DiagnosticosDups),
    list_to_set(DiagnosticosDups, Diagnosticos).
