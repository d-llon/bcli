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


def order_products_table(order_products: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Product ID', 'Name', 'SKU', 'Quantity', 'Total']
    table.align['Product ID'] = CENTER

    for op in order_products:
        table.add_row([
            op['id'],
            op['product_id'],
            ', '.join([op['name'], *[o['display_value'] for o in op['product_options']]]),
            op['sku'],
            op['quantity'],
            '{:,.2f}'.format(float(op['total_inc_tax'] or 0)),
        ])
    return table


def orders_table(orders: list[dict], customers: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Name', 'Email', 'Status', 'Digital', 'Items', 'Total']
    table.align['Items'] = CENTER

    customers_map = {c['id']: c for c in customers}
    for o in orders:
        c = customers_map.get(o['customer_id'], {})  # Sometimes the customer responsible for an order gets deleted
        table.add_row([
            o['id'],
            f'{c.get("first_name", "").strip()} {c.get("last_name", "").strip()}',
            c.get('email', ''),
            o['status'],
            o['order_is_digital'],
            o['items_total'],
            '{:,.2f}'.format(float(o['total_inc_tax'] or 0)),
        ])
    return table


def product_variants_table(product_variants: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Variant', 'SKU', 'Price', 'Purchasable']

    for v in product_variants:
        table.add_row([
            v['id'],
            v['option_values'][0]['label'],
            v['sku'],
            '{:,.2f}'.format(float(v['price'] or 0)),
            not v['purchasing_disabled'],
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
            p['is_visible'],
        ])
    return table


def webhooks_table(webhooks: list[dict]):
    table = BCLITable()
    table.field_names = ['ID', 'Scope', 'Destination', 'Active']

    for w in webhooks:
        table.add_row([
            w['id'],
            w['scope'],
            w['destination'],
            w['is_active'],
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
            store_creds['access_token'],
        ])
    return table
