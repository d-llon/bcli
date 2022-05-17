from abc import ABC
from typing import Optional

from .bigcommerce_request import BigCommerceRequest


class BaseSubresource(ABC):
    api_version: str
    subdir: str
    linking_subdir: str

    @classmethod
    def delete(cls, resource_id: int, subresource_id: int, **kwargs):
        bc_request = BigCommerceRequest()
        bc_request.delete(api_version=cls.api_version,
                          subdir=f'{cls.subdir}/{resource_id}/{cls.linking_subdir}',
                          resource_id=subresource_id,
                          **kwargs)

    @classmethod
    def get(cls, resource_id: int, subresource_id: Optional[int] = None, **kwargs):
        bc_request = BigCommerceRequest()
        subresource_data = bc_request.get(api_version=cls.api_version,
                                          subdir=f'{cls.subdir}/{resource_id}/{cls.linking_subdir}',
                                          resource_id=subresource_id,
                                          **kwargs)
        return subresource_data

    @classmethod
    def post(cls, resource_id: int, **kwargs):
        bc_request = BigCommerceRequest()
        subresource_data = bc_request.get(api_version=cls.api_version,
                                          subdir=f'{cls.subdir}/{resource_id}/{cls.linking_subdir}',
                                          **kwargs)
        return subresource_data

    @classmethod
    def put(cls, resource_id: int, subresource_id: int, **kwargs):
        bc_request = BigCommerceRequest()
        subresource_data = bc_request.put(api_version=cls.api_version,
                                          subdir=f'{cls.subdir}/{resource_id}/{cls.linking_subdir}',
                                          resource_id=subresource_id,
                                          **kwargs)
        return subresource_data
