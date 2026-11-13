# NexoShop — Plataforma de comercio electrónico

NexoShop es una aplicación web de comercio electrónico desarrollada como proyecto académico full-stack. Integra una interfaz de usuario construida con React y una API REST desarrollada con FastAPI, con persistencia de datos mediante SQLAlchemy y una base de datos relacional.

El proyecto implementa los procesos principales de una tienda en línea: consulta de catálogo, autenticación de usuarios, gestión del carrito, generación de pedidos, control de inventario y administración de productos y órdenes.


## Enlaces de acceso

Los siguientes enlaces corresponden al entorno de ejecución del proyecto en GitHub Codespaces:

| Recurso | Enlace | Descripción |
|---|---|---|
| **Frontend** | [NexoShop – Tienda](https://crispy-waddle-4jw95g5p449r37x7v-5173.app.github.dev/) | Interfaz web de la tienda. |
| **Backend** | [API FastAPI](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/) | Servicio backend. |
| **Swagger UI** | [Documentación interactiva](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/docs) | Exploración y ejecución de los endpoints de la API. |
| **OpenAPI** | [Especificación JSON](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/openapi.json) | Esquema de la API en formato OpenAPI. |
| **Health check** | [Estado del backend](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/health) | Verificación básica de disponibilidad del servicio. |

> **Disponibilidad:** estos enlaces pertenecen a un Codespace específico, no a un servicio de hosting permanente. Para acceder a ellos, el Codespace debe estar activo y los servidores frontend y backend deben estar ejecutándose. El acceso desde otros usuarios o dispositivos requiere que los puertos correspondientes estén compartidos con los permisos adecuados.


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

## Buenas prácticas de desarrollo, SOLID y DRY

Esta sección explica las prácticas identificables en la implementación actual y presenta ejemplos del código. Es importante distinguir entre principios aplicados en partes concretas y una implementación completa: la arquitectura tiene separación de responsabilidades en el backend, mientras que el componente principal del frontend todavía concentra varias funciones y puede modularizarse más.

### 1. Buenas prácticas de desarrollo

- **Separación por capas y módulos:** la API, la configuración, la seguridad, las dependencias, los modelos, los esquemas y los servicios se encuentran en módulos diferentes dentro de `backend/app/`.
- **Validación de entrada:** los esquemas Pydantic definen restricciones de tipos, longitudes, rangos y valores permitidos antes de ejecutar las operaciones.
- **Validación en el servidor:** el checkout obtiene precios y existencias desde la base de datos; no confía en los valores enviados por el navegador.
- **Manejo de errores HTTP:** la API comunica situaciones como credenciales incorrectas (401), falta de permisos (403), recursos inexistentes (404), conflictos de inventario (409) y datos inválidos (422).
- **Persistencia consistente:** el checkout actualiza existencias y crea el pedido en una misma transacción; si ocurre un error, ejecuta rollback.
- **Seguridad:** las contraseñas se almacenan mediante hashes Argon2, se utilizan tokens JWT y las operaciones administrativas verifican el rol.
- **Configuración externa:** los parámetros sensibles y de entorno se suministran mediante variables de entorno, no deben quedar escritos directamente en el código.
- **Control de cambios:** el trabajo se organiza en ramas y Pull Requests para revisar los cambios antes de integrarlos a `main`.

**Ejemplo — validación con Pydantic** (`backend/app/schemas.py`):

```python
class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=140)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    stock: int = Field(ge=0)
```

Este esquema evita aceptar nombres demasiado cortos, precios no positivos o existencias negativas. FastAPI utiliza el esquema para validar el cuerpo de la petición y generar respuestas de validación.

**Ejemplo — autorización de una operación administrativa** (`backend/app/dependencies.py`):

```python
def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Se requiere rol administrador")
    return user
```

La dependencia centraliza la comprobación del rol y puede reutilizarse en las rutas que requieren permisos administrativos.

### 2. Principios SOLID

SOLID reúne cinco principios para facilitar el mantenimiento y la evolución del software. En NexoShop se observan aplicaciones parciales y oportunidades de mejora:

| Principio | Aplicación en el proyecto | Ejemplo |
|---|---|---|
| **S — Responsabilidad única** | Hay módulos con responsabilidades diferenciadas: seguridad, configuración, dependencias, modelos, esquemas y servicio de pedidos. | `app/core/security.py` gestiona funciones de seguridad; `app/services/orders.py` contiene el proceso de checkout. |
| **O — Abierto/cerrado** | Los esquemas de creación y actualización separan los datos de entrada y permiten extender validaciones sin cambiar el modelo de salida. | `ProductCreate` y `ProductUpdate` en `app/schemas.py`. |
| **L — Sustitución de Liskov** | Los modelos y esquemas mantienen contratos de datos compatibles con las operaciones que los consumen. No hay una jerarquía polimórfica compleja que permita demostrar este principio de forma amplia. | `ProductOut` extiende `ProductCreate` y añade el identificador para representar la salida del producto. |
| **I — Segregación de interfaces** | Los contratos de entrada y salida se mantienen separados y específicos para cada operación, evitando un único esquema para todos los casos. | `ProductCreate`, `ProductUpdate` y `ProductOut`. |
| **D — Inversión de dependencias** | Las rutas reciben la sesión de base de datos y el usuario mediante dependencias de FastAPI, en lugar de construirlos directamente dentro de cada endpoint. | `Depends(get_db)`, `Depends(get_current_user)` y `Depends(require_admin)`. |

**Ejemplo — inyección de dependencias**:

```python
@api.get("/products", response_model=list[ProductOut])
def list_products(
    q: str | None = None,
    db: Session = Depends(get_db),
):
    statement = select(Product).order_by(Product.id.desc())
    if q:
        statement = statement.where(Product.name.ilike(f"%{q}%"))
    return db.scalars(statement).all()
```

La ruta declara que necesita una sesión, pero la creación y el ciclo de vida de esa sesión corresponden a `get_db`. Esto reduce el acoplamiento con la configuración concreta de la conexión.

**Alcance real de SOLID:** estos ejemplos muestran decisiones alineadas con SOLID, pero no significan que todos los módulos cumplan perfectamente los cinco principios. En particular, `backend/app/api/routes.py` todavía agrupa endpoints de varios recursos y el componente `frontend/src/App.jsx` concentra estado, llamadas HTTP y presentación. Una siguiente refactorización puede separar routers por recurso, extraer servicios de aplicación y dividir el frontend en componentes, hooks y un cliente API. Esa separación debe hacerse acompañada de pruebas de regresión.

### 3. Principio DRY (Don't Repeat Yourself)

DRY busca evitar duplicar reglas o lógica que deban mantenerse sincronizadas. En el proyecto se aplica mediante funciones y dependencias reutilizables:

- `get_db` centraliza la provisión de sesiones de base de datos.
- `get_current_user` centraliza la autenticación del usuario.
- `require_admin` reutiliza la autenticación y añade la regla de autorización administrativa.
- `checkout` concentra el cálculo del pedido, la validación de inventario y la persistencia transaccional en un servicio invocado por la ruta.

**Ejemplo — una sola implementación del checkout**:

```python
@api.post("/orders/checkout", response_model=OrderOut, status_code=201)
def create_order(
    payload: CheckoutIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items = [item.model_dump() for item in payload.items]
    return checkout(db, user.id, items)
```

La ruta se limita a adaptar la petición HTTP y delegar la regla de negocio en `checkout`. Así, la lógica de inventario y creación de pedidos no necesita repetirse en el endpoint.

### 4. Pruebas unitarias y de integración

El proyecto incluye pruebas automatizadas con `pytest` y `FastAPI TestClient`. Las pruebas existentes verifican flujos de API que involucran varias capas; por ello, es más preciso describirlas como pruebas de integración/API, aunque el requisito de pruebas sea opcional.

Actualmente se comprueban, entre otros, estos escenarios:

- Registro de un cliente y asignación del rol `customer`.
- Inicio de sesión y consulta del usuario autenticado.
- Rechazo de una operación administrativa por parte de un cliente (403).
- Rechazo de un checkout cuando no hay existencias suficientes (409).
- Conservación del inventario cuando el checkout falla.
- Creación de un pedido cuando hay existencias y descuento correcto del inventario.

**Ejemplo — prueba de permisos** (`backend/tests/test_api.py`):

```python
assert response.status_code == 201
assert response.json()["role"] == "customer"

# Un cliente no puede crear productos como administrador.
assert product_response.status_code == 403
```

**Ejemplo — prueba de inventario**:

```python
assert insufficient_stock_response.status_code == 409

with SessionLocal() as db:
    assert db.get(Product, product_id).stock == 1
```

Para ejecutar las pruebas desde la carpeta `backend/` en Codespaces:

```bash
pytest -q
```

La existencia de pruebas en el repositorio no implica que se hayan ejecutado en cada entorno. Antes de una entrega se debe ejecutar el comando y registrar el resultado real. También es recomendable ampliar la cobertura con pruebas de actualización y eliminación de productos, acceso administrativo, checkout exitoso, rollback ante errores y validaciones de esquemas.

### 5. Sustentación del desarrollo

La siguiente estructura permite explicar y demostrar el cumplimiento de los criterios durante una presentación:

1. **Arquitectura (1 minuto):** mostrar el recorrido navegador → React/Vite → API FastAPI → SQLAlchemy → SQLite o PostgreSQL. Explicar que el frontend consume la API mediante HTTP/JSON y no accede directamente a la base de datos.
2. **Buenas prácticas (1 minuto):** ubicar `core/security.py`, `dependencies.py`, `schemas.py`, `models/` y `services/orders.py`. Explicar qué responsabilidad tiene cada módulo.
3. **SOLID (1–2 minutos):** demostrar la inyección de `get_db`, la separación de esquemas `ProductCreate/ProductUpdate/ProductOut` y la delegación del checkout al servicio. Reconocer que `routes.py` y `App.jsx` aún admiten una separación adicional.
4. **DRY (1 minuto):** mostrar cómo `get_current_user` y `require_admin` evitan repetir autenticación y autorización, y cómo la ruta de checkout reutiliza el servicio `checkout`.
5. **Demostración funcional (1–2 minutos):** consultar `GET /api/products` en Swagger, registrar o autenticar un cliente, intentar una operación administrativa para mostrar el 403 y ejecutar un checkout para observar el descuento de inventario.
6. **Pruebas (1 minuto):** ejecutar `pytest -q` y explicar qué escenarios cubren las pruebas existentes. Presentar la salida real, sin afirmar que las pruebas pasan si no se han ejecutado.

**Idea central para la sustentación:** NexoShop separa la interfaz, la API y la persistencia; valida las entradas y los permisos en el servidor; centraliza reglas reutilizables y protege la consistencia del inventario mediante transacciones. SOLID y DRY se aplican en decisiones concretas del backend, aunque se reconocen oportunidades de modularización adicional en las rutas y en el frontend.

