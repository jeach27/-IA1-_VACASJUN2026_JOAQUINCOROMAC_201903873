# Smart Warehouse

Sistema inteligente de simulacion de bodega automatizada con robots virtuales que transportan paquetes utilizando reglas de inferencia en Prolog.

## Integrantes

| Nombre | Carnet |
|---|---|
| Joaquin Emmanuel Aldair Coromac Huezo | 201903873 |

## Repositorio

Universidad de San Carlos de Guatemala - Facultad de Ingenieria - Ingenieria en Ciencias y Sistemas  
Curso: Inteligencia Artificial 1

## Descripcion

Smart Warehouse simula una bodega automatizada donde robots virtuales toman decisiones de navegacion, recoleccion y entrega de paquetes utilizando una base de conocimiento en Prolog. El sistema integra un frontend web interactivo, un backend en Python con Flask y el motor de inferencia SWI-Prolog.

## Requisitos Previos

- Python 3.x
- SWI-Prolog instalado y en el PATH del sistema
- Navegador moderno (Chrome, Edge, Firefox)

## Instalacion

```bash
cd backend
pip install -r requirements.txt
```

## Ejecucion

```bash
# Iniciar el backend
cd backend
python app.py

# Abrir el frontend
# Abrir frontend/index.html en el navegador
```

## Ejecucion con Docker

```bash
cd PROYECTO2
docker compose up --build
```

Abrir en el navegador: `http://localhost:5000`

## Estructura del Proyecto

```
PROYECTO2/
    backend/
        app.py              - Servidor Flask con endpoints de la simulacion
        prolog_interface.py - Interfaz de comunicacion con SWI-Prolog
        requirements.txt    - Dependencias Python
    prolog/
        warehouse.pl        - Base de conocimiento y reglas de inferencia
    frontend/
        index.html          - Interfaz web principal
        styles.css          - Estilos de la interfaz
        app.js              - Logica de la simulacion en el cliente
    docs/
        documento_tecnico.md - Arquitectura y documentacion tecnica
        manual_usuario.md    - Guia de instalacion y uso
        evidencias/          - Capturas de pantalla del sistema
    README.md
```