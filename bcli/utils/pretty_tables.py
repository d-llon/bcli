from prettytable import PrettyTable


# BigCommerce Tables ---------------------------------------------------------------------------------------------------

def customers_table(customers: list[dict]):
    table = PrettyTable()
    table.field_names = ['ID', 'Name', 'Email', 'Group ID']
    table.align['Name'] = "l"
    table.align['Email'] = "l"

    for c in customers:
        table.add_row([
            c['id'],
            f'{c["first_name"].strip()} {c["last_name"].strip()}',
            c['email'],
            c['customer_group_id'],
        ])
    return table


def product_variants_table(product_variants: list[dict]):
    table = PrettyTable()
    table.field_names = ['Variant ID', 'Label', 'Price', 'Sale Price']
    table.align['Label'] = "l"
    table.align['Price'] = "l"
    table.align['Sale Price'] = "l"

    for variant in product_variants:
        table.add_row([
            variant['id'],
            variant['option_values'][0]['label'],
            '{:,.2f}'.format(float(variant['price'] or 0)),
            '{:,.2f}'.format(float(variant['sale_price'] or 0)),
        ])
    return table


def products_table(products: list[dict]):
    table = PrettyTable()
    table.field_names = ['ID', 'Name', 'Price', 'Sale Price', 'Variants']
    table.align['Name'] = "l"
    table.align['Price'] = "l"
    table.align['Sale Price'] = "l"

    for cp in products:
        table.add_row([
            cp['id'],
            cp['name'],
            '{:,.2f}'.format(float(cp['price'])),
            '{:,.2f}'.format(float(cp['sale_price'])),
            '🟢' if len(cp['variants']) > 1 else '⚫️'
        ])
    return table


# BCLI Tables ----------------------------------------------------------------------------------------------------------

def stores_table(stores: dict):
    table = PrettyTable()
    table.field_names = ['Store', 'Store Hash', 'Access Token']
    table.align['Store'] = "l"
    table.align['Store Hash'] = "l"
    table.align['Access Token'] = "l"

    for store_name, store_creds in stores.items():
        table.add_row([
            store_name,
            store_creds['store_hash'],
            store_creds['access_token']
        ])
    return table
