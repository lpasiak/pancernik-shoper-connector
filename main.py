from api_connection import ShoperAPIClient
import pandas as pd

special_offer = {
    'discount': 10,
    'date_from': '2024-11-24 00:00:00',
    'date_to': '2026-01-01 00:00:00',
    'product_id': 10745,
    'discount_type': 2,
}

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API
        client.connect()

        client.create_special_offers(special_offer)

        # Fetch and display products
        # df = pd.DataFrame(client.get_all_special_offers_with_ean())
        # df.to_excel('wszystkie_produkty.xlsx', index=False)

    except Exception as e:
        print(f"Error: {e}")

