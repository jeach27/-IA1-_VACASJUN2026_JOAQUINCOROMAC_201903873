# Casos de Prueba - SmartBot

## Entorno de prueba

- Docker Compose levantado con `docker compose up -d`
- API accesible en `http://localhost:8000`
- Panel accesible en `http://localhost:8000/login.html`
- API interactiva (Swagger): `http://localhost:8000/docs`

---

## Casos de prueba ejecutados

| ID    | Escenario                                                           | Resultado esperado                                                       | Resultado |
|-------|---------------------------------------------------------------------|--------------------------------------------------------------------------|-----------|
| CP-01 | Login con credenciales correctas (`IA1-User` / `IA1-password@_new`)| Acceso concedido, token JWT emitido, redirige al panel                  | Correcto  |
| CP-02 | Login con contrasena incorrecta                                     | HTTP 401, mensaje "Usuario o contrasena incorrectos"                    | Correcto  |
| CP-03 | Acceso a `GET /estadisticas` sin token                              | HTTP 401 Unauthorized                                                   | Correcto  |
| CP-04 | Crear una categoria desde el panel                                  | Categoria visible en el listado del panel                               | Correcto  |
| CP-05 | Editar el nombre de una categoria existente                         | Cambio reflejado inmediatamente en el listado                           | Correcto  |
| CP-06 | Eliminar una categoria                                              | Categoria desaparece del listado                                        | Correcto  |
| CP-07 | Crear una pregunta con respuesta desde el panel                     | Pregunta disponible para el bot de inmediato                            | Correcto  |
| CP-08 | Editar la respuesta de una pregunta existente                       | Nueva respuesta retornada por el bot                                    | Correcto  |
| CP-09 | Eliminar una pregunta                                               | El bot ya no responde esa pregunta                                      | Correcto  |
| CP-10 | Desactivar una pregunta (activa = false)                            | El bot no usa esa pregunta para responder                               | Correcto  |
| CP-11 | Consulta al bot con pregunta registrada: "horarios de atencion"     | Bot responde la respuesta almacenada en BD                              | Correcto  |
| CP-12 | Consulta al bot con texto sin coincidencia: "xyz asdf 123"          | Bot responde el mensaje de no encontrado configurado en el sistema      | Correcto  |
| CP-13 | Consulta registrada en el historial                                 | Aparece en `GET /consultas` y en la seccion Historial del panel         | Correcto  |
| CP-14 | Configurar el chat/grupo de Telegram desde el panel                 | Valor guardado en tabla `configuracion` y retornado por la API          | Correcto  |
| CP-15 | Verificar estadisticas despues de varias consultas                  | Totales y rankings reflejan las consultas realizadas                    | Correcto  |
| CP-16 | Desactivar bot desde el panel (toggle a inactivo)                   | Bot responde "El bot se encuentra temporalmente inactivo."              | Correcto  |
| CP-17 | Activar bot desde el panel (toggle a activo)                        | Bot retoma respuestas normales desde la BD                              | Correcto  |
| CP-18 | Acceso a `POST /preguntas` sin token JWT                            | HTTP 401 Unauthorized                                                   | Correcto  |
| CP-19 | Filtrar preguntas por categoria en el panel                         | Solo se muestran preguntas de la categoria seleccionada                 | Correcto  |
| CP-20 | Consulta con bot desactivado queda registrada en historial          | Registro aparece con `encontrada=false` y respuesta "Bot inactivo"      | Correcto  |

---

## Notas de ejecucion

- Las pruebas CP-11 a CP-13, CP-16, CP-17 y CP-20 se ejecutaron enviando mensajes reales desde Telegram al bot.
- Las pruebas CP-01 a CP-03 y CP-18 se ejecutaron contra la API via `http://localhost:8000/docs`.
- Las pruebas CP-04 a CP-10, CP-14, CP-15 y CP-19 se ejecutaron directamente desde el panel administrativo.
- El umbral de similitud para coincidencia de preguntas es 0.45 (parametro `UMBRAL_SIMILITUD` en `consultas.py`).
