from rest_framework import serializers

from .models import Cloth, ClothPrice


class ClothPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothPrice
        fields = (
            "price",
            "date_updated",
        )


class ClothSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    price_history = ClothPriceSerializer(many=True, read_only=True)
    price_history_count = serializers.SerializerMethodField()

    class Meta:
        model = Cloth
        fields = (
            "id",
            "article",
            "name",
            "description",
            "color",
            "width",
            "composition",
            "density",
            "length",
            "country",
            "images",
            "price_history_count",
            "price_history",
        )

    def get_images(self, obj):
        """
        Метод для получения списка изображений в формате [img1, img2, img3...]
        """
        image_fields = [f"image_url_{i}" for i in range(1, 5)]
        # Некоторые поля могут быть None. Не берем мых
        images = [getattr(obj, field) for field in image_fields if getattr(obj, field)]
        return images

    def get_price_history_count(self, obj):
        return obj.price_history.count()
