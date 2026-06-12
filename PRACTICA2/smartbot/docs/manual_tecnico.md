# Manual Tecnico - SmartBot

## 1. Descripcion del sistema

SmartBot es un sistema de respuestas automatizadas que integra un bot de Telegram, una API REST desarrollada en Python con FastAPI, una base de datos PostgreSQL y un panel administrativo web. Permite gestionar preguntas frecuentes y sus respuestas sin modificar el codigo fuente.

## 2. Requerimientos funcionales

| ID   | Descripcion                                                                                      |
|------|--------------------------------------------------------------------------------------------------|
| RF01 | El sistema permite al administrador iniciar sesion con usuario y contrasena                      |
| RF02 | El administrador puede crear, consultar, actualizar y eliminar categorias                        |
| RF03 | El administrador puede crear, consultar, actualizar y eliminar preguntas y respuestas            |
| RF04 | El bot de Telegram recibe mensajes de los usuarios y retorna la respuesta mas cercana            |
| RF05 | El sistema registra cada consulta realizada con fecha, usuario y resultado                       |
| RF06 | El panel muestra estadisticas de uso del bot                                                     |
| RF07 | El administrador puede configurar el ID del chat/grupo de Telegram desde el panel               |
| RF08 | Cuando no existe una respuesta para la consulta, el bot responde con un mensaje predeterminado   |
| RF09 | Las preguntas y respuestas se almacenan y gestionan desde la base de datos, nunca en el codigo  |
| RF10 | El sistema soporta al menos 3 categorias y al menos 20 preguntas frecuentes                     |

## 3. Requerimientos no funcionales

### Rendimiento

| ID    | Descripcion                                                                          |
|-------|--------------------------------------------------------------------------------------|
| RNF01 | La API debe responder en menos de 2 segundos para consultas simples                 |
| RNF02 | El bot debe responder al usuario en menos de 5 segundos                              |

### Seguridad

| ID    | Descripcion                                                                          |
|-------|--------------------------------------------------------------------------------------|
| RNF03 | Las contrasenas de administradores se almacenan con hash bcrypt, nunca en texto plano|
| RNF04 | El acceso al panel administrativo y a los endpoints de gestion requiere token JWT    |
| RNF05 | El token de Telegram y las credenciales de base de datos se almacenan en variables de entorno |
| RNF06 | El archivo .env nunca se versiona en el repositorio                                  |

### Mantenibilidad

| ID    | Descripcion                                                                          |
|-------|--------------------------------------------------------------------------------------|
| RNF07 | El proyecto sigue una estructura de carpetas clara y documentada                     |
| RNF08 | Las dependencias estan fijadas con versiones exactas en requirements.txt             |
| RNF09 | El codigo usa logging en lugar de print para el debug                                |

### Disponibilidad

| ID    | Descripcion                                                                          |
|-------|--------------------------------------------------------------------------------------|
| RNF10 | Docker Compose configura `restart: unless-stopped` para recuperacion automatica     |
| RNF11 | El servicio backend depende del health check de la base de datos antes de iniciar   |

### Usabilidad

| ID    | Descripcion                                                                          |
|-------|--------------------------------------------------------------------------------------|
| RNF12 | El panel administrativo es usable desde Chrome, Edge y Firefox modernos             |
| RNF13 | El bot responde con mensajes claros tanto cuando encuentra como cuando no encuentra una respuesta |

## 4. Tecnologias utilizadas

- **Python 3.11**: lenguaje principal del backend y el bot.
- **FastAPI 0.115**: framework web para la API REST.
- **SQLAlchemy 2.0**: ORM para la comunicacion con PostgreSQL.
- **PostgreSQL 16**: motor de base de datos relacional.
- **python-jose**: generacion y validacion de tokens JWT.
- **passlib/bcrypt**: hashing de contrasenas.
- **python-telegram-bot 21**: interaccion con la API de Telegram.
- **Docker y Docker Compose**: contenedorizacion y orquestacion de servicios.

## 5. Estructura del proyecto

Ver `docs/arquitectura.md` seccion 4.

## 6. Modelo de datos

Ver `docs/arquitectura.md` seccion 5.

## 7. Endpoints de la API

Ver `docs/arquitectura.md` seccion 6.

## 8. Configuracion de Docker Compose

Ver `docs/arquitectura.md` seccion 9.

## 9. Variables de entorno

| Variable                     | Descripcion                                     |
|------------------------------|-------------------------------------------------|
| POSTGRES_USER                | Usuario de la base de datos                     |
| POSTGRES_PASSWORD            | Contrasena de la base de datos                  |
| POSTGRES_DB                  | Nombre de la base de datos                      |
| POSTGRES_HOST                | Host de la base de datos (default: db)          |
| POSTGRES_PORT                | Puerto de la base de datos (default: 5432)      |
| SECRET_KEY                   | Clave secreta para firmar tokens JWT            |
| ALGORITHM                    | Algoritmo JWT (default: HS256)                  |
| ACCESS_TOKEN_EXPIRE_MINUTES  | Duracion del token en minutos (default: 60)     |
| TELEGRAM_TOKEN               | Token del bot obtenido desde BotFather          |
| API_URL                      | URL de la API usada por el bot                  |

## 10. Posibles mejoras futuras

- Implementar busqueda semantica con embeddings para mejorar la precision de las respuestas.
- Agregar soporte para respuestas con imagenes o archivos adjuntos.
- Implementar un sistema de roles con distintos niveles de acceso al panel.
- Agregar notificaciones en tiempo real al panel usando WebSockets.
- Implementar rate limiting en la API para prevenir abuso.
- Agregar pruebas automatizadas con pytest.
