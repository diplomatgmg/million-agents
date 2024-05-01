import re
import time
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from parsers.utils import get_driver, get_soup, wait, get_hrefs, clear

SITE_URL = "https://tashtib-tex.uz"


def scroll_page(driver: WebDriver):
    """
    Прокручивает страницу для подгрузки всех товаров
    """
    for _ in range(5):  # TODO убрать костыль
        driver.execute_script("window.scrollBy(0, 9999);")
        time.sleep(3)


def get_all_clothes_hrefs(driver: WebDriver):
    """
    Получает ссылки на все ткани со страницы
    """
    driver.get(SITE_URL + "/catalog")
    wait(driver, By.CLASS_NAME, "product-img")

    scroll_page(driver)

    soup = get_soup(driver.page_source)

    cloth_divs = soup.find_all("div", class_="product-img")
    cloth_elements = tuple(map(lambda x: x.find("a"), cloth_divs))
    cloth_links = set(get_hrefs(cloth_elements))
    clothes_hrefs = tuple(map(lambda x: SITE_URL + x, cloth_links))

    return clothes_hrefs


def get_description(soup: BeautifulSoup) -> str:
    """
    Возвращает описание товара
    """
    return clear(soup.find("p")).split(",")[0]


def get_density(string: str):
    """
    Возвращает плотность товара
    """
    matches = re.search(r"Плотность: \d+", string)
    return matches.group(0).split()[-1] + " м2"


def get_width(string: str) -> str:
    """
    Возвращает ширину товара
    """
    matches = re.search(r"Ширина: \d+", string)
    return matches.group(0).split()[-1] + " см"


def get_price(string: str) -> float:
    """
    Возвращает цену товара.
    Если есть цена ОТ и ДО - возвращает среднюю стоимость
    """
    start_price_match = re.search(r"Цена: (\d+(?:\s\d+)*)", string)

    if not start_price_match:
        start_price_match = re.search(r"Цена: от (\d+(?:\s\d+)*)", string)

    start_price = int(start_price_match.group(1).replace(" ", ""))

    end_price_match = re.search(r"до (\d+(?:\s\d+)*)", string)

    if end_price_match:
        end_price = int(end_price_match.group(1).replace(" ", ""))
        return round((start_price + end_price) / 2, 2)

    start_price = int(start_price_match.group(1).replace(" ", ""))

    return round(start_price, 2)


def get_cloth_data(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Здоровья программисту, который делал верстку сайта.
    Парсит каждый товар. На одной странице может быть несколько тканей.
    """
    result = []
    details = soup.find("div", class_="product-details-content")

    name = clear(details.find("h2"))

    clothes = map(
        lambda x: x.replace("\xa0", ""), str(details).strip().split("<p>\xa0</p>")[:-1]
    )  # Разделяем разные варианты тканей

    for cloth in clothes:
        if len(cloth.strip()) == 0:  # Могут быть пустые строки
            continue

        image_tag = soup.find("img", class_="img-fluid")
        if image_tag is None:
            continue
        image = image_tag["src"]

        cloth_soup = get_soup(cloth)
        cloth_text = clear(cloth_soup)
        description = get_description(cloth_soup)
        density = get_density(cloth_text)
        width = get_width(cloth_text)
        # FIXME использовать api для получения курса
        price = get_price(cloth_text) / 137

        article = (
            name + description + density + width
        ).lower()  # Костыль, на сайте нет уникального id

        cloth_data = {
            "article": article,
            "name": name,
            "description": description,
            "density": density,
            "width": width,
            "price": price,
            "image_url_1": image,
        }

        result.append(cloth_data)

    return result


def get_data() -> List[Dict[str, str]]:
    """
    Возвращает массив из словарей каждого товара
    """
    driver = get_driver()
    clothes_hrefs = get_all_clothes_hrefs(driver)
    clothes_data = []

    for cloth_href in clothes_hrefs:
        driver.get(cloth_href)
        soup = get_soup(driver.page_source)

        cloth_data = get_cloth_data(soup)
        clothes_data.extend(cloth_data)

    return clothes_data
