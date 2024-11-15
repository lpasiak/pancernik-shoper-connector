from api_connection import ShoperAPIClient
import pandas as pd
import os

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API
        client.connect()

        # Fetch and display products
        products = client.get_all_products()

        df = pd.DataFrame(products)
        print(df)
        df.to_excel('promocje.xlsx', index=None)


    except Exception as e:
        print(f"Error: {e}")
