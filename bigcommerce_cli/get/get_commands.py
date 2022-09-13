import webbrowser

import click

from ..utils import bigcommerce, pretty_tables, get_active_store, format_for_humans


@click.command()
@click.argument('customer_id', default=None, required=False)
@click.option('--filter_email', default=None)
@click.option('-w', '--web', is_flag=True)
def customers(customer_id, filter_email, web):
    """ Request '/customers' endpoint with an optional CUSTOMER_ID. """
    if not customer_id:
        bc_customers = bigcommerce.CustomersV3.get(params={'limit': '250'})
        if filter_email:
            bc_customers = [c for c in bc_customers if
                            filter_email.lower() in c['email'].lower()]

        click.echo(pretty_tables.customers_table(bc_customers))
    else:
        if web:
            store: dict = get_active_store()
            webbrowser.open(
                f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/customers/{customer_id}/edit')
        else:
            bc_customer = bigcommerce.CustomersV2.get(resource_id=customer_id)
            bc_customer.pop('addresses')
            click.echo(format_for_humans(bc_customer))


@click.command()
@click.argument('product_id')
@click.argument('variant_id', default=None, required=False)
def product_variants(product_id, variant_id):
    """ Request '/catalog/products/<product_id>/variants' endpoint with an optional VARIANT_ID. """
    if not variant_id:
        bc_product = bigcommerce.Products.get(resource_id=product_id)
        bc_variants = bigcommerce.ProductVariants.get(resource_id=product_id, params={'limit': '250'})

        if len(bc_variants) == 1 and bc_variants[0]['id'] == bc_product['base_variant_id']:
            # This product's only variant is the base variant
            click.echo(pretty_tables.product_variants_table([]))
        else:
            click.echo(pretty_tables.product_variants_table(bc_variants))
    else:
        bc_variant = bigcommerce.ProductVariants.get(resource_id=product_id, subresource_id=variant_id)
        click.echo(format_for_humans(bc_variant))


@click.command()
@click.argument('product_id', default=None, required=False)
@click.option('--filter_name', default=None)
@click.option('-w', '--web', is_flag=True)
def products(product_id, filter_name, web):
    """ Request '/catalog/products' endpoint with an optional PRODUCT_ID. """
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
            click.echo(format_for_humans(bc_product))


@click.command()
@click.argument('webhook_id', default=None, required=False)
def webhooks(webhook_id):
    """ Request '/hooks' endpoint with an optional WEBHOOK_ID. """
    if not webhook_id:
        bc_webhooks = bigcommerce.Webhooks.get(params={'limit': '250'})
        click.echo(pretty_tables.webhooks_table(bc_webhooks))
    else:
        bc_webhook = bigcommerce.Webhooks.get(resource_id=webhook_id)
        click.echo(format_for_humans(bc_webhook))
