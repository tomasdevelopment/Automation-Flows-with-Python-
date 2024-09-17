from ayx import Alteryx
import pandas as pd

# Step 1: Read incoming data from the S3 Download tool (or any other tool feeding data into this workflow)
df = Alteryx.read("#1")  # The input data is now in df

# Step 2: Define the datetime columns to be converted
datetime_cols = [
    'created ON',
    'submitted date',
   
]

# Step 3: Function to convert columns to datetime
def convert_to_datetime(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime('%Y-%m-%d')
            else:
                print(f"Column {col} could not be converted to datetime.")
        else:
            print(f"Column {col} not found in dataframe.")
    return df

# Step 4: Apply the datetime conversion
df = convert_to_datetime(df, datetime_cols)

# Step 5: Function to filter the dataframe
def filter_dataframe(df):
    # Standardize column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    # Ensure the required columns exist before filtering
    required_columns = ['client id', 'client product id', 'product reference','product type']
    if not all(col in df.columns for col in required_columns):
        print("Required columns are missing. Skipping this DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame

    # Filter the dataframe to include only the rows with the specified job HFM entity and client ID for 'US8424'
    df_main = df[(df['client id'] == '1231') | (df['client product id'] == '3344')]

    # Convert 'brand name' to lowercase for consistent comparison
    df['product reference'] = df['product reference'].str.lower()

    # Additional filtering for 'brand name' containing 'house' and 'project' containing '9th hour - PMX Center'
    df_edible = df[(df['product reference'].str.contains('house', na=False)) & 
                     (df[''product type''].str.contains('Edible', na=False))]

    # Combine both dataframes
    df_filtered = pd.concat([df_main, df_edible]).drop_duplicates()

    return df_filtered

# Step 6: Apply the filtering
df_filtered = filter_dataframe(df)

# Step 7: Write the transformed and filtered data back to Alteryx to pass it to the next tool (S3 Upload)
Alteryx.write(df_filtered, 3)

# Now, Alteryx will pass this data to the Amazon S3 Upload tool.
