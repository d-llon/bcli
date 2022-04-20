import json
import subprocess
import tempfile

import click

from ..utils import bigcommerce


@click.command()
@click.argument('product_id')
def products(product_id):
    # TODO: Use a typed dict?
    editable_keys = ['name', 'type', 'sku', 'weight', 'width', 'depth', 'height', 'price', 'sale_price', 'tax_class_id',
                     'brand_id', 'inventory_level', 'inventory_tracking', 'is_free_shipping', 'is_visible',
                     'is_featured', 'availability', 'sort_order', 'order_quantity_minimum', 'order_quantity_maximum',
                     'page_title']

    bc_product = bigcommerce.Products.get(resource_id=product_id)
    bc_product = {key: bc_product[key] for key in bc_product.keys() if key in editable_keys}

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        json.dump(bc_product, tmp, indent=4)
        tmp.flush()
        subprocess.call(['nano', tmp.name])
        tmp.seek(0)
        bc_product_updated = json.load(tmp)

    fields_updated = dict(set(bc_product_updated.items()) - set(bc_product.items()))

    if fields_updated:
        bigcommerce.Products.put(resource_id=product_id, json=fields_updated)
        print('Fields Updated:')
        print(json.dumps(fields_updated, indent=4))


@click.command()
@click.argument('customer_id')
def customers(customer_id):
    editable_keys = ['email', 'first_name', 'last_name', 'company', 'phone', 'notes', 'tax_exempt_category',
                     'customer_group_id', ]

    bc_customer: dict = bigcommerce.CustomersV2.get(resource_id=customer_id)
    bc_customer = {key: bc_customer[key] for key in bc_customer.keys() if key in editable_keys}

    with tempfile.NamedTemporaryFile(mode='w+') as tmp:
        json.dump(bc_customer, tmp, indent=4)
        tmp.flush()
        subprocess.call(['nano', tmp.name])
        tmp.seek(0)
        bc_customer_updated = json.load(tmp)

    fields_updated = dict(set(bc_customer_updated.items()) - set(bc_customer.items()))

    if fields_updated:
        bigcommerce.CustomersV2.put(resource_id=customer_id, json=fields_updated)
        print('Fields Updated:')
        print(json.dumps(fields_updated, indent=4))
