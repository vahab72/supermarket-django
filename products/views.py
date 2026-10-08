from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = [
        "name",
        "price",
        "stock",
        "created_at",
    ]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        category_id = self.request.query_params.get("category")

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(name__icontains=search)

        min_price = self.request.query_params.get("min_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.query_params.get("max_price")

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(is_active=True)