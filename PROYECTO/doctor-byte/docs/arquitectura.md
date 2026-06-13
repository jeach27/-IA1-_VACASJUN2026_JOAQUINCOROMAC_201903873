# Arquitectura del Sistema - Doctor Byte

**Curso:** Inteligencia Artificial 1
**Proyecto:** Doctor Byte - Fase 1
**Universidad:** Universidad San Carlos de Guatemala - Facultad de Ingenieria

---

## 1. Descripcion General

Doctor Byte es un sistema experto para el diagnostico automatico de fallas comunes en computadoras. El usuario selecciona sintomas desde una interfaz web, el backend consulta el motor de inferencia en Prolog y retorna los diagnosticos con recomendaciones. Los resultados se envian opcionalmente a un bot de Telegram. Un panel de administracion permite gestionar toda la base de conocimiento desde la interfaz.

---

## 2. Diagrama de Arquitectura

```
[Usuario Web]                        [Usuario Telegram]
     |                                      |
     | HTTP (navegador)                     | Telegram API
     v                                      v
[Frontend Web]              [Bot Telegram - polling]
index.html / admin.html          telegram_bot.py
app.js / admin.js                     |
     |                                |
     | HTTP REST (fetch)              | HTTP interno
     v                                v
           [Backend Flask - Python]
     app.py / prolog_bridge.py / history.py
     admin_manager.py / kb_generator.py
          |              |              |
          v              v              v
    [SWI-Prolog]  [historial.json]  [Telegram API]
  knowledge_base.pl                     |
  knowledge_store.json           [Chat Telegram]
```

Flujo de una consulta desde el frontend:
1. El usuario selecciona sintomas y presiona Diagnosticar.
2. El frontend envia POST /diagnostico con la lista de sintomas.
3. El backend llama a SWI-Prolog via pyswip con los sintomas.
4. Prolog evalua las reglas de inferencia y retorna las fallas.
5. El backend obtiene las recomendaciones para cada falla.
6. El backend guarda el registro en historial.json.
7. Si el bot esta habilitado, envia la notificacion a Telegram.
8. El backend responde con el diagnostico completo al frontend.

Flujo del bot interactivo de Telegram:
1. El usuario escribe /diagnosticar pantalla_negra,no_enciende en el chat del bot.
2. El hilo de polling recibe el mensaje via long polling a la API de Telegram.
3. El bot llama internamente a POST http://localhost:5000/diagnostico.
4. Recibe el resultado y lo formatea en Markdown.
5. Responde al usuario en el mismo chat de Telegram.

Flujo de actualizacion desde el panel admin:
1. El administrador crea/edita/elimina un sintoma, falla, recomendacion o regla.
2. admin_manager.py actualiza knowledge_store.json.
3. kb_generator.py regenera knowledge_base.pl desde el store.
4. prolog_bridge.py descarta la instancia singleton y la recarga en la proxima consulta.

---

## 3. Stack Tecnologico

| Componente | Tecnologia | Version |
|---|---|---|
| Motor de inferencia | SWI-Prolog | 10.x |
| Backend | Python + Flask | Python 3.13 / Flask 3.0.3 |
| Puente Python-Prolog | pyswip | 0.3.3 |
| Frontend | HTML5 + CSS3 + JavaScript ES6 (vanilla) | - |
| Bot de Telegram | Telegram Bot API + urllib (stdlib) | - |
| Control de versiones | Git | - |

---

## 4. Estructura del Proyecto

```
doctor-byte/
├── prolog/
│   ├── knowledge_base.pl     # Base de conocimiento (generada por kb_generator)
│   └── tests.pl              # Casos de prueba ejecutables en SWI-Prolog
├── backend/
│   ├── app.py                # Servidor Flask: endpoints del sistema y del admin
│   ├── prolog_bridge.py      # Comunicacion Python <-> SWI-Prolog (singleton + reload)
│   ├── telegram_bot.py       # Bot interactivo (polling) y envio de notificaciones
│   ├── history.py            # Persistencia del historial de diagnosticos en JSON
│   ├── admin_manager.py      # CRUD sobre knowledge_store.json y bot_config.json
│   ├── kb_generator.py       # Genera knowledge_base.pl desde knowledge_store.json
│   ├── requirements.txt      # Dependencias Python con versiones fijas
│   └── data/
│       ├── knowledge_store.json  # Fuente de verdad de la base de conocimiento
│       ├── bot_config.json       # Configuracion del bot (chat_id, mensajes, estado)
│       └── historial.json        # Historial de diagnosticos (generado en ejecucion)
├── frontend/
│   ├── index.html            # Interfaz de usuario principal
│   ├── admin.html            # Panel de administracion
│   ├── css/
│   │   └── styles.css        # Estilos del sistema (usuario y admin)
│   └── js/
│       ├── app.js            # Logica del frontend de usuario
│       └── admin.js          # Logica del panel de administracion
├── docs/
│   ├── arquitectura.md       # Este documento
│   ├── manual_usuario.md     # Manual de usuario y administrador
│   └── casos_de_prueba.md    # Casos de prueba y resultados
├── .env.example              # Plantilla de variables de entorno
├── .gitignore
└── README.md
```

---

## 5. Base de Conocimiento Prolog

### Archivo: prolog/knowledge_base.pl

El archivo esta organizado en cinco secciones y es generado automaticamente por `kb_generator.py` a partir de `knowledge_store.json`. No debe editarse manualmente.

**Seccion 1 - Sintomas (15 hechos)**

```prolog
sintoma(pantalla_negra).
sintoma(reinicio_inesperado).
% ... 13 sintomas mas
```

**Seccion 2 - Fallas (10 hechos)**

```prolog
falla(falla_ram).
falla(falla_disco_duro).
% ... 8 fallas mas
```

**Seccion 3 - Recomendaciones (10 hechos)**

```prolog
recomendacion(falla_ram,
    'Verificar y reemplazar los modulos de RAM...').
```

**Seccion 4 - Reglas de inferencia (12 reglas)**

Las reglas usan el predicado `diagnostico/2` que recibe una lista de sintomas y unifica con una falla:

```prolog
% Regla r1: Fuente de poder falla cuando el equipo no enciende y la pantalla esta negra
diagnostico(Sintomas, falla_fuente_poder) :-
    member(pantalla_negra, Sintomas),
    member(no_enciende, Sintomas),
    !.

% Regla r2: Falla de RAM cuando hay pitidos sin falla de placa madre
diagnostico(Sintomas, falla_ram) :-
    member(sonido_pitidos_arranque, Sintomas),
    \+ member(teclado_no_responde, Sintomas),
    \+ member(mouse_no_responde, Sintomas),
    !.
```

Elementos de Prolog utilizados:
- **Hechos**: `sintoma/1`, `falla/1`, `recomendacion/2`
- **Reglas**: `diagnostico/2`, `listar_sintomas/1`, `obtener_diagnosticos/2`
- **Variables**: `Sintomas`, `Falla`, `Recomendacion`, `Diagnosticos`
- **Listas**: los sintomas se pasan y procesan como listas Prolog
- **Corte (!)**: en todas las reglas principales para evitar backtracking innecesario
- **Negacion**: `\+` para descartar condiciones
- **Predicados de lista**: `member/2`, `list_to_set/2`, `findall/3`

**Seccion 5 - Predicados utilitarios**

```prolog
listar_sintomas(Sintomas) :- findall(S, sintoma(S), Sintomas).

obtener_diagnosticos(Sintomas, Diagnosticos) :-
    findall(F, diagnostico(Sintomas, F), DiagnosticosDups),
    list_to_set(DiagnosticosDups, Diagnosticos).
```

### Ejecucion de consultas manualmente

```prolog
?- consult('prolog/knowledge_base.pl').
?- listar_sintomas(S).
?- obtener_diagnosticos([pantalla_negra, no_enciende], D).
% D = [falla_fuente_poder]
?- recomendacion(falla_fuente_poder, R).
```

---

## 6. Backend - API REST

### Endpoints del sistema experto

#### GET /sintomas

Retorna todos los sintomas disponibles en la base de conocimiento.

**Response (200):**
```json
{ "sintomas": ["pantalla_negra", "reinicio_inesperado", "..."] }
```

#### POST /diagnostico

Recibe sintomas, consulta Prolog, guarda en historial y notifica a Telegram.

**Request:**
```json
{ "sintomas": ["pantalla_negra", "no_enciende"] }
```

**Response (200):**
```json
{
  "id": "a1b2c3d4",
  "fecha": "2026-06-12 22:49:00",
  "sintomas": ["pantalla_negra", "no_enciende"],
  "diagnosticos": [
    { "falla": "falla_fuente_poder", "recomendacion": "Revisar conexiones..." }
  ]
}
```

**Response (400):**
```json
{ "error": "Se requiere el campo sintomas en el cuerpo de la solicitud" }
```

#### GET /historial

Retorna todos los diagnosticos del mas reciente al mas antiguo.

**Response (200):**
```json
{ "historial": [ {...}, {...} ] }
```

### Endpoints del panel de administracion

Todos los endpoints admin requieren Content-Type: application/json.

#### Sintomas

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/sintomas | Lista todos los sintomas |
| POST | /admin/sintomas | Crea un nuevo sintoma `{nombre, etiqueta}` |
| PUT | /admin/sintomas/<nombre> | Actualiza nombre y etiqueta |
| DELETE | /admin/sintomas/<nombre> | Elimina el sintoma |

#### Fallas

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/fallas | Lista todas las fallas |
| POST | /admin/fallas | Crea una nueva falla `{nombre, etiqueta}` |
| PUT | /admin/fallas/<nombre> | Actualiza nombre y etiqueta |
| DELETE | /admin/fallas/<nombre> | Elimina la falla |

#### Recomendaciones

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/recomendaciones | Lista todas las recomendaciones |
| PUT | /admin/recomendaciones/<falla> | Crea o actualiza la recomendacion de una falla |
| DELETE | /admin/recomendaciones/<falla> | Elimina la recomendacion |

#### Reglas

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/reglas | Lista todas las reglas |
| POST | /admin/reglas | Crea una nueva regla |
| PUT | /admin/reglas/<id> | Actualiza una regla existente |
| DELETE | /admin/reglas/<id> | Elimina una regla |

Cuerpo para crear/actualizar regla:
```json
{
  "falla": "falla_ram",
  "sintomas_requeridos": ["sonido_pitidos_arranque"],
  "sintomas_negados": ["teclado_no_responde"],
  "usa_corte": true,
  "descripcion": "Descripcion de la regla"
}
```

#### Asociaciones

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/asociaciones | Vista agrupada: falla + reglas + recomendacion |

#### Configuracion del bot

| Metodo | Ruta | Descripcion |
|---|---|---|
| GET | /admin/configuracion | Lee la configuracion actual del bot |
| PUT | /admin/configuracion | Actualiza chat_id, habilitado y mensajes |

Cuerpo:
```json
{
  "chat_id": "123456789",
  "habilitado": true,
  "mensajes": {
    "bienvenida": "Texto de bienvenida",
    "sin_diagnostico": "Mensaje cuando no hay resultados"
  }
}
```

---

## 7. Gestion de la base de conocimiento (admin)

### Archivo: backend/knowledge_store.json

Fuente de verdad estructurada que alimenta la generacion del archivo Prolog. Contiene:
- `sintomas`: lista de `{nombre, etiqueta}`
- `fallas`: lista de `{nombre, etiqueta}`
- `recomendaciones`: lista de `{falla, texto}`
- `reglas`: lista de `{id, falla, sintomas_requeridos, sintomas_negados, usa_corte, descripcion}`

### Archivo: backend/kb_generator.py

Lee `knowledge_store.json` y genera `prolog/knowledge_base.pl` en formato Prolog valido. Al final llama a `prolog_bridge.recargar()` para que el motor de inferencia use la nueva base.

### Archivo: backend/admin_manager.py

Expone funciones CRUD sobre `knowledge_store.json`. Cada operacion de escritura llama a `kb_generator.regenerar_base_conocimiento()` automaticamente. Valida que los nombres de sintomas y fallas sean atomos Prolog validos (letras minusculas, digitos y guion bajo).

---

## 8. Bot de Telegram

### Archivo: backend/telegram_bot.py

Implementado con `urllib.request` de la libreria estandar de Python, sin dependencias externas adicionales para Telegram.

**Modos de operacion:**

1. **Notificaciones automaticas** (`enviar_diagnostico`): llamado desde el endpoint `/diagnostico` cada vez que se realiza un diagnostico desde el frontend. Lee el `chat_id` y el estado `habilitado` desde `bot_config.json`.

2. **Bot interactivo** (`_hilo_polling`): hilo de fondo que realiza long polling a la API de Telegram. Comandos disponibles:
   - `/start` — mensaje de bienvenida
   - `/sintomas` — lista los sintomas disponibles (llama a GET /sintomas)
   - `/diagnosticar s1,s2,...` — realiza un diagnostico (llama a POST /diagnostico)
   - `/ayuda` — muestra los comandos disponibles

**Variables de entorno:**

| Variable | Descripcion |
|---|---|
| TELEGRAM_TOKEN | Token del bot obtenido de @BotFather (obligatorio) |

**Configuracion desde el admin:**

| Campo en bot_config.json | Descripcion |
|---|---|
| chat_id | ID del chat que recibe las notificaciones automaticas |
| habilitado | Activa o desactiva el envio de notificaciones |
| mensajes.bienvenida | Texto del comando /start |
| mensajes.sin_diagnostico | Texto cuando no hay fallas detectadas |

---

## 9. Frontend

### Interfaz de usuario: frontend/index.html + app.js

SPA que se sirve desde Flask al visitar `http://localhost:5000`.

Secciones:
- **Seleccion de sintomas**: cuadricula de checkboxes cargada dinamicamente desde GET /sintomas
- **Resultado**: muestra fallas y recomendaciones tras el diagnostico
- **Historial**: lista de diagnosticos previos actualizable sin recargar

### Panel de administracion: frontend/admin.html + admin.js

Accesible desde `http://localhost:5000/admin` o desde el enlace en el header.

Secciones del panel:
- **Sintomas**: CRUD completo con validacion de nombres Prolog
- **Fallas**: CRUD completo
- **Recomendaciones**: CRUD completo (crear, editar, eliminar)
- **Reglas**: CRUD con selectores de sintomas requeridos y negados
- **Asociaciones**: vista de solo lectura que muestra como los sintomas se vinculan a fallas
- **Bot Telegram**: configuracion de chat_id, estado habilitado y mensajes personalizables

---

## 10. Variables de Entorno

| Variable | Descripcion | Requerida |
|---|---|---|
| TELEGRAM_TOKEN | Token del bot de Telegram de @BotFather | Para usar Telegram |

El `chat_id` se configura desde el panel admin (Bot Telegram) o como fallback en `TELEGRAM_CHAT_ID` en el `.env`.

Ver `.env.example` para la plantilla de configuracion.

---

## 11. Configuracion en Windows con SWI-Prolog 10.x

La libreria `pyswip 0.3.3` requiere que la variable de entorno `SWI_HOME_DIR` apunte a la carpeta raiz de SWI-Prolog:

```powershell
[System.Environment]::SetEnvironmentVariable("SWI_HOME_DIR", "D:\ruta\a\swipl", "User")
```

Verificar la ruta real con:
```powershell
(Get-Command swipl).Source
```
