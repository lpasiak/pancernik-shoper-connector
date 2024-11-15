import requests
import os

LOGIN = os.environ.get('LOGIN')
PASSWORD = os.environ.get('PASSWORD')
SHOPERSITE = os.environ.get('SHOPERSITE')

# Connecting to Shoper REST API
shoper_session = requests.Session()
response = shoper_session.post(f'{SHOPERSITE}/webapi/rest/auth', auth=(LOGIN, PASSWORD))
token = response.json()['access_token']
shoper_session.headers.update({'Authorization': f'Bearer {token}'})




