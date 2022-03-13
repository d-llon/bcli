import json
import subprocess
import tempfile
import webbrowser

import click
from PyInquirer import prompt
from click import echo
from prettytable import PrettyTable

from ..utils import bigcommerce, pretty_table, read_from_app_dir, write_to_app_dir, delete_from_app_dir


@click.group()
def cli():
    pass


# Store Commands -------------------------------------------------------------------------------------------------------
@cli.group()
def store():
    pass


@store.command('add')
def store_add():
    """ Save store API credentials. """
    user_input = prompt([
        {'type': 'input', 'name': 'store_name', 'message': f'Store name: '},
        {'type': 'input', 'name': 'store_hash', 'message': f'Store hash: '},
        {'type': 'input', 'name': 'access_token', 'message': f'Access token: '},
    ])

    if read_from_app_dir('stores.json').get(user_input['store_name']):
        user_input['confirm'] = prompt([{'type': 'confirm', 'name': 'confirm', 'message': f'Overwrite? '}])['confirm']

    if user_input.get('confirm', True):
        write_to_app_dir('stores.json',
                         key=user_input['store_name'],
                         value={'store_hash': user_input['store_hash'], 'access_token': user_input['access_token']})


@store.command('list')
def store_list():
    """ Print all saved API credentials. """
    stores = read_from_app_dir('stores.json')

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

    echo(table)


@store.command('delete')
@click.argument('store_name')
def store_delete(store_name):
    """ Delete a set of API credentials by store name. """
    delete_from_app_dir('stores.json', key=store_name)
    echo(f'Deleted store ({store_name}).')


# Product Commands -----------------------------------------------------------------------------------------------------
@cli.group()
def product():
    pass


@product.command('list')
@click.option('-s', '--store', required=True)
@click.option('--filter_name', default=None)
def product_list(store, filter_name):
    store = read_from_app_dir('stores.json')[store]
    catalog_products = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                      access_token=store['access_token'],
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
    store = read_from_app_dir('stores.json')[store]
    catalog_product = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                     access_token=store['access_token'],
                                                     resource_id=product_id,
                                                     params={'include': 'variants'})

    catalog_product_variants = bigcommerce.CatalogProductVariant.get(store_hash=store['store_hash'],
                                                                     access_token=store['access_token'],
                                                                     resource_id=product_id)
    if web:
        webbrowser.open(
            f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/products/edit/{product_id}')
    else:
        echo(pretty_table.CatalogProduct.build_table([catalog_product]))
        if len(catalog_product_variants) > 1:
            echo(pretty_table.CatalogProductVariant.build_table(catalog_product_variants))


@product.command('edit')
@click.argument('product_id')
@click.option('-s', '--store', required=True)
@click.option('--field', default=None)
def product_edit(product_id, store, field):
    store = read_from_app_dir('stores.json')[store]
    catalog_product = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                     access_token=store['access_token'],
                                                     resource_id=product_id,
                                                     params={'include_fields': 'name,price,sale_price'})

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        json.dump(catalog_product, tmp, indent=4)
        tmp.flush()
        subprocess.call(['nano', tmp.name])
        tmp.seek(0)
        catalog_product_updated = json.load(tmp)

    fields_updated = dict(set(catalog_product_updated.items()) - set(catalog_product.items()))

    if fields_updated:
        bigcommerce.CatalogProduct.put(store_hash=store['store_hash'],
                                       access_token=store['access_token'],
                                       resource_id=product_id,
                                       json=fields_updated)
