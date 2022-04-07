import json
import subprocess
import tempfile

import click

from ..utils import bigcommerce, get_active_store


@click.command()
@click.argument('product_id')
def product(product_id):
    catalog_product = bigcommerce.CatalogProduct.get(resource_id=product_id,
                                                     params={'include_fields': 'name,price,sale_price'})

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        json.dump(catalog_product, tmp, indent=4)
        tmp.flush()
        subprocess.call(['nano', tmp.name])
        tmp.seek(0)
        catalog_product_updated = json.load(tmp)

    fields_updated = dict(set(catalog_product_updated.items()) - set(catalog_product.items()))

    if fields_updated:
        bigcommerce.CatalogProduct.put(resource_id=product_id,
                                       json=fields_updated)
