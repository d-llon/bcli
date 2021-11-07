import json
import webbrowser
from pathlib import Path

import click
from PyInquirer import prompt
from click import echo
from prettytable import PrettyTable

from ..utils import bigcommerce, pretty_table, get_store_creds


@click.group()
def cli():
    pass


# Store Commands -------------------------------------------------------------------------------------------------------
@cli.group()
def store():
    pass


@store.command('add')
def store_add():
    """  """
    user_input = prompt([
        {'type': 'input', 'name': 'store', 'message': f'Store name: '},
        {'type': 'input', 'name': 'hash', 'message': f'Store hash: '},
        {'type': 'input', 'name': 'access_token', 'message': f'Access token: '},
    ])

    # TODO: Confirm overwrite?
    # TODO: Confirm user input is valid before saving

    app_dir = click.get_app_dir('bcli')
    if not Path(app_dir).is_dir():
        Path(app_dir).mkdir(parents=True, exist_ok=True)

    config_path = f'{app_dir}/stores.json'
    if not Path(config_path).is_file():
        with open(config_path, 'w') as stores_file:
            stores = {}
            stores[user_input['store']] = {'store_hash': user_input['hash'], 'access_token': user_input['access_token']}
            json.dump(stores, stores_file)
    else:
        with open(config_path, 'r') as stores_file:
            stores = json.load(stores_file)
            stores[user_input['store']] = {'store_hash': user_input['hash'], 'access_token': user_input['access_token']}
        with open(config_path, 'w') as stores_file:
            json.dump(stores, stores_file)


@store.command('list')
def store_list():
    """  """
    app_dir = click.get_app_dir('bcli')
    config_path = f'{app_dir}/stores.json'
    if not Path(config_path).is_file():
        stores = {}
    else:
        with open(config_path, 'r') as stores_file:
            stores = json.load(stores_file)

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
@click.argument('store')
def store_delete(store):
    """  """
    app_dir = click.get_app_dir('bcli')
    config_path = f'{app_dir}/stores.json'

    # TODO: Delete confirmation
    # TODO: Decide if I want to check if a store exists before run .pop on it

    if Path(config_path).is_file():
        with open(config_path, 'r') as stores_file:
            stores = json.load(stores_file)
            stores.pop(store)
        with open(config_path, 'w') as stores_file:
            json.dump(stores, stores_file)


# Product Commands -----------------------------------------------------------------------------------------------------
@cli.group()
def product():
    pass


@product.command('list')
@click.option('-s', '--store', required=True)
@click.option('--filter_name', default=None)
def product_list(store, filter_name):
    store = get_store_creds(store)
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
    store = get_store_creds(store)
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
    store = get_store_creds(store)
    catalog_product = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                     access_token=store['access_token'],
                                                     resource_id=product_id,
                                                     params={'include': 'variants'})

    echo(pretty_table.CatalogProduct.build_table([catalog_product]))

    if not field:
        user_input = prompt([
            {
                'type': 'list',
                'name': 'field',
                'message': 'What field would you like to edit?',
                'choices': list(catalog_product.keys())
            },
        ])
        field = user_input['field']

    user_input = prompt([
        {
            'type': 'input',
            'name': 'value',
            'message': f'New value: ',
            'default': catalog_product[field]
        },
        {
            'type': 'confirm',
            'name': 'confirm',
            'message': 'Submit?'
        }
    ])

    if user_input['confirm']:
        bigcommerce.CatalogProduct.put(store_hash=store['store_hash'],
                                       access_token=store['access_token'],
                                       resource_id=product_id,
                                       json={field: user_input['value']})
        echo('Edit complete.')
    else:
        echo('Edit canceled.')
