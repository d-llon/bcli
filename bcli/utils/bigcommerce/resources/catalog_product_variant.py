from ..base_subresource import BaseSubresource


class CatalogProductVariant(BaseSubresource):
    api_version: str = 'v3'
    subdir: str = 'catalog/products'
    linking_subdir: str = 'variants'
