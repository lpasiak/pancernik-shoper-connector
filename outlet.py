import pandas as pd

EXCEL = 'atrybuty_dogrywka.xlsx'

df_shoper = pd.read_excel(EXCEL, sheet_name='Shoper', dtype='str')
dict_shoper = pd.DataFrame.to_dict(df_shoper, orient='records', index='False')

df_sheets = pd.read_excel(EXCEL, sheet_name='Gsheets', dtype='str')
dict_sheets = pd.DataFrame.to_dict(df_sheets, orient='records', index='False')

# I converted dfs into dictionaries because It's easier for me to work on

all_products = []

# {'OUT' : [product_id, product_id2, product_id3...]}

# loop through shoper, then sheets and append ids
for item_shoper in dict_shoper:
    ids_matching = []

    for item_sheets in dict_sheets:

        if item_shoper['ean'] == item_sheets['EAN']:
            ids_matching.append(item_sheets['ID Shoper'])

    product_dict = {'sku': item_shoper['ean'], 'ids': ids_matching}
    all_products.append(product_dict)

final_df = pd.DataFrame(all_products)
print(final_df)
final_df.to_excel('ids.xlsx')
