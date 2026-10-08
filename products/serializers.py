from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price cannot be negative."
            )

        return value

    

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "image",
            "is_active",
            "category",
            "created_at",
            "updated_at",
        ]