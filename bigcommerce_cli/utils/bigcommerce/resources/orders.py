from typing import Optional

from ..base_resource import BaseResource
from ..bigcommerce_request import BigCommerceRequest


class Orders(BaseResource):
    api_version: str = 'v2'
    subdir: str = 'orders'

    @classmethod
    def get(cls, resource_id: Optional[int] = None, **kwargs):
        bc_request = BigCommerceRequest()
        if resource_id:
            resource_data = bc_request.get(api_version=cls.api_version,
                                           subdir=cls.subdir,
                                           resource_id=resource_id,
                                           **kwargs)
        else:
            # The v2 Orders API is one of the few paginated v2 API endpoints
            count_data = bc_request.get(api_version=cls.api_version,
                                        subdir=f'{cls.subdir}/count')
            count = count_data['count']

            resource_data = []
            page = 1
            while len(resource_data) < count:
                kwargs['params'] = kwargs.get('params', {}) | {'limit': 250, 'page': page}
                page_data = bc_request.get(api_version=cls.api_version,
                                           subdir=cls.subdir,
                                           **kwargs)
                resource_data.extend(page_data)
                page += 1

        return resource_data
