from prettytable import PrettyTable


class ProductVariants:
    @staticmethod
    def build_table(catalog_product_variants: list[dict]):
        table = PrettyTable()
        table.field_names = ['Variant ID', 'Label', 'Price', 'Sale Price']
        table.align['Label'] = "l"
        table.align['Price'] = "l"
        table.align['Sale Price'] = "l"

        for variant in catalog_product_variants:
            table.add_row([
                variant['id'],
                variant['option_values'][0]['label'],
                '{:,.2f}'.format(float(variant['price'] or 0)),
                '{:,.2f}'.format(float(variant['sale_price'] or 0)),
            ])
        return table
