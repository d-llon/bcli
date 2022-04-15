from ..base_resource import BaseResource


class Customers(BaseResource):
    api_version: str = 'v3'
    subdir: str = 'customers'
