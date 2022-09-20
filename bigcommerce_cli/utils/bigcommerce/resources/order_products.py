from ..base_subresource import BaseSubresource


class OrderProducts(BaseSubresource):
    api_version: str = 'v2'
    subdir: str = 'orders'
    linking_subdir: str = 'products'
