# Casos de Prueba - Doctor Byte

**Sistema:** Doctor Byte - Sistema Experto de Diagnostico  
**Version:** Fase 1  
**Fecha de ejecucion:** 10/06/2026

---

## Instrucciones para ejecutar las pruebas

Las pruebas se pueden ejecutar de dos formas:

**Opcion A - En SWI-Prolog directamente:**

```prolog
?- consult('prolog/tests.pl'), ejecutar_todas_las_pruebas.
```

**Opcion B - A traves del endpoint REST:**

```bash
curl -X POST http://localhost:5000/diagnostico \
  -H "Content-Type: application/json" \
  -d '{"sintomas": ["pantalla_negra", "no_enciende"]}'
```

---

## Casos de prueba de la base de conocimiento Prolog

| ID | Sintomas ingresados | Diagnostico esperado | Resultado |
|---|---|---|---|
| CP-01 | pantalla_negra, no_enciende | falla_fuente_poder | PASADO |
| CP-02 | lentitud_extrema, aplicaciones_se_cierran_solas | virus_malware | PASADO |
| CP-03 | sobrecalentamiento, ventilador_muy_ruidoso | sobrecalentamiento_cpu | PASADO |
| CP-04 | sonido_pitidos_arranque | falla_ram | PASADO |
| CP-05 | pantalla_azul_muerte, reinicio_inesperado | falla_sistema_operativo | PASADO |
| CP-06 | no_reconoce_disco | falla_disco_duro | PASADO |
| CP-07 | sin_sonido | falla_drivers | PASADO |
| CP-08 | red_no_conecta | falla_drivers | PASADO |
| CP-09 | bateria_no_carga | falla_bateria | PASADO |
| CP-10 | pantalla_negra, sonido_pitidos_arranque | falla_ram | PASADO |

### Notas sobre CP-10

El CP-10 esperaba `falla_ram o falla_placa_madre`. La regla 2 del sistema diagnostica `falla_ram` cuando hay pitidos y los perifericos responden (no hay `teclado_no_responde` ni `mouse_no_responde`). Si ademas de pantalla negra y pitidos se agregan perifericos sin respuesta, la regla 3 activa `falla_placa_madre`.

---

## Casos de prueba adicionales de la API REST

| ID | Metodo | Endpoint | Cuerpo | Respuesta esperada | Resultado |
|---|---|---|---|---|---|
| CP-11 | GET | /sintomas | - | Lista de 15 sintomas | PASADO |
| CP-12 | POST | /diagnostico | {"sintomas": ["sin_sonido", "red_no_conecta"]} | falla_drivers (una vez, sin duplicados) | PASADO |
| CP-13 | POST | /diagnostico | {"sintomas": []} | Error 400 | PASADO |
| CP-14 | POST | /diagnostico | Sin body | Error 400 | PASADO |
| CP-15 | GET | /historial | - | Lista con los diagnosticos del historial | PASADO |

### CP-12 - Detalle de la regla de drivers

Cuando se ingresan `sin_sonido` y `red_no_conecta` juntos, la regla 10 usa `intersection/3` entre la lista de sintomas y `[sin_sonido, red_no_conecta]`. La interseccion es no vacia, se activa la regla y se diagnostica `falla_drivers` una sola vez gracias a `list_to_set/2` en `obtener_diagnosticos/2`.

---

## Casos de prueba de combinaciones multiples

| ID | Sintomas ingresados | Diagnostico esperado | Observacion |
|---|---|---|---|
| CP-16 | teclado_no_responde, mouse_no_responde | falla_placa_madre | Regla 4 activa |
| CP-17 | pantalla_negra, sobrecalentamiento | falla_tarjeta_grafica | Regla 6: no hay no_enciende |
| CP-18 | pantalla_negra, sobrecalentamiento, no_enciende | falla_fuente_poder | Regla 1 tiene prioridad (corte) |
| CP-19 | sonido_pitidos_arranque, teclado_no_responde | falla_placa_madre | Regla 3 activa |
| CP-20 | lentitud_extrema, red_no_conecta | virus_malware, falla_drivers | Dos diagnosticos independientes |

### Observacion sobre CP-18

La regla 1 incluye un corte (`!`) despues de verificar `pantalla_negra` y `no_enciende`. Esto hace que aunque tambien haya `sobrecalentamiento`, Prolog no retrocede para evaluar la regla 6. El sistema devuelve solo `falla_fuente_poder`, lo cual es el comportamiento esperado: si el equipo no enciende, la fuente de poder es la causa prioritaria.

---

## Casos de prueba de Telegram

| ID | Descripcion | Resultado |
|---|---|---|
| CP-21 | POST /diagnostico con chat_id valido y TELEGRAM_TOKEN configurado | Mensaje recibido en Telegram |
| CP-22 | POST /diagnostico sin chat_id | Sin envio a Telegram, diagnostico normal |
| CP-23 | POST /diagnostico con TELEGRAM_TOKEN no configurado | Advertencia en log, sin error en respuesta |

---

## Resultado de los tests de Prolog (tests.pl)

Salida esperada al ejecutar `ejecutar_todas_las_pruebas`:

```
CP-01 PASADO: falla_fuente_poder detectada
CP-02 PASADO: virus_malware detectado
CP-03 PASADO: sobrecalentamiento_cpu detectado
CP-04 PASADO: falla_ram detectada
CP-05 PASADO: falla_sistema_operativo detectada
CP-06 PASADO: falla_disco_duro detectada
CP-07 PASADO: falla_drivers detectada
CP-08 PASADO: falla_drivers detectada
CP-09 PASADO: falla_bateria detectada
CP-10 PASADO: falla_ram o falla_placa_madre detectada
Todas las pruebas completadas.
```
