from functions import clear_console
import pandas as pd
import requests
import os
import time


class ShoperAPIClient:

    def __init__(self):
        self.site_url = os.environ.get('SHOPERSITE')
        self.login = os.environ.get('LOGIN')
        self.password = os.environ.get('PASSWORD')
        self.session = requests.Session()  # Maintain a session
        self.token = None

    def connect(self):
        """Authenticate with the API"""
        response = self.session.post(
            f'{self.site_url}/webapi/rest/auth',
            auth=(self.login, self.password)
        )

        if response.status_code == 200:
            self.token = response.json().get('access_token')
            self.session.headers.update({'Authorization': f'Bearer {self.token}'})
            print("Authentication successful.")
        else:
            raise Exception(f"Authentication failed: {response.status_code}, {response.text}")

    def _handle_request(self, method, url, **kwargs):
        """Handle API requests with automatic retry on 429 errors."""
        while True:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 429:  # Too Many Requests
                retry_after = int(response.headers.get('Retry-After', 1))
                print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
            else:
                return response

    def get_all_products(self):
        """Get all products using pagination and print the result"""
        products = []
        page = 1
        url = f'{self.site_url}/webapi/rest/products'

        while True:
            params = {'limit': 50, 'page': page}
            response = self._handle_request('GET', url, params=params)

            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                clear_console()
                break

            clear_console()
            print(f'Page: {page}')
            products.extend(page_data)
            page += 1

        return products

    def get_all_special_offers(self):
        """Get products only with special offers"""
        special_offers = []
        page = 1
        url = f'{self.site_url}/webapi/rest/specialoffers'

        while True:
            params = {'limit': 50, 'page': page}
            response = self._handle_request('GET', url, params=params)

            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                clear_console()
                break

            clear_console()
            print(f'Page: {page}')
            special_offers.extend(page_data)
            page += 1

        return special_offers

    def get_all_special_offers_with_ean(self):
        """Get all special offers with an EAN column beside."""
        products = self.get_all_products()
        special_offers = self.get_all_special_offers()

        df_products = pd.DataFrame(products)
        df_special_offers = pd.DataFrame(special_offers)

        df = pd.merge(df_special_offers, df_products, on="product_id")
        code_column = df.pop('code')
        df.insert(0, 'code', code_column)
        id_column = df.pop('product_id')
        df.insert(0, 'product_id', id_column)

        return df

    def create_special_offers(self, special_offer):
        """Create a special offer"""
        url = f'{self.site_url}/webapi/rest/specialoffers'
        response = self._handle_request('POST', url, json=special_offer)

        if response.status_code != 200:
            raise Exception(f"Failed to create special offer: {response.status_code}, {response.text}")

        return response
