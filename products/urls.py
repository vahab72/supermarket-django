from django.urls import path

from .views import (
    ProductDetailAPIView,
    ProductListAPIView,
    RegisterAPIView,
    UserProfileAPIView,
)


urlpatterns = [
    path(
        "products/",
        ProductListAPIView.as_view(),
        name="product-list",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path(
        "auth/register/",
        RegisterAPIView.as_view(),
        name="register",
    ),
    path(
        "auth/me/",
        UserProfileAPIView.as_view(),
        name="user-profile",
    ),
]