from typing import Optional

import requests


class BigCommerceRequest:
    api_base: str
    headers: dict

    def __init__(self, store_hash, access_token):
        self.api_base = f'https://api.bigcommerce.com/stores/{store_hash}'
        self.headers = {'accept': 'application/json', 'x-auth-token': access_token}

    def get(self, api_version: str, subdir: str, resource_id: Optional[int] = None, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}'

        if resource_id:
            url = f'{url}/{resource_id}'

        response = requests.get(url, headers=self.headers, **kwargs)
        response.raise_for_status()

        if api_version == "v3":
            return response.json()['data']

        return response.json()

    def put(self, api_version: str, subdir: str, resource_id: int, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}/{resource_id}'

        response = requests.put(url, headers=self.headers, **kwargs)
        response.raise_for_status()

        if api_version == "v3":
            return response.json()['data']

        return response.json()
