from rest_framework import generics

from clothes.models import Cloth
from clothes.serializers import ClothSerializer


class ClothListAPIView(generics.ListAPIView):
    queryset = Cloth.objects.all().prefetch_related("price_history")
    serializer_class = ClothSerializer
