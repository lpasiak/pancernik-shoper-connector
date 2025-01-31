from api_connection import ShoperAPIClient
import pandas as pd
import os

# special_offer = {
#     'discount': 10,
#     'date_from': '2024-12-13 00:00:00',
#     'date_to': '2026-01-01 00:00:00',
#     'product_id': 10753,
#     'discount_type': 2,
# }

GPSR_SHEET = 'https://docs.google.com/spreadsheets/d/1X_Rzj8QjdoBBrbeRKZHklExhWNOIlfGg_lfy8tGKu3k/export?format=csv'
COMBINED_PRODUCTS_SHEET = 'https://docs.google.com/spreadsheets/d/1X_Rzj8QjdoBBrbeRKZHklExhWNOIlfGg_lfy8tGKu3k/export?format=csv&gid=8734097'

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API
        client.connect()

        # == Update GPSR info == #
        client.update_gpsr_info(GPSR_SHEET)

        # == Update Recommended products == #
        # client.update_related_products(COMBINED_PRODUCTS_SHEET)
        
        # == Create a promo offer == #
        # client.create_special_offers(special_offer)

        # == Fetch and display products == #
        # product_df = pd.DataFrame(client.get_all_products())
        # product_df.to_excel(os.path.join('sheets', 'All_products.xlsx'), index=False)

        # category_df = pd.DataFrame(client.get_all_categories())
        # category_df.to_excel('sheets\All_categories.xlsx', index=False)
        # print(category_df)

    except Exception as e:
        print(f"Error: {e}")
