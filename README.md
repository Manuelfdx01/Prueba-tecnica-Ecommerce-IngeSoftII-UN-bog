# NexoShop — Prueba técnica de desarrollo Full Stack

NexoShop es una aplicación web de comercio electrónico desarrollada como solución a una prueba técnica. El proyecto integra una interfaz de usuario construida con **React 19**, una API REST implementada con **FastAPI** y persistencia relacional mediante **SQLAlchemy**. Su objetivo es demostrar la implementación de un flujo de compra funcional, separación de responsabilidades, control de acceso por roles, consistencia de inventario y pruebas automatizadas.

La solución contempla dos perfiles de uso: clientes, que pueden explorar el catálogo y realizar pedidos, y administradores, que pueden gestionar el catálogo y consultar la operación de la tienda.

## Enlaces de acceso

La aplicación de demostración se ejecuta en GitHub Codespaces. Los siguientes enlaces corresponden al entorno configurado para la evaluación:

| Recurso | Enlace | Descripción |
|---|---|---|
| **Frontend** | [NexoShop – Tienda](https://crispy-waddle-4jw95g5p449r37x7v-5173.app.github.dev/) | Interfaz web para clientes y administradores. |
| **Backend** | [API FastAPI](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/) | Servicio REST que implementa las reglas de negocio. |
| **Swagger UI** | [Documentación interactiva](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/docs) | Documentación y exploración de los endpoints. |
| **OpenAPI** | [Especificación JSON](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/openapi.json) | Contrato de la API. |
| **Health check** | [Estado del backend](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/health) | Endpoint de verificación de disponibilidad. |

**Disponibilidad de la demostración:** estos enlaces pertenecen a un entorno de GitHub Codespaces y no representan un servicio de hosting permanente. Para acceder a la aplicación, el Codespace debe estar activo, los servidores frontend y backend deben estar ejecutándose y los puertos deben permitir el acceso externo. Si el entorno está detenido, la demostración no estará disponible hasta que se reactive.

## Credenciales de evaluación

Se incluye una cuenta administrativa de demostración para facilitar la revisión de las funcionalidades restringidas por rol:

| Campo | Credencial |
|---|---|
| **Rol** | Administrador |
| **Correo** | `admin@nexoshop.com` |
| **Contraseña inicial** | `Admin123!` |

La cuenta y los datos de demostración son creados por el módulo `backend/app/seed_admin.py` cuando no existe previamente el usuario administrador. Si la base de datos conserva el correo anterior `admin@nexoshop.local`, el sembrado actualiza ese correo a `admin@nexoshop.com` sin modificar el identificador, la contraseña, el rol ni las relaciones del usuario. La contraseña indicada corresponde a la configuración inicial; si la cuenta ya fue creada y posteriormente modificada, prevalece la contraseña vigente en ese entorno.

**Nota:** estas credenciales son exclusivamente para la evaluación de esta instancia de demostración. No deben reutilizarse en un entorno de producción.

## Funcionalidades

### Experiencia de compra
- Visualización del catálogo de productos.
- Consulta y búsqueda de productos por categorías, precios y disponibilidad.
- Gestión del carrito de compras y cantidades por producto.
- Registro e inicio de sesión de clientes.
- Generación de pedidos mediante el proceso de checkout.
- Consulta del historial de pedidos del cliente.

### Administración
- Acceso a funcionalidades administrativas mediante control de roles.
- Creación, consulta, actualización y eliminación de productos.
- Consulta global de pedidos.
- Visualización de métricas generales de la tienda.

### Reglas de negocio
- El registro público asigna automáticamente el rol de cliente.
- El backend valida los datos recibidos y aplica las reglas de autorización.
- Durante el checkout, los precios y las existencias se consultan en el servidor; no se confía en los valores enviados por el navegador.
- La actualización del inventario y la creación del pedido se ejecutan dentro de una transacción para mantener la consistencia de los datos.
- Si no existe inventario suficiente, el checkout se rechaza y no se descuenta stock.
- El procesamiento de pagos es simulado: no se realizan transacciones bancarias ni se almacenan datos de tarjetas.

## Arquitectura

La solución sigue una arquitectura cliente-servidor por capas. El frontend consume la API mediante solicitudes HTTP y datos JSON; el backend expone los endpoints, valida las solicitudes, aplica las reglas de negocio y coordina la persistencia.

```text
┌──────────────────────────────┐
│       Cliente / navegador    │
└──────────────┬───────────────┘
               │ HTTP / JSON
               ▼
┌──────────────────────────────┐
│       Frontend React         │
│            Vite              │
└──────────────┬───────────────┘
               │ API REST
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│     Routers y dependencias   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Servicios de dominio    │
│   Reglas y casos de uso      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Repositorios / ORM       │
│          SQLAlchemy          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Base de datos SQL      │
│      SQLite / PostgreSQL     │
└──────────────────────────────┘
```

La API separa los adaptadores HTTP de los servicios de aplicación y del acceso a datos. En el catálogo, `ProductService` depende del contrato `ProductRepository`; la implementación SQLAlchemy se inyecta desde las dependencias de FastAPI. Esto permite probar la lógica del servicio con un repositorio falso sin requerir una base de datos real.

## Tecnologías

| Componente | Tecnología |
|---|---|
| Interfaz web | React 19 |
| Herramienta de desarrollo frontend | Vite |
| Estilos | CSS |
| API | Python, FastAPI y Uvicorn |
| Validación de datos | Pydantic |
| ORM | SQLAlchemy 2 |
| Base de datos del entorno Codespaces | SQLite |
| Base de datos alternativa | PostgreSQL 16 |
| Autenticación | JSON Web Tokens (JWT) |
| Hash de contraseñas | Argon2 |
| Migraciones | Alembic |
| Pruebas de backend | pytest y FastAPI TestClient |
| Integración continua | GitHub Actions |
| Contenedores | Docker y Docker Compose |

## Estructura general

```text
.
├── frontend/                 # Aplicación React
│   └── src/
│       ├── services/         # Cliente HTTP
│       ├── hooks/            # Estado de carrito y sesión
│       └── components/       # Componentes de interfaz
├── backend/                  # API FastAPI
│   ├── app/
│   │   ├── api/              # Routers y dependencias HTTP
│   │   ├── ports/             # Contratos de repositorio
│   │   ├── repositories/     # Adaptadores de persistencia
│   │   ├── services/         # Reglas y casos de uso
│   │   ├── core/             # Configuración, seguridad y DB
│   │   └── models/           # Modelos de datos
│   ├── alembic/              # Migraciones
│   └── tests/                # Pruebas automatizadas
├── .github/workflows/        # Integración continua
├── docker-compose.yml        # Entorno alternativo contenerizado
└── README.md
```

## Persistencia de datos

La aplicación admite dos configuraciones:

- **SQLite:** utilizada en el entorno de demostración de Codespaces. La base de datos se almacena en `backend/ecommerce.db`, dentro del Codespace.
- **PostgreSQL 16:** alternativa configurada mediante Docker Compose, con un volumen dedicado para conservar los datos entre reinicios de los contenedores.

SQLAlchemy proporciona la capa de acceso a datos y Alembic administra las migraciones del esquema. La conexión se parametriza mediante `DATABASE_URL`.

## Seguridad

- Autenticación basada en tokens JWT.
- Almacenamiento de contraseñas mediante hashes Argon2.
- Separación de permisos entre usuarios con rol `customer` y `admin`.
- Validación de datos de entrada mediante esquemas Pydantic.
- Restricción de operaciones administrativas según el rol del usuario autenticado.
- Verificación de precios y disponibilidad en el servidor durante el checkout.
- Configuración de orígenes permitidos mediante CORS.
- Variables de entorno para la configuración de secretos y conexiones.

Las credenciales de demostración publicadas en este documento son una excepción deliberada para facilitar la evaluación de esta instancia. No deben utilizarse como credenciales de producción.

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

La especificación OpenAPI y la documentación interactiva de los endpoints se generan automáticamente mediante FastAPI y están disponibles en [Swagger UI](https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/docs) cuando el backend está activo.

## Migraciones y pruebas automatizadas

Las migraciones del esquema se administran con Alembic. El esquema de base de datos se actualiza mediante migraciones versionadas, evitando depender de la creación manual de tablas en cada ejecución.

### Pruebas de backend

El backend utiliza **pytest** y **FastAPI TestClient**. Los casos automatizados están en `backend/tests/`:

| Archivo | Tipo | Qué comprueba |
|---|---|---|
| `test_smoke.py` | Prueba de humo de API | Que `GET /health` responda HTTP 200 y devuelva `{"status": "ok"}`. |
| `test_api.py` | Pruebas de integración de API | Registro de cliente, inicio de sesión, consulta del usuario autenticado y rechazo (403) de una operación administrativa realizada por un cliente. También verifica el checkout: si no hay inventario suficiente responde 409 y conserva el stock; con stock disponible crea el pedido (201), calcula el total y descuenta las existencias. |
| `test_product_service.py` | Pruebas unitarias de servicio | Prueba `ProductService` con un repositorio falso, sin conectarse a una base de datos real: consulta y creación delegadas al repositorio, error al consultar un producto inexistente y protección contra eliminar productos que tienen historial de pedidos. |

Estas pruebas cubren endpoints y reglas seleccionadas del catálogo, autenticación, permisos y checkout. No representan una cobertura exhaustiva de todos los módulos ni sustituyen pruebas de carga, seguridad o aceptación de usuario.

### Validación de frontend

El frontend no tiene actualmente un framework ni una suite de pruebas unitarias o de componentes configurada. La validación automatizada de frontend en CI ejecuta `npm run build`, que utiliza Vite y esbuild para generar el paquete de producción y detectar errores de sintaxis, importaciones o compilación. Esta validación **no equivale a pruebas funcionales de interacción en el navegador**.

### Integración continua con GitHub Actions

El workflow `.github/workflows/ci.yml` ejecuta dos trabajos independientes cuando hay un push a `main` o a ramas `feat/**`, y cuando se abre o actualiza un Pull Request dirigido a `main`:

- **Backend:** configura Python 3.12, instala `backend/requirements-dev.txt`, aplica las migraciones con `alembic upgrade head` y ejecuta `pytest -q`.
- **Frontend:** configura Node.js 20, instala dependencias con `npm install` y ejecuta `npm run build`.

Un resultado exitoso de CI significa que las pruebas automatizadas definidas para backend finalizaron correctamente y que el frontend pudo compilarse para producción. No significa que exista una suite de pruebas de interfaz de usuario para frontend.

## Ejecución y demostración

La instancia publicada en los enlaces de acceso utiliza GitHub Codespaces como entorno de ejecución. El backend se inicia en el puerto `8000` y el frontend en el puerto `5173`; el frontend consume la API mediante la URL reenviada del puerto del backend. La configuración de CORS permite el origen del frontend.

El repositorio también incluye una configuración alternativa con Docker Compose para ejecutar frontend, backend y PostgreSQL 16 en un entorno contenerizado. Esta alternativa permite demostrar la integración entre los servicios y la persistencia con PostgreSQL sin depender de una base de datos administrada externa.

## Alcance y consideraciones

NexoShop implementa un flujo académico de comercio electrónico con autenticación, autorización por roles, administración de catálogo, pedidos y persistencia relacional. El módulo de pago es simulado y no está integrado con entidades financieras ni pasarelas de pago.

La instancia de demostración está orientada a evaluación y depende de la disponibilidad del Codespace. Una puesta en producción requeriría infraestructura permanente, gestión reforzada de secretos, políticas de seguridad adicionales, monitorización, copias de seguridad y pruebas funcionales y de carga.

## Buenas prácticas, SOLID y DRY

La implementación separa responsabilidades en backend y frontend. Las rutas HTTP actúan como adaptadores de entrada; los servicios contienen reglas de aplicación; los repositorios aíslan el acceso a datos; y los esquemas Pydantic definen contratos de entrada y salida.

SOLID se aplica donde reduce acoplamiento y facilita probar o sustituir una implementación. No se crean abstracciones sin necesidad: el contrato de repositorio se utiliza en el servicio de productos para separar las reglas del catálogo de la tecnología de persistencia.

### 1. Buenas prácticas de desarrollo

- **Responsabilidades delimitadas:** los routers se separan por recurso: `api/auth.py`, `api/products.py`, `api/orders.py` y `api/admin.py`.
- **Separación de capas:** las rutas traducen HTTP, los servicios ejecutan casos de uso y los repositorios gestionan persistencia.
- **Validación de entrada:** Pydantic valida tipos, longitudes, rangos y valores permitidos.
- **Reglas críticas en el servidor:** precios y existencias se consultan en la base de datos durante el checkout; el navegador no determina el precio final.
- **Consistencia transaccional:** la actualización del inventario y la creación del pedido se confirman en una transacción; un error provoca rollback.
- **Seguridad:** las contraseñas se almacenan con Argon2, la autenticación usa JWT y las operaciones administrativas exigen el rol correspondiente.
- **Errores explícitos:** la API responde con códigos HTTP adecuados para validación, autenticación, permisos, recursos inexistentes y conflictos de inventario.
- **Configuración por entorno:** URL de base de datos, clave de firma y orígenes CORS se parametrizan mediante variables de entorno.

### 2. Aplicación de los cinco principios SOLID

#### S — Single Responsibility Principle (responsabilidad única)

Cada módulo tiene una responsabilidad principal:

- `api/products.py`: contrato HTTP del catálogo.
- `services/products.py`: reglas de aplicación del catálogo.
- `repositories/sqlalchemy_product_repository.py`: persistencia de productos con SQLAlchemy.
- `services/orders.py`: reglas transaccionales del checkout.
- En frontend, `services/api.js` gestiona comunicación HTTP, `hooks/useCart.js` encapsula las reglas del carrito y `hooks/useSession.js` administra autenticación y persistencia de sesión.

**Ejemplo:** el endpoint de listado delega el caso de uso al servicio `ProductService`. La ruta no construye consultas SQL ni conoce cómo se almacenan los productos.

#### O — Open/Closed Principle (abierto/cerrado)

El servicio de productos trabaja con el contrato `ProductRepository`, no con una implementación SQLAlchemy concreta. Se puede incorporar otra implementación del repositorio, por ejemplo para pruebas u otra tecnología de persistencia, sin reescribir las reglas del servicio.

#### L — Liskov Substitution Principle (sustitución de Liskov)

Las implementaciones que cumplen el contrato `ProductRepository` pueden sustituirse manteniendo las operaciones y expectativas definidas por el servicio. El adaptador real es `SqlAlchemyProductRepository`; las pruebas utilizan `FakeProductRepository` para probar el servicio sin conectarse a una base de datos real.

#### I — Interface Segregation Principle (segregación de interfaces)

El contrato `ProductRepository` contiene las operaciones necesarias para el caso de uso del catálogo. No obliga al servicio de productos a depender de métodos de usuarios, pagos o reportes. Los esquemas también separan creación, actualización y representación de salida: `ProductCreate`, `ProductUpdate` y `ProductOut`.

#### D — Dependency Inversion Principle (inversión de dependencias)

La lógica de aplicación depende de la abstracción `ProductRepository`. La implementación SQLAlchemy se construye en el punto de composición de FastAPI, mediante `get_product_service`, y se inyecta al router.

El flujo es: FastAPI crea `SqlAlchemyProductRepository` con la sesión recibida, `ProductService` recibe el repositorio mediante su constructor y opera únicamente con el contrato. Por ello, el servicio puede probarse con un repositorio falso sin depender de SQLAlchemy.

### 3. Aplicación de DRY (Don't Repeat Yourself)

- La autenticación y autorización se centralizan en `get_current_user` y `require_admin`.
- El acceso a datos del catálogo se concentra en `SqlAlchemyProductRepository`.
- Las reglas del catálogo se implementan una sola vez en `ProductService`.
- La lógica de checkout se centraliza en `services/orders.py`.
- El frontend utiliza un único cliente HTTP en `services/api.js), que centraliza la URL, el token y el manejo común de respuestas.
- El hook `hooks/useCart.js` centraliza cantidades, subtotal, adición, eliminación y límites por existencias.
- El hook `hooks/useSession.js` encapsula autenticación, restauración de sesión y cierre de sesión.

### 4. Estructura relevante de la arquitectura

```text
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
```

### 5. Pruebas automatizadas relacionadas con SOLID

Las pruebas unitarias de `ProductService` utilizan un repositorio falso para comprobar que las reglas del servicio pueden verificarse sin una base de datos real. Las pruebas de integración de API comprueban autenticación, autorización y checkout, incluidos los escenarios de inventario insuficiente y compra exitosa.

### 6. Criterios de evaluación demostrables

La solución permite revisar los siguientes aspectos:

1. **SRP:** separación entre routers, servicios y repositorios.
2. **OCP:** posibilidad de sustituir la implementación del repositorio sin modificar `ProductService`.
3. **LSP:** uso de `FakeProductRepository` como implementación alternativa del contrato en pruebas.
4. **ISP:** contrato `ProductRepository` enfocado en operaciones del catálogo y esquemas específicos para cada operación.
5. **DIP:** inyección de dependencias desde FastAPI hacia `ProductService`.
6. **DRY:** centralización de autenticación, acceso a datos, comunicación HTTP y estado del carrito.
7. **Integración funcional:** recorrido de catálogo, autenticación, permisos, checkout y actualización del inventario.

**Conclusión:** NexoShop integra una aplicación frontend y una API backend con persistencia relacional. La solución demuestra separación de responsabilidades, control de acceso, reglas de negocio ejecutadas en el servidor, consistencia transaccional y pruebas automatizadas sobre los componentes principales. Su arquitectura permite mantener y extender las funcionalidades sin acoplar directamente la lógica de aplicación a los detalles de infraestructura.
