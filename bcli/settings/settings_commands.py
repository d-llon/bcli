import click
from click import echo

from ..utils import read_from_app_dir, write_to_app_dir, delete_from_app_dir, pretty_tables


@click.command()
def list_stores():
    """ Print all saved API credentials. """
    stores = read_from_app_dir('stores.json')
    echo(pretty_tables.stores_table(stores))


@click.command()
def add_store():
    """ Save store API credentials. """
    store_name = click.prompt('Store name: ', type=str)
    store_hash = click.prompt('Store hash: ', type=str)
    access_token = click.prompt('Access token: ', type=str)

    if read_from_app_dir('stores.json').get(store_name):
        if not click.confirm('Overwrite? '):
            return

    write_to_app_dir('stores.json',
                     key=store_name,
                     value={'store_hash': store_hash, 'access_token': access_token})


@click.command()
@click.argument('store_name')
def delete_store(store_name):
    """ Delete a set of API credentials by store name. """
    delete_from_app_dir('stores.json', key=store_name)
    echo(f'Deleted store ({store_name}).')


@click.command()
@click.argument('store_name', required=False, default=None)
def active_store(store_name):
    """ Display or set active store API credentials by store name. """
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
