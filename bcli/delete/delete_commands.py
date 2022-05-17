import click

from ..utils import bigcommerce


@click.command()
@click.argument('product_id')
def products(product_id):
    """ Request '/catalog/products/<product_id>' endpoint. """
    bc_product = bigcommerce.Products.get(resource_id=product_id)

    if click.confirm(f'Delete ({product_id}) {bc_product["name"]}?'):
        bigcommerce.Products.delete(product_id)
        click.echo(f'Deleted ({product_id}) {bc_product["name"]}.')


@click.command()
@click.argument('customer_id')
def customers(customer_id):
    """ Request '/customers/<customer_id>' endpoint. """
    bc_customer = bigcommerce.CustomersV2.get(resource_id=customer_id)
    full_name = f'{bc_customer["first_name"].strip()} {bc_customer["last_name"].strip()}'

    if click.confirm(f'Delete ({customer_id}) {full_name}?'):
        bigcommerce.CustomersV2.delete(customer_id)
        click.echo(f'Deleted ({customer_id}) {full_name}.')
