# NexoShop — E-commerce simplificado

Aplicación académica full-stack para demostrar la comunicación entre un frontend React y un backend FastAPI, con persistencia en base de datos. La demostración se ejecuta íntegramente en **GitHub Codespaces**: no requiere contratar hosting, publicar el backend en otro proveedor ni utilizar una base de datos administrada externa.

## Demostración en GitHub Codespaces

Este es el Codespace configurado para la demostración:

| Componente | URL |
|---|---|
| **Tienda (frontend React)** | https://crispy-waddle-4jw95g5p449r37x7v-5173.app.github.dev/ |
| **API FastAPI** | https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/ |
| **Documentación interactiva (Swagger)** | https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/docs |
| **Estado del backend** | https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/health |

**Importante:** las direcciones anteriores pertenecen a un Codespace concreto. Para que respondan, el Codespace debe estar iniciado y los dos servidores deben estar ejecutándose. En la pestaña **Ports** de Codespaces, los puertos 5173 y 8000 deben estar reenviados. Si el profesor va a abrir la tienda desde otro navegador o dispositivo, configura ambos puertos como **Public**; recuerda que esto hace accesible públicamente la aplicación mientras el Codespace esté activo.

## Arquitectura y comunicación

```text
Navegador del usuario
        |
        v
Frontend React + Vite (puerto 5173)
        |
        | solicitudes HTTP / JSON
        v
API REST FastAPI (puerto 8000)
        |
        v
Servicios y reglas de negocio
        |
        v
SQLAlchemy ORM
        |
        v
SQLite (backend/ecommerce.db)
```

- **Frontend:** React 19 + Vite. Presenta el catálogo, autenticación, carrito, historial de pedidos y panel administrativo.
- **Backend:** FastAPI expone endpoints REST. Recibe solicitudes HTTP, valida los datos con Pydantic, aplica permisos y devuelve respuestas JSON.
- **ORM:** SQLAlchemy permite consultar y modificar las tablas de la base de datos usando modelos y objetos de Python.
- **Base de datos para Codespaces:** SQLite. Es un archivo local dentro del Codespace, ubicado en `backend/ecommerce.db`; no requiere instalar ni contratar un servidor de base de datos.
- **Migraciones:** Alembic administra la creación y evolución del esquema.
- **CORS:** FastAPI permite las solicitudes del dominio del frontend mediante la variable `CORS_ORIGINS`.

El navegador no consulta directamente SQLite. El flujo siempre pasa por FastAPI: React envía una petición a la API, FastAPI ejecuta la lógica y SQLAlchemy lee o modifica la base de datos, y finalmente la API devuelve el resultado al frontend.

## Tecnologías

- Frontend: React 19, Vite y CSS.
- Backend: Python 3.12+, FastAPI, Pydantic y Uvicorn.
- Persistencia para Codespaces: SQLite.
- Persistencia alternativa con Docker: PostgreSQL 16 en un contenedor local.
- ORM: SQLAlchemy 2.
- Seguridad: JWT, contraseñas con hash Argon2 y autorización por roles.
- Migraciones: Alembic.
- Pruebas: pytest y FastAPI TestClient.
- Docker Compose: alternativa opcional para ejecutar frontend, backend y PostgreSQL en contenedores.

## Funcionalidades

- Registro e inicio de sesión; el registro público siempre crea usuarios con rol `customer`.
- Catálogo con búsqueda, categorías, precios y disponibilidad.
- Carrito de compras.
- Checkout: el backend vuelve a consultar los precios y el stock; no confía en el total enviado por el navegador.
- Descuento de inventario dentro de una transacción para evitar vender más unidades de las disponibles.
- Historial de pedidos del cliente.
- Panel administrativo con métricas, creación, edición y eliminación de productos e historial global de pedidos.
- Validación de permisos para las operaciones administrativas.
- Pago simulado: no se reciben ni almacenan números de tarjetas.

## Ejecución en el Codespace existente

### 1. Actualizar el repositorio

Abre el Codespace asociado al repositorio y ejecuta desde la raíz:

```bash
git pull origin main
```

### 2. Preparar la configuración

Desde la raíz del repositorio:

```bash
cp backend/.env.codespaces.example backend/.env
cp frontend/.env.codespaces.example frontend/.env
```

Los archivos de ejemplo ya contienen las direcciones de este Codespace. El archivo `backend/.env` configura SQLite y autoriza CORS desde el frontend; `frontend/.env` indica a React la URL de FastAPI.

Si GitHub asigna otras direcciones a un Codespace nuevo, actualiza:
- `VITE_API_URL` en `frontend/.env`, usando la URL del puerto 8000 seguida de `/api`.
- `CORS_ORIGINS` en `backend/.env`, usando únicamente el origen del frontend (puerto 5173), sin `/api`.

Después de modificar `.env`, reinicia los servidores para que tomen la configuración.

### 3. Preparar la base de datos y el administrador

En una terminal:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
python -m app.seed_admin
```

Esto instala las dependencias, aplica la migración inicial y crea los datos de demostración si todavía no existen. La base SQLite se crea en `backend/ecommerce.db`. No hace falta ejecutar PostgreSQL ni conectarse a un servicio externo.

### 4. Iniciar FastAPI

En esa misma terminal, desde `backend/`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Comprueba el backend en:
- API: https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/
- Swagger: https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/docs
- Health check: https://crispy-waddle-4jw95g5p449r37x7v-8000.app.github.dev/health

El endpoint `/health` debe responder:

```json
{"status":"ok"}
```

### 5. Iniciar React

Abre una segunda terminal desde la raíz del repositorio:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Abre la tienda en:

https://crispy-waddle-4jw95g5p449r37x7v-5173.app.github.dev/

Vite mantiene la actualización automática del frontend cuando guardas cambios en sus archivos. Uvicorn, al ejecutarse con `--reload`, reinicia el backend cuando detecta cambios en Python.

### 6. Verificar que frontend y backend se comunican

1. Abre la tienda y comprueba que el catálogo carga los productos desde `GET /api/products`.
2. Abre Swagger en `/docs` y ejecuta `GET /api/products`; debe devolver los mismos productos.
3. Registra un cliente desde la tienda e inicia sesión.
4. Agrega productos al carrito y realiza una compra.
5. Consulta el historial del cliente y verifica que el stock haya disminuido.
6. Ingresa como administrador y revisa el pedido y las métricas.

Si la tienda muestra productos de demostración pese a que FastAPI está detenido, recuerda que el frontend incluye un catálogo visual de respaldo. Para demostrar la integración real, verifica que el backend esté activo y que `GET /api/products` responda correctamente.

## Base de datos: SQLite en Codespaces

La configuración de Codespaces usa:

```env
DATABASE_URL=sqlite:///./ecommerce.db
```

Como el backend se inicia desde la carpeta `backend/`, el archivo se guarda en `backend/ecommerce.db`.

- No se necesita instalar un servidor PostgreSQL.
- Alembic aplica el esquema con `alembic upgrade head`.
- `python -m app.seed_admin` agrega el administrador y productos iniciales si no existen.
- El archivo de base de datos permanece en el almacenamiento del Codespace cuando este se detiene y se vuelve a iniciar. No elimines el Codespace ni el archivo si quieres conservar los datos de la demostración.
- SQLite es apropiado para esta demostración académica de un solo entorno; para un sistema con múltiples instancias o carga concurrente elevada conviene usar PostgreSQL.

## Credenciales de demostración

- Administrador: `admin@nexoshop.local`
- Contraseña inicial: `Admin123!`
- Cliente: puedes registrarlo desde la interfaz.

Son credenciales de demostración, no deben reutilizarse en un sistema público real. Cambia `SECRET_KEY` y las credenciales antes de cualquier despliegue real.

## Docker opcional

Docker se conserva como una segunda forma de ejecutar el proyecto. No es necesario para la demostración en Codespaces descrita arriba.

Desde la raíz del repositorio:

```bash
docker compose up --build
```

Docker Compose inicia tres contenedores:
1. **db:** PostgreSQL 16, con volumen `postgres_data`.
2. **backend:** FastAPI; aplica las migraciones y prepara el administrador al iniciar.
3. **frontend:** React + Vite.

Con Docker local, abre:
- Tienda: http://localhost:5173
- Swagger: http://localhost:8000/docs

Para detener los contenedores sin borrar los datos:

```bash
docker compose down
```

Para detenerlos y borrar también el volumen de PostgreSQL (esto elimina los datos persistidos):

```bash
docker compose down -v
```

En Docker, el backend utiliza PostgreSQL dentro de la red privada de Compose. No se conecta a un proveedor externo. La configuración de Docker es independiente de la configuración SQLite usada en Codespaces.

## Endpoints principales de FastAPI

| Método | Endpoint | Función |
|---|---|---|
| GET | `/health` | Comprobar que el backend está activo |
| POST | `/api/auth/register` | Registrar cliente |
| POST | `/api/auth/login` | Iniciar sesión y obtener JWT |
| GET | `/api/auth/me` | Consultar usuario autenticado |
| GET | `/api/products` | Listar productos |
| GET | `/api/products/{id}` | Consultar producto |
| POST | `/api/products` | Crear producto (admin) |
| PATCH | `/api/products/{id}` | Editar producto (admin) |
| DELETE | `/api/products/{id}` | Eliminar producto (admin) |
| POST | `/api/orders/checkout` | Crear pedido |
| GET | `/api/orders/me` | Historial del cliente |
| GET | `/api/admin/summary` | Métricas (admin) |
| GET | `/api/admin/orders` | Pedidos globales (admin) |

La documentación interactiva y los esquemas OpenAPI están disponibles en `/docs` y `/openapi.json` del backend.

## Migraciones y pruebas

Desde `backend/`, con el entorno virtual activo:

```bash
alembic upgrade head
pytest -q
```

Para generar una migración después de modificar los modelos:

```bash
alembic revision --autogenerate -m "describe el cambio"
```

Revisa el archivo generado antes de aplicarlo.

## Recorrido sugerido para la presentación

1. Abre la tienda en el puerto 5173.
2. Abre Swagger en el puerto 8000 y muestra que la API está activa.
3. Ejecuta `GET /api/products` y relaciona la respuesta JSON con el catálogo del frontend.
4. Inicia sesión como administrador y muestra métricas y CRUD de productos.
5. Registra un cliente, inicia sesión y realiza una compra.
6. Consulta el historial y verifica que el backend actualizó el inventario en SQLite.
7. Muestra que los pedidos aparecen en el panel administrativo.

## Alcance y limitaciones

- La demostración de frontend, FastAPI y SQLite se ejecuta dentro del mismo GitHub Codespace. No se utiliza Vercel, Render, Supabase ni una base de datos alojada por terceros.
- GitHub Codespaces es el entorno donde se ejecuta la aplicación; por eso el Codespace debe permanecer activo durante la presentación. Los enlaces de los puertos no son un hosting permanente.
- El pago es simulado y no representa una transacción bancaria.
- Las imágenes de productos de ejemplo apuntan a URLs de Unsplash; esto no afecta la comunicación entre frontend, API y base de datos. Si se requiere que tampoco las imágenes dependan de Internet, se pueden sustituir por archivos locales del proyecto.
- Para producción real se necesitarían secretos seguros, HTTPS, CORS restringido, controles adicionales de seguridad, monitorización, copias de seguridad y una pasarela de pago real.
