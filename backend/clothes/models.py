from django.db import models
from django.utils import timezone


class Cloth(models.Model):
    """
    Модель ткани
    """

    article = models.CharField(max_length=40, verbose_name="Артикль", unique=True)
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    color = models.CharField(max_length=50, verbose_name="Цвет", blank=True)
    width = models.CharField(max_length=20, verbose_name="Ширина")
    composition = models.CharField(max_length=100, verbose_name="Состав")
    density = models.CharField(max_length=20, verbose_name="Плотность")
    length = models.CharField(max_length=20, verbose_name="Длина", blank=True)
    country = models.CharField(
        max_length=50, verbose_name="Страна производства", blank=True
    )
    image_url_1 = models.URLField()
    image_url_2 = models.URLField(null=True)
    image_url_3 = models.URLField(null=True)
    image_url_4 = models.URLField(null=True)

    def __str__(self):
        return f"Название - {self.name}"

    class Meta:
        verbose_name = "Ткань"
        verbose_name_plural = "Ткани"


class ClothPrice(models.Model):
    """
    Модель для хранения истории цен каждой ткани
    """

    cloth = models.ForeignKey(
        Cloth,
        on_delete=models.CASCADE,
        related_name="price_history",
        verbose_name="Ткань",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    date_updated = models.DateTimeField(
        default=timezone.now, verbose_name="Дата обновления"
    )

    def __str__(self):
        return f"{self.cloth} - {self.price} rub"

    class Meta:
        verbose_name = "История цены"
        verbose_name_plural = "История цен"
        ordering = ("-cloth",)
