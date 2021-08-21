import requests
from typing import Optional
from urllib.parse import urljoin

def BigCommerceRequest():
    api_base: str
    headers: dict

    def __init__(self, store_hash, access_token):
        self.api_base = urljoin('https://api.bigcommerce.com/stores', f'/{store_hash}')
        self.headers = {'accept': 'application/json', 'x-auth-token': self.access_token}
        return self
    
    def get(api_version: str, subdir: str, resource_id: int, **kwargs)
        url = urljoin(self.api_base, f'/{api_version}/{subdir}/{resource_id}')
        response = requests.get(url, headers=self.headers, **kwargs)
        response.raise_for_status()

        if api_version == "v3":
            return response.json()['data']
            
        return response.json()
