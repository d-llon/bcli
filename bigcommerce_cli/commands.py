import click

from .delete import delete_commands
from .get import get_commands
from .post import post_commands
from .put import put_commands
from .settings import settings_commands


@click.group()  # entry point
def bcli():
    pass


@bcli.group(
    commands=[get_commands.customers, get_commands.order_products, get_commands.orders, get_commands.product_variants,
              get_commands.products, get_commands.webhooks]
)
def get():
    """ Make a GET request. """
    pass


@bcli.group(
    commands=[post_commands.customers, post_commands.products, post_commands.webhooks]
)
def post():
    """ Make a POST request. """
    pass


@bcli.group(
    commands=[put_commands.customers, put_commands.product_variants, put_commands.products, put_commands.webhooks]
)
def put():
    """ Make a PUT request. """
    pass


@bcli.group(
    commands=[delete_commands.customers, delete_commands.products, delete_commands.webhooks]
)
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
