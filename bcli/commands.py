import click

from .get import get_commands
from .put import put_commands
from .settings import settings_commands


@click.group()  # entry point
def bcli():
    pass


@bcli.group(
    commands=[get_commands.product]
)
def get():
    pass


@bcli.group()
def post():
    pass


@bcli.group(
    commands=[put_commands.product]
)
def put():
    pass


@bcli.group()
def delete():
    pass


@bcli.group(
    commands=[settings_commands.list_stores, settings_commands.add_store, settings_commands.delete_store,
              settings_commands.active_store]
)
def settings():
    pass
