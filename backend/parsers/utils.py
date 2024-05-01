from typing import Collection

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


def get_driver() -> WebDriver:
    """
    Возвращает экземпляр веб-драйвера chrome
    """
    options = Options()
    options.add_argument("--no-sandbox")  # Отключает режим песочницы
    options.add_argument("--disable-gpu")  # Отключает использование видеокарты
    options.add_argument("--disable-dev-shm-usage")  # Отключает временное хранилище
    options.add_argument("--start-maximized")  # Максимальное окно браузера
    options.add_argument("--headless")  # Отключает графические интерфейс

    return webdriver.Chrome(options=options)


def get_session() -> requests.Session:
    """
    Возвращает сессию для более быстрых запросов к сайтам
    """
    return requests.Session()


def get_soup(html_str: str) -> BeautifulSoup:
    """
    Возвращает soup спарсенной страницы
    """
    return BeautifulSoup(html_str, "html.parser")


def clear(soup: BeautifulSoup | Tag) -> str:
    """
    Убирает код и лишние отступы
    """
    return soup.get_text().strip()


def get_hrefs(result_set: ResultSet | Collection[Tag]):
    """
    Возвращает список из href элементов
    """
    return [element["href"] for element in result_set]


def wait(driver: webdriver, locator: str, value: str, timeout: int = 10):
    """
    Ожидает появление элемента на web-странице
    """
    WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((locator, value))
    )
