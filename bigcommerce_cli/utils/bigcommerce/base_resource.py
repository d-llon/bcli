from abc import ABC
from typing import Optional

from .bigcommerce_request import BigCommerceRequest


class BaseResource(ABC):
    api_version: str
    subdir: str

    @classmethod
    def delete(cls, resource_id: int, **kwargs):
        bc_request = BigCommerceRequest()
        bc_request.delete(api_version=cls.api_version,
                          subdir=cls.subdir,
                          resource_id=resource_id,
                          **kwargs)

    @classmethod
    def get(cls, resource_id: Optional[int] = None, **kwargs):
        bc_request = BigCommerceRequest()
        resource_data = bc_request.get(api_version=cls.api_version,
                                       subdir=cls.subdir,
                                       resource_id=resource_id,
                                       **kwargs)
        return resource_data

    @classmethod
    def post(cls, **kwargs):
        bc_request = BigCommerceRequest()
        resource_data = bc_request.post(api_version=cls.api_version,
                                        subdir=cls.subdir,
                                        **kwargs)
        return resource_data

    @classmethod
    def put(cls, resource_id: int, **kwargs):
        bc_request = BigCommerceRequest()
        resource_data = bc_request.put(api_version=cls.api_version,
                                       subdir=cls.subdir,
                                       resource_id=resource_id,
                                       **kwargs)
        return resource_data
