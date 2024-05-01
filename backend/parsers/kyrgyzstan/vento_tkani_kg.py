import requests
from bs4 import BeautifulSoup

from parsers.utils import get_session, get_soup

SITE_URL = "https://vento-tkani.kg/shop/tkani/"
SESSION = get_session()


def get_next_page_url(soup: BeautifulSoup):
    """
    Возвращает ссылку на следующую страницу
    """
    next_page = soup.find("a", class_="next page-numbers")
    is_next_page_exist = next_page and next_page.get_text().strip()

    return next_page["href"] if is_next_page_exist == "→" else None


def get_clothes_hrefs(soup: BeautifulSoup):
    """
    Возвращает список ссылок на ткани со страницы
    """
    clothes = soup.find_all(
        "a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link"
    )
    return [a["href"] for a in clothes]


def get_all_clothes_hrefs():
    """Получает список ссылок на все товары со всех страниц"""
    clothes_hrefs = []

    response = requests.get(SITE_URL).text
    main_soup = get_soup(response)

    clothes_hrefs.extend(get_clothes_hrefs(main_soup))
    next_page_url = get_next_page_url(main_soup)

    while next_page_url:
        response = requests.get(next_page_url).text
        soup = get_soup(response)
        clothes_hrefs.extend(get_clothes_hrefs(soup))
        next_page_url = get_next_page_url(soup)

    return clothes_hrefs


def get_images(soup: BeautifulSoup):
    image_urls = soup.find_all("div", class_="woocommerce-product-gallery__image")
    image_url_1, image_url_2, image_url_3, image_url_4 = None, None, None, None

    if len(image_urls) >= 1:
        image_url_1 = image_urls[0].find("a")["href"]
    if len(image_urls) >= 2:
        image_url_2 = image_urls[1].find("a")["href"]
    if len(image_urls) >= 3:
        image_url_3 = image_urls[2].find("a")["href"]
    if len(image_urls) >= 4:
        image_url_4 = image_urls[3].find("a")["href"]

    return image_url_1, image_url_2, image_url_3, image_url_4


def get_cloth_data(soup: BeautifulSoup):
    """
    Возвращаем спарсенные данные с каждого товара
    """
    raw_name = soup.find("h1", class_="product_title")

    if raw_name is None:
        return None

    name = raw_name.get_text().strip()

    price = (
        soup.find("span", class_="woocommerce-Price-amount")
        .get_text()
        .strip()
        .split()[-1]
    )
    # FIXME использовать api для получения курса
    price = round(float(price) * 93, 2)

    description_block = soup.find(
        "div", class_="woocommerce-product-details__short-description"
    )

    description = description_block.find("p").get_text().replace(" ", " ").strip()
    details = description_block.find_all("li")
    article = soup.find("span", class_="sku").get_text().strip()

    image_url_1, image_url_2, image_url_3, image_url_4 = get_images(soup)

    result = {
        "name": name,
        "price": price,
        "description": description,
        "article": article,
        "image_url_1": image_url_1,
        "image_url_2": image_url_2,
        "image_url_3": image_url_3,
        "image_url_4": image_url_4,
    }

    for detail in details:
        clear_text = detail.get_text().strip().replace("\xa0", " ").lower()
        value = clear_text.split(":")[-1].strip().lower()

        if clear_text.startswith("цвет"):
            result["color"] = value
        elif clear_text.startswith("ширина"):
            result["width"] = value
        elif clear_text.startswith("состав"):
            result["composition"] = value
        elif clear_text.startswith("плотность"):
            result["density"] = value
        elif clear_text.startswith("в рулоне"):
            result["length"] = value
        elif clear_text.startswith("страна") or clear_text.startswith("производитель"):
            result["country"] = value
        else:
            raise ValueError(f"Не удалось найти нужное поле: {clear_text}")

    return result


def get_data():
    """
    Возвращает массив из словарей каждого товара
    """
    clothes_hrefs = get_all_clothes_hrefs()
    clothes_data = []

    for cloth_href in clothes_hrefs:
        response = requests.get(cloth_href).text
        soup = get_soup(response)
        is_page_exist = not soup.find("section", class_="error-404")

        if not is_page_exist:
            continue

        cloth_data = get_cloth_data(soup)

        if cloth_data:
            clothes_data.append(cloth_data)

    return clothes_data
