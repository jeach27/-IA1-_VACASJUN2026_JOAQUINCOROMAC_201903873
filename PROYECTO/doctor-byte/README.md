# Doctor Byte

Sistema experto para el diagnostico de fallas comunes en computadoras.

Proyecto Fase 1 - Inteligencia Artificial 1  
Universidad San Carlos de Guatemala - Facultad de Ingenieria  
Ingenieria en Ciencias y Sistemas

---

## Descripcion

El usuario selecciona sintomas desde una interfaz web. El sistema evalua las reglas de inferencia implementadas en Prolog y genera un diagnostico con recomendaciones. Los resultados se guardan en un historial y se pueden enviar opcionalmente a Telegram.

---

## Requisitos

- Python 3.10 o superior
- SWI-Prolog 9.x (debe estar en el PATH del sistema)
- pip

---

## Instalacion

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example ../.env
# Editar .env con el token de Telegram si se desea usar notificaciones
```

---

## Ejecucion

```bash
cd backend
python app.py
```

Abrir en el navegador: http://localhost:5000

---

## Estructura

```
doctor-byte/
├── prolog/          # Base de conocimiento SWI-Prolog
├── backend/         # Servidor Flask + integracion Prolog + Telegram
├── frontend/        # Interfaz web (HTML + CSS + JavaScript)
└── docs/            # Documentacion tecnica, manual y casos de prueba
```

Ver `docs/arquitectura.md` para la descripcion completa del sistema.  
Ver `docs/manual_usuario.md` para instrucciones de uso detalladas.

---

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Motor de inferencia | SWI-Prolog |
| Backend | Python + Flask |
| Frontend | HTML5 + CSS3 + JavaScript |
| Notificaciones | Telegram Bot API |
