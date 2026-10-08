from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Product
from .permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer, RegisterSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Filter products by category ID.",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search products by name.",
            ),
            OpenApiParameter(
                name="min_price",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description="Filter products with a minimum price.",
            ),
            OpenApiParameter(
                name="max_price",
                type=OpenApiTypes.NUMBER,
                location=OpenApiParameter.QUERY,
                description="Filter products with a maximum price.",
            ),
        ]
    )
)
class ProductListAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []