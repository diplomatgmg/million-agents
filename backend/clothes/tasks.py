from celery import shared_task

from clothes.models import Cloth, ClothPrice
from parsers.parsers import PARSERS


@shared_task
def parse_sites():
    """
    Функция для парсинга тканей и добавления их в БД
    """
    for site in PARSERS:
        try:
            all_clothes = site.get_data()
        except Exception as e:
            print(f"Ошибка при получении данных с сайта {site}: {e}")
            continue

        for cloth_data in all_clothes:
            article = cloth_data.pop("article")
            price = cloth_data.pop("price")

            cloth = Cloth.objects.filter(article=article).last()

            if not cloth:
                cloth = Cloth.objects.create(article=article, **cloth_data)

            ClothPrice.objects.create(cloth=cloth, price=price)
