from ..base_resource import BaseResource


class Webhooks(BaseResource):
    api_version: str = 'v3'
    subdir: str = 'hooks'
