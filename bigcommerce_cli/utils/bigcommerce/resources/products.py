from ..base_resource import BaseResource


class Products(BaseResource):
    api_version: str = 'v3'
    subdir: str = 'catalog/products'
