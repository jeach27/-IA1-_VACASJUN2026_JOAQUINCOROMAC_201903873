-- Esquema inicial de SmartBot
-- Ejecutado automaticamente al levantar el contenedor de PostgreSQL

CREATE TABLE IF NOT EXISTS categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    creado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS pregunta (
    id SERIAL PRIMARY KEY,
    texto TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    categoria_id INTEGER REFERENCES categoria(id) ON DELETE SET NULL,
    activa BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS usuario_admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    creado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consulta (
    id SERIAL PRIMARY KEY,
    telegram_user VARCHAR(100),
    telegram_user_id BIGINT,
    texto_consulta TEXT NOT NULL,
    texto_respuesta TEXT,
    pregunta_id INTEGER REFERENCES pregunta(id) ON DELETE SET NULL,
    encontrada BOOLEAN DEFAULT FALSE,
    consultado_en TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS configuracion (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(100) NOT NULL UNIQUE,
    valor TEXT,
    descripcion TEXT,
    actualizado_en TIMESTAMP DEFAULT NOW()
);

-- El usuario administrador es creado por el backend al iniciar (seed_admin en main.py)
-- para garantizar que el hash bcrypt sea generado correctamente con passlib.

-- Categorias iniciales
INSERT INTO categoria (nombre, descripcion) VALUES
('Horarios', 'Informacion sobre horarios de atencion y actividades'),
('Tramites', 'Procedimientos y requisitos para realizar tramites academicos'),
('Tecnologia', 'Preguntas sobre sistemas, plataformas y herramientas digitales'),
('Pagos', 'Informacion sobre pagos, aranceles y costos'),
('General', 'Preguntas generales sobre la institucion')
ON CONFLICT (nombre) DO NOTHING;

-- Preguntas frecuentes con respuestas (minimo 20)
INSERT INTO pregunta (texto, respuesta, categoria_id) VALUES
-- Horarios (categoria 1)
('Cuales son los horarios de atencion?', 'Atendemos de lunes a viernes de 8:00 a 17:00 horas y sabados de 8:00 a 12:00 horas.', 1),
('Cuando esta abierta la biblioteca?', 'La biblioteca esta abierta de lunes a viernes de 7:00 a 20:00 horas y sabados de 8:00 a 14:00 horas.', 1),
('Cuales son los horarios del laboratorio?', 'Los laboratorios estan disponibles de lunes a viernes de 7:00 a 19:00 horas segun disponibilidad de equipos.', 1),
('Hay atencion los dias festivos?', 'No, los dias festivos oficiales no hay atencion presencial. Se puede consultar informacion a traves de este bot.', 1),
('A que hora abren las instalaciones?', 'Las instalaciones abren a las 6:30 horas de lunes a viernes y a las 7:00 horas los sabados.', 1),

-- Tramites (categoria 2)
('Como solicito una constancia de estudios?', 'Para solicitar una constancia de estudios debes ingresar al portal estudiantil con tu numero de carnet, seleccionar la opcion Documentos y completar el formulario de solicitud. El documento se emite en 3 dias habiles.', 2),
('Cuales son los requisitos para inscripcion?', 'Para inscripcion necesitas: carnet universitario vigente, solvencia de biblioteca, solvencia de pagos, y completar el proceso en linea en las fechas establecidas por el calendario academico.', 2),
('Como realizo el cambio de carrera?', 'El cambio de carrera se solicita en Control Academico durante las fechas habilitadas. Debes presentar: carta de solicitud, record de notas y cumplir con los requisitos de la nueva carrera.', 2),
('Donde solicito mi diploma de graduacion?', 'El diploma de graduacion se gestiona en la Secretaria General de la Facultad. Debes presentar tu certificacion de cursos aprobados y estar al dia con todos tus pagos.', 2),
('Como solicito equivalencia de cursos?', 'Las equivalencias se solicitan en la Coordinacion Academica de tu carrera, presentando el pensum de tu institucion anterior y los programas de los cursos a equivalar.', 2),

-- Tecnologia (categoria 3)
('Como accedo al portal estudiantil?', 'Ingresa a portal.usac.edu.gt con tu numero de carnet como usuario y tu fecha de nacimiento en formato DDMMAAAA como contrasena inicial.', 3),
('Donde puedo encontrar los recursos del curso?', 'Los recursos de cada curso estan disponibles en el sistema de gestion de aprendizaje (LMS). Tu docente publicara el enlace de acceso al inicio del semestre.', 3),
('Como me conecto a la red WiFi de la facultad?', 'Conéctate a la red USAC-ESTUDIANTES usando tu correo institucional y la contrasena de tu portal estudiantil.', 3),
('Existe una aplicacion movil para estudiantes?', 'Si, la aplicacion USAC Mobile esta disponible en Google Play y App Store. Permite consultar notas, horarios y comunicados oficiales.', 3),
('Como recupero mi contrasena del portal?', 'Para recuperar tu contrasena visita portal.usac.edu.gt/recuperar e ingresa tu numero de carnet. Recibiras un correo con las instrucciones de recuperacion.', 3),

-- Pagos (categoria 4)
('Cuanto cuesta la inscripcion semestral?', 'El costo de inscripcion varía segun la carrera y el numero de creditos a inscribir. Consulta el arancel vigente en la pagina oficial o en la Tesoreria de la Facultad.', 4),
('Donde puedo pagar mis aranceles universitarios?', 'Los pagos se realizan en el Banco de Desarrollo Rural (Banrural) en cualquier agencia del pais, o mediante transferencia electronica a la cuenta indicada en tu boleta de pago.', 4),
('Cuando vencen los pagos del semestre?', 'Los pagos del semestre deben realizarse antes de la fecha indicada en el calendario academico. El incumplimiento puede resultar en restricciones para inscribir cursos.', 4),
('Como obtengo mi boleta de pago?', 'Tu boleta de pago se descarga desde el portal estudiantil en la seccion de Pagos. Si tienes problemas accediendo, visita la Tesoreria de tu facultad.', 4),

-- General (categoria 5)
('Donde queda la Facultad de Ingenieria?', 'La Facultad de Ingenieria de la USAC se encuentra en el Campus Central de la Universidad de San Carlos de Guatemala, Ciudad Universitaria, zona 12, Ciudad de Guatemala.', 5),
('Como contacto a mi docente?', 'Puedes contactar a tu docente a traves del correo institucional publicado en el listado de docentes de la facultad o mediante el foro de comunicacion del LMS del curso.', 5),
('Existe servicio de tutoria academica?', 'Si, la Unidad de Apoyo Estudiantil ofrece tutorias academicas gratuitas para estudiantes que lo necesiten. Consulta los horarios disponibles en la recepcion de la facultad.', 5),
('Como me afilio al seguro estudiantil?', 'La afiliacion al seguro estudiantil es automatica al momento de inscripcion. Para reportar un accidente o usar el seguro, acude a la Unidad de Salud del campus.', 5)
ON CONFLICT DO NOTHING;

-- Configuracion inicial del sistema
INSERT INTO configuracion (clave, valor, descripcion) VALUES
('telegram_chat_id', '', 'ID del grupo o chat de Telegram donde el bot envia mensajes'),
('bot_nombre', 'SmartBot', 'Nombre del bot mostrado en respuestas'),
('mensaje_no_encontrado', 'Lo siento, no encontre una respuesta para tu consulta. Por favor intenta reformular tu pregunta o contacta directamente con la institucion.', 'Mensaje cuando el bot no encuentra respuesta'),
('bot_activo', 'true', 'Indica si el bot esta activo (true) o inactivo (false). Se controla desde el panel administrativo.')
ON CONFLICT (clave) DO NOTHING;
