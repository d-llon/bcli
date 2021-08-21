from typing import Optional

from .bigcommerce_request import BigCommerceRequest


class BaseResource:
    api_version: str
    subdir: str

    @classmethod
    def get(cls, store_hash: str, access_token: str, resource_id: Optional[int] = None, **kwargs):
        bc_request = BigCommerceRequest(store_hash=store_hash, access_token=access_token)
        resource_data = bc_request.get(api_version=cls.api_version, subdir=cls.subdir,
                                       resource_id=resource_id, **kwargs)
        return resource_data
