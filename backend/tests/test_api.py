from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.main import app
from app.models import Product, User


client = TestClient(app)


def test_register_login_and_customer_permissions():
    email = f"test-{uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "password123",
        },
    )

    assert response.status_code == 201
    assert response.json()["role"] == "customer"

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": "password123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    current_user_response = client.get(
        "/api/auth/me",
        headers=headers,
    )
    assert current_user_response.status_code == 200

    product_response = client.post(
        "/api/products",
        headers=headers,
        json={
            "name": "Blocked",
            "price": 10,
            "stock": 1,
        },
    )
    assert product_response.status_code == 403


def test_checkout_rejects_insufficient_stock_and_preserves_stock():
    email = f"buyer-{uuid4().hex[:8]}@example.com"

    with SessionLocal() as db:
        user = User(
            name="Buyer",
            email=email,
            hashed_password=hash_password("password123"),
            role="customer",
        )
        product = Product(
            name="Test stock item",
            description="test",
            price=1000,
            stock=1,
            category="Test",
            image_url="",
        )
        db.add_all([user, product])
        db.commit()

        product_id = product.id

    login_response = client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": "password123",
        },
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    insufficient_stock_response = client.post(
        "/api/orders/checkout",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 2,
                }
            ]
        },
    )
    assert insufficient_stock_response.status_code == 409

    with SessionLocal() as db:
        assert db.get(Product, product_id).stock == 1

    successful_checkout_response = client.post(
        "/api/orders/checkout",
        headers=headers,
        json={
            "items": [
                {
                    "product_id": product_id,
                    "quantity": 1,
                }
            ]
        },
    )
    assert successful_checkout_response.status_code == 201
    assert successful_checkout_response.json()["total"] == "1000.00"

    with SessionLocal() as db:
        assert db.get(Product, product_id).stock == 0
