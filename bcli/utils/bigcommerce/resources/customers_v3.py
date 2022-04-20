from ..base_resource import BaseResource


class CustomersV3(BaseResource):
    api_version: str = 'v3'
    subdir: str = 'customers'
