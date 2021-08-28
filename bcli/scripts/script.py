import webbrowser

import click
from PyInquirer import prompt
from click import echo

from ..utils import bigcommerce, pretty_table

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
    catalog_products = bigcommerce.CatalogProduct.get(store_hash=store_db[store]['store_hash'],
                                                      access_token=store_db[store]['access_token'],
                                                      params={'limit': 250, 'include': 'variants'})
    if filter_name:
        catalog_products = [p for p in catalog_products
                            if filter_name.lower() in p['name'].lower()]

    echo(pretty_table.CatalogProduct.build_table(catalog_products))


@product.command('view')
@click.argument('product_id')
@click.option('-s', '--store', required=True)
@click.option('-w', '--web', is_flag=True)
def product_view(product_id, store, web):
    catalog_product = bigcommerce.CatalogProduct.get(store_hash=store_db[store]['store_hash'],
                                                     access_token=store_db[store]['access_token'],
                                                     resource_id=product_id,
                                                     params={'include': 'variants'})

    catalog_product_variants = bigcommerce.CatalogProductVariant.get(store_hash=store_db[store]['store_hash'],
                                                                     access_token=store_db[store]['access_token'],
                                                                     resource_id=product_id)
    if web:
        webbrowser.open(
            f'https://store-{store_db[store]["store_hash"]}.mybigcommerce.com/manage/products/edit/{product_id}')
    else:
        echo(pretty_table.CatalogProduct.build_table([catalog_product]))
        if len(catalog_product_variants) > 1:
            echo(pretty_table.CatalogProductVariant.build_table(catalog_product_variants))


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
