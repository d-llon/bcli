import webbrowser

import requests
from prettytable import PrettyTable


class Products:
    api_base = 'https://api.bigcommerce.com/stores'

    def __init__(self, store_hash, access_token):
        self.store_hash = store_hash
        self.access_token = access_token
        self.url = f'{self.api_base}/{self.store_hash}/v3/catalog/products'
        self.headers = {'accept': 'application/json', 'x-auth-token': self.access_token}

    def get(self):
        params = {'limit': 250, 'include': 'variants'}
        response = requests.get(self.url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()['data']

    def retrieve(self, product_id):
        params = {'include': 'variants'}
        response = requests.get(f'{self.url}/{product_id}', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()['data']

    def patch(self, product_id, **kwargs):
        response = requests.put(f'{self.url}/{product_id}', headers=self.headers, json=kwargs)
        response.raise_for_status()
        return response.json()['data']

    def get_pretty_table(self, products):
        table = PrettyTable()
        table.field_names = ['ID', 'Name', 'Price', 'Sale Price', 'Variants']
        table.align['Name'] = "l"
        table.align['Price'] = "l"
        table.align['Sale Price'] = "l"

        for product in products:
            table.add_row([
                product['id'],
                product['name'],
                '{:,.2f}'.format(float(product['price'])),
                '{:,.2f}'.format(float(product['sale_price'])),
                '🟢' if len(product['variants']) > 1 else '⚫️'
            ])
        return table

    def web_view(self, product_id):
        webbrowser.open(f'https://store-{self.store_hash}.mybigcommerce.com/manage/products/edit/{product_id}')
