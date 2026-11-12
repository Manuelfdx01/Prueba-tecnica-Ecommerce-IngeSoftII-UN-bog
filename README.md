# NexoShop

E-commerce académico con FastAPI, React y PostgreSQL. SQLite funciona por defecto para facilitar el desarrollo local. Docker Compose es opcional.

## Funcionalidades
- Registro/login JWT, contraseñas Argon2 y roles customer/admin.
- Catálogo, búsqueda y CRUD administrativo de productos.
- Carrito y checkout; el backend recalcula precios y valida stock.
- Descuento de inventario mediante UPDATE condicional y transacción para evitar sobreventas.
- Órdenes e historial personal, pago simulado, métricas admin y Swagger.

## Arquitectura
Router → Service → ORM → DB. Pydantic separa contratos HTTP de entidades. Capas: `api/`, `core/`, `models/`, `schemas.py`, `services/`. Frontend React/Vite.

## Requisitos
Python 3.11+, Node 20+. PostgreSQL 15+ opcional para desarrollo (SQLite por defecto). Docker opcional.

## Backend sin Docker
`cd backend`; crear/activar venv; `pip install -r requirements.txt`; copiar `.env.example` a `.env`; ejecutar `uvicorn app.main:app --reload`. Swagger: http://localhost:8000/docs

## Frontend sin Docker
En otra terminal: `cd frontend`; `npm install`; copiar `.env.example` a `.env`; `npm run dev`. Abrir http://localhost:5173

## Datos demo y administrador
Desde `backend/`: `python -m app.seed_admin`. Usuario `admin@nexoshop.local`, contraseña `Admin123!`. Cambiar antes de desplegar.

## Docker opcional
Desde la raíz: `docker compose up --build`. Frontend :5173, API :8000, PostgreSQL :5432.

## Pruebas
Desde backend: `pip install -r requirements-dev.txt && pytest`.

## API
POST `/api/auth/register`, POST `/api/auth/login`, GET `/api/auth/me`, GET `/api/products`, POST/PATCH/DELETE `/api/products` (admin), POST `/api/orders/checkout`, GET `/api/orders/me`, GET `/api/admin/summary` (admin).

## Producción
Cambiar SECRET_KEY y credenciales demo, restringir CORS, usar HTTPS. Para pagos reales integrar un proveedor con tokenización. Añadir Alembic, rate limiting, logging y gestión de secretos antes de producción. No se almacenan datos de tarjetas.
