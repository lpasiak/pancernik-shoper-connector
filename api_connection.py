from functions import clear_console
import pandas as pd
import requests
import os
import time
import config
from dotenv import load_dotenv

dotenv_path = os.path.join('credentials', 'env')
load_dotenv(dotenv_path)

class ShoperAPIClient:

    def __init__(self):
        self.site_url = os.getenv(f'SHOPERSITE_{config.SITE}')
        self.login = os.getenv(f'LOGIN_{config.SITE}')
        self.password = os.getenv(f'PASSWORD_{config.SITE}')
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
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            if not page_data:  # If no data is returned
                clear_console()
                break

            clear_console()
            print(f'Page: {page}/{number_of_pages}')
            products.extend(page_data)
            page += 1

        return products
    
    def get_all_categories(self):
        """Get all categories using pagination and print the result"""
        categories = []
        page = 1
        url = f'{self.site_url}/webapi/rest/categories'

        while True:
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
            response = self._handle_request('GET', url, params=params)
            data = response.json()
            number_of_pages = data['pages']

            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            if not page_data:
                clear_console()
                break
        
            clear_console()
            print(f'Page: {page}/{number_of_pages}')
            categories.extend(page_data)
            page += 1
        
        return categories

    def get_all_special_offers(self):
        """Get products only with special offers"""
        special_offers = []
        page = 1
        url = f'{self.site_url}/webapi/rest/specialoffers'

        while True:
            params = {'limit': config.SHOPER_LIMIT, 'page': page}
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

    def update_gpsr_info(self, gsheets):
        """Append GPSR producer ID to products"""
        gpsr_data = pd.read_csv(gsheets, header=None, skiprows=1)
        gpsr_data.columns = ['product_id', 'producer_id', 'gpsr_responsible_id', 'gpsr_certificates']
        result = gpsr_data.to_dict(orient='records')

        for item in result:
            product_id = item['product_id']
            producer_id = item["producer_id"]
            responsible_id = item["gpsr_responsible_id"]
            gpsr_certificates = item["gpsr_certificates"]

            # Build the data dictionary dynamically
            if pd.notna(producer_id):
                safety_info = {"gpsr_producer_id": producer_id}
            
            # Check if gpsr_responsible_id is not NaN, then add it
            if pd.notna(responsible_id):
                safety_info["gpsr_responsible_id"] = responsible_id

            if pd.notna(gpsr_certificates):
                safety_info["gpsr_certificates"] = [int(gpsr_certificates)]

            data = {"safety_information": safety_info}

            # Make the PUT request
            url = f'{self.site_url}/webapi/rest/products/{product_id}'
            response = self._handle_request('PUT', url, json=data)
            print(f'{product_id} producer_id set to {producer_id}, '
                f'producer_id set to {producer_id if pd.notna(producer_id) else "N/A"}, responsible_id set to {responsible_id}, certificates to {gpsr_certificates}.')

            if response.status_code != 200:
                print(f"Failed to update a product: {response.status_code}, {response.text}")

    def update_related_products(self, gsheets):
        """Update Recommended products in products"""
        product_data = pd.read_csv(gsheets)
        result = product_data.to_dict(orient='records')

        for item in result:
            product_id = item['product_id']
            related_products = item["related_products"]

            # Turn a string into an array of related products
            related_list = [int(num.strip()) for num in related_products.split(', ')]

            data = {"related": related_list}

            # Make the PUT request
            url = f'{self.site_url}/webapi/rest/products/{product_id}'
            response = self._handle_request('PUT', url, json=data)
            print(f'{product_id}: related products set to {data["related"]} ')

            if response.status_code != 200:
                print(f"Failed to update a product: {response.status_code}, {response.text}") 
                