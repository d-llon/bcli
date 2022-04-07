from typing import Optional

from .bigcommerce_request import BigCommerceRequest


class BaseSubresource:
    api_version: str
    subdir: str
    linking_subdir: str

    @classmethod
    def get(cls, resource_id: int, subresource_id: Optional[int] = None, **kwargs):
        bc_request = BigCommerceRequest()
        subresource_data = bc_request.get(api_version=cls.api_version,
                                          subdir=f'{cls.subdir}/{resource_id}/{cls.linking_subdir}',
                                          resource_id=subresource_id,
                                          **kwargs)
        return subresource_data
