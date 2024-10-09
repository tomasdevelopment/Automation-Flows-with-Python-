from ayx import Alteryx
import pandas as pd
import json
#to read alteryx
df = Alteryx.read("#1")

df['DownloadData_parsed'] = df['DownloadData'].apply(json.loads)

# Extract the 'data' field from the parsed JSON
df['data'] = df['DownloadData_parsed'].apply(lambda x: x.get('data', []))

# Flatten the nested 'data' field into its own DataFrame
data_flat = pd.json_normalize(df['data'].explode())

# Drop the original columns (optional) and keep the flattened 'data' columns
df_final = data_flat

#Add additional columns or filters to you data before actually loading it
#Remove trainees
df_final = df_final[~df_final['ProductCategory'].str.contains('beverages', case=False, na=False)]##remove trainees


#remove duplicated products by purhcase date
df_final = df_final.sort_values(by=['PurchaseDate'], ascending=[False]).drop_duplicates(subset='ProductId', keep='first')

#To write on alteryx
Alteryx.write(df_final,1)
