from api_connection import ShoperAPIClient
import pandas as pd
import os

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API
        client.connect()

        # Fetch and display products
        df = client.get_all_special_offers_with_code()
        df.to_excel('wszystko.xlsx', index=False)

    except Exception as e:
        print(f"Error: {e}")

