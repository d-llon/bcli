import requests
from prettytable import PrettyTable


class Variants:
    api_base = 'https://api.bigcommerce.com/stores'

    def __init__(self, store_hash, access_token):
        self.store_hash = store_hash
        self.access_token = access_token
        self.url = f'{self.api_base}/{self.store_hash}/v3/catalog/products'
        self.headers = {'accept': 'application/json', 'x-auth-token': self.access_token}

    def get(self, product_id):
        params = {'limit': 250}
        response = requests.get(f'{self.url}/{product_id}/variants', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()['data']

    def get_pretty_table(self, variants):
        table = PrettyTable()
        table.field_names = ['Variant ID', 'Label', 'Price', 'Sale Price']
        table.align['Label'] = "l"
        table.align['Price'] = "l"
        table.align['Sale Price'] = "l"

        for variant in variants:
            table.add_row([
                variant['id'],
                variant['option_values'][0]['label'],
                '{:,.2f}'.format(float(variant['price'])),
                '{:,.2f}'.format(float(variant['sale_price'])),
            ])
        return table
