import webbrowser

import click

from ..utils import bigcommerce, pretty_table, get_active_store


@click.command()
@click.argument('product_id', default=None, required=False)
@click.option('--filter_name', default=None)
@click.option('-w', '--web', is_flag=True)
def products(product_id, filter_name, web):
    store: dict = get_active_store()
    if not product_id:
        bc_products = bigcommerce.Products.get(params={'include': 'variants'})
        if filter_name:
            bc_products = [p for p in bc_products
                           if filter_name.lower() in p['name'].lower()]

        click.echo(pretty_table.Products.build_table(bc_products))
    else:
        bc_product = bigcommerce.Products.get(resource_id=product_id,
                                              params={'include': 'variants'})

        bc_product_variants = bigcommerce.ProductVariants.get(resource_id=product_id)
        if web:
            webbrowser.open(
                f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/products/edit/{product_id}')
        else:
            click.echo(pretty_table.Products.build_table([bc_product]))
            if len(bc_product_variants) > 1:
                click.echo(pretty_table.ProductVariants.build_table(bc_product_variants))
