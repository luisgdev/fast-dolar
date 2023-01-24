""" Scraping Telegram channel functions """

import re
from pprint import pformat, pprint
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from requests import Response

PARALELO_CHANNEL: str = "https://t.me/s/enparalelovzlatelegram?q=Bs."
ALERTAS24_CHANNEL: str = "https://t.me/s/Alertas24?q=AHORA.+El+dólar"

HTML_PARSER: str = "html.parser"
HTML_CLASS: str = "class"
HTML_TARGET_TAG: str = "div"
HTML_TARGET_CLASS: str = "tgme_widget_message_text"
RE_PATTERN: str = r"\d{1,2}[.,]\d{1,2}"


# pylint: disable=broad-except


class ScraperException(Exception):
    """Exception ocurred on scraper module"""


def _get_page(url: str) -> Response:
    """
    Get source code of the web page. \f
    :param url: URL of the webpage.
    :return: Response object.
    :raises: ScraperException If fails.
    """
    try:
        res = requests.get(url=url, timeout=30)
        if res.status_code == 200:
            return res
        print(pformat(ScraperException(f"HTTP status code: {res.status_code}.")))
    except Exception as ex:
        print(pformat(ex))


def _parse_channel(
    source_url: str, page_content: Optional[str] = None
) -> Optional[List[str]]:
    """
    Parse paralelo telegram channel and return last rate messages. \f
    :param source_url: URL of the webpage.
    :param page_content: Webpage content for tests.
    :return: List of strings with messages.
    """
    result = []
    if not page_content:
        response = _get_page(source_url)
    if not response:
        return None
    soup = BeautifulSoup(response.text, HTML_PARSER)
    divs = soup.find_all(HTML_TARGET_TAG)
    result = tuple(div for div in divs if HTML_TARGET_CLASS in div[HTML_CLASS])
    return None if len(result) == 0 else result[-1].text


def get_paralelo_rate() -> Optional[float]:
    """
    Get PARALELO rate from @enparalelovzlatelegram channel.
    Example message: '🗓️ 23/09/2022 🕒 1:04 PM 💵 Bs. 8,34 🔻 0,12% Bs 0,01' \f
    :return: Float with the rate or None.
    """
    message: Optional[str] = _parse_channel(source_url=PARALELO_CHANNEL)
    if not message:
        return message
    sub_start: int = message.find("Bs. ")
    sub_end: int = message.find("%")
    result = re.findall(pattern=RE_PATTERN, string=message[sub_start:sub_end], flags=0)
    return None if len(result) == 0 else float(result[0].replace(",", "."))


def get_bcv_rate() -> Optional[float]:
    """
    Get BCV rate from @Alertas24 telegram channel.
    Example message:
        'Así cerró el dólar esta tarde 23/09/22
        8,34 (Monitor) ⬇️8,41 (Dólar Today) ⬆️8,11 (BCV)  =' \f
    :param message: Message from channel.
    :return: Float with the rate or None.
    """
    message: Optional[str] = _parse_channel(source_url=ALERTAS24_CHANNEL)
    if not message:
        return message
    sub_start: int = message.find(" en ")
    sub_end: int = message.find("Fecha ")
    result = re.findall(pattern=RE_PATTERN, string=message[sub_start:sub_end], flags=0)
    return None if len(result) == 0 else float(result[0].replace(",", "."))


def main() -> None:
    """Main function"""
    output = {
        "PARALELO": get_paralelo_rate(),
        "DOLARBCV": get_bcv_rate(),
    }
    pprint(output)


if __name__ == "__main__":
    main()
