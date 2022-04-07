import webbrowser

import click

from ..utils import read_from_app_dir, bigcommerce, pretty_table


@click.command()
@click.argument('product_id', default=None, required=False)
@click.option('--filter_name', default=None)
@click.option('-s', '--store', required=True)
@click.option('-w', '--web', is_flag=True)
def product(product_id, filter_name, store, web):
    if not product_id:
        store = read_from_app_dir('stores.json')[store]
        catalog_products = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                          access_token=store['access_token'],
                                                          params={'limit': 250, 'include': 'variants'})
        if filter_name:
            catalog_products = [p for p in catalog_products
                                if filter_name.lower() in p['name'].lower()]

        click.echo(pretty_table.CatalogProduct.build_table(catalog_products))
    else:
        store = read_from_app_dir('stores.json')[store]
        catalog_product = bigcommerce.CatalogProduct.get(store_hash=store['store_hash'],
                                                         access_token=store['access_token'],
                                                         resource_id=product_id,
                                                         params={'include': 'variants'})

        catalog_product_variants = bigcommerce.CatalogProductVariant.get(store_hash=store['store_hash'],
                                                                         access_token=store['access_token'],
                                                                         resource_id=product_id)
        if web:
            webbrowser.open(
                f'https://store-{store["store_hash"]}.mybigcommerce.com/manage/products/edit/{product_id}')
        else:
            click.echo(pretty_table.CatalogProduct.build_table([catalog_product]))
            if len(catalog_product_variants) > 1:
                click.echo(pretty_table.CatalogProductVariant.build_table(catalog_product_variants))
