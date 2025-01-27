import pandas as pd

EXCEL = r'sheets\Atrybuty_dogrywka.xlsx'

# Load Excel sheets into dictionaries
df_shoper = pd.read_excel(EXCEL, sheet_name='Shoper', dtype='str')
dict_shoper = pd.DataFrame.to_dict(df_shoper, orient='records', index='False')

df_sheets = pd.read_excel(EXCEL, sheet_name='Gsheets', dtype='str')
dict_sheets = pd.DataFrame.to_dict(df_sheets, orient='records', index='False')

# Process data
all_products = []
metafield_headers = ['Grupy atrybutów', '', '_Outlet|577|pl_PL', 'Outlet|593|pl_PL']

for item_shoper in dict_shoper:
    ids_matching = []

    for item_sheets in dict_sheets:
        if item_shoper['ean'] == item_sheets['EAN']:
            ids_matching.append(item_sheets['ID Shoper'])

    product_dict = {
        'Kod produktu': item_shoper['ean'],
        'Nazwa Produktu': None,
        'ids': ids_matching,
        'Outlet|1538|select': '<nie dotyczy>'
    }
    all_products.append(product_dict)

# Convert to DataFrame
final_df = pd.DataFrame(all_products)

# Convert 'ids' column from list to comma-separated string
final_df['ids'] = final_df['ids'].apply(lambda x: ', '.join(map(str, x)))

# Rename 'ids' column
final_df.rename(columns={'ids': '_outlet|1402|text'}, inplace=True)

# Create a DataFrame for current headers as the second row and create new headers
headers_row = pd.DataFrame([final_df.columns], columns=final_df.columns)
final_df = pd.concat([headers_row, final_df], ignore_index=True)
final_df.columns = metafield_headers

# Save to Excel
final_df.to_excel('sheets\Atrybuty_Import.xlsx', index=False)
