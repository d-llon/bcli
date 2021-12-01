import json
from pathlib import Path

import click


def read_from_app_dir(file_name: str) -> dict:
    """ Read JSON data from a file in the bcli app dir. """
    app_dir = click.get_app_dir('bcli')
    file_path = f'{app_dir}/{file_name}'

    if not Path(file_path).is_file():
        file_data = {}
    else:
        with open(file_path, 'r') as file:
            file_data = json.load(file)

    return file_data


def write_to_app_dir(file_name: str, key: str, value: dict) -> dict:
    """ Write JSON data to a file in the bcli app dir. """
    app_dir = click.get_app_dir('bcli')
    file_path = f'{app_dir}/{file_name}'

    if not Path(app_dir).is_dir():
        Path(app_dir).mkdir(parents=True, exist_ok=True)

    if not Path(file_path).is_file():
        with open(file_path, 'w') as file:
            file_data = {key: value}
            json.dump(file_data, file)
    else:
        with open(file_path, 'r') as file:
            file_data = json.load(file)
            file_data[key] = value
        with open(file_path, 'w') as file:
            json.dump(file_data, file)

    return file_data


def delete_from_app_dir(file_name: str, key: str) -> dict:
    """ Delete a JSON key from a file in the bcli app dir. """
    app_dir = click.get_app_dir('bcli')
    file_path = f'{app_dir}/{file_name}'

    with open(file_path, 'r') as file:
        file_data = json.load(file)
        file_data.pop(key)
    with open(file_path, 'w') as file:
        json.dump(file_data, file)

    return file_data
