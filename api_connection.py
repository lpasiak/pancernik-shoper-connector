import requests
import os


class ShoperAPIClient:

    def __init__(self):
        self.site_url = os.environ.get('SHOPERSITE')
        self.login = os.environ.get('LOGIN')
        self.password = os.environ.get('PASSWORD')
        self.session = requests.Session()  # Maintain a session
        self.token = None

    def connect(self):
        '''Authenticate with the API'''
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

    def get_all_products(self):
        '''Get all products using pagination and print the result'''
        products = []
        page = 1
        url = f'{self.site_url}/webapi/rest/products'

        while True:
            params = {'limit': 10, 'page': page}
            response = self.session.get(url, params=params)
            
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data: {response.status_code}, {response.text}")

            page_data = response.json().get('list', [])

            # If no data is returned
            if not page_data:
                break

            print(f'Page: {page}')
            products.extend(page_data)
            page += 1

        return products
