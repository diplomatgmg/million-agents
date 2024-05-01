from django.urls import path

from clothes.views import ClothListAPIView

urlpatterns = [
    path("cloths/", ClothListAPIView.as_view(), name="cloth-list"),
]
