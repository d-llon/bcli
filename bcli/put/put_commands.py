import json
import subprocess
import tempfile

import click

from ..utils import bigcommerce


@click.command()
@click.argument('product_id')
def products(product_id):
    catalog_product = bigcommerce.Products.get(resource_id=product_id,
                                               params={'include_fields': 'name,price,sale_price'})

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        json.dump(catalog_product, tmp, indent=4)
        tmp.flush()
        subprocess.call(['nano', tmp.name])
        tmp.seek(0)
        catalog_product_updated = json.load(tmp)

    fields_updated = dict(set(catalog_product_updated.items()) - set(catalog_product.items()))

    if fields_updated:
        bigcommerce.Products.put(resource_id=product_id,
                                 json=fields_updated)
