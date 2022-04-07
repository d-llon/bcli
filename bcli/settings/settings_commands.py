import click
from PyInquirer import prompt
from click import echo
from prettytable import PrettyTable

from ..utils import read_from_app_dir, write_to_app_dir, delete_from_app_dir


@click.command()
def list_stores():
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


@click.command()
def add_store():
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


@click.command()
@click.argument('store_name')
def delete_store(store_name):
    """ Delete a set of API credentials by store name. """
    delete_from_app_dir('stores.json', key=store_name)
    echo(f'Deleted store ({store_name}).')


@click.command()
@click.argument('store_name', required=False, default=None)
def active_store(store_name):
    """ Read or set an active store. """
    settings = read_from_app_dir('settings.json')
    stores = read_from_app_dir('stores.json')

    if store_name:
        if store_name not in stores.keys():
            raise ValueError(f'No saved store \'{store_name}\'')
        write_to_app_dir('settings.json',
                         key='active_store',
                         value=store_name)
    else:
        store_name = settings.get('active_store')
        if not store_name or store_name not in stores.keys():
            echo('No active store.')
            return

        store_hash = stores[store_name]["store_hash"]
        echo(f'Active store: {store_name} ({store_hash})')
