# BKLibDB

BKLibDB es una librería modular diseñada para simplificar la interacción con bases de datos en Python, utilizando SQLAlchemy. Ofrece una arquitectura extensible basada en modelos y managers que simplifican la realización de consultas, operaciones CRUD y manejo de lógica personalizada.

---

## **Características**

- Soporte para múltiples motores de bases de datos (PostgreSQL, SQLite, etc.).
- Estructura modular con modelos (`BKModel`) y managers (`BKManager`).
- Conversión automática de resultados de consultas en modelos (objetos).
- Métodos genéricos y personalizados para operaciones CRUD.
- Métodos `before_` y `after_` para ejecutar lógica antes y después de las operaciones CRUD.
- Métodos para convertir modelos en diccionarios o listas de diccionarios.

---

## **Requisitos**

- Python 3.8 o superior.
- SQLAlchemy.

---

## **Instalación**

Sigue estos pasos para configurar el proyecto:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/theleerise/BKLibDB.git
   cd BKLibDB/src
