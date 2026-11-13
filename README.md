# NexoShop — E-commerce simplificado

Aplicación académica full-stack con catálogo, autenticación, inventario, carrito, checkout y administración.

## Tecnologías
- Frontend: React 19 + Vite.
- Backend: Python 3.12 + FastAPI + Pydantic.
- Persistencia: SQLAlchemy 2 + SQLite por defecto o PostgreSQL.
- Seguridad: JWT, hash Argon2 y autorización por roles.
- Migraciones: Alembic. Pruebas: pytest + FastAPI TestClient.
- Docker es opcional; no es requisito para ejecutar el proyecto.

## Funcionalidades
- Registro e inicio de sesión; los registros públicos siempre crean usuarios customer.
- Catálogo con búsqueda, categorías, precio y disponibilidad.
- Carrito y checkout: el servidor vuelve a consultar precios y stock, nunca confía en el total enviado por el navegador.
- Descuento atómico de inventario dentro de una transacción para impedir vender más unidades de las disponibles.
- Historial de pedidos del cliente.
- Panel admin con métricas, CRUD de productos e historial global de pedidos.
- Pago simulado: no se reciben ni almacenan números de tarjetas.

## Arquitectura
Frontend React → API REST FastAPI → servicios de negocio → SQLAlchemy ORM → SQLite/PostgreSQL.
En backend, api/routes.py define endpoints y permisos; services/ contiene reglas de negocio; models/ define entidades; schemas.py valida entradas y salidas; core/ concentra configuración, seguridad y conexión. Alembic versiona el esquema.

## Requisitos
Python 3.12+, Node.js 20+. PostgreSQL 15+ solo si se elige ese motor. Docker Desktop/Engine solo se necesita para ejecutar contenedores.

## Ejecución local sin Docker
Terminal 1:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
python -m app.seed_admin
uvicorn app.main:app --reload
```
API: http://localhost:8000 · Swagger: http://localhost:8000/docs

Terminal 2:
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Tienda: http://localhost:5173

## Credenciales de demostración
- Administrador: admin@nexoshop.local
- Contraseña inicial: Admin123!
- Usuario cliente: regístralo desde la interfaz.

La contraseña del administrador es solo para demostración. Cámbiala y reemplaza SECRET_KEY antes de cualquier despliegue público.

## Docker opcional
Desde la raíz del repositorio:
```bash
docker compose up --build
```
Abre http://localhost:5173 y http://localhost:8000/docs. Para detener: docker compose down. Para borrar también los datos persistidos: docker compose down -v.

## Migraciones y pruebas
Desde backend/ con el entorno virtual activo:
```bash
alembic upgrade head
pytest -q
```
Para generar una migración después de cambiar modelos: alembic revision --autogenerate -m "describe el cambio". Revisa siempre el archivo generado antes de aplicarlo.

## Recorrido sugerido
1. Inicia sesión como administrador y muestra panel, métricas y CRUD.
2. Cierra sesión, registra un cliente y agrega productos al carrito.
3. Finaliza una compra con pago simulado.
4. Comprueba el historial del cliente y el nuevo stock desde el panel admin.
5. Intenta comprar más unidades de las disponibles para observar la respuesta 409.

## Endpoints principales
- POST /api/auth/register, POST /api/auth/login, GET /api/auth/me
- GET /api/products, GET /api/products/{id}, POST/PATCH/DELETE /api/products
- POST /api/orders/checkout, GET /api/orders/me
- GET /api/admin/summary, GET /api/admin/orders

## Alcance y producción
El proveedor de pago es simulado, adecuado para una prueba académica. Producción requiere pasarela tokenizada, secretos seguros, HTTPS, CORS restringido, rate limiting, observabilidad, privacidad y revisión de seguridad. El pago simulado no representa una transacción bancaria real.
