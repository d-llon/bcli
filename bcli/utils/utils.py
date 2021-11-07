import json

import click


def get_store_creds(store: str):
    """ Get a saved store hash and access token from a store name. """
    app_dir = click.get_app_dir('bcli')
    config_path = f'{app_dir}/stores.json'

    with open(config_path, 'r') as stores_file:
        stores = json.load(stores_file)
        return stores[store]
