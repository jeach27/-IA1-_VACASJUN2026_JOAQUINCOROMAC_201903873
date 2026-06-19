# SmartInvoice

Sistema inteligente para el procesamiento automatico de facturas mediante Computer Vision, OCR y automatizacion RPA.

## Descripcion

SmartInvoice permite a las organizaciones automatizar el procesamiento de facturas digitales. El sistema carga facturas en formato PDF, JPG, JPEG o PNG, extrae la informacion relevante mediante tecnicas de vision por computadora y OCR, almacena los datos en una base de datos relacional, genera reportes administrativos y envia notificaciones por correo electronico.

## Tecnologias utilizadas

- **Backend:** Python 3.11, FastAPI
- **Base de datos:** PostgreSQL, SQLAlchemy, Alembic
- **OCR:** EasyOCR
- **Computer Vision:** OpenCV
- **RPA:** Playwright
- **Reportes:** ReportLab (PDF), openpyxl (Excel), csv (CSV)
- **Contenedores:** Docker, Docker Compose
- **Autenticacion:** JWT con python-jose

## Instrucciones de instalacion local

### Requisitos previos
- Docker y Docker Compose instalados
- Git instalado

### Clonar el repositorio
```bash
git clone <URL_REPOSITORIO>
cd smartinvoice
```

### Configurar variables de entorno
```bash
cp backend/.env.example backend/.env
```
Editar `backend/.env` con los valores correspondientes.

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

El sistema estara disponible en:
- Frontend: http://localhost:8080
- API REST: http://localhost:8000
- Documentacion API: http://localhost:8000/docs

## URL de despliegue en la nube

Pendiente de configurar en la Fase 12.

## Repositorio

Practicas del curso IA1 - Vacaciones del primer semestre 2026
Universidad San Carlos de Guatemala - Facultad de Ingenieria

**Estudiante:** Joaquin Coromac - 201903873