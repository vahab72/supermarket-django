from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Category, Product


User = get_user_model()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(
        username="testuser",
        password="testpassword123",
    )

    client = APIClient()
    client.force_authenticate(user=user)

    return client


@pytest.mark.django_db
def test_product_list():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy",
    )

    Product.objects.create(
        category=category,
        name="شیر کم چرب",
        slug="test-low-fat-milk",
        description="شیر کم چرب",
        price="1000.00",
        stock=20,
        is_active=True,
    )

    client = APIClient()

    response = client.get("/api/products/")

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_product_detail():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-detail",
    )

    product = Product.objects.create(
        category=category,
        name="پنیر کم چرب",
        slug="test-low-fat-cheese",
        description="پنیر کم چرب",
        price="90000.00",
        stock=20,
        is_active=True,
    )

    client = APIClient()

    response = client.get(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == 200
    assert response.data["id"] == product.id
    assert response.data["name"] == "پنیر کم چرب"


@pytest.mark.django_db
def test_product_not_found():
    client = APIClient()

    response = client.get("/api/products/999/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_negative_price(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-negative-price",
    )

    response = authenticated_client.post(
        "/api/products/",
        {
            "name": "محصول تست",
            "slug": "test-negative-price",
            "description": "محصول تست",
            "price": "-100.00",
            "stock": 10,
            "is_active": True,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 400
    assert "price" in response.data


@pytest.mark.django_db
def test_duplicate_slug(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-duplicate",
    )

    Product.objects.create(
        category=category,
        name="محصول اول",
        slug="test-duplicate-slug",
        description="محصول اول",
        price="1000.00",
        stock=10,
        is_active=True,
    )

    response = authenticated_client.post(
        "/api/products/",
        {
            "name": "محصول دوم",
            "slug": "test-duplicate-slug",
            "description": "محصول دوم",
            "price": "2000.00",
            "stock": 10,
            "is_active": True,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 400
    assert "slug" in response.data


@pytest.mark.django_db
def test_product_search():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-search",
    )

    Product.objects.create(
        category=category,
        name="شیر کم چرب",
        slug="test-search-milk",
        description="شیر",
        price="1000.00",
        stock=10,
        is_active=True,
    )

    Product.objects.create(
        category=category,
        name="پنیر کم چرب",
        slug="test-search-cheese",
        description="پنیر",
        price="50000.00",
        stock=10,
        is_active=True,
    )

    client = APIClient()

    response = client.get(
        "/api/products/?search=پنیر"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "پنیر کم چرب"


@pytest.mark.django_db
def test_product_price_filter():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-price",
    )

    Product.objects.create(
        category=category,
        name="محصول ارزان",
        slug="test-cheap-price",
        description="محصول ارزان",
        price="1000.00",
        stock=10,
        is_active=True,
    )

    Product.objects.create(
        category=category,
        name="محصول گران",
        slug="test-expensive-price",
        description="محصول گران",
        price="90000.00",
        stock=10,
        is_active=True,
    )

    client = APIClient()

    response = client.get(
        "/api/products/?min_price=50000"
    )

    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "محصول گران"


@pytest.mark.django_db
def test_product_ordering():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-ordering",
    )

    Product.objects.create(
        category=category,
        name="محصول ارزان",
        slug="test-cheap-product",
        description="محصول ارزان",
        price="1000.00",
        stock=10,
        is_active=True,
    )

    Product.objects.create(
        category=category,
        name="محصول گران",
        slug="test-expensive-product",
        description="محصول گران",
        price="90000.00",
        stock=10,
        is_active=True,
    )

    client = APIClient()

    response = client.get(
        "/api/products/?ordering=-price"
    )

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert response.data["results"][0]["name"] == "محصول گران"
    assert response.data["results"][1]["name"] == "محصول ارزان"


@pytest.mark.django_db
def test_product_pagination():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-pagination",
    )

    for i in range(15):
        Product.objects.create(
            category=category,
            name=f"محصول {i}",
            slug=f"test-pagination-{i}",
            description=f"محصول تست {i}",
            price="1000.00",
            stock=10,
            is_active=True,
        )

    client = APIClient()

    response = client.get("/api/products/")

    assert response.status_code == 200
    assert response.data["count"] == 15
    assert len(response.data["results"]) == 10
    assert response.data["next"] is not None
    assert response.data["previous"] is None


@pytest.mark.django_db
def test_product_create_without_authentication():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-create-unauthenticated",
    )

    client = APIClient()

    response = client.post(
        "/api/products/",
        {
            "name": "محصول جدید",
            "slug": "test-new-product-unauthenticated",
            "description": "محصول جدید",
            "price": "15000.00",
            "stock": 20,
            "is_active": True,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_product_create(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-create",
    )

    response = authenticated_client.post(
        "/api/products/",
        {
            "name": "محصول جدید",
            "slug": "test-new-product",
            "description": "محصول جدید",
            "price": "15000.00",
            "stock": 20,
            "is_active": True,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["name"] == "محصول جدید"
    assert response.data["price"] == "15000.00"

    assert Product.objects.filter(
        slug="test-new-product"
    ).exists()


@pytest.mark.django_db
def test_product_update(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-update",
    )

    product = Product.objects.create(
        category=category,
        name="محصول قدیمی",
        slug="test-old-product",
        description="توضیحات قدیمی",
        price="10000.00",
        stock=10,
        is_active=True,
    )

    response = authenticated_client.put(
        f"/api/products/{product.id}/",
        {
            "name": "محصول ویرایش شده",
            "slug": "test-updated-product",
            "description": "توضیحات جدید",
            "price": "20000.00",
            "stock": 30,
            "is_active": True,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["name"] == "محصول ویرایش شده"
    assert response.data["price"] == "20000.00"
    assert response.data["stock"] == 30

    product.refresh_from_db()

    assert product.name == "محصول ویرایش شده"
    assert product.price == Decimal("20000.00")
    assert product.stock == 30


@pytest.mark.django_db
def test_product_partial_update(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-patch",
    )

    product = Product.objects.create(
        category=category,
        name="محصول اصلی",
        slug="test-patch-product",
        description="توضیحات",
        price="10000.00",
        stock=10,
        is_active=True,
    )

    response = authenticated_client.patch(
        f"/api/products/{product.id}/",
        {
            "price": "25000.00",
        },
        format="json",
    )

    assert response.status_code == 200
    assert response.data["price"] == "25000.00"

    product.refresh_from_db()

    assert product.price == Decimal("25000.00")
    assert product.name == "محصول اصلی"


@pytest.mark.django_db
def test_product_delete_without_authentication():
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-delete-unauthenticated",
    )

    product = Product.objects.create(
        category=category,
        name="محصول قابل حذف",
        slug="test-delete-product-unauthenticated",
        description="محصول قابل حذف",
        price="10000.00",
        stock=10,
        is_active=True,
    )

    client = APIClient()

    response = client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == 401
    assert Product.objects.filter(
        id=product.id
    ).exists()


@pytest.mark.django_db
def test_product_delete(authenticated_client):
    category = Category.objects.create(
        name="لبنیات",
        slug="test-dairy-delete",
    )

    product = Product.objects.create(
        category=category,
        name="محصول قابل حذف",
        slug="test-delete-product",
        description="محصول قابل حذف",
        price="10000.00",
        stock=10,
        is_active=True,
    )

    response = authenticated_client.delete(
        f"/api/products/{product.id}/"
    )

    assert response.status_code == 204

    assert not Product.objects.filter(
        id=product.id
    ).exists()
# Create your tests here.
