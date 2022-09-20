from typing import Optional

import requests
from click import ClickException

from ..utils import get_active_store


def raise_click_exception_for_status(response: requests.Response):
    """ Raises a ClickException for status codes between 400 and 600. """
    if 400 <= response.status_code < 600:
        message = f'BigCommerce exception ({response.status_code})'
        if title := response.json().get('title'):
            message = f'{message} \'{title}\''
        raise ClickException(message)


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
        raise_click_exception_for_status(response)

    def get(self, api_version: str, subdir: str, resource_id: Optional[int] = None, **kwargs):
        params = kwargs.pop('params', {})

        if resource_id:
            url = f'{self.api_base}/{api_version}/{subdir}/{resource_id}'
        else:
            url = f'{self.api_base}/{api_version}/{subdir}'
            params['page'] = params.get('page', 1)
            params['limit'] = params.get('limit', 250)

        response = requests.get(url, headers=self.headers, params=params, **kwargs)
        raise_click_exception_for_status(response)

        if api_version == 'v2':
            if not resource_id and response.status_code == 204:
                # If you are making a list request for a page without content
                return []

            return response.json()

        if api_version == "v3":
            data = response.json()['data']
            meta = response.json()['meta']

            if meta.get('pagination'):
                while (current_page := meta['pagination']['current_page']) < meta['pagination']['total_pages']:
                    params['page'] = current_page + 1

                    response = requests.get(url, headers=self.headers, params=params, **kwargs)
                    raise_click_exception_for_status(response)

                    data.extend(response.json()['data'])
                    meta = response.json()['meta']

            return data

    def post(self, api_version: str, subdir: str, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}'

        response = requests.post(url, headers=self.headers, **kwargs)
        raise_click_exception_for_status(response)

        if api_version == "v3":
            return response.json()['data']

        return response.json()

    def put(self, api_version: str, subdir: str, resource_id: int, **kwargs):
        url = f'{self.api_base}/{api_version}/{subdir}/{resource_id}'

        response = requests.put(url, headers=self.headers, **kwargs)
        raise_click_exception_for_status(response)

        if api_version == "v3":
            return response.json()['data']

        return response.json()
