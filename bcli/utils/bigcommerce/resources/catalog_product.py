from ..base_resource import BaseResource


class CatalogProduct(BaseResource):
    api_version: str = 'v3'
    subdir: str = 'catalog/products'
