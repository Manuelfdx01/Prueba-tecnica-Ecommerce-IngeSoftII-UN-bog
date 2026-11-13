# NexoShop — Plataforma de comercio electrónico

NexoShop es una aplicación web de comercio electrónico desarrollada como proyecto académico full-stack. Integra una interfaz de usuario construida con React y una API REST desarrollada con FastAPI, con persistencia de datos mediante SQLAlchemy y una base de datos relacional.

El proyecto implementa los procesos principales de una tienda en línea: consulta de catálogo, autenticación de usuarios, gestión del carrito, generación de pedidos, control de inventario y administración de productos y órdenes.

## Funcionalidades

### Experiencia de compra
- Visualización del catálogo de productos.
- Consulta y búsqueda de productos, categorías, precios y disponibilidad.
- Gestión del carrito de compras.
- Registro e inicio de sesión de clientes.
- Generación de pedidos mediante el proceso de checkout.
- Consulta del historial de pedidos del cliente.

### Administración
- Acceso a funcionalidades administrativas mediante control de roles.
- Creación, consulta, actualización y eliminación de productos.
- Consulta global de pedidos.
- Visualización de métricas generales de la tienda.

### Reglas de negocio
- El registro público asigna el rol de cliente.
- El backend valida los datos recibidos y aplica las reglas de autorización.
- Durante el checkout, los precios y las existencias se consultan en el servidor.
- La actualización del inventario y la creación del pedido se realizan dentro de una transacción para mantener la consistencia de los datos.
- El procesamiento de pagos es simulado; la aplicación no procesa transacciones bancarias ni almacena datos de tarjetas.

## Arquitectura

La solución sigue una arquitectura cliente-servidor organizada en dos aplicaciones principales:

```text
┌──────────────────────────────┐
│       Cliente / navegador    │
└──────────────┬───────────────┘
               │ HTTP / JSON
               ▼
┌──────────────────────────────┐
│       Frontend React         │
│          Vite                │
└──────────────┬───────────────┘
               │ API REST
               ▼
┌──────────────────────────────┐
│        Backend FastAPI       │
│  Rutas, validación y lógica   │
│         de negocio            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       SQLAlchemy ORM         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Base de datos SQL        │
│   SQLite / PostgreSQL        │
└──────────────────────────────┘
```

El frontend consume los endpoints HTTP de FastAPI e intercambia información en formato JSON. El backend centraliza la validación, autenticación, autorización y ejecución de las reglas de negocio. La persistencia se gestiona mediante modelos y sesiones de SQLAlchemy; el cliente no accede directamente a la base de datos.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Interfaz web | React 19 |
| Herramienta de desarrollo frontend | Vite |
| Estilos | CSS |
| API | Python, FastAPI y Uvicorn |
| Validación de datos | Pydantic |
| ORM | SQLAlchemy 2 |
| Base de datos principal de desarrollo | SQLite |
| Base de datos alternativa | PostgreSQL 16 |
| Autenticación | JSON Web Tokens (JWT) |
| Hash de contraseñas | Argon2 |
| Migraciones | Alembic |
| Pruebas | pytest y FastAPI TestClient |
| Contenedores | Docker y Docker Compose |

## Estructura general

```text
.
├── frontend/                 # Aplicación React
├── backend/                  # API FastAPI
│   ├── app/                  # Aplicación, modelos y lógica
│   ├── alembic/               # Migraciones de base de datos
│   └── ecommerce.db          # Base SQLite (generada en ejecución)
├── docker-compose.yml        # Orquestación de servicios
└── README.md
```

## Persistencia de datos

La aplicación admite dos configuraciones de base de datos:

- **SQLite:** configuración ligera para desarrollo y ejecución en un único entorno. En la configuración utilizada por Codespaces, el archivo de base de datos se encuentra en `backend/ecommerce.db`.
- **PostgreSQL 16:** alternativa ejecutada mediante Docker Compose, dentro de la red de contenedores del proyecto.

SQLAlchemy proporciona la capa de acceso a datos y Alembic administra las migraciones del esquema. La configuración de la conexión se define mediante la variable de entorno `DATABASE_URL`.

## Seguridad

- Autenticación basada en tokens JWT.
- Almacenamiento de contraseñas mediante hashes Argon2.
- Separación de permisos entre usuarios con rol `customer` y `admin`.
- Validación de datos de entrada en el backend.
- Restricción de operaciones administrativas según el rol del usuario.
- Verificación de precios y disponibilidad en el servidor durante el checkout.
- Configuración de orígenes permitidos mediante CORS.

Las claves de firma, credenciales y demás valores sensibles deben suministrarse mediante variables de entorno y no deben incluirse en el control de versiones.

## Requisitos

Para ejecutar el proyecto sin contenedores se requiere:

- Python 3.12 o superior.
- Node.js y npm.
- Git.

Para la ejecución contenerizada se requiere Docker y Docker Compose.

## Configuración y ejecución

### Backend

Desde la raíz del repositorio:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Configura las variables de entorno necesarias para la aplicación, incluyendo `DATABASE_URL` y `CORS_ORIGINS`. Para una ejecución con SQLite, la configuración de base de datos puede utilizar:

```env
DATABASE_URL=sqlite:///./ecommerce.db
```

Aplica las migraciones y prepara los datos iniciales:

```bash
alembic upgrade head
python -m app.seed_admin
```

Inicia el servidor:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

La API y su documentación interactiva estarán disponibles en el puerto 8000. La documentación OpenAPI se encuentra en `/docs`.

### Frontend

En otra terminal, desde la raíz del repositorio:

```bash
cd frontend
npm install
```

Configura la variable `VITE_API_URL` con la URL base de la API, incluyendo el prefijo `/api`. Por ejemplo, para una ejecución local:

```env
VITE_API_URL=http://localhost:8000/api
```

Inicia el servidor de desarrollo:

```bash
npm run dev -- --host 0.0.0.0
```

El frontend se ejecuta por defecto en el puerto 5173. Las variables de entorno de Vite se cargan al iniciar el servidor de desarrollo.

## Ejecución con Docker Compose

El repositorio incluye una configuración alternativa para ejecutar los servicios contenerizados. Desde la raíz del proyecto:

```bash
docker compose up --build
```

La configuración levanta los servicios de frontend, backend y PostgreSQL 16. La base de datos utiliza un volumen de Docker para persistir la información entre reinicios de los contenedores.

Para detener los servicios:

```bash
docker compose down
```

Para detenerlos y eliminar también el volumen de datos de PostgreSQL:

```bash
docker compose down -v
```

La configuración de Docker utiliza PostgreSQL dentro de la red privada de Compose; no requiere una base de datos administrada externa.

## API REST

Los principales recursos expuestos por el backend son:

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |
| POST | `/api/auth/register` | Registro de clientes |
| POST | `/api/auth/login` | Autenticación |
| GET | `/api/auth/me` | Información del usuario autenticado |
| GET | `/api/products` | Listado de productos |
| GET | `/api/products/{id}` | Consulta de un producto |
| POST | `/api/products` | Creación de productos (administrador) |
| PATCH | `/api/products/{id}` | Actualización de productos (administrador) |
| DELETE | `/api/products/{id}` | Eliminación de productos (administrador) |
| POST | `/api/orders/checkout` | Creación de pedidos |
| GET | `/api/orders/me` | Historial de pedidos del cliente |
| GET | `/api/admin/summary` | Métricas administrativas |
| GET | `/api/admin/orders` | Consulta global de pedidos (administrador) |

La especificación OpenAPI y la documentación interactiva de los endpoints se generan automáticamente mediante FastAPI y están disponibles en `/docs` cuando el backend está en ejecución.

## Migraciones y pruebas

Las migraciones del esquema se administran con Alembic. Para aplicar las migraciones:

```bash
cd backend
alembic upgrade head
```

Para ejecutar las pruebas automatizadas:

```bash
pytest -q
```

Para generar una migración a partir de cambios en los modelos:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

Las migraciones generadas deben revisarse antes de aplicarse.

## Alcance

NexoShop implementa un flujo académico de comercio electrónico con autenticación, autorización por roles, administración de catálogo, pedidos y persistencia relacional. El módulo de pago es una simulación y no está integrado con entidades financieras ni pasarelas de pago. La configuración de seguridad y despliegue está orientada al entorno de desarrollo y demostración; una puesta en producción requeriría, entre otros aspectos, gestión de secretos, políticas de seguridad reforzadas, monitorización, copias de seguridad y configuración de infraestructura apropiada.
