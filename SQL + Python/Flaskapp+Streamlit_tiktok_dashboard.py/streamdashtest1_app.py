import requests
import pandas as pd
import streamlit as st
import json
from datetime import datetime, date
import plost
from streamlit_echarts import st_echarts, JsCode
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
import hydralit_components as hc
import os
import openai
from dotenv import load_dotenv
import pydeck as pdk

country_coords = {
    'United States': [37.0902, -95.7129],
    'Canada': [56.1304, -106.3468],
    'Mexico': [23.6345, -102.5528],
    'Colombia': [4.5709, -74.2973],
    'Chile': [-35.6751, -71.5430],
    'Costa Rica': [9.7489, -83.7534],
    'Argentina': [-38.4161, -63.6167],
    'Bolivia': [-16.2902, -63.5887],
    'Ecuador': [-1.8312, -78.1834],
    'Spain': [40.4637, -3.7492],
    'Guatemala': [15.7835, -90.2308],
    'Peru': [-9.19, -75.0152],
    'Venezuela': [6.4238, -66.5897],
    # Add more countries and their coordinates as needed
}


# Constants for API access
load_dotenv()
api_key ='123'
BASE_URL = 'http://tomasdev.pythonanywhere.com'
openai.api_key = api_key
SECURITY_TOKEN = '123'
##GPT FUNCTIONS
# Chatbot utility functions
def dataframe_to_text(df):
    if isinstance(df, pd.DataFrame):
        return df.to_string(index=False)
    return "No data available for the selected dataset."

def chat_gpt_generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # or another suitable model
            messages=[{'role': 'system', 'content': prompt}]
        )
        return response.choices[0].message.content if response.choices else "No response."
    except Exception as e:
        return f"Error in generating response: {e}"

def ask_chatgpt_about_data(query, data_as_text):
    prompt = f"Here is the data:\n{data_as_text}\n\nUser's question: {query}\nAnswer:"
    response = chat_gpt_generate_response(prompt)
    return response

           ##visual funcitions

def convert_df_to_echarts_data(df, value_col, name_col):
    return df.apply(lambda row: {"value": row[value_col], "name": row[name_col]}, axis=1).tolist()

# Function to filter data by date
def filter_data_by_date(dataframe, start_date, end_date):
    """Filters the DataFrame to include data between the start and end dates."""
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    return dataframe[(dataframe['date'] >= start_date) & (dataframe['date'] <= end_date)]

def display_metrics(data):
    if isinstance(data, pd.Series):
        # Convert the Series to a dictionary, ensuring all values are strings
        data = data.to_dict()
    
    with st.container():
        html_str = ""
        
        for label, value in data.items():
            # Ensure value is of a type accepted by HTML (i.e., convert to string)
            if not isinstance(value, (int, float, str, type(None))):
                value = str(value)
            
            # Create a HTML string for each metric
            # Styling can be adjusted as needed
            html_str += f"<div style='display:inline-block; padding:10px;'><h2>{label.replace('_', ' ').title()}</h2><h3>{value}</h3></div>"
        
        # Display the HTML in the container
        st.markdown(html_str, unsafe_allow_html=True)
def compile_datasets():
    datasets = {
        'Metrics_Daily_Tiktok': st.session_state.metrics_data['Metrics_Daily_Tiktok'] if 'metrics_data' in st.session_state else pd.DataFrame(),
        'Organic_Tiktok_Data': st.session_state.organic_data if 'organic_data' in st.session_state else pd.DataFrame(),
        'Video_Data': st.session_state.video_data if 'video_data' in st.session_state else pd.DataFrame(),
        'Users_Data': st.session_state.users_data['gender_data'] if 'users_data' in st.session_state else pd.DataFrame(),
        'Country_Data': st.session_state.users_data['country_data'] if 'users_data' in st.session_state else pd.DataFrame()
    }
    return datasets

# Define the Streamlit app
def streamlit_app():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    st.sidebar.header('TomasDevelopment `Dashboard`')
    st.title('TikTok Organic Dashboard')
    company = st.text_input('Enter Company Name')
    
    if 'company_name' not in st.session_state or st.session_state.company_name != company:
        st.session_state.company_name = company
    fetch_button_clicked = st.sidebar.button('Fetch TikTok Data')

    # Chatbot setup
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", "content": "How can I help you?"}]
    
    if fetch_button_clicked or not st.session_state.get('data_fetched', False):
        st.session_state.metrics_data = fetch_tiktok_data(BASE_URL, SECURITY_TOKEN, company)
        st.session_state.organic_data = fetch_tiktok_organic_data(BASE_URL, SECURITY_TOKEN, company)
        st.session_state.video_data = get_tiktok_video_data(company)
        st.session_state.users_data = fetch_tiktok_data(BASE_URL, SECURITY_TOKEN, company)  
        st.session_state.data_fetched = True
        st.session_state['animate_chart'] = True  # Set the animation flag

        st.sidebar.markdown(f'''
        ---
        Tailor Made for `{company}` ⚡.
        ''')
                                     #reset animation
    if st.sidebar.button('Reset Animation'):
        st.session_state['animate_chart'] = False



    if 'data_fetched' in st.session_state and 'metrics_data' in st.session_state and st.session_state.metrics_data is not None:
        metrics_display_data = st.session_state.metrics_data['Metrics_Daily_Tiktok']
        metrics_display_data['date'] = pd.to_datetime(metrics_display_data['date']).dt.date

        if 'audience_activity' in metrics_display_data.columns:
            metrics_display_data = metrics_display_data.drop(columns=['audience_activity'])
            metrics_display_data = metrics_display_data.set_index('date')
            min_date = metrics_display_data.index.min()
            max_date = metrics_display_data.index.max()
        
        if 'organic_data' in st.session_state and st.session_state.organic_data is not None:
            st.write("Organic General TikTok Data:")
            follower_count = st.session_state.organic_data.loc['follower_count', 'user']
            following_count = st.session_state.organic_data.loc['following_count', 'user']
            likes_count = st.session_state.organic_data.loc['likes_count', 'user']
            open_id = st.session_state.organic_data.loc['open_id', 'user']
            username = st.session_state.organic_data.loc['username', 'user']
            video_count = st.session_state.organic_data.loc['video_count', 'user']
            
            dark_theme_good = {'bgcolor': '#2E2E2E', 'title_color': 'lightgreen', 'content_color': 'lightgreen', 'icon_color': 'lightgreen', 'icon': 'fa fa-check-circle'}
            dark_theme_neutral = {'bgcolor': '#2E2E2E', 'title_color': 'lightblue', 'content_color': 'lightblue', 'icon_color': 'lightblue', 'icon': 'fa fa-question-circle'}
            dark_theme_bad = {'bgcolor': '#2E2E2E', 'title_color': 'red', 'content_color': 'red', 'icon_color': 'red', 'icon': 'fa fa-times-circle'}

            cc = st.columns(4)

            with cc[0]:
                hc.info_card(title='Follower Count', content=follower_count, sentiment='good', theme_override=dark_theme_good)
            with cc[0]:
                hc.info_card(title='Likes Count', content=likes_count, sentiment='good', theme_override=dark_theme_good)
            with cc[0]:
                hc.info_card(title='Following Count', content=following_count, sentiment='bad', theme_override=dark_theme_bad)
            with cc[1]:
                hc.info_card(title='Open ID', content=open_id, sentiment='neutral', theme_override=dark_theme_neutral)
            with cc[1]:
                hc.info_card(title='Username', content=username, sentiment='neutral', theme_override=dark_theme_good)
            with cc[1]:
                hc.info_card(title='Video Count', content=video_count, sentiment='good', theme_override=dark_theme_good)
            with cc[2]:
                if 'users_data' in st.session_state and st.session_state.users_data is not None:
                    users_data = st.session_state.users_data
                    gender_data_reset = users_data['gender_data'].reset_index()

                    gender_chart_data = convert_df_to_echarts_data(gender_data_reset, 'percentage', 'gender')

                    options2 = {
                        "tooltip": {"trigger": "item"},
                        "legend": {"top": "5%", "left": "center",
                                    "textStyle": {"color": "#ffffff"}},
                        "series": [
                            {
                                "name": "Audience Gender Distribution",
                                "type": "pie",
                                "radius": ["40%", "70%"],
                                "avoidLabelOverlap": False,
                                "itemStyle": {
                                    "borderRadius": 10,
                                    "borderColor": "#fff",
                                    "borderWidth": 2,
                                },
                                "label": {"show": False, "position": "center"},
                                "emphasis": {
                                    "label": {"show": True, "fontSize": "20", "fontWeight": "bold"}
                                },
                                "labelLine": {"show": False},
                                "data": gender_chart_data,
                            }
                        ],
                    }
                    st_echarts(options=options2, height="500px")
            
            st.sidebar.subheader("Filter Profile Data by Date")
            if 'metrics_start_date' not in st.session_state:
                st.session_state.metrics_start_date = min_date
            if 'metrics_end_date' not in st.session_state:
                st.session_state.metrics_end_date = max_date
            
            metrics_start_date = st.sidebar.date_input('Start date', st.session_state.metrics_start_date, key='metrics_start_date')
            metrics_end_date = st.sidebar.date_input('End date', st.session_state.metrics_end_date, key='metrics_end_date')
            
            filtered_metrics_data = metrics_display_data.loc[metrics_start_date:metrics_end_date]
            filtered_metrics_data2 = filtered_metrics_data.reset_index()
            
            filtered_metrics_data2['date'] = pd.to_datetime(filtered_metrics_data2['date'])
            filtered_metrics_data2['date'] = filtered_metrics_data2['date'].dt.strftime('%Y-%m-%d')
            plost.area_chart(
                data=filtered_metrics_data2,
                x='date',
                y='video_views',
                color={'video_views': '#223344'},
                opacity=0.8,
                title='Video Views Over Time',
                stack=False
            )

            animation_duration = 10000 if st.session_state.get('animate_chart', False) else 0

            options = {
                "animationDuration": animation_duration,
                "dataset": {
                    "source": filtered_metrics_data2.to_dict('list'),
                    "dimensions": ['date', 'likes', 'comments', 'profile_views', 'shares', 'followers_count']
                },
                "tooltip": {
                    "trigger": 'axis',
                    "axisPointer": {
                        "type": 'cross'
                    }
                },
                "xAxis": {
                    "type": 'category',
                    "name": 'Date',
                },
                "yAxis": {
                    "type": 'value',
                    "name": 'Count'
                },
                "series": [
                    {
                        "type": 'line',
                        "seriesLayoutBy": 'row',
                        "name": "Likes",
                        "showSymbol": False,
                        "emphasis": {"focus": "series"},
                        "endLabel": {
                            "show": True,
                            "formatter": JsCode("function(params) { return params.seriesName + ': ' + params.value[1]; }").js_code
                        }
                    },
                    {
                        "type": 'line',
                        "seriesLayoutBy": 'row',
                        "name": "Comments",
                        "showSymbol": False,
                        "emphasis": {"focus": "series"},
                        "endLabel": {
                            "show": True,
                            "formatter": JsCode("function(params) { return params.seriesName + ': ' + params.value[2]; }").js_code
                        }
                    },
                    {
                        "type": 'line',
                        "seriesLayoutBy": 'row',
                        "name": "Profile Views",
                        "showSymbol": False,
                        "emphasis": {"focus": "series"},
                        "endLabel": {
                            "show": True,
                            "formatter": JsCode("function(params) { return params.seriesName + ': ' + params.value[3]; }").js_code
                        }
                    },
                    {
                        "type": 'line',
                        "seriesLayoutBy": 'row',
                        "name": "Shares",
                        "showSymbol": False,
                        "emphasis": {"focus": "series"},
                        "endLabel": {
                            "show": True,
                            "formatter": JsCode("function(params) { return params.seriesName + ': ' + params.value[4]; }").js_code
                        }
                    },
                    {
                        "type": 'line',
                        "seriesLayoutBy": 'row',
                        "name": "Followers Count",
                        "showSymbol": False,
                        "emphasis": {"focus": "series"},
                        "endLabel": {
                            "show": True,
                            "formatter": JsCode("function(params) { return params.seriesName + ': ' + params.value[5]; }").js_code
                        }
                    }
                ],
                "title": {"text": "Likes, Comments, Profile Views, Shares, and Followers Count Over Time"}
            }

            st_echarts(options=options, height="800px")
            ccalternate = st.columns(3)
            with ccalternate[0]:

                st.write("Filtered Profile KPI by Day:")
                st.dataframe(filtered_metrics_data)
            if 'Organic_Tiktok_Data' in users_data:
                users_data['Organic_Tiktok_Data']['date'] = pd.to_datetime(users_data['Organic_Tiktok_Data']['date']).dt.date
                filtered_profile_data = users_data['Organic_Tiktok_Data'].set_index('date').loc[metrics_start_date:metrics_end_date]
                with ccalternate[1]:
                    st.write("Filtered Profile KPI by Hour:")
                    st.dataframe(filtered_profile_data)
            with ccalternate[2]:
                st.write("Audience Data:")
                #st.dataframe(users_data['country_data'])    # mp meeded caise we nio;t tje ,a[]

                # Map country names to their coordinates
                country_data = users_data['country_data'].reset_index()
                country_data['coordinates'] = country_data['Country'].map(country_coords)

                # Drop rows with missing coordinates
                country_data = country_data.dropna(subset=['coordinates'])

                # Split the coordinates into separate latitude and longitude columns
                country_data['lat'] = country_data['coordinates'].apply(lambda x: x[0])
                country_data['lon'] = country_data['coordinates'].apply(lambda x: x[1])

                # Create a DataFrame for the map
                df_map = pd.DataFrame({
                    'lat': country_data['lat'],
                    'lon': country_data['lon']
                })

                st.map(df_map)
      
        if 'video_data' in st.session_state and st.session_state.video_data is not None:
            video_data = st.session_state.video_data
            if video_data:
                video_info, audience_countries = extract_nested_data(video_data, 'audience_countries', ['audience_countries', 'impression_sources'], ['create_time', 'share_url', 'thumbnail_url', 'caption'])
                _, impression_sources = extract_nested_data(video_data, 'impression_sources', [], ['create_time', 'share_url', 'thumbnail_url', 'caption'])
            
                if video_info is not None and not video_info.empty:
                   
                        
                   st.write("Video Data:")
                   video_info = video_info.set_index('create_time')
                   st.dataframe(video_info)
                else:
                    st.error("No video data available.")

                if audience_countries is not None and not audience_countries.empty:
                    st.write("Audience Countries:")
                    audience_countries = audience_countries.set_index('create_time')
                    st.dataframe(audience_countries)
                else:
                    st.error("No audience country data available.")

                if impression_sources is not None and not impression_sources.empty:
                    st.write("Impression Sources:")
                    impression_sources = impression_sources.set_index('create_time')
                    st.dataframe(impression_sources)
                else:
                    st.error("No impression source data available.")
        
        else:
            if fetch_button_clicked:
                st.error("Failed to fetch or process video data.")
        datasets = compile_datasets()

    # Chatbot interaction after data fetching
    if 'data_fetched' in st.session_state:
        st.header("💬 Chatbot")

        dataset_keys = list(datasets.keys())
        selected_dataset = st.selectbox("Select a dataset to query", dataset_keys)
    
        # Add a button to submit the selected dataset
        if 'selected_dataset' not in st.session_state:
            st.session_state.selected_dataset = None

        if st.button("Submit Dataset"):
            st.session_state.selected_dataset = selected_dataset

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if st.session_state.selected_dataset:
            if prompt := st.chat_input("Ask the chatbot about your data..."):
                if not openai_api_key:
                    st.info("Please add your OpenAI API key to continue.")
                    st.stop()

                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
            
                data_as_text = dataframe_to_text(datasets[st.session_state.selected_dataset])
                response_text = ask_chatgpt_about_data(prompt, data_as_text)
            
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.chat_message("assistant").write(response_text)
        else:
            st.info("Please submit a dataset to query.")

def process_tiktok_data(data):
    normalized_data = pd.json_normalize(data)
    gender_data = extract_gender_data(normalized_data)
    country_data = extract_country_data(normalized_data)
    Metrics_Daily_Tiktok = extract_metrics_tiktok(normalized_data)
    Organic_Tiktok_Data =  extract_organic_tiktok(normalized_data)
    
    return {
        'gender_data': gender_data,
        'country_data': country_data,
        'Metrics_Daily_Tiktok': Metrics_Daily_Tiktok,
        'Organic_Tiktok_Data': Organic_Tiktok_Data
    }

def fetch_tiktok_data(base_url, security_token, company):
    """
    Fetches TikTok data from the specified API and processes it into structured DataFrames.
    """
    data_endpoint = f"{base_url}/get_tiktok_data"
    headers = {'Authorization': security_token, 'Content-Type': 'application/json'}
    data = {'company_name': company}
    
    response = requests.post(data_endpoint, headers=headers, json=data)
    if response.status_code == 200:
        profile_data = response.json()
        if 'data' in profile_data:
            return process_tiktok_data(profile_data['data'])
        else:
            return None
    else:
        return None

def fetch_tiktok_organic_data(base_url, security_token, company):
    """
    Fetches TikTok data from the specified API and saves processed data into Excel files.
    """
    data_endpoint = f"{base_url}/get_tiktok_data_organic"
    headers = {
        'Authorization': security_token,
        'Content-Type': 'application/json'  # Specify the content type as JSON
    }
    # Assuming the API expects company name in the body of the POST request
    data = {
        'company_name': company
    }
    # Use json parameter to ensure the request body is correctly formatted as JSON
    data_response = requests.post(data_endpoint, headers=headers, json=data)
    print(data_response.status_code)

    if data_response.status_code == 200:
        profile_data = data_response.json()
        print(profile_data)
        profile_data = profile_data.get('data')
        profile_df = pd.DataFrame(profile_data)

        print('Tiktok Organic Data pulled')
        return profile_df

def extract_followers_data(normalized_data):
    followers_columns = ['followers_count', 'username', 'is_business_account']
    followers_data = normalized_data[followers_columns]
    return followers_data

def extract_gender_data(normalized_data):
    gender_data = normalized_data.explode('audience_genders')
    gender_data_normalized = pd.json_normalize(gender_data['audience_genders'])
    gender_data_normalized['percentage'] = gender_data_normalized['percentage'].astype(float) * 100
    return gender_data_normalized.set_index('gender')

def extract_country_data(normalized_data):
    country_mapping = {
        'CO': 'Colombia', 'US': 'United States', 'CL': 'Chile',
        'CR': 'Costa Rica', 'AR': 'Argentina', 'BO': 'Bolivia',
        'EC': 'Ecuador', 'ES': 'Espana', 'GT': 'Guatemala',
        'MX': 'Mexico', 'PE': 'Peru', 'VE': 'Venezuela'
    }
    countries_data = normalized_data.explode('audience_countries')
    countries_normalized = pd.json_normalize(countries_data['audience_countries'])
    countries_normalized['percentage'] = countries_normalized['percentage'] * 100
    countries_normalized['Country'] = countries_normalized['country'].map(country_mapping)
    return countries_normalized.set_index('Country')

def extract_metrics_tiktok(normalized_data):
    metrics_exploded = normalized_data.explode('metrics')
    metrics_normalized = pd.json_normalize(metrics_exploded['metrics'])
    metrics_normalized['date'] = pd.to_datetime(metrics_normalized['date'])
    metrics_normalized.sort_values('date', inplace=True)
    return metrics_normalized

def extract_organic_tiktok(normalized_data):
    metrics_normalized = extract_metrics_tiktok(normalized_data)
    audience_activity_exploded = metrics_normalized.explode('audience_activity')
    audience_activity_normalized = pd.json_normalize(audience_activity_exploded['audience_activity'])
    audience_activity_exploded = audience_activity_exploded.reset_index()
    audience_activity_normalized = audience_activity_normalized.reset_index()
    merged_df = pd.merge(audience_activity_exploded, audience_activity_normalized, left_index=True, right_index=True)
    merged_df = merged_df.drop(['audience_activity', 'index_x', 'index_y'], axis=1)
    return merged_df

def get_tiktok_video_data(company_name):
    """
    Retrieves TikTok video data for a specified company by sending a request
    to a Flask API that manages TikTok API interactions.
    """
    api_url = f"{BASE_URL}/get_tiktok_data_organic_video"
    headers = {
        'Authorization': SECURITY_TOKEN,
        'Content-Type': 'application/json'
    }
    data = json.dumps({'company_name': company_name})
    response = requests.post(api_url, headers=headers, data=data)
    
    try:
        response_data = response.json()
        if response.status_code == 200:
            return response_data
        else:
            print(f"Failed to retrieve data: {response_data.get('error', 'No error message returned')}")
            return None
    except json.JSONDecodeError:
        print("Invalid JSON response")
        return None

def extract_nested_data(response_json, column_name, remove_columns, additional_columns):
    """
    Processes nested data from a pandas DataFrame.

    Args:
    - response_json: The JSON data from the API response.
    - column_name: The key where nested data is stored in each item.
    - remove_columns: List of columns to remove from the main DataFrame.
    - additional_columns: Columns to add to the nested DataFrame for additional context. tiktok organic api

    Returns:
    - Tuple of (clean DataFrame, nested DataFrame)
    """
    if 'data' not in response_json or 'videos' not in response_json['data']:
        print("No video data found")
        return None, None
    
    videos_data = response_json['data']['videos']
    main_df = pd.DataFrame(videos_data)
    
    if 'create_time' in main_df.columns:
        main_df['create_time'] = pd.to_numeric(main_df['create_time'], errors='coerce')
        main_df['create_time'] = pd.to_datetime(main_df['create_time'], unit='s')

    cleandf = main_df.drop(columns=remove_columns).copy(deep=True)

    all_rows = []
    for _, row in main_df.iterrows():
        nested_data = pd.json_normalize(row[column_name])
        nested_data['item_id'] = row['item_id']
        for col in additional_columns:
            if col in row:
                nested_data[col] = row[col]
        all_rows.append(nested_data)
    nested_df = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    
    return cleandf, nested_df

if __name__ == '__main__':
    streamlit_app()
