from prettytable import PrettyTable

from . import bigcommerce_strptime

LEFT = 'l'
RIGHT = 'r'
CENTER = 'c'


class BCLITable(PrettyTable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.align = LEFT


# BigCommerce Tables ---------------------------------------------------------------------------------------------------

def customers_table(customers: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Name', 'Email', 'Phone', 'Group ID', 'Joined']
    table.align['Group ID'] = CENTER

    for c in customers:
        table.add_row([
            c['id'],
            f'{c["first_name"].strip()} {c["last_name"].strip()}',
            c['email'],
            c['phone'],
            c['customer_group_id'],
            bigcommerce_strptime(c['date_created']).strftime('%b %d %Y'),
        ])
    return table


def product_variants_table(product_variants: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Variant', 'SKU', 'Price', 'Purchasable']

    for variant in product_variants:
        table.add_row([
            variant['id'],
            variant['option_values'][0]['label'],
            variant['sku'],
            '{:,.2f}'.format(float(variant['price'] or 0)),
            not variant['purchasing_disabled'],
        ])
    return table


def products_table(products: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'SKU', 'Name', 'Price', 'Visible']

    for p in products:
        table.add_row([
            p['id'],
            p['sku'],
            p['name'],
            '{:,.2f}'.format(float(p['price'])),
            p['is_visible']
        ])
    return table


# BCLI Tables ----------------------------------------------------------------------------------------------------------

def stores_table(stores: dict):
    table = BCLITable()
    table.field_names = ['Store', 'Store Hash', 'Access Token']

    for store_name, store_creds in stores.items():
        table.add_row([
            store_name,
            store_creds['store_hash'],
            store_creds['access_token']
        ])
    return table
