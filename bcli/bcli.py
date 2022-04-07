import click

from .get import get_commands
from .put import put_commands
from .settings import settings_commands


@click.group()  # entry point
def bcli():
    pass


@bcli.group()
def get():
    pass


get.add_command(get_commands.product)


@bcli.group()
def post():
    pass


@bcli.group()
def put():
    pass


put.add_command(put_commands.product)


@bcli.group()
def delete():
    pass


@bcli.group()
def settings():
    pass


settings.add_command(settings_commands.list_stores)
settings.add_command(settings_commands.add_store)
settings.add_command(settings_commands.delete_store)
settings.add_command(settings_commands.active_store)
