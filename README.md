# Supermarket Django API

A professional RESTful backend API for a supermarket e-commerce platform, built with Django and Django REST Framework.

This project is being developed as a portfolio backend project with a focus on clean architecture, REST API design, authentication, validation, automated testing, API documentation, and Git-based development workflow.

---

## Features

### Product Management

- Product and Category models
- Product CRUD operations
- Django Admin integration
- Product activation/deactivation
- Product stock management
- Product image support
- Product price validation
- Unique product slugs

### Product API

- Product listing
- Product details
- Product creation
- Product update
- Partial product update
- Product deletion
- Search by product name
- Category filtering
- Minimum price filtering
- Maximum price filtering
- Ordering
- Pagination

### Authentication

- User registration
- JWT authentication
- Access token
- Refresh token
- Protected product write operations
- User profile endpoint
- User profile update

### API Documentation

- Swagger UI
- OpenAPI schema
- Documented query parameters

### Testing

- Automated API tests with Pytest
- Django integration testing
- Authentication tests
- Registration tests
- Product CRUD tests
- Validation tests
- Filtering tests
- Pagination tests
- Ordering tests
- User profile tests

---

## Tech Stack

- Python 3.10
- Django 5.2
- Django REST Framework
- Simple JWT
- drf-spectacular
- Pytest
- pytest-django
- SQLite
- Git
- GitHub

---

## Project Structure

```text
supermarket/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── products/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
├── pytest.ini
├── requirements.txt
└── README.md