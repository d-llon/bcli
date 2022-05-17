from typing import Optional

import requests

from ..utils import get_active_store


class BigCommerceRequest:
    api_base: str
    headers: dict

    def __init__(self):
        store = get_active_store()
        self.api_base = f'https://api.bigcommerce.com/stores/{store["store_hash"]}'
        self.headers = {'accept': 'application/json', 'x-auth-token': store['access_token']}

    def delete(self, api_version: str, subdir: str, resource_id: int, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}/{resource_id}'

        response = requests.delete(url, headers=self.headers, **kwargs)
        response.raise_for_status()

    def get(self, api_version: str, subdir: str, resource_id: Optional[int] = None, **kwargs):
        params = kwargs.pop('params', {})

        if resource_id:
            url = f'{self.api_base}/{api_version}/{subdir}/{resource_id}'
        else:
            url = f'{self.api_base}/{api_version}/{subdir}'
            params['page'] = 1

        response = requests.get(url, headers=self.headers, params=params, **kwargs)
        response.raise_for_status()

        if api_version == "v3":
            data = response.json()['data']
            meta = response.json()['meta']

            if meta.get('pagination'):
                while (current_page := meta['pagination']['current_page']) != meta['pagination']['total_pages']:
                    params['page'] = current_page + 1

                    response = requests.get(url, headers=self.headers, params=params, **kwargs)
                    response.raise_for_status()

                    data.extend(response.json()['data'])
                    meta = response.json()['meta']

            return data

        return response.json()

    def post(self, api_version: str, subdir: str, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}'

        response = requests.post(url, headers=self.headers, **kwargs)
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
