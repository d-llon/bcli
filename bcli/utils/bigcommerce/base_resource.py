from .bigcommerce import BigCommerceRequest

class BaseResource():
    api_version: str 
    subdir: str

    class get(resource_id: str, **kwargs):
        bc_request = BigCommerceRequest()
        resource_data = bc_request.get(api_version=self.api_version, subdir=self.subdir, 
                                       resource_id=resource_id **kwargs)
        return resource_data
