import click

from .get import get_commands
from .put import put_commands
from .settings import settings_commands


@click.group()  # entry point
def bcli():
    pass


@bcli.group(
    commands=[get_commands.products, get_commands.customers]
)
def get():
    """ Make a GET request. """
    pass


@bcli.group()
def post():
    """ Make a POST request. """
    pass


@bcli.group(
    commands=[put_commands.products, put_commands.customers]
)
def put():
    """ Make a PUT request. """
    pass


@bcli.group()
def delete():
    """ Make a DELETE request. """
    pass


@bcli.group(
    commands=[settings_commands.list_stores, settings_commands.add_store, settings_commands.delete_store,
              settings_commands.active_store]
)
def settings():
    """ Manage BCLI settings and stores. """
    pass
