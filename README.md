# hotel-reservation-api
Backend manejo de lógica del negocio, reservas 
# Hotel Reservation API

API REST desarrollada con FastAPI para consultar disponibilidad de habitaciones y calcular tarifas de una cadena hotelera.

## Tecnologías

- Python 3.11
- FastAPI
- SQLAlchemy
- Pydantic
- MariaDB 10.6
- Docker y Docker Compose

## Arquitectura

El proyecto implementa programación orientada a objetos y arquitectura por capas mediante los patrones Repository, Service Layer e inyección de dependencias.

```text
app/
├── core/
├── db/
├── models/
├── repositories/
├── services/
├── schemas/
├── routers/
└── main.py
```

## Funcionalidades

Consulta de hoteles y tipos de habitación, disponibilidad por fechas, validación de capacidad de alojamiento y cálculo de tarifas según hotel, temporada, categoría, número de personas y habitaciones solicitadas.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Verificar conexión con MariaDB |
| GET | `/api/v1/hoteles` | Consultar hoteles |
| GET | `/api/v1/tipos-habitacion` | Consultar tipos de habitación |
| GET | `/api/v1/disponibilidad` | Consultar disponibilidad y calcular tarifas |

## Ejecución con Docker

El proyecto utiliza dos contenedores: FastAPI y MariaDB.

Los scripts SQL se encuentran en el repositorio independiente `hotel-booking-architecture`, que debe estar clonado al mismo nivel que este repositorio.

Crear `.env` a partir de `.env.example` y configurar las credenciales.

```bash
docker compose up -d --build
```

Verificar los servicios:

```bash
docker compose ps
```

Documentación interactiva:

http://localhost:8000/docs

Para detener los contenedores:

```bash
docker compose down
```

## Ejecución local

Crear un entorno virtual con Python 3.11, activarlo e instalar las dependencias:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La conexión local utiliza `DATABASE_URL` del archivo `.env`.

## Base de datos

Esquema: `hotel_reservations`.

El modelo relacional contiene ocho tablas y contempla cuatro sedes hoteleras con 108 habitaciones.

Las tarifas y temporadas utilizadas son datos de prueba.

## Documentación

La documentación técnica y las evidencias de ejecución se almacenan en `docs/`.

La implementación permite incorporar posteriormente la gestión de reservas y operaciones CRUD.