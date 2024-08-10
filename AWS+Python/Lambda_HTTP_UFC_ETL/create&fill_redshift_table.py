
import pandas as pd
import boto3
import redshift_connector
import os
import requests
from io import BytesIO
import datetime

# AWS credentials
S3_BUCKET_NAME = 'your-bucket-collectionname'
FOLDER_PREFIX = '/datasets/amazon-s3/Bucket-Subfolder/'


# Redshift connection details
host = os.getenv('REDSHIFT_HOST')
database = os.getenv('REDSHIFT_DATABASE')
username = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
port = int(os.getenv('REDSHIFT_PORT', 5439))  # Default Redshift port is 5439

# Function to read Excel file from S3 path
def read_excel_from_s3(file_path):
    return pd.read_csv(file_path)

# Function to list files in S3 path
def list_files_in_s3(s3_path):
    return [f for f in os.listdir(s3_path) if f.endswith('.csv')]

# Collect all DataFrames into a list

excel_files = list_files_in_s3(FOLDER_PREFIX)
print(excel_files)
for file in excel_files:
    file_path = os.path.join(FOLDER_PREFIX, file)
    print(file_path)
    df = read_excel_from_s3(file_path)
    # Example usage
    table_name = 'ufc_df'
    print(df.head())


# Prepare DataFrame by ensuring correct data types
def prepare_data(df):
    # Specify data type conversions for all columns
    type_conversions = {
        # Float columns
        'B_avg_KD': float,
        'B_avg_opp_KD': float,
        'B_avg_SIG_STR_pct': float,
        'B_avg_opp_SIG_STR_pct': float,
        'B_avg_TD_pct': float,
        'B_avg_opp_TD_pct': float,
        'B_avg_SUB_ATT': float,
        'B_avg_opp_SUB_ATT': float,
        'B_avg_REV': float,
        'B_avg_opp_REV': float,
        'B_avg_SIG_STR_att': float,
        'B_avg_SIG_STR_landed': float,
        'B_avg_opp_SIG_STR_att': float,
        'B_avg_opp_SIG_STR_landed': float,
        'B_avg_TOTAL_STR_att': float,
        'B_avg_TOTAL_STR_landed': float,
        'B_avg_opp_TOTAL_STR_att': float,
        'B_avg_opp_TOTAL_STR_landed': float,
        'B_avg_TD_att': float,
        'B_avg_TD_landed': float,
        'B_avg_opp_TD_att': float,
        'B_avg_opp_TD_landed': float,
        'B_avg_HEAD_att': float,
        'B_avg_HEAD_landed': float,
        'B_avg_opp_HEAD_att': float,
        'B_avg_opp_HEAD_landed': float,
        'B_avg_BODY_att': float,
        'B_avg_BODY_landed': float,
        'B_avg_opp_BODY_att': float,
        'B_avg_opp_BODY_landed': float,
        'B_avg_LEG_att': float,
        'B_avg_LEG_landed': float,
        'B_avg_opp_LEG_att': float,
        'B_avg_opp_LEG_landed': float,
        'B_avg_DISTANCE_att': float,
        'B_avg_DISTANCE_landed': float,
        'B_avg_opp_DISTANCE_att': float,
        'B_avg_opp_DISTANCE_landed': float,
        'B_avg_CLINCH_att': float,
        'B_avg_CLINCH_landed': float,
        'B_avg_opp_CLINCH_att': float,
        'B_avg_opp_CLINCH_landed': float,
        'B_avg_GROUND_att': float,
        'B_avg_GROUND_landed': float,
        'B_avg_opp_GROUND_att': float,
        'B_avg_opp_GROUND_landed': float,
        'B_avg_CTRL_time(seconds)': float,
        'B_avg_opp_CTRL_time(seconds)': float,
        'B_total_time_fought(seconds)': float,
        'B_total_rounds_fought': float,
        'B_total_title_bouts': float,
        'B_current_win_streak': float,
        'B_current_lose_streak': float,
        'B_longest_win_streak': float,
        'B_wins': float,
        'B_losses': float,
        'B_draw': float,
        'B_win_by_Decision_Majority': float,
        'B_win_by_Decision_Split': float,
        'B_win_by_Decision_Unanimous': float,
        'B_win_by_KO/TKO': float,
        'B_win_by_Submission': float,
        'B_win_by_TKO_Doctor_Stoppage': float,
        'R_avg_KD': float,
        'R_avg_opp_KD': float,
        'R_avg_SIG_STR_pct': float,
        'R_avg_opp_SIG_STR_pct': float,
        'R_avg_TD_pct': float,
        'R_avg_opp_TD_pct': float,
        'R_avg_SUB_ATT': float,
        'R_avg_opp_SUB_ATT': float,
        'R_avg_REV': float,
        'R_avg_opp_REV': float,
        'R_avg_SIG_STR_att': float,
        'R_avg_SIG_STR_landed': float,
        'R_avg_opp_SIG_STR_att': float,
        'R_avg_opp_SIG_STR_landed': float,
        'R_avg_TOTAL_STR_att': float,
        'R_avg_TOTAL_STR_landed': float,
        'R_avg_opp_TOTAL_STR_att': float,
        'R_avg_opp_TOTAL_STR_landed': float,
        'R_avg_TD_att': float,
        'R_avg_TD_landed': float,
        'R_avg_opp_TD_att': float,
        'R_avg_opp_TD_landed': float,
        'R_avg_HEAD_att': float,
        'R_avg_HEAD_landed': float,
        'R_avg_opp_HEAD_att': float,
        'R_avg_opp_HEAD_landed': float,
        'R_avg_BODY_att': float,
        'R_avg_BODY_landed': float,
        'R_avg_opp_BODY_att': float,
        'R_avg_opp_BODY_landed': float,
        'R_avg_LEG_att': float,
        'R_avg_LEG_landed': float,
        'R_avg_opp_LEG_att': float,
        'R_avg_opp_LEG_landed': float,
        'R_avg_DISTANCE_att': float,
        'R_avg_DISTANCE_landed': float,
        'R_avg_opp_DISTANCE_att': float,
        'R_avg_opp_DISTANCE_landed': float,
        'R_avg_CLINCH_att': float,
        'R_avg_CLINCH_landed': float,
        'R_avg_opp_CLINCH_att': float,
        'R_avg_opp_CLINCH_landed': float,
        'R_avg_GROUND_att': float,
        'R_avg_GROUND_landed': float,
        'R_avg_opp_GROUND_att': float,
        'R_avg_opp_GROUND_landed': float,
        'R_avg_CTRL_time(seconds)': float,
        'R_avg_opp_CTRL_time(seconds)': float,
        'R_total_time_fought(seconds)': float,
        'R_total_rounds_fought': float,
        'R_total_title_bouts': float,
        'R_current_win_streak': float,
        'R_current_lose_streak': float,
        'R_longest_win_streak': float,
        'R_wins': float,
        'R_losses': float,
        'R_draw': float,
        'R_win_by_Decision_Majority': float,
        'R_win_by_Decision_Split': float,
        'R_win_by_Decision_Unanimous': float,
        'R_win_by_KO/TKO': float,
        'R_win_by_Submission': float,
        'R_win_by_TKO_Doctor_Stoppage': float,
        'B_Height_cms': float,
        'B_Reach_cms': float,
        'B_Weight_lbs': float,
        'R_Height_cms': float,
        'R_Reach_cms': float,
        'R_Weight_lbs': float,
        'B_age': float,
        'R_age': float,
        # String columns
        'R_Stance': str,
        'B_Stance': str,
        'weight_class':str
    }

    for col, dtype in type_conversions.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
    
    # Format datetime columns
    datetime_cols = ['date']
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df


# Function to map pandas data types to SQL data types
def map_pandas_dtype_to_sql(dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return 'BIGINT' if dtype == 'int64' else 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'VARCHAR(255)'  # Convert datetime columns to string for Redshift
    else:
        return 'VARCHAR(255)'

# Function to check if table exists in Redshift
def check_table_exists(table_name):
    with redshift_connector.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            port=port) as conn:
        cursor = conn.cursor()
        query = f"""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name = '{table_name}'
        );
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0]

# Function to create a table in Redshift
def create_redshift_table(df, table_name):
    with redshift_connector.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            port=port) as conn:
        cursor = conn.cursor()

        # Generate CREATE TABLE statement
        columns = ",\n".join(
            '"{}" {}'.format(col, map_pandas_dtype_to_sql(df[col].dtype)) for col in df.columns
        )
        create_table_sql = f"""
        CREATE TABLE {table_name} (
            {columns}
        );
        """
        cursor.execute(create_table_sql)
        conn.commit()

def format_sql_value(value):
    if pd.isnull(value):
        return 'NULL'
    elif isinstance(value, str):
        return "'{}'".format(value.replace("'", "''"))
    elif isinstance(value, (pd.Timestamp, datetime.datetime, datetime.date)):
        return "'{}'".format(value.strftime('%Y-%m-%d %H:%M:%S'))
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return "'{}'".format(value)

def replace_data_in_redshift(df, table_name):
    with redshift_connector.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            port=port
    ) as conn:
        cursor = conn.cursor()

        # Truncate table before inserting new data
        cursor.execute(f"TRUNCATE TABLE {table_name};")

        # Insert data in batches
        batch_size = 1000  # Adjust batch size as needed
        cols = ', '.join(['"{}"'.format(i) for i in df.columns.tolist()])

        for i in range(0, len(df), batch_size):
            batch_df = df.iloc[i:i + batch_size]
            values = [
                '(' + ', '.join(map(format_sql_value, row)) + ')'
                for _, row in batch_df.iterrows()
            ]
            values_sql = ',\n'.join(values)

            # Ensure values_sql is not empty
            if values_sql.strip():
                insert_query = f"""
                INSERT INTO {table_name} ({cols})
                VALUES {values_sql};
                """

                try:
                    cursor.execute(insert_query)
                except redshift_connector.ProgrammingError as e:
                    print(f"Error executing query: {e}")
                    print(insert_query)
                    raise

        conn.commit()

# Main script execution
if __name__ == '__main__':
    table_name = 'ufc_db'
    
    # Ensure table exists before trying to upsert data
    if not check_table_exists(table_name):
        create_redshift_table(df, table_name)
        print(f"Table structure for {table_name} created in Redshift.")
    else:
        print(f"Table {table_name} already exists in Redshift.")
    
    # Upsert data into Redshift
    replace_data_in_redshift(df, table_name)
    print(f"Data upserted into {table_name} in Redshift.")

   
