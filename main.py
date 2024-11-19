from api_connection import ShoperAPIClient
import pandas as pd

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API
        client.connect()

        # Fetch and display products
        df = pd.DataFrame(client.get_all_products())
        df.to_excel('wszystkie_produkty.xlsx', index=False)

    except Exception as e:
        print(f"Error: {e}")
