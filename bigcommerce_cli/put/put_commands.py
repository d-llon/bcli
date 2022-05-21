import json

import click

from ..utils import bigcommerce


@click.command()
@click.argument('product_id')
def products(product_id):
    """ Request '/catalog/products/<product_id>' endpoint. """
    editable_keys = ['name', 'type', 'sku', 'weight', 'width', 'depth', 'height', 'price', 'sale_price', 'tax_class_id',
                     'brand_id', 'inventory_level', 'inventory_tracking', 'is_free_shipping', 'is_visible',
                     'is_featured', 'availability', 'sort_order', 'order_quantity_minimum', 'order_quantity_maximum',
                     'page_title']

    bc_product = bigcommerce.Products.get(resource_id=product_id)
    bc_product = {key: bc_product[key] for key in bc_product.keys() if key in editable_keys}

    fields_edited = launch_editor(bc_product)

    if fields_edited:
        bigcommerce.Products.put(resource_id=product_id, json=fields_edited)
        click.echo('Fields Updated:')
        click.echo(json.dumps(fields_edited, indent=4))


@click.command()
@click.argument('product_id')
@click.argument('variant_id')
def product_variants(product_id, variant_id):
    """ Request '/catalog/products/<product_id>/variants' endpoint. """
    editable_keys = ['sku', 'price', 'sale_price', 'retail_price', 'map_price', 'weight', 'width', 'height', 'depth',
                     'is_free_shipping', 'fixed_cost_shipping_price', 'purchasing_disabled',
                     'purchasing_disabled_message', 'image_url', 'cost_price', 'upc', 'mpn', 'gtin', 'inventory_level',
                     'inventory_warning_level', 'bin_picking_number']

    bc_variant = bigcommerce.ProductVariants.get(resource_id=product_id, subresource_id=variant_id)
    bc_variant = {key: bc_variant[key] for key in bc_variant.keys() if key in editable_keys}

    fields_edited = launch_editor(bc_variant)

    if fields_edited:
        bigcommerce.ProductVariants.put(resource_id=product_id, subresource_id=variant_id, json=fields_edited)
        click.echo('Fields Updated:')
        click.echo(json.dumps(fields_edited, indent=4))


@click.command()
@click.argument('customer_id')
def customers(customer_id):
    """ Request '/customers/<customer_id>' endpoint. """
    editable_keys = ['email', 'first_name', 'last_name', 'company', 'phone', 'notes', 'tax_exempt_category',
                     'customer_group_id', 'authentication', 'accepts_product_review_abandoned_cart_emails',
                     'store_credit_amounts', 'origin_channel_id', 'channel_ids', 'form_fields']

    bc_customer: dict = bigcommerce.CustomersV2.get(resource_id=customer_id)
    bc_customer = {key: bc_customer[key] for key in bc_customer.keys() if key in editable_keys}

    fields_edited = launch_editor(bc_customer)

    if fields_edited:
        bigcommerce.CustomersV2.put(resource_id=customer_id, json=fields_edited)
        click.echo('Fields Updated:')
        click.echo(json.dumps(fields_edited, indent=4))


# HELPERS --------------------------------------------------------------------------------------------------------------
def launch_editor(value: dict) -> dict:
    """ Launch the user's default editor with dictionary data and return any fields edited. """
    text = json.dumps(value, indent=4)
    edited_text = click.edit(text=text, require_save=False, extension='.json')
    edited_value = json.loads(edited_text)

    if len(edited_value.keys()) != len(value.keys()):
        raise ValueError('You may not add or remove keys when editing BigCommerce data.')

    fields_edited = dict(set(edited_value.items()) - set(value.items()))
    return fields_edited
