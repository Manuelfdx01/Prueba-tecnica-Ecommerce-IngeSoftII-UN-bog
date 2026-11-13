# Backend NexoShop

## Desarrollo
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements-dev.txt
cp .env.example .env
alembic upgrade head
python -m app.seed_admin
uvicorn app.main:app --reload
```

## Migraciones
- `alembic upgrade head`: aplicar cambios pendientes.
- `alembic revision --autogenerate -m "descripcion"`: generar una migración tras modificar modelos (revisar el archivo antes de aplicarlo).
- `alembic downgrade -1`: revertir una migración.

## Pruebas
`pytest -q`
