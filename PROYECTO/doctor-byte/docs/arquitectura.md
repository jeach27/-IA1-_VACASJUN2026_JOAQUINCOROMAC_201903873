# Arquitectura del Sistema - Doctor Byte

**Curso:** Inteligencia Artificial 1  
**Proyecto:** Doctor Byte - Fase 1  
**Universidad:** Universidad San Carlos de Guatemala - Facultad de Ingenieria

---

## 1. Descripcion General

Doctor Byte es un sistema experto para el diagnostico automatico de fallas comunes en computadoras. El usuario selecciona sintomas desde una interfaz web, el backend consulta el motor de inferencia en Prolog y retorna los diagnosticos con recomendaciones. Los resultados tambien se envian opcionalmente a un bot de Telegram.

---

## 2. Diagrama de Arquitectura

```
[Usuario]
    |
    | (HTTP - navegador)
    v
[Frontend Web]
index.html / styles.css / app.js
    |
    | (HTTP REST - fetch API)
    v
[Backend Flask - Python]
app.py / prolog_bridge.py / history.py / telegram_bot.py
    |               |               |
    v               v               v
[SWI-Prolog]  [historial.json]  [Telegram Bot API]
knowledge_base.pl                     |
                                 [Chat Telegram]
```

Flujo de una consulta:

1. El usuario selecciona sintomas en el frontend y presiona Diagnosticar.
2. El frontend envia POST /diagnostico al backend con la lista de sintomas.
3. El backend llama a SWI-Prolog via pyswip con los sintomas.
4. Prolog evalua las reglas de inferencia y retorna las fallas diagnosticadas.
5. El backend obtiene las recomendaciones para cada falla.
6. El backend guarda el registro en historial.json.
7. Si se proporciono un chat_id, el backend envia la notificacion a Telegram.
8. El backend responde al frontend con el diagnostico completo.
9. El frontend muestra los resultados al usuario.

---

## 3. Stack Tecnologico

| Componente | Tecnologia | Version |
|---|---|---|
| Motor de inferencia | SWI-Prolog | 9.x |
| Backend | Python + Flask | Python 3.11 / Flask 3.0.3 |
| Puente Python-Prolog | pyswip | 0.2.10 |
| Frontend | HTML5 + CSS3 + JavaScript ES6 | - |
| Notificaciones | Telegram Bot API (requests) | - |
| Control de versiones | Git | - |

---

## 4. Estructura del Proyecto

```
doctor-byte/
├── prolog/
│   ├── knowledge_base.pl     # Base de conocimiento principal
│   └── tests.pl              # Casos de prueba ejecutables en SWI-Prolog
├── backend/
│   ├── app.py                # Servidor Flask y definicion de endpoints
│   ├── prolog_bridge.py      # Comunicacion Python <-> SWI-Prolog via pyswip
│   ├── telegram_bot.py       # Envio de notificaciones al bot de Telegram
│   ├── history.py            # Persistencia del historial de diagnosticos en JSON
│   ├── requirements.txt      # Dependencias Python con versiones fijas
│   └── data/
│       └── historial.json    # Historial de diagnosticos (generado en ejecucion)
├── frontend/
│   ├── index.html            # Pagina principal de la interfaz
│   ├── css/
│   │   └── styles.css        # Estilos de la interfaz
│   └── js/
│       └── app.js            # Logica del cliente
├── docs/
│   ├── arquitectura.md       # Este documento
│   ├── manual_usuario.md     # Manual de usuario
│   └── casos_de_prueba.md    # Casos de prueba y resultados
├── .env.example              # Ejemplo de variables de entorno
├── .gitignore
└── README.md
```

---

## 5. Base de Conocimiento Prolog

### Archivo: prolog/knowledge_base.pl

El archivo esta organizado en cinco secciones:

**Seccion 1 - Sintomas (15 hechos)**

Cada sintoma se declara con el predicado `sintoma/1`:

```prolog
sintoma(pantalla_negra).
sintoma(reinicio_inesperado).
% ... 13 sintomas mas
```

**Seccion 2 - Fallas (10 hechos)**

Cada falla diagnosticable se declara con el predicado `falla/1`:

```prolog
falla(falla_ram).
falla(falla_disco_duro).
% ... 8 fallas mas
```

**Seccion 3 - Recomendaciones (10 hechos)**

Cada recomendacion se asocia a una falla con `recomendacion/2`:

```prolog
recomendacion(falla_ram, 'Verificar y reemplazar los modulos de RAM...').
```

**Seccion 4 - Reglas de inferencia (11 reglas)**

Las reglas usan el predicado `diagnostico/2` que recibe una lista de sintomas y unifica con una falla:

```prolog
diagnostico(Sintomas, falla_fuente_poder) :-
    member(pantalla_negra, Sintomas),
    member(no_enciende, Sintomas),
    !.
```

Elementos de Prolog utilizados:
- **Hechos**: `sintoma/1`, `falla/1`, `recomendacion/2`
- **Reglas**: `diagnostico/2`, `listar_sintomas/1`, `obtener_diagnosticos/2`
- **Variables**: `Sintomas`, `Falla`, `Recomendacion`, `Diagnosticos`
- **Listas**: los sintomas se pasan como lista, `SintomasDrivers = [sin_sonido, red_no_conecta]`
- **Corte (!)**: presente en las reglas principales para evitar backtracking innecesario
- **Predicados de lista**: `member/2`, `intersection/3`, `list_to_set/2`, `findall/3`
- **Negacion**: `\+` para descartar condiciones

**Seccion 5 - Predicados utilitarios**

```prolog
% Retorna todos los sintomas disponibles como lista
listar_sintomas(Sintomas) :- findall(S, sintoma(S), Sintomas).

% Retorna todas las fallas diagnosticadas para una lista de sintomas
obtener_diagnosticos(Sintomas, Diagnosticos) :-
    findall(F, diagnostico(Sintomas, F), DiagnosticosDups),
    list_to_set(DiagnosticosDups, Diagnosticos).
```

### Ejecucion de consultas manualmente

```prolog
% Cargar la base de conocimiento
?- consult('prolog/knowledge_base.pl').

% Listar todos los sintomas
?- listar_sintomas(S).

% Diagnosticar con sintomas especificos
?- obtener_diagnosticos([pantalla_negra, no_enciende], D).
% D = [falla_fuente_poder]

% Obtener recomendacion de una falla
?- recomendacion(falla_fuente_poder, R).
```

---

## 6. Backend - API REST

### Archivo: backend/app.py

El servidor Flask expone los siguientes endpoints:

#### GET /sintomas

Retorna la lista de todos los sintomas disponibles en la base de conocimiento.

**Response (200 OK):**
```json
{
  "sintomas": [
    "pantalla_negra",
    "reinicio_inesperado",
    "lentitud_extrema",
    "..."
  ]
}
```

#### POST /diagnostico

Recibe una lista de sintomas y retorna las fallas diagnosticadas con sus recomendaciones.

**Request body:**
```json
{
  "sintomas": ["pantalla_negra", "no_enciende"],
  "chat_id": "123456789"
}
```

El campo `chat_id` es opcional. Si se proporciona, el diagnostico se envia al chat de Telegram indicado.

**Response (200 OK):**
```json
{
  "id": "a1b2c3d4",
  "fecha": "2026-06-10 14:30:00",
  "sintomas": ["pantalla_negra", "no_enciende"],
  "diagnosticos": [
    {
      "falla": "falla_fuente_poder",
      "recomendacion": "Revisar conexiones de la fuente de poder..."
    }
  ]
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Se requiere el campo sintomas en el cuerpo de la solicitud"
}
```

#### GET /historial

Retorna el historial de todos los diagnosticos realizados, del mas reciente al mas antiguo.

**Response (200 OK):**
```json
{
  "historial": [
    {
      "id": "a1b2c3d4",
      "fecha": "2026-06-10 14:30:00",
      "sintomas": ["pantalla_negra", "no_enciende"],
      "diagnosticos": [...]
    }
  ]
}
```

### Archivo: backend/prolog_bridge.py

Encapsula la comunicacion con SWI-Prolog usando la libreria `pyswip`. Mantiene una instancia singleton de Prolog para evitar recargar la base de conocimiento en cada solicitud.

Funciones expuestas:
- `consultar_sintomas()` - retorna lista de strings
- `consultar_diagnostico(sintomas: list)` - retorna lista de dicts `{falla, recomendacion}`

### Archivo: backend/history.py

Persiste cada diagnostico en `backend/data/historial.json`. Las funciones principales son:
- `guardar_diagnostico(sintomas, diagnosticos)` - escribe el registro y retorna el objeto creado
- `obtener_historial()` - lee y retorna todos los registros en orden inverso

---

## 7. Bot de Telegram

### Archivo: backend/telegram_bot.py

Usamos `urllib.request` de la libreria estandar de Python para hacer la peticion HTTP a la API REST de Telegram, sin dependencias externas especificas para Telegram. Tanto el token como el chat_id de destino se leen exclusivamente desde variables de entorno.

**Variables de entorno requeridas:**

| Variable | Descripcion |
|---|---|
| TELEGRAM_TOKEN | Token del bot obtenido desde @BotFather |
| TELEGRAM_CHAT_ID | ID del chat que recibe las notificaciones |

Si alguna de las dos no esta configurada, el envio se omite sin interrumpir el flujo principal ni retornar error al usuario.

**Flujo de notificacion:**
1. El endpoint `/diagnostico` llama a `enviar_diagnostico(diagnosticos)` en cada solicitud.
2. La funcion lee `TELEGRAM_TOKEN` y `TELEGRAM_CHAT_ID` del entorno.
3. Construye un mensaje en formato Markdown con las fallas y recomendaciones.
4. Realiza POST a `https://api.telegram.org/bot{TOKEN}/sendMessage` via `urllib.request`.
5. El resultado se registra en el log. Los errores no interrumpen la respuesta al usuario.

**Configuracion del bot:**
1. Abrir Telegram y buscar @BotFather.
2. Ejecutar `/newbot` y seguir las instrucciones.
3. Copiar el token al archivo `.env` como `TELEGRAM_TOKEN=tu_token`.
4. Para obtener el Chat ID: escribirle al bot @userinfobot en Telegram.
5. Copiar el ID al archivo `.env` como `TELEGRAM_CHAT_ID=tu_chat_id`.

---

## 8. Frontend

### Archivos: frontend/

El frontend es una SPA (Single Page Application) que se sirve directamente desde Flask al visitar `http://localhost:5000`.

**Interaccion con el backend:**

1. Al cargar la pagina, `app.js` llama a `GET /sintomas` y renderiza los checkboxes dinamicamente.
2. Al presionar Diagnosticar, se llama a `POST /diagnostico` con los sintomas seleccionados.
3. Los resultados se muestran en la seccion de resultado sin recargar la pagina.
4. El historial se carga al inicio y se actualiza despues de cada diagnostico.

**Dependencias:** ninguna libreria externa. Vanilla HTML + CSS + JavaScript.

---

## 9. Variables de Entorno

| Variable | Descripcion | Requerida |
|---|---|---|
| TELEGRAM_TOKEN | Token del bot de Telegram obtenido de @BotFather | Si se usa Telegram |
| TELEGRAM_CHAT_ID | ID del chat de destino para las notificaciones | Si se usa Telegram |

Ambas variables deben estar presentes para que el envio a Telegram funcione.
Si falta alguna, el sistema omite el envio y continua normalmente.

Ver `.env.example` para la plantilla de configuracion.
