% knowledge_base.pl
% Generado automaticamente por kb_generator.py desde knowledge_store.json.
% Para modificar la base de conocimiento usa la interfaz de administracion.

% =============================================================================
% SECCION 1: SINTOMAS DISPONIBLES (17 sintomas)
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
sintoma(sintomas_calificacion_1).
sintoma(sintomas_calificacion_2).

% =============================================================================
% SECCION 2: FALLAS DIAGNOSTICABLES (11 fallas)
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
falla(falla_calificacion).

% =============================================================================
% SECCION 3: RECOMENDACIONES (11 recomendaciones)
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
recomendacion(falla_calificacion,
    'recomendacion_calificacion').

% =============================================================================
% SECCION 4: REGLAS DE INFERENCIA (13 reglas)
% Usamos member/2 para verificar pertenencia en la lista de sintomas.
% Usamos cortes (!) para evitar backtracking cuando la causa es clara.
% =============================================================================

% Regla r1: Fuente de poder falla cuando el equipo no enciende y la pantalla esta negra
diagnostico(Sintomas, falla_fuente_poder) :-
    member(pantalla_negra, Sintomas),
    member(no_enciende, Sintomas),
    !.

% Regla r2: Falla de RAM cuando hay pitidos al arranque sin falla evidente de placa madre
diagnostico(Sintomas, falla_ram) :-
    member(sonido_pitidos_arranque, Sintomas),
    \+ member(teclado_no_responde, Sintomas),
    \+ member(mouse_no_responde, Sintomas),
    !.

% Regla r3: Falla de placa madre cuando los pitidos van acompanados de teclado sin respuesta
diagnostico(Sintomas, falla_placa_madre) :-
    member(sonido_pitidos_arranque, Sintomas),
    member(teclado_no_responde, Sintomas),
    !.

% Regla r4: Falla de placa madre cuando teclado y mouse dejan de responder simultaneamente
diagnostico(Sintomas, falla_placa_madre) :-
    member(teclado_no_responde, Sintomas),
    member(mouse_no_responde, Sintomas),
    !.

% Regla r5: Sobrecalentamiento del CPU cuando hay calor excesivo y el ventilador esta forzado
diagnostico(Sintomas, sobrecalentamiento_cpu) :-
    member(sobrecalentamiento, Sintomas),
    member(ventilador_muy_ruidoso, Sintomas),
    !.

% Regla r6: Falla de tarjeta grafica cuando la pantalla se apaga por calor pero el equipo sigue encendido
diagnostico(Sintomas, falla_tarjeta_grafica) :-
    member(pantalla_negra, Sintomas),
    member(sobrecalentamiento, Sintomas),
    \+ member(no_enciende, Sintomas),
    !.

% Regla r7: Falla del sistema operativo cuando hay pantalla azul con reinicios inesperados
diagnostico(Sintomas, falla_sistema_operativo) :-
    member(pantalla_azul_muerte, Sintomas),
    member(reinicio_inesperado, Sintomas),
    !.

% Regla r8: Falla de disco duro cuando el sistema no reconoce el dispositivo de almacenamiento
diagnostico(Sintomas, falla_disco_duro) :-
    member(no_reconoce_disco, Sintomas),
    !.

% Regla r9: Virus o malware cuando la lentitud extrema coincide con aplicaciones que se cierran
diagnostico(Sintomas, virus_malware) :-
    member(lentitud_extrema, Sintomas),
    member(aplicaciones_se_cierran_solas, Sintomas),
    !.

% Regla r10a: Falla de drivers cuando hay ausencia de sonido
diagnostico(Sintomas, falla_drivers) :-
    member(sin_sonido, Sintomas),
    !.

% Regla r10b: Falla de drivers cuando la red no conecta
diagnostico(Sintomas, falla_drivers) :-
    member(red_no_conecta, Sintomas),
    !.

% Regla r11: Falla de bateria cuando la bateria no carga
diagnostico(Sintomas, falla_bateria) :-
    member(bateria_no_carga, Sintomas),
    !.

% Regla r275399: calificacion
diagnostico(Sintomas, falla_calificacion) :-
    member(sintomas_calificacion_1, Sintomas),
    member(sintomas_calificacion_2, Sintomas),
    !.

% =============================================================================
% SECCION 5: PREDICADOS UTILITARIOS
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
