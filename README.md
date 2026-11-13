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

## Ejecución en GitHub Codespaces

Esta es la forma recomendada de iniciar el proyecto en el entorno de desarrollo del repositorio. No requiere contratar hosting ni utilizar una base de datos administrada externa: el backend se ejecuta en Codespaces con SQLite y el frontend se comunica con la API mediante los puertos reenviados del mismo Codespace.

### 1. Abrir el Codespace

1. Abre el repositorio en GitHub y selecciona **Code → Codespaces**.
2. Inicia el Codespace existente o crea uno nuevo desde la rama `main`.
3. Abre una terminal integrada en VS Code.

Verifica que estás trabajando en la rama principal:

```bash
git branch --show-current
```

Si necesitas actualizar el entorno con la versión más reciente de `main`, primero revisa que no tengas cambios locales pendientes con `git status`. Si el árbol de trabajo está limpio, ejecuta:

```bash
git pull origin main
```

### 2. Preparar y ejecutar el backend

Desde la raíz del repositorio:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.codespaces.example .env
```

Revisa el archivo `.env` y confirma que `DATABASE_URL` apunte a SQLite y que `CORS_ORIGINS` contenga el origen del frontend que aparece en la pestaña **Ports** de Codespaces. Si la URL reenviada de tu Codespace es diferente a la del archivo de ejemplo, actualízala.

Aplica las migraciones y carga los datos de demostración:

```bash
alembic upgrade head
python -m app.seed_admin
```

Inicia FastAPI:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend queda escuchando en el puerto `8000`. Mantén esta terminal abierta.

### 3. Preparar y ejecutar el frontend

Abre una segunda terminal desde la raíz del repositorio:

```bash
cd frontend
npm install
cp .env.codespaces.example .env
```

Comprueba que `VITE_API_URL` tenga la URL reenviada del puerto 8000, terminada en `/api`. Por ejemplo:

```env
VITE_API_URL=https://<tu-codespace>-8000.app.github.dev/api
```

Inicia Vite:

```bash
npm run dev -- --host 0.0.0.0
```

El frontend queda escuchando en el puerto `5173`. Mantén también esta terminal abierta.

### 4. Configurar y abrir los puertos

En la pestaña **Ports** de VS Code:

| Puerto | Servicio | Uso |
|---|---|---|
| `8000` | FastAPI | API REST y documentación |
| `5173` | Vite | Aplicación web |

Abre la URL reenviada del puerto `5173` para usar la tienda. Para verificar el backend, abre la URL del puerto `8000` y añade `/docs` para Swagger UI o consulta `/health`.

Los puertos pueden mantenerse como **Private** para uso personal. Si necesitas que otra persona pruebe la aplicación, cambia la visibilidad del puerto correspondiente a **Public** solo cuando sea necesario y comparte las URLs generadas por Codespaces.

**Importante:** los dominios `.app.github.dev` dependen del Codespace y del reenvío de puertos. Si recreas el Codespace o cambia la URL, actualiza `VITE_API_URL` en el frontend y `CORS_ORIGINS` en el backend con los nuevos orígenes. Reinicia ambos servidores después de modificar los archivos `.env`, porque Vite y la configuración de FastAPI leen esas variables al iniciar.

### 5. Detener y reanudar

Para detener los servidores, usa `Ctrl + C` en cada terminal. Esto no elimina el archivo SQLite ni los cambios del repositorio. Para volver a trabajar, abre el mismo Codespace y ejecuta nuevamente los comandos de inicio del backend y frontend; no necesitas crear otro entorno cada vez.

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

## Migraciones y pruebas automatizadas

Las migraciones del esquema se administran con Alembic. Desde la carpeta `backend`, aplica las migraciones con:

```bash
alembic upgrade head
```

### Pruebas de backend

El backend utiliza **pytest** y **FastAPI TestClient**. Los casos automatizados están en `backend/tests/`:

| Archivo | Tipo | Qué comprueba |
|---|---|---|
| `test_smoke.py` | Prueba de humo de API | Que `GET /health` responda HTTP 200 y devuelva `{"status": "ok"}`. |
| `test_api.py` | Pruebas de integración de API | Registro de cliente, inicio de sesión, consulta del usuario autenticado y rechazo (403) de una operación administrativa realizada por un cliente. También verifica el checkout: si no hay inventario suficiente responde 409 y conserva el stock; con stock disponible crea el pedido (201), calcula el total y descuenta las existencias. |
| `test_product_service.py` | Pruebas unitarias de servicio | Prueba `ProductService` con un repositorio falso, sin conectarse a una base de datos real: consulta y creación delegadas al repositorio, error al consultar un producto inexistente y protección contra eliminar productos que tienen historial de pedidos. |

Para ejecutar todas las pruebas desde Codespaces:

```bash
cd backend
source .venv/bin/activate
pytest -q
```

Estas pruebas cubren endpoints y reglas seleccionadas del catálogo, autenticación, permisos y checkout. No representan una cobertura exhaustiva de todos los módulos ni sustituyen pruebas de carga, seguridad o aceptación de usuario.

### Validación de frontend

El frontend actualmente no tiene un framework ni una suite de pruebas unitarias o de componentes configurada en `package.json`. La validación automatizada de frontend en CI ejecuta `npm run build`, que usa Vite y esbuild para transformar los módulos JSX/JavaScript y generar el paquete de producción. Esto detecta, entre otros problemas, errores de sintaxis e importaciones que impiden compilar la aplicación, pero **no equivale a pruebas funcionales de interacción en el navegador**.

Para ejecutar la misma validación localmente:

```bash
cd frontend
npm install
npm run build
```

### Integración continua con GitHub Actions

El workflow `.github/workflows/ci.yml` ejecuta dos trabajos independientes cuando hay un push a `main` o a ramas `feat/**`, y cuando se abre o actualiza un Pull Request dirigido a `main`:

- **backend:** configura Python 3.12, instala `backend/requirements-dev.txt`, aplica las migraciones con `alembic upgrade head` y ejecuta `pytest -q`.
- **frontend:** configura Node.js 20, instala dependencias con `npm install` y ejecuta `npm run build`.

Un resultado exitoso de CI significa que las pruebas automatizadas definidas para backend finalizaron correctamente y que el frontend pudo compilarse para producción. No significa que exista una suite de pruebas de interfaz de usuario para frontend.

### Generar migraciones

Para generar una migración a partir de cambios en los modelos:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
```

Las migraciones generadas deben revisarse antes de aplicarse.

## Alcance

NexoShop implementa un flujo académico de comercio electrónico con autenticación, autorización por roles, administración de catálogo, pedidos y persistencia relacional. El módulo de pago es una simulación y no está integrado con entidades financieras ni pasarelas de pago. La configuración de seguridad y despliegue está orientada al entorno de desarrollo y demostración; una puesta en producción requeriría, entre otros aspectos, gestión de secretos, políticas de seguridad reforzadas, monitorización, copias de seguridad y configuración de infraestructura apropiada.

## Buenas prácticas, SOLID y DRY

La implementación separa responsabilidades en backend y frontend. Las rutas HTTP actúan como adaptadores de entrada; los servicios contienen reglas de aplicación; los repositorios aíslan el acceso a datos; y los esquemas Pydantic definen contratos de entrada y salida.

SOLID no significa crear interfaces o clases sin necesidad. Se aplica donde reduce acoplamiento y facilita probar o sustituir una implementación. El alcance se demuestra con los ejemplos y pruebas descritos abajo; no se afirma que un software sea perfecto o que no requiera evolución.

### 1. Buenas prácticas de desarrollo

- **Responsabilidades delimitadas:** los routers se separan por recurso: api/auth.py, api/products.py, api/orders.py y api/admin.py.
- **Separación de capas:** las rutas traducen HTTP, los servicios ejecutan casos de uso y los repositorios gestionan persistencia.
- **Validación de entrada:** Pydantic valida tipos, longitudes, rangos y valores permitidos.
- **Reglas críticas en el servidor:** precios y existencias se consultan en la base de datos durante el checkout; el navegador no determina el precio final.
- **Consistencia transaccional:** la actualización del inventario y la creación del pedido se confirman en una transacción; un error provoca rollback.
- **Seguridad:** las contraseñas se almacenan con Argon2, la autenticación usa JWT y las operaciones administrativas exigen el rol correspondiente.
- **Errores explícitos:** la API responde con códigos HTTP adecuados para validación, autenticación, permisos, recursos inexistentes y conflictos de inventario.
- **Configuración por entorno:** URL de base de datos, clave de firma y orígenes CORS se parametrizan mediante variables de entorno.
- **Cambios revisables:** las mejoras se trabajan en ramas y Pull Requests para no mezclar refactorizaciones con main.

### 2. Aplicación de los cinco principios SOLID

#### S — Single Responsibility Principle (responsabilidad única)

Cada módulo tiene un motivo principal para cambiar:

- api/products.py: contrato HTTP del catálogo.
- services/products.py: reglas de aplicación del catálogo.
- repositories/sqlalchemy_product_repository.py: persistencia de productos con SQLAlchemy.
- services/orders.py: reglas transaccionales del checkout.
- En frontend, services/api.js gestiona comunicación HTTP, hooks/useCart.js encapsula las reglas del carrito y hooks/useSession.js administra autenticación y persistencia de sesión. App.jsx actúa como componente de composición de la pantalla.

**Ejemplo:** el endpoint de listado delega el caso de uso al servicio ProductService. La ruta no construye consultas SQL ni conoce cómo se almacenan los productos.

#### O — Open/Closed Principle (abierto/cerrado)

El servicio de productos trabaja con el contrato ProductRepository, no con una implementación SQLAlchemy concreta. Se puede incorporar otra implementación del repositorio (por ejemplo, para otra base de datos o pruebas) sin reescribir las reglas del servicio. Los nuevos endpoints también se incorporan como routers independientes y se registran en el agregador.

#### L — Liskov Substitution Principle (sustitución de Liskov)

Cualquier implementación que cumpla el contrato ProductRepository debe poder sustituir a otra sin romper las expectativas del servicio: listar, consultar, crear, actualizar, verificar historial y eliminar productos con los mismos contratos de retorno y comportamiento.

El adaptador real es SqlAlchemyProductRepository; las pruebas utilizan FakeProductRepository, que implementa el mismo contrato para probar el servicio sin conectarse a la base de datos.

**Ejemplo:** ProductService recibe un repositorio falso en las pruebas y obtiene productos sin saber si la persistencia real es SQLAlchemy o una implementación de prueba. Esto comprueba la sustitución estructural del contrato.

#### I — Interface Segregation Principle (segregación de interfaces)

El contrato ProductRepository contiene únicamente operaciones necesarias para el caso de uso del catálogo. No obliga al servicio de productos a depender de métodos de usuarios, pagos o reportes. Los esquemas también separan creación, actualización y representación de salida: ProductCreate, ProductUpdate y ProductOut.

#### D — Dependency Inversion Principle (inversión de dependencias)

La lógica de aplicación depende de la abstracción ProductRepository. La implementación SQLAlchemy se construye en el punto de composición de FastAPI, mediante get_product_service, y se inyecta al router.

**Ejemplo conceptual del flujo:**

- FastAPI ejecuta get_product_service y crea SqlAlchemyProductRepository con la sesión recibida.
- ProductService recibe el repositorio mediante su constructor.
- ProductService solo conoce las operaciones definidas por ProductRepository; no conoce SQLAlchemy ni crea sesiones.

Así, el servicio puede probarse con un repositorio falso y la persistencia puede cambiarse sin reescribir las reglas del catálogo.

**Ejemplo de implementación del contrato y del servicio:**

    class ProductService:
        def __init__(self, repository: ProductRepository):
            self._repository = repository

        def list_products(self, query=None, category=None):
            return self._repository.list(query, category)

La clase recibe una abstracción y delega la consulta. No importa ni instancia SqlAlchemyProductRepository.

### 3. Aplicación de DRY (Don't Repeat Yourself)

- La autenticación y autorización se centralizan en get_current_user y require_admin.
- El acceso a datos del catálogo se concentra en SqlAlchemyProductRepository.
- Las reglas del catálogo se implementan una sola vez en ProductService.
- La lógica de checkout se centraliza en services/orders.py.
- El frontend utiliza un único cliente HTTP en services/api.js, que normaliza la URL, agrega el token, interpreta errores y expone operaciones específicas.
- El hook hooks/useCart.js centraliza cálculo de cantidades, subtotal, adición, eliminación y límites por existencias.\n- El hook hooks/useSession.js encapsula autenticación, restauración de sesión y cierre de sesión.

Los componentes llaman api.getProducts() o api.checkout(...); no necesitan repetir la construcción de URLs, encabezados ni manejo común de respuestas.

### 4. Estructura resultante relevante

    backend/app/
    ├── api/
    │   ├── auth.py
    │   ├── products.py
    │   ├── orders.py
    │   ├── admin.py
    │   ├── dependencies.py
    │   └── routes.py
    ├── ports/
    │   └── product_repository.py
    ├── repositories/
    │   └── sqlalchemy_product_repository.py
    ├── services/
    │   ├── products.py
    │   └── orders.py
    ├── core/
    ├── models/
    └── schemas.py

    frontend/src/
    ├── services/
    │   └── api.js
    ├── hooks/
    │   ├── useCart.js
    │   └── useSession.js
    ├── App.jsx
    └── main.jsx

### 5. Pruebas automatizadas relacionadas con SOLID

Las pruebas automatizadas existentes se describen en la sección **Migraciones y pruebas automatizadas**. Incluyen pruebas de humo y de integración de API, además de pruebas unitarias del servicio de productos con un repositorio falso.

Escenarios del servicio:

- El servicio consulta productos a través del contrato del repositorio.
- La creación delega la persistencia en el repositorio.
- La consulta de un producto inexistente genera ProductNotFoundError.
- No se permite eliminar productos con historial de pedidos.

Ejecutar desde Codespaces:

    cd backend
    pytest -q

Validar la compilación del frontend:

    cd frontend
    npm run build

La compilación de Vite es una comprobación de construcción, no una suite de pruebas funcionales de frontend.

### 6. Sustentación: cómo demostrar SOLID

1. **SRP:** abrir api/products.py, services/products.py y repositories/sqlalchemy_product_repository.py; explicar la diferencia entre HTTP, reglas de aplicación y persistencia.
2. **OCP:** mostrar que se puede cambiar el repositorio inyectado sin modificar ProductService.
3. **LSP:** mostrar que FakeProductRepository sustituye al adaptador SQLAlchemy en las pruebas respetando el contrato.
4. **ISP:** mostrar que ProductRepository expone solo las operaciones del catálogo y que los esquemas de entrada/salida son específicos.
5. **DIP:** seguir el flujo get_product_service → ProductService → ProductRepository; explicar que el servicio depende de una abstracción.
6. **DRY:** mostrar el cliente api.js, los hooks useCart.js y useSession.js y la reutilización de las dependencias de autenticación.
7. **Demostración funcional:** consultar productos en Swagger, registrar/autenticar un cliente, verificar el 403 al intentar una operación administrativa y ejecutar un checkout que actualice el inventario.

**Conclusión para la presentación:** NexoShop separa los adaptadores HTTP, los casos de uso y la persistencia. El servicio de catálogo depende de un contrato sustituible, las reglas del carrito y la comunicación HTTP están centralizadas en módulos frontend reutilizables, y las pruebas ejercitan tanto la API como el servicio aislado. La arquitectura evita acoplamientos innecesarios y permite extender cada parte sin modificar las demás cuando el cambio pertenece a una responsabilidad diferente.
