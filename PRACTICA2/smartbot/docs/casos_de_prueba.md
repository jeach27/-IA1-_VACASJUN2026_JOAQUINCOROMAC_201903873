# Casos de Prueba - SmartBot

## Entorno de prueba

- Docker Compose levantado con `docker compose up -d`
- API accesible en `http://localhost:8000`
- Panel accesible en `http://localhost:8000/login.html`

---

| ID    | Escenario                                                        | Resultado esperado                                    | Resultado |
|-------|------------------------------------------------------------------|-------------------------------------------------------|-----------|
| CP-01 | Login con credenciales correctas (`IA1-User` / `IA1-password@_new`) | Acceso concedido, token JWT emitido, redirige al panel | Pendiente |
| CP-02 | Login con contrasena incorrecta                                  | HTTP 401, mensaje "Usuario o contrasena incorrectos"  | Pendiente |
| CP-03 | Acceso a `GET /estadisticas` sin token                           | HTTP 401 Unauthorized                                 | Pendiente |
| CP-04 | Crear una categoria desde el panel                               | Categoria visible en el listado del panel             | Pendiente |
| CP-05 | Editar el nombre de una categoria existente                      | Cambio reflejado inmediatamente en el listado         | Pendiente |
| CP-06 | Eliminar una categoria                                           | Categoria desaparece del listado                      | Pendiente |
| CP-07 | Crear una pregunta con respuesta desde el panel                  | Pregunta disponible para el bot de inmediato          | Pendiente |
| CP-08 | Editar la respuesta de una pregunta existente                    | Nueva respuesta retornada por el bot                  | Pendiente |
| CP-09 | Eliminar una pregunta                                            | El bot ya no responde esa pregunta                    | Pendiente |
| CP-10 | Desactivar una pregunta (activa = false)                         | El bot no usa esa pregunta para responder             | Pendiente |
| CP-11 | Consulta al bot con pregunta registrada                          | Bot responde la respuesta almacenada                  | Pendiente |
| CP-12 | Consulta al bot con texto que no coincide con ninguna pregunta   | Bot responde el mensaje de no encontrado              | Pendiente |
| CP-13 | Consulta registrada en el historial                              | Aparece en `GET /consultas` y en la seccion Historial | Pendiente |
| CP-14 | Configurar el chat/grupo de Telegram desde el panel              | Valor guardado en `configuracion` y retornado por la API | Pendiente |
| CP-15 | Verificar estadisticas despues de varias consultas               | Totales y rankings reflejan las consultas realizadas  | Pendiente |
