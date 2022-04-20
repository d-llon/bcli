from ..base_resource import BaseResource


class CustomersV2(BaseResource):
    api_version: str = 'v2'
    subdir: str = 'customers'
