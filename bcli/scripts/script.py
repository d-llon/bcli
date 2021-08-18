import click
from PyInquirer import prompt
from click import echo

from ..utils import bigcommerce

store_db = {
}


@click.group()
def cli():
    pass


@cli.group()
def product():
    pass


@product.command('list')
@click.option('-s', '--store', required=True)
@click.option('--filter_name', default=None)
def product_list(store, filter_name):
    bc_products = bigcommerce.Products(store_hash=store_db[store]['store_hash'],
                                       access_token=store_db[store]['access_token'])
    products = bc_products.get()

    if filter_name:
        products = [p for p in products
                    if filter_name.lower() in p['name'].lower()]

    table = bc_products.get_pretty_table(products)
    echo(table)


@product.command('view')
@click.argument('product_id')
@click.option('-s', '--store', required=True)
@click.option('-w', '--web', is_flag=True)
def product_view(product_id, store, web):
    bc_products = bigcommerce.Products(store_hash=store_db[store]['store_hash'],
                                       access_token=store_db[store]['access_token'])
    product = bc_products.retrieve(product_id)

    bc_variants = bigcommerce.Variants(store_hash=store_db[store]['store_hash'],
                                       access_token=store_db[store]['access_token'])
    variants = bc_variants.get(product_id)

    if web:
        bc_products.web_view(product_id)
    else:
        table = bc_products.get_pretty_table([product])
        echo(table)

        table = bc_variants.get_pretty_table(variants)
        echo(table)


@product.command('edit')
@click.argument('product_id')
@click.option('-s', '--store', required=True)
def product_edit(product_id, store):
    bc_products = bigcommerce.Products(store_hash=store_db[store]['store_hash'],
                                       access_token=store_db[store]['access_token'])
    product = bc_products.retrieve(product_id)

    table = bc_products.get_pretty_table([product])
    echo(table)

    user_input = prompt([
        {
            'type': 'list',
            'name': 'field',
            'message': 'What field would you like to edit?',
            'choices': ['price', 'sale_price']
        },
        {
            'type': 'input',
            'name': 'value',
            'message': f'New value: '
        },
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Submit?'
        }
    ])

    if user_input['confirm']:
        if user_input['field'] == 'price':
            bc_products.patch(product_id, price=float(user_input['value']))
            echo('Edit complete.')
        if user_input['field'] == 'sale_price':
            bc_products.patch(product_id, sale_price=float(user_input['value']))
            echo('Edit complete.')
    else:
        echo('Edit canceled.')
