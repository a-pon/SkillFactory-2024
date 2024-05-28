import requests
import json
from config import ER_KEY, currencies


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/{ER_KEY}/latest/{base_ticker}')
        quote_price = json.loads(r.content)['conversion_rates'][quote_ticker]
        total_quote = quote_price * amount

        return total_quote
