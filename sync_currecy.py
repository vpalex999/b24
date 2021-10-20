import logging
from contextlib import ContextDecorator

import bs4
import requests

TEMPLATE_NAME_PAIR = 'RUB-{}'

logger = logging.getLogger('sync_currency')
logger.level = logging.INFO
console_hundler = logging.StreamHandler()
file_hundler = logging.FileHandler('sync_currency.log')
console_hundler.setLevel(logging.INFO)
file_hundler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
file_hundler.setFormatter(formatter)
console_hundler.setFormatter(formatter)
logger.addHandler(console_hundler)
logger.addHandler(file_hundler)


class ProdContext(ContextDecorator):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            logger.warning(
                f"Some gone wrong:{exc_type}\n{exc_value}\n{traceback}")
        return True


class B24Repo:

    url = "http://b24.comn"

    def sync_currency(self, currency_pairs: dict) -> None:
        logger.info(f'send to fake API "{self.url}" data currency-pairs: {currency_pairs}')


class CBRRepo:

    url = 'http://www.cbr.ru/scripts1/XML_daily.asp'

    def _request_all_currency(self) -> str:
        response = requests.get(self.url)
        logging.info(f'get currency data from {self.url}')

        if response.status_code != 200 or 'Error' in response.url:
            raise Exception(
                f'wrong get currency from cbr API {self.url}: {response.text}')

        return response.text

    def get_currency(self) -> dict:
        currency_xml = self._request_all_currency()

        parser = bs4.BeautifulSoup(currency_xml, features='lxml')

        return {xml_item.find('charcode').text: xml_item.find(
            'value').text for xml_item in parser.find_all('valute')}


@ProdContext()
def sync_currency(currency_list, src_repo: CBRRepo, dst_repo) -> bool:
    src_currency = src_repo.get_currency()

    selected_pairs = {
        TEMPLATE_NAME_PAIR.format(cur): value for cur, value in src_currency.items()
        if TEMPLATE_NAME_PAIR.format(cur) in currency_list}

    dst_repo.sync_currency(selected_pairs)


if __name__ == "__main__":
    currency_list = [
        'RUB-EUR',
        'RUB-USD',
        'RUB-KZT',
        'RUB-PLN',
    ]

    sync_currency(currency_list, CBRRepo(), B24Repo())
