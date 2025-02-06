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

# Jeśli chcecie zmienić arkusz do produktów powiązanych, to zróbcie nowego
# Google sheetsa i zmieńcie link do arkusza w zmiennej COMBINED_PRODUCTS_SHEET
# Arkusz musi mieć kolumny product_id oraz related_products
# related products w formie id produktów oddzielonych przecinkami

if __name__ == "__main__":
    client = ShoperAPIClient()

    try:
        # Authenticate with the Shoper API

        operation = str(input('''
Co chcesz zrobić?
1. Uzupełnić produkty powiązane.
2. Pobrać wszystkie produkty.\n'''))
        
        client.connect()

        if operation == '1':
            client.update_related_products(COMBINED_PRODUCTS_SHEET)
        elif operation == '2':
            product_df = pd.DataFrame(client.get_all_products())
            product_df.to_excel(os.path.join('sheets', 'All_products.xlsx'), index=False)
        else:
            print('Nieprawidłowa wartość wariacie')

    except Exception as e:
        print(f"Error: {e}")
