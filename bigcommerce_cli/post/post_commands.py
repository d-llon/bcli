import click

from bigcommerce_cli.utils import bigcommerce
from bigcommerce_cli.utils.click_extensions import DictParamType


@click.command()
def customers():
    """ Request '/customers' endpoint. """
    first_name = click.prompt('First name', type=str)
    last_name = click.prompt('Last name', type=str)
    email = click.prompt('Email', type=str)

    bc_customer = bigcommerce.CustomersV2.post(json={'first_name': first_name,
                                                     'last_name': last_name,
                                                     'email': email})

    full_name = f'{bc_customer["first_name"].strip()} {bc_customer["last_name"].strip()}'
    click.echo(f'Created ({bc_customer["id"]}) {full_name}')


@click.command()
def products():
    """ Request '/catalog/products' endpoint. """
    name = click.prompt('Name', type=str)
    type = click.prompt('Type', type=str, default='physical')
    weight = click.prompt('Weight', type=float, default=0.0)
    price = click.prompt('Price', type=float)
    visible = click.confirm('Visible')

    bc_product = bigcommerce.Products.post(json={'name': name,
                                                 'type': type,
                                                 'weight': weight,
                                                 'price': price,
                                                 'is_visible': visible})

    click.echo(f'Created ({bc_product["id"]}) {bc_product["name"]}')


@click.command()
def webhooks():
    """ Request '/hooks' endpoint. """
    scope = click.prompt('Scope', type=str)
    destination = click.prompt('Destination', type=str)
    headers = click.prompt('Headers', type=DictParamType(), default={})

    bc_webhook = bigcommerce.Webhooks.post(json={'scope': scope,
                                                 'destination': destination,
                                                 'headers': headers or None})

    click.echo(f'Created ({bc_webhook["id"]}) with scope \'{bc_webhook["scope"]}\'')
