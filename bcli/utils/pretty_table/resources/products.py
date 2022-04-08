from prettytable import PrettyTable


class Products:
    @staticmethod
    def build_table(catalog_products: list[dict]):
        table = PrettyTable()
        table.field_names = ['ID', 'Name', 'Price', 'Sale Price', 'Variants']
        table.align['Name'] = "l"
        table.align['Price'] = "l"
        table.align['Sale Price'] = "l"

        for cp in catalog_products:
            table.add_row([
                cp['id'],
                cp['name'],
                '{:,.2f}'.format(float(cp['price'])),
                '{:,.2f}'.format(float(cp['sale_price'])),
                '🟢' if len(cp['variants']) > 1 else '⚫️'
            ])
        return table
