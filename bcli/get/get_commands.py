import json
import webbrowser

import click

from ..utils import bigcommerce, pretty_tables, get_active_store


@click.command()
@click.argument('product_id', default=None, required=False)
@click.option('--filter_name', default=None)
@click.option('-w', '--web', is_flag=True)
def products(product_id, filter_name, web):
    """ Request '/catalog/products' endpoint with an optional PRODUCT_ID`. """
    if not product_id:
        bc_products = bigcommerce.Products.get(params={'limit': '250'})
        if filter_name:
            bc_products = [p for p in bc_products
                           if filter_name.lower() in p['name'].lower()]

        click.echo(pretty_tables.products_table(bc_products))
    else:
        if web:
            store: dict = get_active_store()
            webbrowser.open(
                f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/products/edit/{product_id}')
        else:
            bc_product = bigcommerce.Products.get(resource_id=product_id)
            bc_product.pop('description')
            print(json.dumps(bc_product, indent=4))


@click.command()
@click.argument('customer_id', default=None, required=False)
@click.option('--filter_name', default=None)
@click.option('-w', '--web', is_flag=True)
def customers(customer_id, filter_name, web):
    """ Request '/customers' endpoint with an optional CUSTOMER_ID. """
    if not customer_id:
        bc_customers = bigcommerce.CustomersV3.get(params={'limit': '250'})
        if filter_name:
            bc_customers = [c for c in bc_customers if
                            filter_name.lower() in f"{c['first_name']} {c['last_name']}".lower()]

        click.echo(pretty_tables.customers_table(bc_customers))
    else:
        if web:
            store: dict = get_active_store()
            webbrowser.open(
                f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/customers/{customer_id}/edit')
        else:
            bc_customer = bigcommerce.CustomersV2.get(resource_id=customer_id)
            bc_customer.pop('addresses')
            print(json.dumps(bc_customer, indent=4))
